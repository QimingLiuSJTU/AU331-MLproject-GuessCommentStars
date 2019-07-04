# -*- coding: utf-8 -*-
"""
Created on Thu Dec 20 19:26:30 2018

@author: lenovo
"""

import numpy as np
import pandas as pd
from wordcloud import WordCloud #导入词云库
import matplotlib.pyplot as plt
from scipy.misc import imread   

if __name__ == '__main__':
    #导入包含关键词及其出现频次的文件word_dict.csv
    data = pd.read_csv('word_dict.csv', encoding = 'utf_8')
    score = data['averange_score']
    
    
    #经过观察平均分在2.95-3.01间的词中很多与情感色彩无关，初步删去
    del_list = []
    for i in range(len(score)):
        if score[i] >= 2.95 and score[i] <= 3.01:
            del_list.append(i) 
    data = data.drop(del_list)
    data.index = range(len(data))
    
    
    #选择前top_k个词用于显示
    top_k = 150
    words = data['word']
    times = data['appeared_times']
    show_words = list(words[:top_k])
    show_fre = list(times[:top_k])
    
    
    #将关键词和出现次数合为一个字典
    dic = dict(zip(show_words, show_fre))
    
    
    #选择背景图，没有找到非常好的背景图，所以没有用
    #pic=imread('tmp2.jpg')  #读取背景图片
    
    
    #根据关键词出现的次数来显示前top_k个关键词,次数越多字体越大
    #font_path用于设置字体, background_color用于设置背景颜色,width,height用于设置图片大小
    #prefer_horizontal用于设置显示的词语中水平显示的占比，min_font_size用于设置最小的字体大小
    wordcloud = WordCloud( font_path="STKAITI.TTF", background_color='white', 
                          width = 2000, height = 1200, prefer_horizontal = 1.0, min_font_size=5,
                          relative_scaling= 0.8)
    show = wordcloud.generate_from_frequencies(dic)
    #显示及保存图片
    plt.imshow(show)
    plt.axis('off')
    plt.savefig('words_cloud.jpg',dpi=1600)
    plt.show()
   
    
    