# -*- coding: utf-8 -*-
import csv
import numpy as np

movieName = np.load("moviename.npy").tolist()
#movieName = ['钢铁侠','钢铁侠2','钢铁侠3',
#             '无敌浩克',
#             '雷神','雷神2','雷神3',
#             '美队','美队2','美队3',
#             '复联','复联2','复联3',
#             '银河护卫队','银河护卫队2',
#             '蚁人','蚁人2',
#             '奇异博士','蜘蛛侠','黑豹','毒液']

movie_for_test = ['神奇女侠','正义联盟','海王']


for i in range(movieName.__len__()):
    fr = open('{}.csv'.format(movieName[i]), 'r', newline='', encoding='utf-8-sig').read()
    with open('合集.csv', 'a', newline='', encoding='utf-8-sig') as f:
        f.write(fr)
