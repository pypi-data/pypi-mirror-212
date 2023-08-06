BASIC_URL = "https://github.com/djsaber/kboxx/releases/download/transformer_weights/"


WEIGHTS = ["AI_Challenger_Translation_2017"]


FNAMES = [
    "weights_12k_50_AI_Challenger_Translation_2017.h5", 
    ]


PRE_TRAINED_WEIGHTS_FNAME = {
    WEIGHTS[0]: FNAMES[0],
    }


PRE_TRAINED_MODEL_CONFIG = {
    WEIGHTS[0]: {
        'src_vocab':12000, 'tgt_vocab':12000, 'src_seq_len':50, 'tgt_seq_len':50,
        'num_heads':12, 'hidden_dim':64, 'linear_dim':2048, 'encoder_depth':6, 'decoder_depth':6, 'dropout':0.1, 
        'activation':"leaky_relu", 'padding_value':0, }
    }
