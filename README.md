# AU331-MLproject-GuessCommentStars
 输入一段影评，自动给出可能的星级。亦可用作筛选恶意评论。

## Description
该项目是上海交通大学AU331本科课程的课程大项目，主要目的是分析一段影评中的情感并给出最可能的星级。一般在撰写影评时，用户需要给出对电影的星级评价。在正常情况下，星级与给出的影评是相关的。项目中使用了三种方法：基于词性的朴素贝叶斯法、基于词嵌入的神经网络、基于词嵌入的LSTM网络。

## File Functions

1.影评爬取：<br>
    **get_comment.py**: 是爬取影评部分的代码<br>
    **data.csv**: 是包含电影名+电影网址序列号信息的文件<br>

2.基于词性的朴素贝叶斯法<br>
    **segmentation.py**: 是将原始数据进行分词的程序（包含词性判断以及词频统计）<br>
    **predict_star.py**: 是可视化星级预测程序，可以输入评论，在可视化窗口中进行星级评定<br>
    **test_predict.py**: 是利用DC测试集进行精度测试的程序<br>
    **all_comment.csv**: 是包含约32000条评论的原始数据集<br>
    **not_allowed_noun.csv**: 是不允许进入词库的无意义常见词<br>
    **word_dict.csv**: 是分词及统计后形成的词库，星级预测即基于词库中各词的平均星级和出现次数<br>
    
3.基于词嵌入的神经网络<br> 
    **prepare_data.py**: 数据预处理：将已经合并好的csv文件进行处理，获得词语转换为整数的列表（词表），并且将所有的短评进行分词和转换，并且用0补足到256维整数向量，保存为npy文件<br>
    **together.py**: 合并所有爬到的电影短评csv文件<br>
    **train.py**: 训练模型，最终得到一个权重文件<br>
    **application.py**: 使用图形化界面进行预测<br>
    **all.csv**: 只包含漫威21部电影的原始数据（未做任何删减）<br>
    **test.csv**: 包含三部dc电影的原始数据（未做任何删减）<br>
    **data.csv**: 包含漫威和120部动作片和科幻片的短评数据（删减了少量无效数据）<br>
    **dataset.npy**: 训练集的特征向量<br>
    **labels.npy**: 训练集的标记文件<br>
    **comments_word.npy**: 词表文件，运行application.py时需要<br>
    **moviename.npy**: 合并电影短评时用来记录所有电影名字的文件<br>
    **weights_best.h5**: 权重文件，运行application.py时需要<br>
    
4.基于词嵌入的LSTM网络<br>
    包括3万和19万两次的训练过程，内容相近只是数据集和代码中稍作修改<br> 
    **get_order_word2.py**: 将影评+评分的初步数据转化成按在影评中出现的顺序排列的顺序关键词list，即将movie_score_comment_seg.csv -> new_data.csv 同理 test.csv -> test_data.csv<br>
    **order_word_to_number_list.py**: 将顺序关键词list转化成number list，即将new_data.csv -> features.npy 并得到 labels.npy 同理得到 test_features.npy和test_labels.npy<br>
    **test_number_list.py**: 将交互输入的影评转化成可输入训练好的模型中进行预测的number list形式<br>
    **lstm1.py，lstm2.py**: 构建lstm网络：其中lstm1构建的是精确相等即5类标签的网络而lstm2是3类标签（好中差）网络<br>
    **movie_score_comment_seg.csv**: 初始数据：包含影评+评分信息<br>
    **new_data.csv**: 顺序关键词list数据集：将每条影评提取top40关键词后并按在影评中出现的顺序排列<br>
    **test.csv**: 初始测试集：包含影评+评分信息<br>
    **test_data.csv**: 顺序关键词list测试集：将每条影评提取top40关键词后并按在影评中出现的顺序排列 <br>
    **features.npy**: 训练集特征向量（数字list形式）<br>
    **labels.npy**: 训练集的标记文件<br>
    **test_features.npy**: 测试集特征向量（数字list形式）<br>
    **test_labels.npy**: 测试集的标记文件<br>
    
5.结果可视化<br>
    词云设计文件夹<br>
    **word.cloud.py**: 制作词云代码<br>
    **word_dict.csv**: 包含关键词，出现频次，平均分数信息的数据集<br>
    **words_cloud.jpg**: 运行程序word.cloud.py后保存的词云图片<br>
    **STKAITI.TFF**: 选择显示的字体文件<br>
    交互界面设计文件夹<br>
    **application.py**: 交互界面的设计<br>
    **predict_star.py**: 调用交互界面的程序<br>
    **word_dict.csv**: 调用程序中需要的数据<br>

## Project participant
蔡建伟、严威豪、刘启明 上海交通大学自动化系

## Data Sources
豆瓣，主要收集漫威超级英雄系列、DC系列以及其它著名动作及科幻类电影影评。
