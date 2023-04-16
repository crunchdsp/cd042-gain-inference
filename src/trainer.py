from log import LOG
import numpy as np
import os

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'    # import Tensorflow with some warnings hidden
import tensorflow as tf

class Trainer:

    def __init__(self):
        LOG("initialising trainer")

    def go(
        self,
            dir_input,
            dir_output,
            validation_split = 0.2,                     # proportion of data used for validation
            batch_size = 32,                            # number of training samples per update
            epochs = 3,                                 # number of times each sample is presented
        ):

        LOG("training")

        LOG("importing Tensorflow with some warnings hidden")
        LOG("tensorFlow version: %s" % tf.__version__)

        LOG("loading data")
        X = np.load("%s/level_dBSPL_mixed_stacked.npy" % dir_input)
        y = np.load("%s/gains_dB.npy" % dir_input)
        LOG("    loaded X with shape %s" % str(X.shape))
        LOG("    loaded y with shape %s" % str(y.shape))
        length_total, number_of_levels = X.shape
        length_total, number_of_gains = y.shape
        LOG("        there are %d levels per sample" % number_of_levels)
        LOG("        there are %d gains per sample" % number_of_gains)

        LOG("shuffling data")
        assert len(X) == len(y)
        permutated = np.random.permutation(len(X))
        X, y = X[permutated], y[permutated]
        LOG("    shuffled %d samples" % length_total)

        LOG("partitioning data")
        length_test = int(validation_split * length_total)
        length_train = length_total - length_test
        LOG("    using %d samples for training" % length_train)
        LOG("    using %d samples for testing" % length_test)
        X_train, y_train = X[0:length_train], y[0:length_train]
        X_test, y_test = X[length_train:], y[length_train:]

        LOG("building model")
        # hidden_layers = [ (1.0, 0.2, 'relu'), (1.0, 0.2, 'relu') ]       # tuples (output_proportion, dropout_rate, activation) per hidden layer
        hidden_layers = []
        model = tf.keras.models.Sequential()
        output_length = number_of_levels

        LOG("    input layer length %d" % output_length)
        model.add(tf.keras.layers.InputLayer(output_length))

        for (output_proportion, dropout_rate, activation) in hidden_layers:
            output_length = int(output_proportion * output_length)
            LOG("    dense layer output length %d, activation %s" % (output_length, activation))
            model.add(tf.keras.layers.Dense(output_length, activation=activation))
            if dropout_rate is not None:
                LOG("    dropout length proportion %f" % (dropout_rate))
                model.add(tf.keras.layers.Dropout(dropout_rate))

        LOG("    output layer length %d" % output_length)
        model.add(tf.keras.layers.Dense(number_of_gains, activation='relu'))

        LOG("defining a loss function")
        loss_fn = tf.keras.losses.MeanSquaredError()

        LOG("compiling the model")
        model.compile(
            optimizer='adam',
            loss=loss_fn,
            metrics=['accuracy']
        )

        LOG("fitting the model")
        LOG("    batch size is %d" % batch_size)
        LOG("    over %s epochs" % epochs)
        model.fit(
            x = X_train, 
            y = y_train, 
            batch_size = batch_size,
            epochs = epochs,
            validation_data = (X_test, y_test),
        )

    # An example training session
    def go_example(self):

        LOG("example from https://www.tensorflow.org/tutorials/quickstart/beginner")
        
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

