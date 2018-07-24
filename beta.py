import os

LTP_DATA_DIR="D:\myprojects\LTP\ltp_data_v3.4.0"
cws_model_path = os.path.join(LTP_DATA_DIR, 'cws.model')
pos_model_path = os.path.join(LTP_DATA_DIR, 'pos.model')
par_model_path = os.path.join(LTP_DATA_DIR, 'parser.model')  # 依存句法分析模型路径，模型名称为`parser.model`
ner_model_path = os.path.join(LTP_DATA_DIR, 'ner.model')     #命名实体识别
srl_model_path = os.path.join(LTP_DATA_DIR, 'srl')

from pyltp import Segmentor,Postagger,Parser,NamedEntityRecognizer,SementicRoleLabeller

segmentor = Segmentor()  # 初始化实例
segmentor.load(cws_model_path)
postagger = Postagger() # 初始化实例
postagger.load(pos_model_path)  # 加载模型
parser = Parser() # 初始化实例
parser.load(par_model_path)  # 加载模型
recognizer = NamedEntityRecognizer()
recognizer.load(ner_model_path)
labeller = SementicRoleLabeller()
labeller.load(srl_model_path)


line='手机外型很漂亮，屏幕也不错，就是太容易发烫了，电池不耐用，这些都是预想到的，我很少玩游戏就还好。喇叭真的太垃圾了。'

words = list(segmentor.segment(line))
postags = list(postagger.postag(words))
arcs = parser.parse(words, postags)  # 句法分析
netags = recognizer.recognize(words, postags)  # 命名实体识别
roles = labeller.label(words, postags, netags, arcs)


print(words)
print(postags)
print("\t".join("%d:%s" % (arc.head, arc.relation) for arc in arcs))
print('\t'.join(netags))
for role in roles:
    print(role.index, "".join(
        ["%s:(%d,%d)" % (arg.name, arg.range.start, arg.range.end) for arg in role.arguments]))

segmentor.release()  # 释放模型
postagger.release()  # 释放模型
parser.release()  # 释放模型
parser.release()  # 释放模型