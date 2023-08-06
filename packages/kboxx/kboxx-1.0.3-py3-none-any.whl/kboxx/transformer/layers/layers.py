from keras import layers
from keras import activations
from .. import utils


class Embedding(layers.Layer):
    """Input embedding.
    args:
        - size: the size of the vocabulary
        - dim: embedding dimension for each word
    """
    def __init__(self, size, dim, **kwargs):
        super().__init__(**kwargs)
        self.embedding=layers.Embedding(size, dim)

    def call(self, inputs):
        return self.embedding(inputs)


class PositionalEncoding(layers.Layer):
    """Add Positional encoding to inputs.
    args:
        - pos: position length
        - dim: encoding length for each position
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
    def build(self, input_shape):
        pos, dim = input_shape[1:]    
        self.pe = utils.get_positional_encoding(pos, dim)
        return super().build(input_shape)

    def call(self, inputs):
        return inputs + self.pe


class GetMasks(layers.Layer):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def call(self, encoder_inputs, decoder_inputs, padding_value):
        masks = utils.get_transformer_masks(encoder_inputs, decoder_inputs, padding_value)
        return masks


class MultiHeadAttention(layers.Layer):
    """MultiHeadAttention layer.
    args:
        - num_heads: number of heads in a multi head attention layer
        - hiddem_dim: dimensions of queries, keys, and values for each attention head
        - dropout: dropout probability
    call arguments:
        - query, shape-->(B, T, dim)
        - value, shape-->(B, S, dim)
        - key=None, shape-->(B, S, dim)
        - mask=None, shape-->(B, T, S)
    """
    def __init__(
        self, 
        num_heads, 
        hiddem_dim, 
        dropout,
        **kwargs):
        super().__init__(**kwargs)
        self.num_heads = num_heads
        self.hiddem_dim = hiddem_dim
        self.dropout = dropout

    def build(self, input_shape):
        self.multi_head_attetion = layers.MultiHeadAttention(
            key_dim=self.hiddem_dim,
            num_heads=self.num_heads, 
            dropout=self.dropout,
            )
        return super().build(input_shape)

    def call(self, query, value, key=None, mask=None):
        return self.multi_head_attetion(query, value, key=key, attention_mask=mask)


class AddNorm(layers.Layer):
    """Add and Norm, Layer Normalize x first, then add y.
    call arguments:
        - x: inputs 1
        - y: inputs 2
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layer_norm = layers.LayerNormalization(epsilon=1e-6)

    def call(self, x, y):
        return y + self.layer_norm(x)


class FeedForward(layers.Layer):
    """FeedForward layer for encoder and decoder.
    args:
        - linear_dim: dimension of the linear projection
        - dropout: dropout probability
        - activation=None: activation function of the first linear projection
    """
    def __init__(
        self, 
        linear_dim,
        dropout,
        activation=None,
        **kwargs):
        super().__init__(**kwargs)
        self.linear_dim = linear_dim
        self.dropout = dropout
        self.activation = activations.get(activation)

    def build(self, input_shape):
        output_dim = self.output_dim = input_shape[-1]
        self.linear_1 = layers.Dense(self.linear_dim, self.activation)
        self.linear_2 = layers.Dense(output_dim)
        self.dropout_layer = layers.Dropout(self.dropout)
        return super().build(input_shape)

    def call(self, inputs):
        x = self.linear_1(inputs)
        x = self.dropout_layer(x)
        x = self.linear_2(x)
        return x


class Linear(layers.Layer):
    """linear projection.
    args:
        - output_dim: linear projection output dimension
        - use_bias=False: whether to use bias
    """
    def __init__(self, output_dim, use_bias=False, **kwargs):
        super().__init__(**kwargs)
        self.output_dim = output_dim
        self.use_bias = use_bias

    def build(self, input_shape):
        self.linear = layers.Dense(self.output_dim, use_bias=self.use_bias)
        return super().build(input_shape)

    def call(self, inputs):
        return self.linear(inputs)


class TransformerEncoderBlock(layers.Layer):
    """Classic Transformer Encoder Block.
    args:
        - num_heads: the number of heads in a multi head attention layer
        - hidden_dim: dimensions of queries, keys, and values for each attention head 
        - linear_dim: the linear projection dimension of feedforward
        - dropout: dropout probability
        - activation: activation function of feedforward layer
    call arguments:
        - inputs, shape-->(B, S, dim)
        - padding_mask=None, shape-->(B, S, S)
    """
    def __init__(
        self, 
        num_heads,
        hidden_dim,
        linear_dim,
        dropout,
        activation,
        **kwargs
        ):
        super().__init__(**kwargs)
        self.num_heads = num_heads
        self.hidden_dim = hidden_dim
        self.linear_dim = linear_dim
        self.dropout = dropout
        self.activation = activation
        
    def build(self, input_shape):
        self.multi_head_attention = MultiHeadAttention(
            num_heads=self.num_heads,
            hiddem_dim=self.hidden_dim, 
            dropout=self.dropout,
            )
        self.add_norm_1 = AddNorm()
        self.feed_forward = FeedForward(
            linear_dim=self.linear_dim,
            dropout = self.dropout,
            activation=self.activation
            )
        self.add_norm_2 = AddNorm()
        super().build(input_shape)

    def call(self, inputs, padding_mask=None):
        x = self.multi_head_attention(inputs, inputs, mask=padding_mask)
        x = self.add_norm_1(x, inputs)
        y = self.feed_forward(x)
        y = self.add_norm_2(y, x)
        return y


class TransformerDecoderBlock(layers.Layer):
    """Classic Transformer Decoder Block.
    args:
        - num_heads: the number of heads in a multi head attention layer
        - hidden_dim: dimensions of queries, keys, and values for each attention head 
        - linear_dim: the linear projection dimension of feedforward
        - dropout: dropout probability
        - activation: activation function of feedforward layer
    call arguments:
        - decoder_inputs, shape-->(B, T, dim)
        - encoder_outputs, shape-->(B, S, dim)
        - sequence_mask, shape-->(B, T, T)
        - padding_mask, shape-->(B, T, S)
    """
    def __init__(
        self, 
        num_heads,
        hidden_dim,
        linear_dim,
        dropout,
        activation,
        **kwargs
        ):
        super().__init__(**kwargs)     
        self.num_heads = num_heads
        self.hidden_dim = hidden_dim
        self.linear_dim = linear_dim
        self.dropout = dropout
        self.activation = activation

    def build(self, input_shape):
        self.masked_multi_head_attention = MultiHeadAttention(
            num_heads=self.num_heads,
            hiddem_dim=self.hidden_dim, 
            dropout=self.dropout,
            )
        self.add_norm_1 = AddNorm()
        self.multi_head_attention = MultiHeadAttention(
            num_heads=self.num_heads,
            hiddem_dim=self.hidden_dim, 
            dropout=self.dropout,
            )
        self.add_norm_2 = AddNorm()
        self.feed_forward = FeedForward(
            linear_dim=self.linear_dim,
            dropout=self.dropout,
            activation=self.activation
            )
        self.add_norm_3 = AddNorm()
        super().build(input_shape)

    def call(self, decoder_inputs, encoder_outputs, sequence_mask=None, padding_mask=None):
        x = self.masked_multi_head_attention(decoder_inputs, decoder_inputs, mask=sequence_mask)
        x = self.add_norm_1(x, decoder_inputs)
        y = self.multi_head_attention(x, encoder_outputs, mask=padding_mask)
        y = self.add_norm_2(y, x)
        z = self.feed_forward(y)
        z = self.add_norm_3(z, y)
        return z