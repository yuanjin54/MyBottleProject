from pyltp import SentenceSplitter  # 分句

import jieba  # 切词


def sentence_split(text):
    return list(SentenceSplitter.split(text))  # 分句


def cut_word(sentence):
    return ' '.join(jieba.cut(sentence))
