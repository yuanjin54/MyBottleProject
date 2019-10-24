# -*- coding: utf-8 -*-
from pyltp import SentenceSplitter, Segmentor, Postagger, NamedEntityRecognizer, Parser

import os
import warnings

warnings.filterwarnings("ignore")


class MyPyLtp:
    # 本地配置ltp model路径
    LTP_DATA_DIR = '/Users/yuanjin/PycharmProjects/ltp_data_v3.4.0'  # ltp模型目录的路径
    # linux配置ltp model路径
    # LTP_DATA_DIR = '/home/student/project/project-01/ltp_data'
    pos_model_path = os.path.join(LTP_DATA_DIR, 'pos.model')  # 词性标注模型路径，模型名称为`pos.model`
    cws_model_path = os.path.join(LTP_DATA_DIR, 'cws.model')
    special_word_path = os.path.join(LTP_DATA_DIR, 'special_word.txt')
    ner_model_path = os.path.join(LTP_DATA_DIR, 'ner.model')
    parser_model_path = os.path.join(LTP_DATA_DIR, 'parser.model')

    # 初始化模型
    def __init__(self):
        # 初始化实例，加载模型
        self.segmentor = Segmentor()  # 初始化实例
        self.segmentor.load_with_lexicon(self.cws_model_path, self.special_word_path)  # 加载模型，第二个参数是您的外部词典文件路径
        self.postagger = Postagger()
        self.postagger.load(self.pos_model_path)
        self.recognizer = NamedEntityRecognizer()
        self.recognizer.load(self.ner_model_path)
        self.parser = Parser()
        self.parser.load(self.parser_model_path)

    # 分句
    def split_sentence(self, text):
        return SentenceSplitter.split(text)

    # 分词
    def split_word(self, sentence):
        self.words = list(self.segmentor.segment(sentence))  # 分词
        return self.words

    # 词性标注
    def tagging_word(self):
        self.tagging = self.postagger.postag(self.words)  # 词性标注
        return self.tagging

    # 命名实体识别
    def name_recognizer(self):
        self.names = self.recognizer.recognize(self.words, self.tagging)  # 命名实体识别
        return self.names

    # 依存句法分析
    def relation_analysis(self, sentence):
        self.split_word(sentence)
        self.tagging_word()
        self.name_recognizer()

        arcs = self.parser.parse(self.words, self.tagging)  # 句法分析
        return [[arc.head, arc.relation] for arc in arcs]

if __name__ == '__main__':
    sentence = '''台湾工业总会指出，2015年的白皮书就特别提到台湾面临“五缺”（缺水、缺电、缺工、缺地、缺人才）困境，使台湾整体投资环境走向崩坏。然而四年过去，“五缺”未见改善，反而劳动法规日益僵化、两岸关系陷入紧张、对外关系更加孤立。该团体质疑，台当局面对每年的建言，“到底听进去多少，又真正改善了几多”？ '''
    # sentence = '''国家主席中央军委主席袁进表示青少年应该好好学习天天下降！'''
    sentence = '台湾政府声称要与大陆实现完全统一。'

    mypyltp = MyPyLtp()
    sents = mypyltp.split_sentence(sentence)
    print('\n'.join(sents))
    arcs = mypyltp.relation_analysis(sents[0])
    print('\t'.join(mypyltp.words))
    print('\t'.join(mypyltp.tagging))
    print('\t'.join(mypyltp.names))
    print("\t".join("%d:%s" % (arc[0], arc[1]) for arc in arcs))
