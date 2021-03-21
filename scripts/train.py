import os
import sys
import argparse
from train_utils import make_label,load_data, build_model
import tensorflow as tf


def main(dirname):
    dirname = "/home/julian/Desktop/Work/Thesis/videoData/coordData/Absolute"
    print(dirname)
    x_train,y_train,x_test,y_test=load_data(dirname)
    num_val_samples=(x_train.shape[0])//5
    model=build_model(y_train.shape[1])
    print('Training stage')
    print('==============')
    history=model.fit(x_train,y_train,epochs=100,batch_size=16,validation_data=(x_test,y_test))
    score, acc = model.evaluate(x_test,y_test,batch_size=16,verbose=0)
    print('Test performance: accuracy={0}, loss={1}'.format(acc, score))
    model.save('model_static_abcde.h5')

    # Save the model as tflite
    # converter = tf.lite.TFLiteConverter.from_keras_model(model)
    # tflite_model = converter.convert()
    # open("model_static_abcde.tflite", "wb").write(tflite_model)

    
if __name__=='__main__':
    parser = argparse.ArgumentParser(description='Training Model')
    parser.add_argument("--input_train_path",help=" ")
    args=parser.parse_args()
    input_train_path=args.input_train_path
    main(input_train_path)
