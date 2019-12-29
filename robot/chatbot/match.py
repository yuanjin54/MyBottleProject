# -*- coding:utf-8 -*-
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
from scipy.spatial.distance import cosine
import numpy as np
import jieba
import re
from collections import Counter
from spherecluster import SphericalKMeans
from robot.chatbot.embedding import Embedding
from robot.chatbot.utils import write_json
from typing import List, Tuple
from bert_serving.client import BertClient

regex = re.compile(r'^[\d\w]+$')


class Retrieve(object):
    def __init__(self, config):
        self.config = config
        self.data = pd.read_csv(config['knowledge_base'])

    def _gen_vocab(self):
        word_counter = Counter()
        for sent in self.data['question']:
            word_counter.update(
                [word for word in jieba.cut(sent) if regex.search(word)])
        write_json(word_counter, self.config['vocab_path'])
        return word_counter

    def _init_search(self):
        self.tfidf_vectorizer = TfidfVectorizer(max_features=10000)
        tfidf = self.tfidf_vectorizer.fit_transform(self.data['qs_processed']
                                                    .tolist())
        self.word2id = self.tfidf_vectorizer.vocabulary_
        self.id2word = {idx: word for word, idx in self.word2id.items()}
        self.tfidf_trans = tfidf.toarray().T

    def _preprocess(self):
        self.data.dropna(inplace=True)
        self.data['qid'] = self.data['qid'].astype(int)
        self._gen_vocab()
        self.data['qs_processed'] = self.data['question'].apply(lambda x: ' '.join(jieba.cut(x)))
        self.embedding = Embedding(self.config['vocab_path'], self.config['w2v_path'])
        self.data['qid'] = self.data['qid'].astype(int)
        self.data['qs_embed'] = self.data['qs_processed'].apply(
            lambda x: self.embedding.sentence_embedding(x.split()))

    def _init_match(self):
        skm = SphericalKMeans(n_clusters=self.config['cluster_nums'], init='k-means++', n_init=20)
        data = self.data
        data = data[data['qs_embed'].apply(
            lambda x: True if np.linalg.norm(x) > 0 else False)]
        skm.fit(data['qs_embed'].tolist())
        data['skm_label'] = skm.labels_
        data = data[['qid', 'skm_label']]
        self.data = pd.merge(self.data, data, how='left', on=['qid'])
        self.data['skm_label'] = self.data['skm_label'].fillna(-1)
        self._cluster_centers = skm.cluster_centers_

    def init(self):
        print('start init ...')
        self._preprocess()
        self._init_search()
        self._init_match()
        print('finished init ...')

    def search(self, words: List[str], top=10):
        docs = set()
        for word in words:
            if word not in self.word2id:
                continue
            idx = self.word2id[word]
            docs.update(set(np.where(self.tfidf_trans[idx])[0]))
        qs_tfidf = self.tfidf_vectorizer.transform([' '.join(words)]).toarray() \
            .flatten()
        distances = []
        for idx in docs:
            vec = self.tfidf_trans[:, idx].flatten()
            dist = cosine(qs_tfidf, vec)
            distances.append((idx, dist))
        docs_ids = [idx for idx, dist in sorted(distances, key=lambda x: x[1])[:
                                                                               top]]
        qids = []
        for row in self.data.loc[docs_ids].itertuples():
            qids.append(row.qid)
        return qids

    def shallow_match(self, words: List[str], top=10):
        words_embd = self.embedding.sentence_embedding(words)
        if np.linalg.norm(words_embd) == 0:
            return []
        min_dist = 20
        clus = -1
        for cid, center_embd in enumerate(self._cluster_centers):
            dist = cosine(center_embd, words_embd)
            if dist < min_dist:
                min_dist = dist
                clus = cid
        distances = []
        for row in self.data[self.data['skm_label'] == clus].itertuples():
            qid = row.qid
            qs_embed = row.qs_embed
            distances.append((qid, cosine(qs_embed, words_embd)))
        return [qid for qid, dist in sorted(distances, key=lambda x: x[1])[:top]]

    def qid2col(self, qid, col):
        return self.data[self.data['qid'] == qid][col].tolist()[0]


class SemanticMatch(object):
    """
    基于预训练中文bert的深层语义匹配
    """

    def __init__(self):
        self.bc = BertClient()

    def match(self, question: str, candidates: List[Tuple[int, str]], top=3):
        """
        candidates是召回的候选问题list，list中是(qid,question)组成的tuple
        :param question:
        :param candidates:
        :param top:
        :return:
        """
        qids, cand_sents = zip(*candidates)
        qs_embed = self.bc.encode([question])[0]
        cand_embed = self.bc.encode(list(cand_sents))
        similarities = [1. - cosine(qs_embed, embd) for embd in cand_embed]
        qids_sim = list(zip(qids, similarities))
        return sorted(qids_sim, key=lambda x: x[1], reverse=True)[:top]
