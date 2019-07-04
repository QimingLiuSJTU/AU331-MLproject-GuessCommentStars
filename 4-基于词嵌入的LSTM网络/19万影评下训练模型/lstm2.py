from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import Dropout, LSTM, Dense, Activation, Embedding 
from tensorflow.keras import optimizers
from tensorflow.keras.callbacks import EarlyStopping
import tensorflow as tf
import numpy as np
from test_number_list import get_test_number_list
import pandas as pd

#将样本标记转化为单热向量，三种类型，好中差
def one_hot(labels):
    labels = list(labels)
    for i in range(len(labels)):
        label = labels[i]
        labels[i] = [0]*3
        if label<=2:
            labels[i][0] = 1
        elif label == 3:
            labels[i][1] = 1
        else:
            labels[i][2] = 1
    labels = np.array(labels)
    return labels


#用于测试集的样本features转化成可输入网络的形式
def test_comment_transfer(test_comment):
    for i in range(len(test_comment)):
        test_comment[i] = get_test_number_list(test_comment[i])
    return test_comment


if __name__ == '__main__':
    
    ########################################
    #载入数据
    features = np.load('big_features.npy')
    labels = np.load('big_labels.npy')
    labels = one_hot(labels)
    
    #分成训练集和测试集
    N, D = features.shape
    training_num = int(N*1)
    #testing_num = N - training_num
    training_samples = features[:training_num]
    training_labels = labels[:training_num]
    
    #打乱数据
    np.random.seed(6)
    np.random.shuffle(training_samples)
    np.random.seed(6)
    np.random.shuffle(training_labels)
    #testing_samples = features[training_num:]
    #testing_labels = labels[training_num:]
    ###########################################
    
    
    
    ###########################################
    #建立模型
    #build model
    model = Sequential()
    #Embedding 层， 从句子list(每个词对应一个整数)到句子矩阵(一个词对应一个词向量，维数为output_dim)
    model.add(Embedding(output_dim = 20, input_dim =  np.max(features) + 1, input_length=40))
    
    #LSTM层 输出维度
    model.add(LSTM(80, dropout = 0.5, recurrent_dropout = 0.3))
    #model.add(GRU(150))
    
    #全连接层
    '''
    model.add(Dense(units=100))
    model.add(Activation('relu'))
    model.add(Dense(units=50))
    model.add(Activation('relu'))
    '''
    model.add(Dense(units=20))
    model.add(Activation('relu'))
    
    model.add(Dense(units=3))
    model.add(Activation('sigmoid'))
    #显示模型信息
    model.summary()
    ##########################################
    
    
    
    ###########################################
    #得到测试集
    test_features = np.load('test_features.npy')
    test_labels = np.load('test_labels.npy')
    test_labels = one_hot(test_labels)
    #训练模型
    early_stopping = EarlyStopping(monitor = 'val_acc', patience = 3)
    model.compile(loss = 'categorical_crossentropy', optimizer='Adam', metrics = ['accuracy'])
    model.fit(training_samples, training_labels, epochs = 50, batch_size = 30, validation_data = (test_features, test_labels), shuffle = True, callbacks = [early_stopping])
    model.save('model.h5')
    ###########################################
    
    
    
    ##################################################
    #测试模型的泛化能力,用不在训练集中的影评进行精度测试
    '''
    #交互输入方式
    print('请输入一段影评: ')
    get = input()
    get = get_test_number_list(get)
    predict = model.predict(get)
    print('predict', np.argmax(predict))
    '''
    #用额外的测试集测试效果
    test_labels = np.load('test_labels.npy')
    count = 0
    for i in range(len(test_features)):
        test_tmp = test_features[i]
        test_tmp.shape = (40,1)
        test_tmp = test_tmp.reshape(1,40)
        predict = np.argmax(model.predict(test_tmp)) + 1
        if (predict >= (int(test_labels[i]) - 1)) and predict <= ((int(test_labels[i]) + 1)):
            count += 1
    print('test_acc: ' , count / len(test_features))
    ###################################################
    
    
    

    