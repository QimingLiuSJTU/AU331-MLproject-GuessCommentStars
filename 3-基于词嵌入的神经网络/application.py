import tkinter as tk

import jieba
import numpy as np
import tensorflow as tf
from tensorflow import keras

vocab_size = 52117
model = keras.Sequential()
model.add(keras.layers.Embedding(vocab_size, 32))
model.add(keras.layers.GlobalAveragePooling1D())
model.add(keras.layers.Dense(16, activation=tf.nn.relu))
model.add(keras.layers.Dense(5, activation=tf.nn.softmax))
model.load_weights('weights_best.h5')
comments_word = list(np.load('comments_word.npy'))

def wordslist2input(comment):
    comment = list(jieba.cut(comment,cut_all = False))
    print(comment)
    inputvector=[]
    for i in range(comment.__len__()):
        if comment[i] in comments_word:
            inputvector.append(comments_word.index(comment[i]) + 1)
        else:
            inputvector.append(0)
    print(inputvector)
    inputvector = np.array([inputvector])
    return inputvector

window = tk.Tk()
window.title('电影短评星级预测demo')
window.geometry('400x300')

e = tk.Entry(window,width = 50)
e.pack()

# t = tk.Text(e,height=5)
# t.pack(after=e)

def touch_clear():
    e.delete(0, tk.END)
    #t.delete(0.0, tk.END)
    showstar.set('')


def predict():
# comment是字符串
# star是一个int
    comment = e.get()
    star = model.predict_classes(wordslist2input(comment))[0] + 1
    showstar.set(star)

showstar = tk.StringVar()   # 文字变量储存器
l = tk.Label(window,
    textvariable=showstar,   # 使用 textvariable 替换 text, 因为这个可以变化
    bg='hotpink', font=('Times',40,'bold'), width=4, height=2)
l.pack(pady=30)

b1 = tk.Button(window,
    text='清空',      # 显示在按钮上的文字
    width=16, height=4,
    command=touch_clear)     # 点击按钮式执行的命令
b1.pack(padx=50,side=tk.LEFT)    # 按钮位置

b2 = tk.Button(window,
    text='预测',      # 显示在按钮上的文字
    width=16, height=4,
    command=predict)     # 点击按钮式执行的命令
b2.pack(side=tk.LEFT)    # 按钮位置

window.mainloop()
