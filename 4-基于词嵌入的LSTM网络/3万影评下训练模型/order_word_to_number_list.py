# -*- coding: utf-8 -*-
"""
Created on Sun Dec 16 16:46:37 2018

@author: lenovo
"""
import numpy as np
import pandas as pd

#全部关键词连在一起的list类型的comment，转化成单个关键词排序成的list
#如'讨厌这部电影'->['讨厌','这部','电影']
def str_to_list(order_word):
    words_list = []
    start = 1
    end = 2
    while(start<len(order_word) and end < len(order_word)):
        while(order_word[end] != '\'' and end < (len(order_word) - 1)):
            end += 1
        words_list.append(order_word[start+1:end])
        
        start = end + 1
        while(order_word[start] != '\'' and start < (len(order_word) - 1)):
            start += 1
        
        end = start + 1
    return words_list

#根据关键词库构建关键词字典
def words_dictionary(data):
    word_dic = {} #初始化词典
    
    for i in range(len(data)):
        order_word = data['order_word'][i]
        order_word = str_to_list(order_word)
        for item in order_word:
            if item not in word_dic:
                word_dic[item] = len(word_dic) + 1#避免占用数字0
                
    return word_dic

if __name__ == '__main__':
    
    #加载数据
    data = pd.read_csv('new_data.csv')    
    
    #得到关键词字典
    word_dic = words_dictionary(data)
    #保存字典以备后用
    f = open('word_dic.txt', 'w')
    f.write(str(word_dic))
    f.close
    '''
    #若已经得到了关键词词典，在对训练样本进行构建时打开利用即可
    #打开关键词字典
    f = open('word_dic.txt', 'r')
    word_dic = eval(f.read())
    f.close()
    '''
    dataset = pd.DataFrame(columns = ('score','number_list'))
    
    #将关键词list转化成数字list
    for i in range(len(data)):
        word_num_list = []
        order_word = data['order_word'][i]
        order_word = str_to_list(order_word)
        for item in order_word:
            if item in word_dic:
                word_num_list.append(word_dic[item])
            else:
                word_num_list.append(0)
        dataset.loc[len(dataset)] = (data['score'][i], word_num_list)
        
    labels = np.array(list(dataset['score']))
    np.save('labels.npy', labels) #保存label.npy文件，训练样本的标记
    
    features = list(dataset['number_list'])
    
    
    #找到最大长度的features，即最长的关键词list的length，此处直接设置为40维，因为取关键词时最大40个
    max_len = 40
    '''
    for i in range(len(features)):
        if len(features[i]) > max_len:
            max_len = len(features[i])
    '''
    
    #将不够长的number_list补零
    for i in range(len(features)):
        if len(features[i]) != max_len:
            for j in range(max_len - len(features[i])):
                features[i].append(0)
    
    features = np.array(features)
    np.save('features.npy', features) #保存features.npy文件，训练样本的特征
    
    
    
        
    
                
    
                
    