from keras import backend as K

def get_padding_mask(batch_inputs, padding_value):
    """Generate padding mask based on input sequence.
    args:
        - batch_inputs: batch input sequence, shape-->(b, len)
        - padding_value: Padding values in the input sequence
    return:
        - mask: Boolean type mask, Masked out as False, retained as True, shape-->(b, len)
    """
    mask = K.not_equal(batch_inputs, padding_value)
    return mask

def get_sequence_mask(batch_inputs):
    """Generate sequence mask based on input sequence.
    args:
        - batch_inputs: batch input sequence, shape-->(b, len)
    return:
        - mask: Upper triangular mask of Boolean type, Masked out as False, retained as True, shape-->(len, len)
    """
    mask = K.cast(K.np.tri(K.int_shape(batch_inputs)[-1], K.int_shape(batch_inputs)[-1]), bool)
    return mask

def get_transformer_masks(encoder_inputs, decoder_inputs, padding_value):
    """Generate an attention mask for the encoder and decoder of the transformer model.
    args:
        - encoder_inputs: Inputs of transformer encoder, shape-->(b, s])
        - decoder_inputs:  Inputs of transformer decoder, shape-->(b, t)
        - padding_value: Padding values in the input sequence
    return:
        - encoder_padding_mask: Padding_mask for transformer encoder, shape-->(b, s, s)
        - decoder_padding_mask: Padding_mask for transformer decoder, shape-->(b, t, s)
        - sequence_mask: Sequence_mask for transformer decoder, shape-->(b, t, t)
    """
    padding_mask = get_padding_mask(encoder_inputs, padding_value)
    sequence_mask =get_sequence_mask(decoder_inputs)
    encoder_padding_mask = K.tile(K.expand_dims(padding_mask, 1), [1, K.shape(encoder_inputs)[1], 1])
    decoder_padding_mask = K.tile(K.expand_dims(padding_mask, 1), [1, K.shape(decoder_inputs)[1], 1])
    sequence_mask = K.tile(K.expand_dims(sequence_mask, 0), [K.shape(decoder_inputs)[0], 1, 1])
    return encoder_padding_mask, decoder_padding_mask, sequence_mask

def get_positional_encoding(pos, dim):
    """Generate positional encoding.
    args:
        - pos: Position length of position encoding
        - dim: Encoding dimension for each position
    return:
        - positional encoding: Shape like-->(1, pos, dim)
    """
    numerator = K.tile(K.constant(range(pos), shape=(pos,1)), [1, dim])
    denominator = 1e4 ** (K.tile(K.constant([[i if i%2==0 else i-1 for i in range(dim)]]), [pos,1]) / dim)
    pe = K.np.zeros((1, pos, dim))
    pe[0,:,0::2] = K.sin((numerator/denominator)[:,0::2])
    pe[0,:,1::2] = K.cos((numerator/denominator)[:,1::2])
    return K.constant(pe)

def auto_regressive(model, src, tgt):
    """transformer auto regressive output
    args: 
        - src: source token sequence
        - tgt: target initial token sequence
    return:
        - tgt: target output toekn sequence 
    """
    for i in range(tgt.shape[1]-1):
        pred = K.np.argmax(K.np.asarray(model([src, tgt])), -1)
        next_word = pred[:, i]
        tgt[:,i+1] = next_word
    return tgt