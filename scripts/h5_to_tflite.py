import tensorflow as tf

model = tf.keras.models.load_model('model_static_abcde.h5')
converter = tf.lite.TFLiteConverter.from_keras_model(model)
tflite_model = converter.convert()
open("model_static_abcde.tflite", "wb").write(tflite_model)