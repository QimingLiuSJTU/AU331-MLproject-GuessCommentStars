# -*- coding: utf-8 -*-
import jieba
import numpy as np
import pandas as pd
import re

comments_word = list(np.load('comments_word.npy'))
comments_train = list(pd.read_csv('all.csv')['comments'])
scores_train = np.array(list(pd.read_csv('all.csv')['scores']))
comments_test = list(pd.read_csv('test.csv')['comments'])
scores_test = np.array(list(pd.read_csv('test.csv')['scores']))

def comment2vector(comment):
    #短评变成256维的表示向量，最后用0填充
    text = ''.join(re.findall(u'[\u4e00-\u9fff]+', comment))
    comment = list(jieba.cut(text,cut_all = False))
    inputvector=[]
    for i in range(comment.__len__()):
        if comment[i] in comments_word:
            inputvector.append(comments_word.index(comment[i]) + 1)
        else:
            inputvector.append(0)
    inputvector = inputvector + (256 - comment.__len__()) * [0]
    return inputvector

training_set=[]
testing_set=[]

for i in range(comments_train.__len__()):
    training_set.append(comment2vector(comments_train[i]))
    print(i)

for i in range(comments_test.__len__()):
    testing_set.append(comment2vector(comments_test[i]))
    print(i)

testing_set=np.array(testing_set)

training_set=np.array(training_set)

np.save("testing_set.npy",testing_set)

np.save("training_set.npy",training_set)

np.save("testing_labels.npy",scores_test)

np.save("training_labels.npy",scores_train)
#lens = [] #每条短评的词数
#comments_word = [] #数据里所有出现过的单词
#
#for i in range(comments.__len__()):
#    text = ''.join(re.findall(u'[\u4e00-\u9fff]+', comments[i]))
#    tmp = list(jieba.cut(text,cut_all = False))
#    comments_word.extend(tmp)
#    lens.append(tmp.__len__())
#
#comments_word = list(set(comments_word))
#
#np.save("comments_word.npy",comments_word)