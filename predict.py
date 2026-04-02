import tensorflow as tf
import numpy as np

model = tf.keras.models.load_model('my_model.keras')


CLASS_NAMES = ['Potato_Early___blight', 'Potato___healthy', 'Potato___Late_blight']
IMAGE_SIZE  = (200, 200)


def predict_image(img_path):
    img = tf.keras.utils.load_img(img_path, target_size=IMAGE_SIZE)

    img_array = tf.keras.utils.img_to_array(img)

    img_array = tf.expand_dims(img_array, axis=0)

    predictions = model.predict(img_array)

    predicted_index = np.argmax(predictions[0])

    predicted_class = CLASS_NAMES[predicted_index]

    confidence = predictions[0][predicted_index] * 100

    print(f"Prediction : {predicted_class}")
    print(f"Confidence : {confidence:.2f}%")


predict_image('TEST/early/14efc692-8ac6-4bd8-a71a-943192d6831a___RS_Early.B 6841.JPG')
