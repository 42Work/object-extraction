import pickle
import requests
import re
from bs4 import BeautifulSoup as BS
import time
import pickle

num_all=732,000,000     #bing:的
num_tf=452              #很


##===========爬取天猫十三个大类各十个产品的各四百条评论==============##
##===========暂时只爬取了3100条评论============##
# def help():
#     print("{0}+{1}error！")
#
# f_url_list=[]
# review_all=[] #爬到的所有评论
#
# with open('./data/天猫爬取网址.txt',encoding='GBK') as f_url:
#     for l in f_url:
#         if l[0]=='#':
#             continue
#         f_url_list.append(l[:-1])
#
# url_pre="https://rate.tmall.com/list_detail_rate.htm?itemId={0}&sellerId=268451883&currentPage={1}"
# for sale_id in f_url_list:
#     for i in range(1,21):
#         url = url_pre.format(sale_id,i)
#         my_content = requests.get(url)
#         if my_content.status_code != 200:
#             help()
#             continue
#         else:
#             content = my_content.text
#             xr = r'("rateContent":".+?")'
#             results = re.findall(xr, content)
#         for r in results:
#             line=r.split('":"')[1][:-1]
#             review_all.append(line)
#
# with open('./data/review_all.pkl','wb') as r_w:
#     pickle.dump(review_all,r_w)



#============计算抽取评论中出现频率最多的词===========#
# with open('./data/word_seach.pkl','wb') as w_s:
#     pickle.dump(w_s,words_tf_idf)

# from pyltp import Segmentor, Postagger
# import os
# from collections import Counter
#
# LTP_DATA_DIR = "D:\myprojects\LTP\ltp_data_v3.4.0"
# cws_model_path = os.path.join(LTP_DATA_DIR, 'cws.model')
# pos_model_path = os.path.join(LTP_DATA_DIR, 'pos.model')
#
# segmentor = Segmentor()  # 初始化实例
# segmentor.load(cws_model_path)
# postagger = Postagger()  # 初始化实例
# postagger.load(pos_model_path)  # 加载模型

# words=[]
# with open('./data/file.txt', 'rt', encoding='utf-8') as ft:
#     for l in ft:
#         line = l.split(',', 4)[4][2:-4]
#         words+=segmentor.segment(line)
# word_count=Counter(words)
# top_one=word_count.most_common(5)
# print(top_one)

#============计算tf-idf值===================
import math

f1=open('./data/words_tf.pkl','rb')
tf=pickle.load(f1)
f1.close()
f2=open('./data/review_all.pkl','rb')
idf=pickle.load(f2)
f2.close()
f3=open('./data/words_item.pkl','rb')
words_item=pickle.load(f3)
f3.close()

words_tfidf={}
for w in tf:
    num=0
    tf_val=tf[w]/num_tf
    for l in idf:
        if w in l:
            num+=1
        else:
            for i in range(len(words_item[w])):
                if words_item[w][i] not in idf:
                    break
            if i ==len(words_item[w])-1:
                num+=1
    idf_val=math.log(3100/(num+1))
    tf_idf=tf_val*idf_val
    words_tfidf[w]=tf_idf

    with open('./data/word_tf_idf.pkl','wb') as f_t_i:
        pickle.dump(words_tfidf,f_t_i)

# for line in words_tfidf:
#     print(line,words_tfidf[line])

