from keras.layers import Input
from keras.models import Model
from keras import utils
from keras import backend as K
from .. import layers
from .. import config


def Transformer(
    src_vocab, 
    tgt_vocab, 
    src_seq_len,
    tgt_seq_len,
    num_heads=12,
    hidden_dim=64,
    linear_dim=2048,
    encoder_depth=6,
    decoder_depth=6,
    dropout=0.1,
    activation="leaky_relu",
    padding_value=0,
    **kwargs
    ):
    """Classic Transformer implementation.
    args:
        - src_vocab: the vocabulary size of the encoder input sequence
        - tgt_vocab: the vocabulary size of the decoder input sequence
        - src_seq_len: the length of the encoder input sequence
        - tgt_seq_len: the length of the decoder input sequence
        - num_heads: number of heads in a multi head attention layer
        - hidden_dim: dimensions of queries, keys, and values for each attention head
        - linear_dim: dimension of Linear projection of feedforward
        - encoder_depth: number of encoder_block stacks
        - decoder_depth: number of decoder_block stacks
        - dropout: dropout probability, default to 0.1
        - activation: activation function of feedforward layer, default to "leaky_relu"
        - padding_value: the padding values in the input sequence are used to calculate padding mask

    call arguments:
        - inputs: list of encoder and decoder inputs, shape-->[(b, s), (b, t)]
    """
    encoder_inputs = Input((src_seq_len, ))
    decoder_inputs = Input((tgt_seq_len, ))
    
    masks = layers.GetMasks(name="get_masks")(encoder_inputs, decoder_inputs, padding_value)
    encoder_padding_mask, decoder_padding_mask, sequence_mask = masks

    encoder_x = layers.Embedding(src_vocab, hidden_dim*num_heads, name="input_embedding")(encoder_inputs)
    decoder_x = layers.Embedding(tgt_vocab, hidden_dim*num_heads, name="output_embedding")(decoder_inputs)

    encoder_x = layers.PositionalEncoding(name="input_positiaonal_encoding")(encoder_x)
    decoder_x = layers.PositionalEncoding(name="output_positiaonal_encoding")(decoder_x)

    for i in range(encoder_depth):
        encoder_x = layers.TransformerEncoderBlock(
            num_heads,
            hidden_dim,
            linear_dim,
            dropout,
            activation,
            name=f"encoder_blockd_{i}"
            )(encoder_x, encoder_padding_mask)

    for i in range(decoder_depth):
        decoder_x = layers.TransformerDecoderBlock(
            num_heads,
            hidden_dim,
            linear_dim,
            dropout,
            activation,
            name=f"decoder_blockd_{i}"
            )(decoder_x, encoder_x, sequence_mask, decoder_padding_mask)

    decoder_y = layers.Linear(tgt_vocab, name="linear")(decoder_x)
    decoder_y =  K.softmax(decoder_y)
    model = Model([encoder_inputs,decoder_inputs], decoder_y, **kwargs)

    return model

def Transformer12K(weights:str):
    assert weights in config.WEIGHTS, f'please make sure that `weights` is in the {config.WEIGHTS}'
    MODEL_CONFIG = config.PRE_TRAINED_MODEL_CONFIG.get(weights)
    BASIC_URL = config.BASIC_URL
    FNAME = config.PRE_TRAINED_WEIGHTS_FNAME.get(weights)
    weights = utils.get_file(FNAME, origin=BASIC_URL+FNAME, cache_subdir="weights")
    model = Transformer(**MODEL_CONFIG)
    model.load_weights(weights)
    return model