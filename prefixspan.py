#!/usr/bin/python
# -*- coding: utf-8 -*-
# author: Tianming Lu
# adapted by: Nicolas Rangeon

class PrefixSpan:
    def __init__(self, sequences, minSupport=0.1, maxPatternLength=10):

        minSupport = minSupport
        self.PLACE_HOLDER = '_'

        freqSequences = self._prefixSpan(
            self.SequencePattern([], None, maxPatternLength, self.PLACE_HOLDER),
            sequences, minSupport, maxPatternLength)

        self.freqSeqs = PrefixSpan.FreqSequences(freqSequences)

    @staticmethod
    def train(sequences, minSupport=0.1, maxPatternLength=10):
        return PrefixSpan(sequences, minSupport, maxPatternLength)

    def freqSequences(self):
        return self.freqSeqs

    class FreqSequences:
        def __init__(self, fs):
            self.fs = fs

        def collect(self):
            return self.fs

    class SequencePattern:
        def __init__(self, sequence, support, maxPatternLength, place_holder):
            self.place_holder = place_holder
            self.sequence = []
            for s in sequence:
                self.sequence.append(list(s))
            self.freq = support

        def append(self, p):
            if p.sequence[0][0] == self.place_holder:
                first_e = p.sequence[0]
                first_e.remove(self.place_holder)
                self.sequence[-1].extend(first_e)
                self.sequence.extend(p.sequence[1:])
            else:
                self.sequence.extend(p.sequence)
                if self.freq is None:
                    self.freq = p.freq
            self.freq = min(self.freq, p.freq)

    def _checkPatternLengths(self, pattern, maxPatternLength):
        for s in pattern.sequence:
            if len(s) > maxPatternLength:
                return False
        return True

    def _prefixSpan(self, pattern, S, threshold, maxPatternLength):
        patterns = []

        if self._checkPatternLengths(pattern, maxPatternLength):
            f_list = self._frequent_items(S, pattern, threshold, maxPatternLength)

            for i in f_list:
                p = self.SequencePattern(pattern.sequence, pattern.freq, maxPatternLength, self.PLACE_HOLDER)
                p.append(i)
                if self._checkPatternLengths(pattern, maxPatternLength):
                    patterns.append(p)

                p_S = self._build_projected_database(S, p)
                p_patterns = self._prefixSpan(p, p_S, threshold, maxPatternLength)
                patterns.extend(p_patterns)

        return patterns

    def _frequent_items(self, S, pattern, threshold, maxPatternLength):
        items = {}
        _items = {}
        f_list = []
        if S is None or len(S) == 0:
            return []

        if len(pattern.sequence) != 0:
            last_e = pattern.sequence[-1]
        else:
            last_e = []
        for s in S:

            # class 1
            is_prefix = True
            for item in last_e:
                if item not in s[0]:
                    is_prefix = False
                    break
            if is_prefix and len(last_e) > 0:
                index = s[0].index(last_e[-1])
                if index < len(s[0]) - 1:
                    for item in s[0][index + 1:]:
                        if item in _items:
                            _items[item] += 1
                        else:
                            _items[item] = 1

            # class 2
            if self.PLACE_HOLDER in s[0]:
                for item in s[0][1:]:
                    if item in _items:
                        _items[item] += 1
                    else:
                        _items[item] = 1
                s = s[1:]

            # class 3
            counted = []
            for element in s:
                for item in element:
                    if item not in counted:
                        counted.append(item)
                        if item in items:
                            items[item] += 1
                        else:
                            items[item] = 1

        f_list.extend([self.SequencePattern([[self.PLACE_HOLDER, k]], v, maxPatternLength, self.PLACE_HOLDER)
                       for k, v in _items.items()
                       if v >= threshold])
        f_list.extend([self.SequencePattern([[k]], v, maxPatternLength, self.PLACE_HOLDER)
                       for k, v in items.items()
                       if v >= threshold])

        # todo: can be optimised by including the following line in the 2 previous lines
        f_list = [i for i in f_list if self._checkPatternLengths(i, maxPatternLength)]

        sorted_list = sorted(f_list, key=lambda p: p.freq)
        return sorted_list

    def _build_projected_database(self, S, pattern):
        """
        suppose S is projected database base on pattern's prefix,
        so we only need to use the last element in pattern to
        build projected database
        """
        p_S = []
        last_e = pattern.sequence[-1]
        last_item = last_e[-1]
        for s in S:
            p_s = []
            for element in s:
                is_prefix = False
                if self.PLACE_HOLDER in element:
                    if last_item in element and len(pattern.sequence[-1]) > 1:
                        is_prefix = True
                else:
                    is_prefix = True
                    for item in last_e:
                        if item not in element:
                            is_prefix = False
                            break

                if is_prefix:
                    e_index = s.index(element)
                    i_index = element.index(last_item)
                    if i_index == len(element) - 1:
                        p_s = s[e_index + 1:]
                    else:
                        p_s = s[e_index:]
                        index = element.index(last_item)
                        e = element[i_index:]
                        e[0] = self.PLACE_HOLDER
                        p_s[0] = e
                    break
            if len(p_s) != 0:
                p_S.append(p_s)

        return p_S

import pickle

if __name__ == "__main__":

    with open('./data/data.pkl','rb')as f:
        sequences=pickle.load(f)

    # sequences = [
    #     [[1, 2], [3]],
    #     [[1], [3, 2], [1, 2]],
    #     [[1, 2], [5]],
    #     [[6]],
    # ]

    model = PrefixSpan.train(sequences, minSupport=2, maxPatternLength=2)
    result = model.freqSequences().collect()
    # for fs in result:
    #     print('{}, {}'.format(fs.sequence, fs.freq))


##=======改变结果格式===========##
#content=[
#       ["手电筒","收音机"],
#       [...]
#   ]
    content=[]
    for fs in result:
        i=fs.sequence
        if len(i)==1:
            content.extend(i)
            continue
        seq = []
        for j in i:
            seq.extend(j)
        content.append(seq)

##=======把项集里的词合并=========##
    t_words=[]
    t_words_num={}
    words_item={}     # 词：它的组成项
    for l in content:
        if len(l)==1:
            t_words.extend(l)
            t_words_num[l[0]]=1
            words_item[l[0]]=l[0]
        else:
            temp=''
            for i in range(len(l)):
                temp+=l[i]
            t_words.append(temp)
            t_words_num[temp]=0
            words_item[temp]=l
    t_words_set=set(t_words)


##=========去除未出现过的词=======##

    from pyltp import Segmentor, Postagger, Parser
    import os
    import pickle
    import copy

    LTP_DATA_DIR = "D:\myprojects\LTP\ltp_data_v3.4.0"
    cws_model_path = os.path.join(LTP_DATA_DIR, 'cws.model')
    pos_model_path = os.path.join(LTP_DATA_DIR, 'pos.model')
    par_model_path = os.path.join(LTP_DATA_DIR, 'parser.model')

    segmentor = Segmentor()  # 初始化实例
    segmentor.load(cws_model_path)  # 加载模型
    postagger = Postagger()
    postagger.load(pos_model_path)
    parser = Parser()
    parser.load(par_model_path)

    pre_sens = []  # 未分词的句子组成的列表
    with open('./data/file.txt', 'rt', encoding='utf-8') as f_pre:
        for l in f_pre:
            line = l.split(',', 4)[4][2:-4]
            pre_sens.append(line)

    data_pos = pickle.load(open('./data/data_pos.pkl', 'rb'))
    new_words_set = set()
    a = []
    for w in t_words_set:
        for l in pre_sens:
            if w in l:
                new_words_set.add(w)

    nnew_words_set=copy.deepcopy(new_words_set)
    xxx={}
    for w in nnew_words_set:
        number_word=0
        number_all=0
        for l in pre_sens:
            if w in l:
                words = list(segmentor.segment(l))  # 分词
                postags = list(postagger.postag(words))  # 词性标注
                arcs = list(parser.parse(words, postags))  # 句法分析
                if t_words_num[w]:
                    if w not in words:
                        continue
                    number_all += 1
                    if data_pos[w]=='n':
                        if arcs[words.index(w)].relation=='POB' and postags[arcs[words.index(w)].head-1]=='p':
                            number_word+=1
                            if w in new_words_set and number_word/number_all>0.25:
                                    new_words_set.remove(w)
                    # if data_pos[w]=='v':
                    #     if words.count(w)==1:
                    #         if arcs[words.index(w)].relation=='SBV' and postags[arcs[words.index(w)].head-1]=='a':
                    #             new_words_set.add(w)
                    #         if arcs[words.index(w)].relation == 'VOB' and postags[arcs[words.index(w)].head-1] == 'v':
                    #             new_words_set.add(w)
                    #     else:
                    #         a.append((w,words.count(w)))


##==========人工标注的评价对象=========##
    content_man=[]
    with open('./data/man_can.txt','rt',encoding='utf-8') as f1:
        for l in f1:
            content_man.append(l.split(',',4)[3][2:-1])
        data_man=set(content_man)


##==========计算TF-IDF值=============##
    # from pyltp import Segmentor, Postagger
    # import os
    # import pickle
    #
    # LTP_DATA_DIR = "D:\myprojects\LTP\ltp_data_v3.4.0"
    # cws_model_path = os.path.join(LTP_DATA_DIR, 'cws.model')
    # pos_model_path = os.path.join(LTP_DATA_DIR, 'pos.model')
    #
    # segmentor = Segmentor()  # 初始化实例
    # segmentor.load(cws_model_path)
    # postagger = Postagger()  # 初始化实例
    # postagger.load(pos_model_path)  # 加载模型
    #
    # tf_idf_all = []
    # tf_idf_sen = []
    # words_tf = {}
    # with open('./data/file.txt', 'rt', encoding='utf-8') as ft:
    #     for l in ft:
    #         line = l.split(',', 4)[4][2:-4]
    #         words = segmentor.segment(line)
    #         tf_idf_all.extend(words)
    #         tf_idf_sen.append(line)
    #     for w in new_words_num:
    #         if new_words_num[w]:
    #             words_tf[w]=tf_idf_all.count(w)
    #         else:
    #             num=0
    #             for s in tf_idf_sen:
    #                 for i in range(len(words_item[w])):
    #                     if words_item[w][i] not in s:
    #                         break
    #                 if i==len(words_item[w])-1:
    #                     num+=1
    #                 if w in s:
    #                     num+=1
    #             words_tf[w]=num

    # open('./data/words_tf_idf.pkl', 'rb')
    # fwti=pickle.load(open('./data/words_tf_idf.pkl','rb'))



    #写入筛选出的词的词频；
    # with open('./data/words_tf.pkl','wb') as wtf:
    #     pickle.dump(words_tf,wtf)

    #===============剪枝================##



    current_num=0
    for w in new_words_set:
        if w in data_man:
            current_num+=1
    current_j=current_num/len(new_words_set)
    current_z=current_num/len(data_man)
    print(current_num)
    print(len(new_words_set))
    print(len(data_man))
    print(current_j)
    print(current_z)

    # words_rest=copy.deepcopy(data_man)
    # for w in new_words_set:
    #     if w in words_rest:
    #         words_rest.remove(w)
    # print(words_rest)

    for cont in new_words_set:
        if cont not in data_man:
            print(cont)

    # for cont in data_man:
    #     if cont not in new_words_set:
    #         print(cont)