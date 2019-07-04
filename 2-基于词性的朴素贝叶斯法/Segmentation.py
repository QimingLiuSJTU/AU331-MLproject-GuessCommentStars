# -*- coding: utf-8 -*-
"""
Created on Mon Dec  3 10:28:48 2018

@author: ML group
"""

import pandas as pd
import jieba
import jieba.posseg as pseg
import jieba.analyse
import numpy as np
import re

original_data = pd.read_csv(r'all_comment.csv',encoding='UTF-8')
print(original_data.head())
print('-------------------------------\nread data size:', original_data.shape[0], '\n-------------------------------')

not_allowed_noun_csv = pd.read_csv(r'not_allowed_noun.csv',encoding='UTF-8')
not_allowed_noun = list(not_allowed_noun_csv.iloc[:, 0])
print(not_allowed_noun)

seg_data = original_data.copy()
seg_data['seg_comment'] = 'NaN'

word_dict = pd.DataFrame(columns = ['word', 'total_score', 'appeared_times', 'averange_score'])
final_word_dict = pd.DataFrame(columns = ['word', 'total_score', 'appeared_times', 'averange_score'])
appeared_word_list = []

for i in range(original_data.shape[0]):
    if i % 300 == 0:
        print(i,  '----------', round(i / original_data.shape[0] * 100, 4), '%')
    
    temp_list = ''
    comment = original_data.iloc[i, 1]
    # test is without numbers, English alphabet and punctuation
    text = ''.join(re.findall(u'[\u4e00-\u9fff]+', comment))
    
    ################### For test ###################
    '''
    if i == 0:
        print(comment)
        print(type(comment))
        print('score: ',original_data.iloc[i, 0])
        
        print(text)
    comment_seg_list = jieba.lcut(text, cut_all = False, HMM = True)
    '''
    ################################################

    allow_pos = ('a', 'ad', 'v', 'vd', 'vn', 'z', 'i', 'nz', 'n', 'l')
    for x, w in jieba.analyse.extract_tags(text, topK = 20, withWeight = True, allowPOS=allow_pos):
        if x not in not_allowed_noun and original_data.iloc[i, 0] != 'NA':
            if x in appeared_word_list:
                word_dict.loc[word_dict['word'] == x, 'total_score'] += int(original_data.iloc[i, 0])
                word_dict.loc[word_dict['word'] == x, 'appeared_times'] += 1
                word_dict.loc[word_dict['word'] == x, 'averange_score'] = round(int(word_dict.loc[word_dict['word'] == x, 'total_score']) / int(word_dict.loc[word_dict['word'] == x, 'appeared_times']), 4)
            else:
                s = pd.Series({'word':x, 'total_score':int(original_data.iloc[i, 0]), 'appeared_times':1, 'averange_score':float(original_data.iloc[i, 0])})
                word_dict = word_dict.append(s, ignore_index=True)
                appeared_word_list.append(x)
            temp_list += (str(x) + ':' + str(round(w, 4)) + ' ')
            
    # print(temp_list)
    if temp_list != '':
        seg_data.iloc[i, 2] = temp_list
    
    if i % 5000 == 0:
        print(word_dict)

# delete some unnecessary words in the dict
print('begin resampling and deleting process')
for k in range(word_dict.shape[0]):
    word = str(word_dict.iloc[k, 0])
    words = pseg.cut(word)
    for w in words:
        _, word_type = w.word, w.flag
    word_appeared_times = int(word_dict.iloc[k, 2])
    if word_appeared_times == 1:
        if word_type in ['v', 'l', 'i']:
            # print(word_dict.iloc[k])
            final_word_dict = final_word_dict.append(word_dict.iloc[k])
    if word_appeared_times == 2 or word_appeared_times == 3:
        if word_type in ['v', 'l', 'a', 'i']:
            # print(word_dict.iloc[k])
            final_word_dict = final_word_dict.append(word_dict.iloc[k])
    else:
        final_word_dict = final_word_dict.append(word_dict.iloc[k])

print(final_word_dict)    
       
seg_data.to_csv('movie_score_comment_seg.csv', encoding="utf_8_sig")
word_dict.to_csv('word_dict.csv', encoding="utf_8_sig")