"""
    实现了的项目需求：
    1、
    从命令行参数给出：论文原文的文件的绝对路径。
    从命令行参数给出：抄袭版论文的文件的绝对路径。
    从命令行参数给出：输出的答案文件的绝对路径。
    2、
    genhash算法
    3、
    对中文文本查重实现
                                                ————2020.9.22~2020.9.23
"""

"""
    第二次更新：
    1、
    按照老师要求添加了异常处理：命令行参数输入，文件名、绝对路径输入出错。
    
                                                ————2020.9.23~2020.9.24
"""

"""
    第三次更新：
    1、
    优化报异常的逻辑，第一个异常报告便不再报告第二个异常。
    
                                                ————2020.9.24~
"""
import re
import sys
import jieba
from gensim import corpora, models, similarities
from collections import defaultdict
from gensim.similarities import Similarity

if __name__ == '__main__':

    #命令行参数传入：main.py、[论文原文的文件的绝对路径]、[抄袭版论文的文件的绝对路径]、[输出的答案文件的绝对路径]
    try:
        text1_abs_path = sys.argv[1]
        text2_abs_path = sys.argv[2]
        save_abs_path = sys.argv[3]
    except Exception as e:
        print("'main.py' 后未输入 文本1 文本2 计算结果保存文件 的绝对路径")
        print("正确样例：python main.py 1.txt 2.txt 3.txt")
        print("")
        #异常报告优化，若第一个异常报告则不需要再报告第二个异常。
        flag = 1
    #过滤非中文
    filter = re.compile(u"[^a-zA-Z0-9\u4e00-\u9fa5]")

    #文件操作
    try:
        with open(text1_abs_path,'r',encoding='UTF-8') as f1,open(text2_abs_path,'r',encoding='UTF-8') as f2:

            #读取文件内容
            doc1=f1.read()
            doc2=f2.read()

            #对文本中的非中文内容等进行删去
            doc1 = filter.sub('',doc1)
            doc2 = filter.sub('',doc2)
            # 将文本载入一个列表，待分词
    except Exception as error:
        if flag != 1:
            print("")
            print("读取文件失败，请检查文件名或绝对路径是否正确")

#将文本1 jieba 分词，转向量
doc1_list = [jieba.lcut(doc1)]
dic = corpora.Dictionary(doc1_list)
num_fea = len(dic.token2id)
corpus = [dic.doc2bow(doc1) for doc1 in doc1_list]
doc2_vec = dic.doc2bow(jieba.lcut(doc2))

#计算两篇文章的相似度并打印
similarity = Similarity('-Similarity-index', corpus, num_fea)
calculation = similarity[doc2_vec]
print("两篇文章的相似度约为：%.5s" %str(calculation[0]*100) +"%")

# 输出结果写入指定文档
with open(save_abs_path,'w',encoding='UTF-8') as f3:

    f3.write("两个文本的相似度：%s" %calculation[0]*100 +"")
    f3.close()
