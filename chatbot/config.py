# -*- coding:utf-8 -*-

config = {
    'knowledge_base': '../chatbot/data/qa_corpus.csv',
    'suggest_temp': '您是想问：{question} 吗？这个问题的回答是：{answer}',
    'similarity_threshold': 0.9,
    'vocab_path': '../chatbot/data/vocab.json',
    'w2v_path': '../chatbot/data/sgns.wiki.word2vec',
    'cluster_nums': 120,
    'eval_path': '../chatbot/data/qa_val.csv'
}
