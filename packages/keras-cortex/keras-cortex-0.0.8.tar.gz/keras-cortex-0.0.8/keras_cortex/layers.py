import tensorflow as tf


class SpatialSoftmax(tf.keras.layers.Layer):
    """Deep Spatial Autoencoders for Visuomotor Learning (Finn et al., 2015)"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def build(self, input_shape):
        print(input_shape)
        N, H, W, C = list(input_shape)

        self.alpha = self.add_weight(
            "alpha",
            shape=(1,),
            initializer=tf.keras.initializers.RandomNormal(stddev=0.01),
            trainable=True
        )

        posx, posy = tf.meshgrid(tf.linspace(-1., 1., num=H),
                                 tf.linspace(-1., 1., num=W))

        image_coords = tf.stack([posx, posy], axis=-1)
        self.image_coords = self.add_weight(
            "image_coords",
            initializer=tf.keras.initializers.constant(image_coords),
            shape=image_coords.shape,
            trainable=False)

    def call(self, inputs, **kwargs):
        print(inputs.shape)
        N, H, W, C = list(inputs.shape)

        if N is None:
            N = -1

        # per filter softmax
        features = tf.reshape(tf.transpose(inputs / self.alpha, 
                                           perm=[0, 3, 1, 2]), 
                              [-1, H * W if not H is None and not W is None else 1])
        softmax = tf.nn.softmax(features)
        softmax = tf.transpose(tf.reshape(softmax, [N, C, H if H is not None else 1, W if W is not None else 1]), [0, 2, 3, 1])

        # expected position
        softmax = tf.expand_dims(softmax, -1)
        image_coords = tf.expand_dims(self.image_coords, 2)
        spatial_soft_argmax = tf.reduce_sum(softmax * image_coords, axis=[1, 2])

        return spatial_soft_argmax

    def compute_output_shape(self, input_shape):
        return (input_shape[0], input_shape[-1])

