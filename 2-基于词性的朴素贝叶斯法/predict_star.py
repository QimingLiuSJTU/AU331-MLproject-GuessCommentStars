# -*- coding: utf-8 -*-
"""
Created on Fri Dec 14 18:43:50 2018

@author: ML group
"""

import pandas as pd
import jieba
import tkinter as tk

# import jieba.posseg as pseg

########################################################################################
# 1、对原始的数据进行清洗，word_dict太多的无用词语需要删掉了，这些词语非常影响训练的精度
# 2、能够将否定词代入考虑，否定词与形容词结合考虑，可以防止判断反向
# 3、weight的smoothing变换需要更加优化
# 4、写可视化界面的代码
# 5、可否对score调整部分的代码进行优化（函数优化），要充分考虑词语出现次数与平均值之间的关系，最终形成变换后的分数
# 6、word_dict中只出现了一次或两次的词语，可否进行删除，这些词语大多数是无意义的
########################################################################################


def give_score(sentence):
    
    word_score = pd.read_csv(r'word_dict.csv',encoding='UTF-8')
    not_allowed_noun_csv = pd.read_csv(r'not_allowed_noun.csv',encoding='UTF-8')
    not_allowed_noun = list(not_allowed_noun_csv.iloc[:, 0])

    allow_pos = ('a', 'ad', 'v', 'vd', 'vn', 'z', 'i', 'nz', 'n', 'l')
    div_sentence = pd.DataFrame(columns = ['word', 'weight'])
    for x, w in jieba.analyse.extract_tags(sentence, topK = 20, withWeight = True, allowPOS=allow_pos):
        if x not in not_allowed_noun:
            s = pd.Series({'word':x, 'weight':w})
            div_sentence = div_sentence.append(s, ignore_index=True)
    print(div_sentence, '\n')

    
    all_word_list = list(word_score.iloc[:, 0])
    word_num = div_sentence.shape[0]
    
    div_sentence['score'] = 'NaN'
    div_sentence['times'] = 'NaN'
    
    div_sentence_delete_neuter = pd.DataFrame(columns = ['word', 'weight', 'score', 'times'])

    for i in range(word_num):
        if str(div_sentence.iloc[i, 0]) in all_word_list:
            div_sentence.iloc[i, 2] = float(word_score.loc[word_score['word'] == str(div_sentence.iloc[i, 0]), 'averange_score'])
            div_sentence.iloc[i, 3] = int(word_score.loc[word_score['word'] == str(div_sentence.iloc[i, 0]), 'appeared_times'])
            if float(div_sentence.iloc[i, 2]) > 3.1 or float(div_sentence.iloc[i, 2]) < 2.9:                
                s = pd.Series({'word':str(div_sentence.iloc[i, 0]), 'weight':float(div_sentence.iloc[i, 1]), 'score':float(div_sentence.iloc[i, 2]), 'times':int(div_sentence.iloc[i, 3])})
                div_sentence_delete_neuter = div_sentence_delete_neuter.append(s, ignore_index=True)
        
        
        
    print(div_sentence_delete_neuter)
    word_num = div_sentence_delete_neuter.shape[0]
    for i in range(word_num):
        div_sentence_delete_neuter.iloc[i, 1] = div_sentence_delete_neuter.iloc[i, 1] ** (3/2)
    smoothing = round(word_num * 0.25)
    total_weight = div_sentence_delete_neuter.iloc[0:,1].sum()
    print(total_weight)
    for i in range(word_num):
        div_sentence_delete_neuter.iloc[i, 1] = (div_sentence_delete_neuter.iloc[i, 1] + smoothing) / (total_weight + word_num * smoothing)
    
    
    
    
    ################# Now determine score #################
    div_sentence_delete_neuter['transcore'] = 'NaN'
    for j in range(word_num):
        score = float(div_sentence_delete_neuter.iloc[j, 2])
        times = int(div_sentence_delete_neuter.iloc[j, 3])
        if str(div_sentence_delete_neuter.iloc[j, 2]) != 'NaN':
            if score > 3.750 and times >=3:
                nextscore = 5.0
            elif score > 3.350:
                if times >= 25 * (5-score) * (5-score) * (5-score):
                    nextscore = score + 1.2
                elif times >= 12 * (5-score) * (5-score) * (5-score):
                    nextscore = score + 0.8
                else:
                    nextscore = score + (times - 10) / 60
            elif score > 3.15:
                if times >= 25 * (5-score) * (5-score):
                    nextscore = score + 0.5
                elif times >= 12 * (5-score) * (5-score):
                    nextscore = score + 0.25
                else:
                    nextscore = score + (times - 20) / 80
            elif score > 2.9:
                nextscore = 3
            elif score > 2.5:
                nextscore = 2
            elif score > 2.3:
                nextscore = 1
            else:
                nextscore = 0
        div_sentence_delete_neuter.iloc[j, 4] = nextscore
    print(div_sentence_delete_neuter)
    
    final_score = 0.0
    good_word_num = 0
    bad_word_num = 0
    neuter_word_num = 0
    for k in range(word_num):
        final_score += float(div_sentence_delete_neuter.iloc[k, 1]) * float(div_sentence_delete_neuter.iloc[k, 4])
        if div_sentence_delete_neuter.iloc[k, 4] <= 2.1:
            bad_word_num += 1
        elif div_sentence_delete_neuter.iloc[k, 4] >= 3.9:
            good_word_num += 1
        else:
            neuter_word_num += 1
    
    if good_word_num / word_num > 0.249 and bad_word_num / word_num < 0.12:
        final_score += 0.5
    if bad_word_num / word_num > 0.349 and bad_word_num / word_num < 0.15:
        final_score -= 0.5
    if final_score >= 5:
        final_score = 5
    elif final_score <= 1:
        final_score = 1
    print('\n\n')
    print('final score (float):', final_score)
    print('final_score (int):', round(final_score))
    return round(final_score), round(final_score, 3)
                    
        
def touch_clear():
    e.delete(0, tk.END)
    #t.delete(0.0, tk.END)
    showstar_1.set('')  
    showstar_2.set('')

def predict():
# comment是字符串
# star是一个int
    comment = e.get()
    star, star_f = give_score(comment)
    showstar_1.set(star)
    showstar_2.set(star_f)
    
    
    
window = tk.Tk()
window.title('电影短评星级预测')
window.geometry('400x500')

e = tk.Entry(window,width = 50)
e.pack()

showstar_1 = tk.StringVar()   # 文字变量储存器
showstar_2 = tk.StringVar()
l1 = tk.Label(window,
    textvariable=showstar_1,   # 使用 textvariable 替换 text, 因为这个可以变化
    bg='blue', font=('Times',40,'bold'), width=4, height=2)
l1.pack(pady = 30)

l2 = tk.Label(window,
    textvariable=showstar_2,   # 使用 textvariable 替换 text, 因为这个可以变化
    bg='hotpink', font=('Times',40,'bold'), width=4, height=2)
l2.pack()

b2 = tk.Button(window,
    text='预测',      # 显示在按钮上的文字
    width=16, height=4,
    command=predict)     # 点击按钮式执行的命令
b2.pack(padx=50, side=tk.LEFT)    # 按钮位置

b1 = tk.Button(window,
    text='清空',      # 显示在按钮上的文字
    width=16, height=4,
    command=touch_clear)     # 点击按钮式执行的命令
b1.pack(side=tk.LEFT)    # 按钮位置

window.mainloop()