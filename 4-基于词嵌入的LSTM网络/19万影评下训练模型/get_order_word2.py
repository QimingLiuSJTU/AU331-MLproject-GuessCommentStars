# -*- coding: utf-8 -*-
"""
Created on Sun Dec 16 21:21:29 2018

@author: lenovo
"""

import jieba
import jieba.analyse #用于获取关键词
import pandas as pd

#得到一个短评和关键词列表，返回按短评中出现的顺序排列的关键词列表
def get_order_words(comment, b):
    position_df = pd.DataFrame(columns = ('word', 'position')) #store the words and pos
    for item in b:
        position_df.loc[len(position_df)] = [item, comment.find(item)]
    #利用dataframe中的position行的值进行从小到大排序
    position_df.sort_values('position', inplace = True)
    word_list = list(position_df['word'])
    
    return word_list


if __name__ == '__main__':
    #读入影评+评分数据
    data = pd.read_csv('big_data.csv') 
    comment = list(data['comments'])
    score = list(data['scores'])
    
    new_data = pd.DataFrame(columns = ('score', 'order_word'))
    for i in range(len(data)):
        if type(comment[i]) != float:
            tmp_com = comment[i]
            tmp_sco = score[i]
            #对每一个影评，提取其中top40关键词（不足40的就按照最多能提取出来的）
            b = jieba.analyse.extract_tags(tmp_com, topK = 40, withWeight=False)
            #将提取出来的关键词按照在句子中出现的顺序进行排序
            b = get_order_words(tmp_com, b)
            #将数据加入new_data
            new_data.loc[len(new_data)] = [int(tmp_sco), b]
    #将new_data文件转化成csv文件用于后续处理      
    new_data.to_csv('big_new_data.csv' , encoding="utf_8_sig")
            
    