# -*- coding: utf-8 -*-
"""
Created on Sun Dec 16 20:05:18 2018

@author: lenovo
"""
import jieba
import jieba.analyse #用于获取关键词
import pandas as pd
import numpy as np


#输入一个影评返回网络的输入形式即数字list
def get_test_number_list(comment):
    
    f = open('word_dic.txt', 'r')#读取词字典文件
    a = f.read()
    word_dict = eval(a)
    f.close
    
    a = comment
    
    '''
    #精确分词
    #full cut
    b = jieba.cut(a, cut_all=True)
    tmp = ','.join(b)
    tmp += ','
    
    start,end = 0,1
    b = []
    while(start < len(tmp) and end<len(tmp)):
        while(tmp[end] != ','):
            end +=1
        b.append(str(tmp[start:end]))
        
        start = end + 1
        end = start + 1
    '''
    #关键分词
    #get the key words
    b = jieba.analyse.extract_tags(a, topK = 40, withWeight=False) #用analyse功能得到top40的关键词
    
    #得到按出现顺序排列的关键词
    #get the ordered key words
    position_df = pd.DataFrame(columns = ('word', 'position')) #store the words and pos
    for item in b:
        position_df.loc[len(position_df)] = [item, a.find(item)]
    position_df.sort_values('position', inplace = True)
    word_list = list(position_df['word'])
    
    #将顺序排列的关键词列表转化成可输入网络的数字列表
    #get the number_list
    number_list = []
    for item in word_list:
        if item in word_dict:#如果输入的词在字典中
            number_list.append(word_dict[item])
        else:
            number_list.append(0)#如果输入的词不再字典中，补0
            
    if len(number_list)<40:#如果长度小于40,补0
        for i in range(40-len(number_list)):
            number_list.append(0)
    number_list = np.array(number_list)
    #将number_List的shape更改成可输入模型的形式
    number_list.shape = (40,1)
    number_list = number_list.reshape(1,40)
    return number_list
    
            

    
        
        