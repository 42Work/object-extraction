from pyltp import Segmentor,Postagger,Parser
import os
import pickle

LTP_DATA_DIR="D:\myprojects\LTP\ltp_data_v3.4.0"
cws_model_path = os.path.join(LTP_DATA_DIR, 'cws.model')
pos_model_path = os.path.join(LTP_DATA_DIR, 'pos.model')
par_model_path = os.path.join(LTP_DATA_DIR, 'parser.model')


segmentor = Segmentor()  # 初始化实例
segmentor.load(cws_model_path)  #加载模型
postagger = Postagger()
postagger.load(pos_model_path)
parser = Parser()
parser.load(par_model_path)


##===========去除前后多余部分==========##
# content=[
#     [('现在', 'nt'), ('已经', 'd'), ('坏', 'a'), ('了', 'u'), ('，', 'wp'), ('假', 'a'), ('的', 'u'), ('数据线', 'n')]
#      ...
# ]
content=[]
sen_feature=[]    #对每个句子，保存分词，词性，依存句法[, , []]

with open('./data/file.txt','rt',encoding='utf-8') as f1:
    for l in f1:
        line=l.split(',',4)[4][2:-4]   #去除前后多余部分
        words = segmentor.segment(line)   #分词
        postags = postagger.postag(words)   #词性标注
        arcs = list(parser.parse(words, postags))   # 句法分析
        word_pos=list(zip(words,postags))
        content.append(word_pos)
        item=[]
        for i in range(len(words)):
            item.append([words[i],postags[i],[arcs[i].head,arcs[i].relation]])
        sen_feature.append(item)


##==========读取出停用词表=============##
fs=open('./data/stay.txt','rt',encoding='utf-8')
stay_words=[]
for line in fs:
    stay_words.append(line[:-1])
fs.close()


##==========构造算法输入格式==========##
# data = [
#     [[1, 2], [3]],
#     [[1], [3, 2], [1, 2]],
#     [[1, 2], [5]],
#     [[6]],
# ]

data=[]
data_pos={}
for sen in content:
    temp=[]
    for i in range(len(sen)):
        if sen[i][1] =='n':
            if sen[i][0] in stay_words:
                continue
            temp.append([sen[i][0]])
            if not data_pos.get(sen[i][0]):
                data_pos[sen[i][0]]='n'
        if sen[i][1] =='v':
            if i ==len(sen)-1:
                break
            elif sen[i+1][1] =='a':
                if sen[i][0] in stay_words:
                    continue
                temp.append([sen[i][0]])
                data_pos[sen[i][0]] = 'v'
                continue
            if len(sen)<3 or i>=len(sen)-2:
                break
            if sen[i+1][1] =='n' and sen[i+2][1]=='a' and sen[i+2][1]=='d':
                if sen[i][0] in stay_words:
                    continue
                temp.append([sen[i][0]])
                data_pos[sen[i][0]] = 'v'
            if sen[i+1][1] =='d' and sen[i+2][1]=='a':
                if sen[i][0] in stay_words:
                    continue
                temp.append([sen[i][0]])
                data_pos[sen[i][0]] = 'v'
    if len(temp)!=0:
        data.append(temp)

with open('./data/data.pkl','wb') as f2:
    pickle.dump(data,f2)

with open('./data/data_pos.pkl','wb') as f3:
    pickle.dump(data_pos,f3)

with open('./data/sen_feature.pkl','wb') as f4:
    pickle.dump(sen_feature,f4)
