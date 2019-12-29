# -*- coding:utf-8 -*-
from robot.chatbot.match import Retrieve, SemanticMatch
from robot.chatbot.config import config
import jieba
from robot.chatbot.zhidao_spider import Spider


class ChatBot(object):
    def __init__(self):
        self.retriever = Retrieve(config)
        self.retriever.init()
        self.matcher = SemanticMatch()
        self.spider = Spider()

    def answer(self, question):
        words = list(jieba.cut(question))
        candidates_qids = self.retriever.search(words, top=10) + self.retriever.shallow_match(words, top=10)
        cands_qs = []
        for row in self.retriever.data[self.retriever.data['qid'].isin(candidates_qids)].itertuples():
            cands_qs.append((row.qid, row.question))
        matched_qs = self.matcher.match(question, cands_qs)
        suggest_qs_ans = (None, None)
        if len(matched_qs) > 0 and matched_qs[0][1] >= config['similarity_threshold']:
            ans = self.retriever.qid2col(matched_qs[0][0], 'answer')
            return ans
        elif len(matched_qs) > 0 and matched_qs[0][1] < config['similarity_threshold']:
            qid = matched_qs[0][0]
            suggest_qs_ans = (self.retriever.qid2col(qid, 'question'), self.retriever.qid2col(qid, 'answer'))
        spider_qs_ans = self.spider.search_qs(question)
        spider_qs_nb = [(i, spider_qs_ans[i][0]) for i in range(len(spider_qs_ans))]
        spider_match = self.matcher.match(question, spider_qs_nb)
        if len(spider_match) > 0 and spider_match[0][1] >= config['similarity_threshold']:
            return spider_qs_ans[spider_match[0][0]][1]
        elif len(spider_match) > 0 and spider_match[0][1] < config['similarity_threshold'] and suggest_qs_ans == (
                None, None):
            ind = spider_match[0][0]
            suggest_qs_ans = (spider_qs_ans[ind][0], spider_qs_ans[ind][1])
        if suggest_qs_ans != (None, None):
            return config['suggest_temp'].format(question=suggest_qs_ans[0], answer=suggest_qs_ans[1])
        else:
            return self._gen_suggest_qs(question)

    def eval(self, question, topn=10):
        words = list(jieba.cut(question))
        candidates_qids = self.retriever.search(words, top=10) + self.retriever.shallow_match(words, top=10)
        cands_qs = []
        for row in self.retriever.data[self.retriever.data['qid'].isin(candidates_qids)].itertuples():
            cands_qs.append((row.qid, row.question))
        matched_qs = self.matcher.match(question, cands_qs, top=20)
        qids, _ = zip(*matched_qs[:topn])
        res = self.retriever.data[self.retriever.data['qid'].isin(qids)]['question'].tolist()
        if len(res) < topn:
            res += [''] * (topn - len(res))
        return res

    def _gen_suggest_qs(self, question):
        return '非常抱歉，我不太明白您的意思'


if __name__ == '__main__':
    qs = '网银贷款申请的种类有哪些'
    cands = [(1, '一个客户最多可以用几个手机号码开通账户变动通知服务'), (2, '车票允许改签吗'),
             (3, '补发网银盾'), (4, '代发工资	')]

    sm = SemanticMatch()
    result = sm.match(qs, cands)
    print(result)

    chatbot = ChatBot()
    question = '网银申请贷款有哪些种类啊'
    ans = chatbot.answer(question)
    print(ans)
