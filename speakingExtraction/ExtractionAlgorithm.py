# -*- coding: utf-8 -*-
from speakingExtraction.CommonUtils import sentence_split
from speakingExtraction.MyPyLtp import MyPyLtp

import joblib
import os


class MessageExtraction:
    KEYS = ['HED', 'COO', 'VOB']

    def __init__(self):
        self.root_path = os.path.dirname(os.path.abspath(__file__))
        self.keywords = joblib.load(self.root_path + '/keyword_similar.pkl')

    def selectVerbIdx(self, arcs, words):
        self.verbIdx = -1
        keywordIdx = []
        # 找出所有可能的动词的索引
        for i in range(len(arcs)):
            if arcs[i][1] in self.KEYS:
                keywordIdx.append(i)
        if len(keywordIdx) > 0:
            # 找出与“说”是最相似的词的索引
            for id in keywordIdx:
                if self.keywords[words[id]] > 2:
                    self.verbIdx = id
                    break

    # 查询关键动词
    def selectVerb(self, arcs, words):
        self.selectVerbIdx(arcs, words)
        if self.verbIdx >= 0:
            return words[self.verbIdx]

    # 主语名词索引一定在动词索引的左边
    def selectSpeakerIdx(self, arcs):
        self.speakerIdx = -1
        if self.verbIdx > 0:
            for i in range(self.verbIdx, -1, -1):
                if arcs[i][1] == 'SBV':
                    self.speakerIdx = i
                    break

    def selectSpeaker(self, tagging, arcs, words):
        self.selectSpeakerIdx(arcs)
        if self.speakerIdx >= 0:
            idx = self.speakerIdx - 1
            if idx >= 0 and tagging[idx] == 'ns':  # 台湾 政府 表示... => 台湾政府 表示 ...
                return ''.join(words[idx:self.speakerIdx + 1])

            return words[self.speakerIdx]

    # 言论内容可能在关键动词的右边，也可能在主语的左边
    def selectMessage(self, arcs, words):
        isEnd = False  # 默认表示言论内容在主语的左边
        idx = -1
        if self.verbIdx >= 0 and self.speakerIdx >= 0:
            # 判断动词后面不全是符号，说明有内容
            for i in range(self.verbIdx + 1, len(arcs)):
                if arcs[i][1] != 'WP':
                    idx = i
                    isEnd = True
                    break
            if isEnd:
                return ''.join(words[idx:])
            else:
                idx = -1
                for i in range(self.speakerIdx, -1, -1):
                    if arcs[i][1] == 'WP' and i - 1 > -1 and arcs[i - 1][1] != 'WP':  # 符号前面的一个词不是符号
                        idx = i
                        break
                if idx > -1:
                    return ''.join(words[:idx + 1])

    def extract(self, text):
        result = []
        if len(text) < 3:
            return result
        sentences = sentence_split(text)
        ltp = MyPyLtp()
        for sent in sentences:
            if len(sent.strip()) == 0:
                continue
            arcs = ltp.relation_analysis(sent)
            # print("分词结果：%s" % (ltp.words))
            # print("\t".join("%d:%s" % (arc[0], arc[1]) for arc in arcs))
            verb = self.selectVerb(arcs, ltp.words)
            speaker = self.selectSpeaker(ltp.tagging, arcs, ltp.words)
            message = self.selectMessage(arcs, ltp.words)
            if verb is not None:
                result.append([speaker, verb, message])
            # print("抽取结果：{}  {}  {}".format(speaker, verb, message))
        return result


# 分析：
# 1、找言论动词：首先要找出句子中的所有核心词（'HED'或者'COO'），并找出其中一个与“说”相似度最高的词。
# 2、找主语：主语一定在动词的左边，根据上一步找出的核心词为中心。
# 3、言论内容：可能在关键动词的右边，也可能在主语的左边。

if __name__ == '__main__':
    # text = "昨天是小强的生日，我们应该给他买个礼物，张晓玲在会上说。"
    text = """
    台湾工业总会是岛内最具影响力的工商团体之一，2008年以来，该团体连续12年发表对台当局政策的建言白皮书，集中反映岛内产业界的呼声。\
    台湾工业总会指出，2015年的白皮书就特别提到台湾面临“五缺”（缺水、缺电、缺工、缺地、缺人才）困境，使台湾整体投资环境走向崩坏。\
    然而四年过去，“五缺”未见改善，反而劳动法规日益僵化、两岸关系陷入紧张、对外关系更加孤立。该团体质疑，台当局面对每年的建言，\
    “到底听进去多少，又真正改善了几多”？围绕当局两岸政策，工总认为，由数据来看，当前大陆不仅是台湾第一大出口市场，亦是第一大进口来源及首位对外投资地，\
    建议台湾当局摒弃两岸对抗思维，在“求同存异”的现实基础上，以“合作”取代“对立”，为台湾多数民众谋福创利。\
    工总现任理事长、同时也是台塑企业总裁的王文渊指出，过去几年，两岸关系紧张，不仅影响岛内观光、零售、饭店业及农渔蔬果产品的出口，\
    也使得岛内外企业对投资台湾却步，2020年新任台湾领导人出炉后，应审慎思考两岸问题以及中国大陆市场。\
    “2022年是中国最重要的一年，国家致力于发展人工智能产业，将实现人民生活的智能化”，国家主席习近平在全国人大会议上明确指出。
    """
    # text = '台湾政府声称要与大陆实现完全统一。'
    model = MessageExtraction()
    result = model.extract(text)
    for ele in result:
        print(' '.join(ele))
