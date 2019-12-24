# coding=utf-8
import pandas as pd
from chatbot.config import config
from chatbot import ChatBot


def main():
    topn = 20
    data = pd.read_csv(config['eval_path'])
    questions_sel = data.sample(100)['question'].tolist()

    ct_bot = ChatBot()
    topn_question = {'top' + str(i): [] for i in range(topn)}
    for question in questions_sel:
        cand_questions = ct_bot.eval(question, topn=topn)
        for i, qs in enumerate(cand_questions):
            topn_question['top' + str(i)].append(qs)
    topn_question['input'] = questions_sel
    topn_question['model'] = 'bert_match'
    eval_data = pd.DataFrame(topn_question)
    eval_data.to_csv('./data/eval_data.csv')
    print('finished create eval data')


if __name__ == '__main__':
    main()
