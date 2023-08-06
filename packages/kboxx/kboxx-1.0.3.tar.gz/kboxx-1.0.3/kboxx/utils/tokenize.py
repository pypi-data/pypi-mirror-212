import collections
import json
import sys
import spacy


class BPETokenizer():
    """Byte pair encoding tokenizer.it iteratively counts the byte pairs 
    with the highest co-occurrence frequency and considers them 
    together as a new 'byte'.

    bpe = BPETokenizer('spacy_en')
    
    1. Using `fit` method to establish a subwords vocabulary with a 
    specified size in a given corpus.
    >> bpe.fit(corpus, max_size, save_path)
    This will generate a subwords vocabulary file in JSON format in 
    the given path.

    2. Using `tokenize` method to tokenize to segment a given text.
    >> sent = 'I really like puppies!'
    >> bpe.tokenize(sent, sep="@")
    >> ['I', 'really', 'like', 'pup@', 'pie@', 's', '!']

    3. Using `detokenize` method to merge tokens back to words.
    >> tokens = ['I', 'really', 'like', 'pup@', 'pie@', 's', '!']
    >> bpe.detokenize(tokens, sep="@")
    >> 'I really like puppies !'

    4. Using `save` and `load` method to save or load subwords 
    vocabulary.
    >> bpe.save(save_path)
    >> bpe.load(save_path)
    """

    def __init__(self, basic_tokenizer=None, path=None, lowercase=False):
        """initialize BPETokenizer.
        args:
            - basic_tokenizer: 'list', 'space', 'spacy_en', 'spacy_zh' or function
            'list': split by each character
            'space': split by space characters
            'spacy_en': use spacy_en tokenizer
            'spacy_zh': use spacy_zh tokenizer
            function: input: 'i have a dog.', output: ['i', 'have', 'a', 'dog', '.']
            - path: load the saved sub vocabulary file under this path
            - lowercase: whether using lowercase to replaces uppercase
        """
        self.lowercase = lowercase
        if basic_tokenizer == 'list': self.basic_tokenizer = self.__list_tokenize
        elif basic_tokenizer == 'space': self.basic_tokenizer = self.__space_tokenize
        elif basic_tokenizer == 'spacy_en': self.basic_tokenizer = self.__spacy_en_tokenize()
        elif basic_tokenizer == 'spacy_zh': self.basic_tokenizer = self.__spacy_zh_tokenize()
        else: self.basic_tokenizer = basic_tokenizer
        assert hasattr(self.basic_tokenizer, '__call__'), 'error argument `basic_tokenizer`!'
        self.subwords = None
        if path: self.load(path)

    def fit(self, corpus:list, max_size:int, save_path=None):
        """fit BPETokenizer with corpus, the subwords vocabulary will be built.
        args:
            - corpus: input corpus list
            - max_size: max size of subwords vocabulary
            - save_path: subwords vocabulary file save path
        """
        if self.lowercase:
            corpus = [s.lower() for s in corpus]
        
        vocab = self.__init_vocab(corpus)
        size = self.__count_subwords(vocab)
        sys.stdout.flush()
        
        while size < max_size:
            most_bp = self.__get_most_byte_pair(vocab)
            if most_bp is None:
                break
            self.__merge_vocab(vocab, most_bp)
            size = self.__count_subwords(vocab)
            sys.stdout.write(f'\rbuilt subwords: [{size} / {max_size}]')
        sys.stdout.write(f'\n')

        self.subwords = self.__get_subwords(vocab)
        if save_path is not None:
            self.save(save_path)

    def tokenize(self, sent:str, sep="@"):
        """partitioning the input sentence.
        eg: 'I really like puppies !' --> ['I', 'really', 'like', 'pup@', 'pie@', 's', '!']
        args:
            - sent: input sentence
            - sep: subwords separator symbol, 'puppies' --> 'pup@', 'pie@', 's'
        return:
            - tokens: list of tokens
        """
        assert self.subwords is not None, "subwords is None, please fit or load subwords first"
        if self.lowercase:
            sent = sent.lower()
        sent = self.basic_tokenizer(sent)
        tokens = [token for word in sent for token in self.__word_tokenize(word, sep)]
        return tokens

    def detokenize(self, tokens, sep="@"):
        """restore tokens sequence to sentence.
        eg: ['I', 'really', 'like', 'pup@', 'pie@', 's', '!'] --> 'I really like puppies !'
        args:
            - tokens: tokens sequence
            - sep: subwords separator symbol, 'puppies' --> 'pup@', 'pie@', 's'
        return:
            - tokens: list of tokens
        """
        out = []
        for token in tokens:
            if token[-1]!= sep:
                out.append(token+' ')
            elif len(token) > 1:
                out.append(token[:-1])
            else:
                out.append(token)
        return ''.join(out)

    def save(self, path):
        with open(path, 'w') as f:
            json.dump(self.subwords, f)

    def load(self, path):
        self.subwords = json.load(open(path, 'r'))

    def __space_tokenize(self, sent:str):
        return sent.split()

    def __list_tokenize(self, sent:str):
        return list(sent)

    def __spacy_en_tokenize(self):
        model = spacy.load("en_core_web_sm")
        def apply(sent:str):
            return [tok.text for tok in model.tokenizer(sent)]
        return apply

    def __spacy_zh_tokenize(self):
        model = spacy.load("zh_core_web_sm")
        def apply(sent:str):
            return [tok.text for tok in model.tokenizer(sent)]
        return apply

    def __init_vocab(self, corpus:list):
        sys.stdout.flush()
        vocab = collections.defaultdict(int)
        for i, sent in enumerate(corpus):
            sys.stdout.write(f'\rinitialize vocabulary: [{i} / {len(corpus)}]')
            for word in self.basic_tokenizer(sent):
                vocab[' '.join(list(word))] += 1

        sys.stdout.write(f'\n')
        return dict(vocab)

    def __get_subwords(self, vocab:dict):
        subwords = collections.defaultdict(int)
        for word, freq in vocab.items():
            for token in word.split():
                subwords[token] += freq
        sorted_keys = list(sorted(subwords.keys(), key=lambda x:subwords[x], reverse=True))
        subwords = dict((k,v) for v,k in enumerate(sorted_keys))
        return subwords

    def __count_subwords(self, vocab:dict):
        subwords = set(token for word in vocab.keys() for token in word.split())
        return len(subwords)

    def __get_most_byte_pair(self, vocab:dict):
        byte_pairs = collections.defaultdict(int)
        for word, freq in vocab.items():
            symbols = word.split()
            for i in range(len(symbols)-1):
                byte_pairs[symbols[i]+symbols[i+1]] += freq
        return max(byte_pairs, key=byte_pairs.get) if byte_pairs else None

    def __merge_vocab(self, vocab:dict, byte_pair:str):
        for word in vocab.keys():
            merge, temp = False, word.split()
            for i in range(len(temp)-1):
                if byte_pair == temp[i]+temp[i+1]:
                    temp[i] = byte_pair
                    temp[i+1] = ''
                    merge = True
            if merge:
                new_word = ' '.join(temp)
                vocab[new_word] = vocab.pop(word)
        return vocab

    def __word_tokenize(self, word:str, sep:str):
        word = list(word)
        tokens = []
        start, end = 0, len(word)
        while start < end:
            subword = ''.join(word[start:end])
            if subword in self.subwords:
                if end != len(word):
                    subword += sep
                tokens.append(subword)
                start = end
                end = len(word)
            elif end - start == 1:
                if end != len(word):
                    subword += sep
                tokens.append(subword)
                start = end
                end = len(word)
            else:
                end -= 1
        return tokens