# -*- coding: utf-8 -*-
from speakingExtraction.CommonUtils import sentence_split
from speakingExtraction.MyPyLtp import MyPyLtp

import joblib
import os
import re


class SpeakingExtractionModel:
    KEYS = ['HED', 'COO', 'VOB']

    def __init__(self):
        self.root_path = os.path.dirname(os.path.abspath(__file__))
        self.keywords_path = self.root_path + '/keywords.txt'
        self.keywords = joblib.load(self.root_path + '/keyword_similar.pkl')

    def read_keywords(self):
        with open(self.keywords_path, 'r', encoding='utf-8') as f:
            self.keywords = [''.join(re.findall(r'\w+', ele)) for ele in f.readlines()]

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
                if self.keywords[words[id]] > 5:
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
            if idx >= 0 and tagging[idx] in ['ns', 'nh']:  # 台湾 政府 表示... => 台湾政府 表示 ...
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
            print("分词结果：%s" % (ltp.words))
            print(list(ltp.tagging))
            print("\t".join("%d:%s" % (arc[0], arc[1]) for arc in arcs))
            verb = self.selectVerb(arcs, ltp.words)
            speaker = self.selectSpeaker(ltp.tagging, arcs, ltp.words)
            message = self.selectMessage(arcs, ltp.words)
            if verb is not None:
                result.append([len(result) + 1, speaker, verb, message])
            # print("抽取结果：{}  {}  {}".format(speaker, verb, message))
        return result


# 分析：
# 1、找言论动词：首先要找出句子中的所有核心词（'HED'或者'COO'），并找出其中一个与“说”相似度最高的词。
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
    model = SpeakingExtractionModel()
    result = model.extract(text)
    model.read_keywords()

    # with open('keywords.txt', 'w') as f:
    #     for k, v in model.keywords.items():
    #         f.write(k+'\n')

    for ele in result:
        print(' '.join(str(ele)))
