from log import LOG
import os

class Trainer:

    def __init__(self):
        LOG("initialising trainer")

    def go(
        self,
            dir_input,
            dir_output,
        ):

        LOG("training")

        LOG("importing Tensorflow with some warnings hidden")
        os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 
        import tensorflow as tf
        LOG("    tensorFlow version: %s" % tf.__version__)

        LOG("selecting dataset")
        dataset = tf.keras.datasets.mnist

        ds = ds_in.shuffle(buffer_size=rec_count)
        ds_train = ds.skip(400)
        ds_validate = ds.take(400)

        LOG("loading dataset")
        (x_train, y_train), (x_test, y_test) = dataset.load_data()
        x_train, x_test = x_train / 255.0, x_test / 255.0

        LOG("building model")
        model = tf.keras.models.Sequential([
          tf.keras.layers.Flatten(input_shape=(28, 28)),
          tf.keras.layers.Dense(128, activation='relu'),
          tf.keras.layers.Dropout(0.2),
          tf.keras.layers.Dense(10)
        ])

        LOG("training predictions")
        predictions = model(x_train[:1]).numpy()
        LOG(predictions)

        LOG("defining a loss function")
        loss_fn = tf.keras.losses.MeanSquaredError(from_logits=True)

        LOG("compiling the model")
        model.compile(
            optimizer='adam',
            loss=loss_fn,
            metrics=['accuracy']
        )

        LOG("fitting the model")
        model.fit(x_train, y_train, epochs=5)

        LOG("calculating probabilities")
        probability_model = tf.keras.Sequential(
            [
                model,
                tf.keras.layers.Softmax()
            ]
        )
        LOG(probability_model(x_test[:5]))

    # An example training session
    def go_example(self):

        LOG("training")
        
        LOG("importing Tensorflow with some warnings hidden")
        os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 
        import tensorflow as tf
        LOG("    tensorFlow version: %s" % tf.__version__)

        LOG("selecting dataset")
        dataset = tf.keras.datasets.mnist

        LOG("loading dataset")
        (x_train, y_train), (x_test, y_test) = dataset.load_data()
        x_train, x_test = x_train / 255.0, x_test / 255.0

        LOG("building model")
        model = tf.keras.models.Sequential([
          tf.keras.layers.Flatten(input_shape=(28, 28)),
          tf.keras.layers.Dense(128, activation='relu'),
          tf.keras.layers.Dropout(0.2),
          tf.keras.layers.Dense(10)
        ])

        LOG("training predictions")
        predictions = model(x_train[:1]).numpy()
        LOG(predictions)

        LOG("defining a loss function")
        loss_fn = tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True)

        LOG("compiling the model")
        model.compile(
            optimizer='adam',
            loss=loss_fn,
            metrics=['accuracy']
        )

        LOG("fitting the model")
        model.fit(x_train, y_train, epochs=5)

        LOG("calculating probabilities")
        probability_model = tf.keras.Sequential(
            [
                model,
                tf.keras.layers.Softmax()
            ]
        )
        LOG(probability_model(x_test[:5]))

