# -*- coding: utf-8 -*-
from commonUtils.CommonUtils import sentence_split, clean_sent
from commonUtils.MyPyLtp import MyPyLtp
from sklearn.decomposition import PCA
from sklearn.metrics.pairwise import cosine_similarity

import joblib
import os
import fasttext
import numpy as np
import operator
import random


class Word:
    def __init__(self, word, vector):
        self.word = word
        self.word_vector = vector


class Sentence:
    def __init__(self, vector):
        self.sent_vector = vector

    def len(self) -> int:
        return len(self.sent_vector)


class SentSim:
    def __init__(self, idx, sim):
        self.idx = idx
        self.sim = sim


class AbstractExtractionModel:
    embedding_size = 150  # 词向量的维度

    threshold = '0.6'  # 相似度大小阈值

    def __init__(self):
        self.root_path = os.path.dirname(os.path.abspath(__file__))
        # 可以用来获取每个词语的词向量 word_to_vector
        self.fast_model = fasttext.load_model(self.root_path + "fast2.bin")
        # 每个词出现的次数
        self.word_count_dict = joblib.load(self.root_path + '/word_count_dict.pkl')  # word={'此外':4241,'本周':483, ...}
        self.init_all_word_count(self.word_count_dict)

    def init_all_word_count(self, word_count_dict):
        count = 0
        for k, v in word_count_dict.item():
            count += v
        self.all_word_count = count

    def get_word_frequency(self, word, word_count_dict):  # 计算语料库中每个单词出现的频率
        if word in word_count_dict:
            return word_count_dict[word] / self.all_word_count
        else:
            return 0.0

    # wordEmbeddings:
    def sentence_to_vec(self, sentences, embedding_size, word_count_dict, a=1e-3):
        sentence_set = []
        for sentence in sentences:
            vs = np.zeros(embedding_size)  # add all word2vec values into one vector for the sentence
            sentence_length = sentence.len()
            for word in sentence.sent_vector:
                a_value = a / (a + self.get_word_frequency(word.word, word_count_dict))  # smooth inverse frequency, SIF
                vs = np.add(vs, np.multiply(a_value, word.word_vector))  # vs += sif * word_vector
            vs = np.divide(vs, sentence_length)  # weighted average
            sentence_set.append(vs)  # add to our existing re-calculated set of sentences
        # calculate PCA of this sentence set
        pca = PCA()  # (n_components=embedding_size)
        pca.fit(np.array(sentence_set))
        u = pca.components_[0]  # the PCA vector
        u = np.multiply(u, np.transpose(u))  # u x uT
        # pad the vector?  (occurs if we have less sentences than embeddings_size)
        if len(u) < embedding_size:
            for i in range(embedding_size - len(u)):
                u = np.append(u, 0)  # add needed extension for multiplication below
        # resulting sentence vectors, vs = vs -u x uT x vs
        sentence_vecs = []
        for vs in sentence_set:
            sub = np.multiply(u, vs)
            sentence_vecs.append(np.subtract(vs, sub))
        return sentence_vecs

    def generate_abstract(self, sentence_vectors, sentences_dict):
        paragragh_vec = sentence_vectors[-1]  # 最后一个是整篇文档向量
        # 计算每个句子与文章的相似度, 并找出相似度比设定阈值较高的句子
        sent_sim = []
        for i in range(len(sentence_vectors) - 1):
            sim = cosine_similarity([sentence_vectors[i], paragragh_vec])
            sim_value = sim[0][1]
            if sim_value > float(self.threshold):
                sent_sim.append(SentSim(i, sim_value))
        # 安装相似度高低排序
        order_by = operator.attrgetter('sim')
        sent_sim.sort(key=order_by, reverse=True)
        # 选取相似度最高的几个句子
        random_n = random.sample([i for i in range(4, 8)], 1)
        if len(sent_sim) > random_n:
            sent_sim = sent_sim[:random_n]
        abstract = ''
        for ele in sent_sim:
            abstract += str(sentences_dict[ele.idx])
        # 去掉句子中的某些修饰词语 TUDO
        return abstract

    # 计算每个句子与整篇文档的相似度，大于阈值的留下
    def simple_extract(self, text):
        sents = sentence_split(text)
        sentences_dict, sents_clean = clean_sent(sents)
        # 整篇文章的词
        whole_words = []
        # 整篇文章的所有句子的句子向量
        whole_sents = []
        ltp = MyPyLtp()
        for sent in sents_clean:
            # 每个句子 = [word1_vector, word2_vector, ...]
            sent_obj = []
            # 先分词
            words = ltp.split_word(sent)
            for word in words:
                # 获得每个词语的词向量
                word_vector = self.fast_model.get_word_vector(word)
                word_obj = Word(word, word_vector)
                sent_obj.append(word_obj)
                whole_words.append(word_obj)
            sentence = Sentence(sent_obj)
            whole_sents.append(sentence)
        # 整篇文章当成一个句子
        one_sents = Sentence(whole_words)
        whole_sents.append(one_sents)
        sentence_vectors = self.sentence_to_vec(whole_sents, self.embedding_size, self.word_count_dict)
        return self.generate_abstract(sentence_vectors, sentences_dict)


# 分析：
# 1、先对原文本text进行分句，
# 2、找主语：主语一定在动词的左边，根据上一步找出的核心词为中心。
# 3、言论内容：可能在关键动词的右边，也可能在主语的左边。

if __name__ == '__main__':
    # text = "昨天是小强的生日，我们应该给他买个礼物，张晓玲在会上说。"
    text = """
    习近平强调，创新是乡村全面振兴的重要支撑。要坚持把科技特派员制度作为科技创新人才服务乡村振兴的重要工作进一步抓实抓好。广大科技特派员要秉持初心，在科技助力脱贫攻坚和乡村振兴中不断作出新的更大的贡献。

　　科技特派员制度推行20周年总结会议21日在北京召开，会上传达了习近平的重要指示。

　　中共中央政治局委员、国务院副总理刘鹤出席会议并讲话。他表示，习近平总书记的重要指示是新时代深入推进科技特派员制度的根本遵循和行动指南。20年来，科技特派员制度坚持以服务“三农”为出发点和落脚点、以科技人才为主体、以科技成果为纽带，在推动乡村振兴发展、助力打赢脱贫攻坚战中取得显著成效。新时代深入实施科技特派员制度，要紧紧围绕创新驱动发展、乡村振兴和脱贫攻坚，进一步完善制度体系和政策环境，进一步发展壮大科技特派员队伍，把创新的动能扩散到田间地头。

　　会议对92名科技特派员和43家组织实施单位进行了通报表扬。浙江省、福建省南平市、江西省井冈山市和科技特派员代表在会上作交流发言。

　　有关部门负责同志，各省区市和计划单列市、新疆生产建设兵团有关负责同志，部分通报表扬的科技特派员和组织实施单位代表等参加会议。    """
    # text = '台湾政府声称要与大陆实现完全统一。'
    model = AbstractExtractionModel()
    result = model.simple_extract(text)
    print(result)

    # with open('keywords.txt', 'w') as f:
    #     for k, v in model.keywords.items():
    #         f.write(k+'\n')

    for ele in result:
        print(' '.join(str(ele)))
