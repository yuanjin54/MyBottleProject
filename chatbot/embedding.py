# -*- coding:utf-8 -*-
import json
from gensim.models.keyedvectors import Word2VecKeyedVectors
from typing import List
import numpy as np


class Embedding(object):
    def __init__(self, vocab_path, w2v_path):
        self.vocab = self._load_vocab(vocab_path)
        self.embedding = self._load_w2v(w2v_path)
        self.dim = self._get_embedding_dim()

    def sentence_embedding(self, sentence: List[str]):
        a = 0.001
        sentence_embd = np.zeros(shape=(self.dim,))
        s_len = 0
        for word in sentence:
            if word in self.embedding:
                s_len += 1
                word_embd = a / (a + self.vocab.get(word, 0)) * self.embedding[word]
                sentence_embd += np.asarray(word_embd)
        return sentence_embd / max(s_len, 1)

    def _load_vocab(self, vocab_path):
        with open(vocab_path, 'r') as f:
            vocab = json.load(f)
        return vocab

    def _load_w2v(self, w2v_path):
        return Word2VecKeyedVectors.load_word2vec_format(w2v_path, binary=False)

    def _get_embedding_dim(self):
        word = self.embedding.index2word[0]
        return len(self.embedding[word])


if __name__ == '__main__':
    a = np.array([1, 2, 3, 4])
    print(a.shape)
    print('hello word')
