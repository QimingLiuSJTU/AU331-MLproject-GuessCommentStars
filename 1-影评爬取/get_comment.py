# -*- coding: utf-8 -*-
import requests        # 从网页上将html源码爬下来
import re              # 进行正则表达式匹配
import pandas as pd    # 整理成最后的表格以及输出
import time            # 每次爬取设置停止时间
import numpy as np     # 随机设置停止时间
import csv             
import matplotlib.pyplot as plt # plt 用于显示图片
import matplotlib.image as mpimg # mpimg 用于读取图片
from bs4 import BeautifulSoup
import urllib

url = 'https://movie.douban.com/subject/{0}/comments?start={1}&limit=20&sort=new_score&status=P&percent_type={2}'


#读入需要爬取的电影文件（电影名+网址填充数字）
data = pd.read_csv('data.csv')
movieId = list(data['number'])
movieName = list(data['film'])

commentType = ['h','m','l'] #分别对应好评中评差评

def log_in():

    s = requests.Session()
    #登录网址
    loginUrl = 'https://accounts.douban.com/login'
    #需要填入的登录信息
    formData = {
    'source': 'movie',
    'redir': 'https://movie.douban.com/',
    "form_email": "17317799025",
    "form_password": "ywh123456789",
    "login": u'登录'
    }
    
    #浏览器中网页的headers
    headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36"}
    
    #尝试登陆
    r = s.post(loginUrl,data=formData,headers=headers)
    #读取尝试登陆后的网页信息
    page = r.text

    #获取验证码
    soup = BeautifulSoup(page, "html.parser")
    captcha = soup.find('img', id='captcha_image')
    #若网页信息中有需要输入图片验证码的框
    if captcha:
        captcha_url = captcha['src']
        reCaptchaID = r'<input type="hidden" name="captcha-id" value="(.*?)"/'
        captchaID = re.findall(reCaptchaID, page)
        #将网页中的验证码图片保存为captcha.jpg文件
        urllib.request.urlretrieve(captcha_url, "captcha.jpg")
        lena = mpimg.imread('captcha.jpg') # 读取和代码处于同一目录下的 lena.png
        plt.imshow(lena) # 显示图片
        plt.axis('off') # 不显示坐标轴
        plt.show()
        #请求输入验证码
        captcha_text = input('please input the captcha:')
        formData['captcha-solution'] = captcha_text
        formData['captcha-id'] = captchaID
        #输入完成后再次尝试登陆
        r = s.post(loginUrl, data=formData, headers=headers)
        page = r.text
    return s



# 匹配对电影的短评
def getComment(html):
    commentList = re.findall(r'<span class="short">(.*?)</span>', html, re.S)
    return commentList

# 匹配对电影的评分
def getScore(html):
    is_scoreList = re.findall(r'<span class="comment-info">(.*?)<span class="comment-time "', html, re.S)
    scoreList = []
    for item in is_scoreList:
        if item.count('rating') == 0: #如果没有评分
            scoreList.append(0)
        else:
            scoreList.append(int(re.findall(r'<span class="allstar(.*?)0 rating"', item, re.S)[0]))
    return scoreList

def getTime(html):
    timelist = re.findall(r'<span class="comment-time " title="(.*?)">', html, re.S)
    return timelist

#得到所有的电影的好中差3*500=1500条影评+评分信息
def getAll(s):
    f = open('all.csv', 'a', newline='', encoding='utf-8-sig')
    w = csv.writer(f)
    for i in range(movieId.__len__()):
        for j in range(3):
            for page in range(0,500,20):
                url_tmp = url.format(movieId[i],page,commentType[j])
                html = s.get(url_tmp).content.decode("UTF-8") # 注意这里需要进行UTF-8转码，通常中文网页都是这种编码
                # 爬取分数与评论
                scoreList = getScore(html)
                commentList = getComment(html)
                w.writerows(zip(commentList, scoreList))
                time.sleep(1) #爬完一页
            time.sleep(3)
    time.sleep(5)
            
    f.close()

#得到一部电影的好中差3*500=1500条影评+评分信息，为了防止频率过快导致封号，选择使用的是这个函数，并设置爬取间隔
def getOneMovie(i,s):
    
    f = open('{}.csv'.format(movieName[i]), 'a', newline='', encoding='utf-8-sig')
    w = csv.writer(f)
    for j in range(3):#对应好中差三种类型影评
        for page in range(0,500,20):#一种类型的影评从0-25页，每页20条
            url_tmp = url.format(movieId[i],page,commentType[j])
            html = s.get(url_tmp).content.decode("UTF-8") # 注意这里需要进行UTF-8转码，通常中文网页都是这种编码
            # 爬取分数与评论
            scoreList = getScore(html)
            commentList = getComment(html)
            w.writerows(zip(scoreList,commentList))
            time.sleep(3)#一页挺2s
        time.sleep(3)#一种类型停2s
    f.close()

if __name__=="__main__" :

    s = log_in()
    for i in range(len(movieId)):#遍历每一部电影
        print(movieName[i])
        getOneMovie(i,s)
        time.sleep(10)#一部电影停5s

