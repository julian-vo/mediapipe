from __future__ import absolute_import, division, print_function, unicode_literals
from keras.preprocessing import sequence
from keras.datasets import imdb
from keras import layers, models
from keras.models import Sequential
from keras import layers
import numpy as np
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.utils import to_categorical
import random
from keras import optimizers
from keras.layers import SimpleRNN, Dense
from keras.layers import Bidirectional
import os
import sys

def make_label(text):
    with open("label.txt", "w") as f:
         f.write(text)
    f.close()
    
def load_data(dirname):
    if dirname[-1]!='/':
        dirname=dirname+'/'
    listfile=os.listdir(dirname)
    X = []
    Y = []
    XT = []
    YT = []
    for file in listfile:
        if "_" in file:
            continue
        wordname=file
        textlist=os.listdir(dirname+wordname)
        a=len(textlist)
        b=a//3
        k=0
        for text in textlist:
            if "DS_" in text:
                continue
            textname=dirname+wordname+"/"+text
            numbers=[]
            print(textname)
            with open(textname, mode = 'r') as t:

                # Get the text file contents
                numbers = [float(num) for num in t.read().split()]

                # Extend numbers to be 25200 nums long - fill with 0.000s
                # for i in range(len(numbers),25200):
                for i in range(len(numbers),126):
                    numbers.extend([0.000])
            row=0
            # landmark_frame=[]
            # for i in range(0,70):
            #     landmark_frame.extend(numbers[row:row+84])
            #     row += 84
            # landmark_frame=np.array(landmark_frame)
            # landmark_frame=list(landmark_frame.reshape(-1,84))
            landmark_frame=[]
            for i in range(0,42):
                landmark_frame.extend(numbers[row:row+3])
                row += 3
            landmark_frame=np.array(landmark_frame)
            landmark_frame=list(landmark_frame.reshape(42,3))
            if (k%3==2):
                XT.append(np.array(landmark_frame))
                YT.append(wordname)
            else:
                X.append(np.array(landmark_frame))
                Y.append(wordname)
            k+=1
            
    X=np.array(X)
    Y=np.array(Y)
    XT=np.array(XT)
    YT=np.array(YT)
    
    tmp = [[x,y] for x, y in zip(X, Y)]
    random.shuffle(tmp)

    tmp1 = [[xt,yt] for xt, yt in zip(XT, YT)]
    random.shuffle(tmp1)
    
    X = [n[0] for n in tmp]
    Y = [n[1] for n in tmp]
    XT = [n[0] for n in tmp1]
    YT = [n[1] for n in tmp1]
    
    k=set(Y)
    ks=sorted(k)
    text=""
    for i in ks:
        text=text+i+" "
    make_label(text)
    
    s = Tokenizer()
    s.fit_on_texts([text])
    encoded=s.texts_to_sequences([Y])[0]
    encoded1=s.texts_to_sequences([YT])[0]
    one_hot = to_categorical(encoded)
    one_hot2=to_categorical(encoded1)
    

    (x_train, y_train) = X, one_hot
    (x_test,y_test)=XT,one_hot2
    x_train=np.array(x_train)
    y_train=np.array(y_train)
    x_test=np.array(x_test)
    y_test=np.array(y_test)
    return x_train,y_train,x_test,y_test

def build_model(label):
    model = Sequential()
    # model.add(layers.LSTM(64, return_sequences=True,
    #                input_shape=(70, 84)))
    model.add(layers.LSTM(64, return_sequences=True,
                   input_shape=(42, 3)))
    model.add(layers.LSTM(32, return_sequences=True))
    model.add(layers.LSTM(32))
    model.add(layers.Dense(label, activation='softmax'))
    model.compile(loss='categorical_crossentropy',
                  optimizer='adam',
                  metrics=['accuracy'])
    return model

#
# def main():
#     dirname = "/home/julian/Desktop/Work/Thesis/videoData/coordData/Absolute"
#     print(dirname)
#     x_train,y_train,x_test,y_test=load_data(dirname)
#     num_val_samples=(x_train.shape[0])//5
#     model=build_model(y_train.shape[1])
#     print('Training stage')
#     print('==============')
#     history=model.fit(x_train,y_train,epochs=100,batch_size=16,validation_data=(x_test,y_test))
#     score, acc = model.evaluate(x_test,y_test,batch_size=16,verbose=0)
#     print('Test performance: accuracy={0}, loss={1}'.format(acc, score))
#     model.save('model.h5')