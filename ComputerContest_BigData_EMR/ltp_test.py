# -*- coding: utf-8 -*-
# import os
# LTP_DATA_DIR = r''  # ltp模型目录的路径
# par_model_path = os.path.join(LTP_DATA_DIR, 'parser.model')  # 依存句法分析模型路径，模型名称为`parser.model`
# cws_model_path = os.path.join(LTP_DATA_DIR, 'cws.model')  # 分词模型路径，模型名称为`cws.model`
# pos_model_path = os.path.join(LTP_DATA_DIR, 'pos.model')  # 词性标注模型路径，模型名称为`pos.model`


from pyltp import Segmentor
from pyltp import Postagger
from pyltp import Parser


# 分词
def segmentor(sentence=''):
    segmentor = Segmentor()  # 初始化实例
    segmentor.load(r'D:\SUFE\ComputerContest\QASystem\DrQA-CN-master\data\ltp_data_v3.4.0\cws.model')  # 加载模型
    words = segmentor.segment(sentence)  # 产生分词
    words_list = list(words)
    segmentor.release()  # 释放模型
    return words_list


# 词性标注
def posttagger(words):
    postagger = Postagger()  # 初始化实例
    postagger.load(r'D:\SUFE\ComputerContest\QASystem\DrQA-CN-master\data\ltp_data_v3.4.0\pos.model')
    postags = postagger.postag(words)  # 词性标注
    postagger.release()
    return postags


# 依存语义分析
def parse(words, postags):
    parser = Parser()  # 初始化实例
    parser.load(r'D:\SUFE\ComputerContest\QASystem\DrQA-CN-master\data\ltp_data_v3.4.0\parser.model')
    arcs = parser.parse(words, postags)  # 依存语义分析

    i = 0
    print('loc_head/head/relation/loc_tail/tail')
    for word, arc in zip(words, arcs):
        i = i + 1
        print( str(arc.head-1)+ '/' +str(words[arc.head-1])+ '/' + str(arc.relation) + '/' + str(i-1)+ '/' +str(words[i-1] ))
    parser.release()
    return arcs


if __name__ == '__main__':
    sentence = '“直肠癌根治标本”中分化腺癌（溃疡型），浸润至浆膜层，侵犯神经，脉管内见癌栓。上切端、下切端未见癌累及。找到肠系膜淋巴结 5/21 枚有癌转移。'

    words = segmentor(sentence)
    postags = posttagger(words)
    parse(words, postags)

