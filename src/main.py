# https://www.tensorflow.org/tutorials/quickstart/beginner

from log import LOG
import os

LOG("Importing Tensorflow with some warnings hidden")
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 
import tensorflow as tf
print("TensorFlow version:", tf.__version__)

LOG("Selecting dataset")
dataset = tf.keras.datasets.mnist

LOG("Loading dataset")
(x_train, y_train), (x_test, y_test) = dataset.load_data()
x_train, x_test = x_train / 255.0, x_test / 255.0

LOG("Building mode")
model = tf.keras.models.Sequential([
  tf.keras.layers.Flatten(input_shape=(28, 28)),
  tf.keras.layers.Dense(128, activation='relu'),
  tf.keras.layers.Dropout(0.2),
  tf.keras.layers.Dense(10)
])

LOG("Training predictions")
predictions = model(x_train[:1]).numpy()
LOG(predictions)

LOG("Defining a loss function")
loss_fn = tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True)

LOG("Compiling the model")
model.compile(
    optimizer='adam',
    loss=loss_fn,
    metrics=['accuracy']
)

LOG("Fitting the model")
model.fit(x_train, y_train, epochs=5)

LOG("Calculating probabilities")
probability_model = tf.keras.Sequential(
    [
        model,
        tf.keras.layers.Softmax()
    ]
)
LOG(probability_model(x_test[:5]))

