import numpy as np
import tensorflow as tf

# TensorFlow/Keras Test
# Einfacher Klassifizierer von Kleidung


def testFlow():
    # Lade Test-/Trainingsdaten
    fashion_mnist = tf.keras.datasets.fashion_mnist
    (train_images, train_labels), (test_images, test_labels) = fashion_mnist.load_data()
    classes = {0: 'T-shirt/top', 1: 'Trouser', 2: 'Pullover', 3: 'Dress', 4: 'Coat',
               5: 'Sandal', 6: 'Shirt', 7: 'Sneaker', 8: 'Bag', 9: 'Ankle boot'}

    # preprocess - Mappe jeden pixel in das Intervall [0,1] für bessere Ergebnisse
    train_images = train_images / 255.0
    test_images = test_images / 255.0

    model = buildModel()

    model.fit(train_images, train_labels, epochs=5)
    predictions = model.predict(test_images)

    for i in range(10):
        print('Bild {}: {}'.format(i, classes[int(np.argmax(predictions[i]))]))


def buildModel():
    model = tf.keras.Sequential([
        tf.keras.layers.Flatten(input_shape=(28, 28)),
        tf.keras.layers.Dense(128, activation='relu'),
        tf.keras.layers.Dense(10, activation='softmax')
    ])
    model.compile(optimizer='adam',
                  loss='sparse_categorical_crossentropy',
                  metrics=['accuracy'])
    return model


testFlow()
