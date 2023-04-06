# https://www.tensorflow.org/tutorials/quickstart/beginner

import tensorflow as tf
print("TensorFlow version:", tf.__version__)

# Select dataset
dataset = tf.keras.datasets.mnist

# Load dataset
(x_train, y_train), (x_test, y_test) = dataset.load_data()
x_train, x_test = x_train / 255.0, x_test / 255.0

# Build a model
model = tf.keras.models.Sequential([
  tf.keras.layers.Flatten(input_shape=(28, 28)),
  tf.keras.layers.Dense(128, activation='relu'),
  tf.keras.layers.Dropout(0.2),
  tf.keras.layers.Dense(10)
])

# 
predictions = model(x_train[:1]).numpy()
print(predictions)

# Compile the model
model.compile(
    optimizer='adam',
    loss=loss_fn,
    metrics=['accuracy']
)

# Fit the model
model.fit(x_train, y_train, epochs=5)

# Return a probability
probability_model = tf.keras.Sequential(
    [
        model,
        tf.keras.layers.Softmax()
    ]
)
print(probability_model(x_test[:5]))