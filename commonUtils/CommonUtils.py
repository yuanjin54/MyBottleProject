from pyltp import SentenceSplitter  # 分句

import jieba  # 切词
import re


def sentence_split(text):
    sentences = []
    sents = list(SentenceSplitter.split(text))  # 分句
    if len(sents) < 1:
        return sentences
    for ele in sents:
        if len(ele.strip()) == 0:
            continue
        sentences.append(ele.strip())
    return sentences


# 返回结果{id:sentence}
def sentence_dict_split_by_text(text):
    sentences = {}
    sents = list(SentenceSplitter.split(text))  # 分句
    if len(sents) < 1:
        return sentences
    i = 0
    for ele in sents:
        if len(ele.strip()) == 0:
            continue
        sentences[i] = ele.strip()
        i += 1
    return sentences


def clean_sent(sents):
    sentences = {}
    sent_clean = []
    if len(sents) < 1:
        return sentences, sent_clean
    i = 0
    for ele in sents:
        if len(filter(ele.strip())) == 0:
            continue
        sentences[i] = ele.strip()
        sent_clean.append(filter(ele.strip()))
        i += 1
    return sentences, sent_clean


def cut_word(sentence):
    return ' '.join(jieba.cut(sentence))


# 文本预处理，正则化
def filter(string):
    string1 = string.replace('\\n', '')
    arr = re.findall('\w+', string1)
    return ''.join(arr)
