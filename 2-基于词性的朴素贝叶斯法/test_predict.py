# -*- coding: utf-8 -*-
"""
Created on Thu Dec 20 21:21:34 2018

@author: Administrator
"""

import pandas as pd
import jieba

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
    # print(div_sentence, '\n')

    
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
        
    # print(div_sentence_delete_neuter)
    word_num = div_sentence_delete_neuter.shape[0]
    if word_num == 0:
        return None, None
    for i in range(word_num):
        div_sentence_delete_neuter.iloc[i, 1] = div_sentence_delete_neuter.iloc[i, 1] ** (3/2)
    smoothing = round(word_num * 0.25)
    total_weight = div_sentence_delete_neuter.iloc[0:,1].sum()
    # print(total_weight)
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
    # print(div_sentence_delete_neuter)
    
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
    # print('\n\n')
    # print('final score (float):', final_score)
    # print('final_score (int):', round(final_score))
    return round(final_score), round(final_score, 3)

test_data = pd.read_csv(r'test.csv', encoding='UTF-8')
test_num = test_data.shape[0]
correct_num_strict = 0
correct_num_nstrict = 0
correct_num_nnstrict = 0
c_num = 0
for i in range(5000):
    score, score_f = give_score(str(test_data.iloc[i, 1]))
    if score == None:
        continue
    if score == test_data.iloc[i, 0]:
        correct_num_strict += 1
        correct_num_nstrict += 1
        correct_num_nnstrict += 1
        c_num += 1
    elif test_data.iloc[i, 0] == int(score_f) or test_data.iloc[i, 0] == int(score_f) + 1:
        correct_num_nstrict += 1
        correct_num_nnstrict += 1
        c_num += 1
    elif test_data.iloc[i, 0] == score or test_data.iloc[i, 0] == score + 1 or test_data.iloc[i, 0] == score - 1:
        correct_num_nnstrict += 1
        c_num += 1
    else:
        c_num += 1
    if i % 10 == 0:
        print(i, '----', i/test_num * 100, '%')
    if i % 200 == 0 and i != 0:
        print('accuracy:', correct_num_strict/c_num)

        print('accuracy:', correct_num_nstrict/c_num)

        print('accuracy:', correct_num_nnstrict/c_num)

print('\n\n')

print('accuracy:', correct_num_strict/c_num)

print('accuracy:', correct_num_nstrict/c_num)

print('accuracy:', correct_num_nnstrict/c_num)