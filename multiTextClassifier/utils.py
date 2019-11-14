# coding: UTF-8
import torch
from tqdm import tqdm
import time
from datetime import timedelta
import pandas as pd
from sklearn.utils import shuffle

PAD, CLS = '[PAD]', '[CLS]'  # padding符号, bert中综合信息符号


def build_dataset(config):
    def load_dataset(path, pad_size=config.pad_size):
        contents = []
        with open(path, 'r', encoding='UTF-8') as f:
            for line in tqdm(f):
                lin = line.strip()
                if not lin:
                    continue
                content, label = lin.split('\t')
                token = config.tokenizer.tokenize(content)
                token = [CLS] + token
                seq_len = len(token)
                mask = []
                token_ids = config.tokenizer.convert_tokens_to_ids(token)

                if pad_size:
                    if len(token) < pad_size:
                        mask = [1] * len(token_ids) + [0] * (pad_size - len(token))  # 是否为填充的对象
                        token_ids += ([0] * (pad_size - len(token)))
                    else:
                        mask = [1] * pad_size
                        token_ids = token_ids[:pad_size]
                        seq_len = pad_size
                contents.append((token_ids, int(label), seq_len, mask))
        return contents

    train = load_dataset(config.train_path, config.pad_size)
    dev = load_dataset(config.dev_path, config.pad_size)
    test = load_dataset(config.test_path, config.pad_size)
    return train, dev, test


def build_dataset_csv_train(config):
    def load_dataset_train(path, pad_size=config.pad_size):

        # 平均长度348个

        # 解决类别不平衡

        file = pd.read_csv(path)
        value_count = file[config.feature_name].value_counts()
        count_base = value_count[1]

        final_result = file[['content', config.feature_name]][file[config.feature_name] == 1]
        for i in [-2, -1, 0]:
            if value_count[i] > count_base:
                temp = file[['content', config.feature_name]][file[config.feature_name] == i][
                       :count_base]
                final_result = final_result.append(temp)
            else:
                copy_times = count_base // value_count[i]
                temp_file = file[['content', config.feature_name]][file[config.feature_name] == i]
                temp = [temp_file] * copy_times
                final_result = final_result.append(pd.concat(temp))
        print(final_result[config.feature_name].value_counts())
        contents = []
        final_result = final_result.reset_index()
        final_result = shuffle(final_result)
        print('final_result shuffle')
        # for i in range(100):
        for i in range(len(final_result)):

            lin = final_result.loc[i]['content']

            content = regular(str(lin))
            label = final_result.loc[i][config.feature_name] + 2  # 让序号从0，1，2，3
            token = config.tokenizer.tokenize(content)
            token = [CLS] + token
            seq_len = len(token)
            mask = []
            token_ids = config.tokenizer.convert_tokens_to_ids(token)

            if pad_size:
                if len(token) < pad_size:
                    mask = [1] * len(token_ids) + [0] * (pad_size - len(token))  # 是否为填充的对象
                    token_ids += ([0] * (pad_size - len(token)))
                else:
                    mask = [1] * pad_size
                    token_ids = token_ids[:pad_size]
                    seq_len = pad_size
            contents.append((token_ids, int(label), seq_len, mask))
            contents = shuffle(contents)

        return contents

    train = load_dataset_train(config.train_path, config.pad_size)
    print(config.feature_name + ' already shuffle')

    return train


def build_dataset_csv_test(config):
    def load_dataset_test(path, pad_size=config.pad_size):

        # 平均长度348个

        final_result = pd.read_csv(path)

        contents = []

        for i in range(len(final_result)):
            lin = final_result.loc[i]['content']

            content = regular(str(lin))
            label = final_result.loc[i][config.feature_name] + 2  # 让序号从0，1，2，3
            token = config.tokenizer.tokenize(content)
            token = [CLS] + token
            seq_len = len(token)
            mask = []
            token_ids = config.tokenizer.convert_tokens_to_ids(token)

            if pad_size:
                if len(token) < pad_size:
                    mask = [1] * len(token_ids) + [0] * (pad_size - len(token))  # 是否为填充的对象
                    token_ids += ([0] * (pad_size - len(token)))
                else:
                    mask = [1] * pad_size
                    token_ids = token_ids[:pad_size]
                    seq_len = pad_size
            contents.append((token_ids, int(label), seq_len, mask))

        return contents

    dev = load_dataset_test(config.dev_path, config.pad_size)

    return dev


import re


def regular(string):
    # regular expression next course.
    string2 = string.replace('\\n', '')
    string2 = re.findall('\w+', string2)
    return "".join(string2)


class DatasetIterater(object):
    def __init__(self, batches, batch_size, device):
        self.batch_size = batch_size
        self.batches = batches
        self.n_batches = len(batches) // batch_size
        self.residue = False  # 记录batch数量是否为整数
        if len(batches) % self.n_batches != 0:
            self.residue = True
        self.index = 0
        self.device = device

    def _to_tensor(self, datas):
        x = torch.LongTensor([_[0] for _ in datas]).to(self.device)
        y = torch.LongTensor([_[1] for _ in datas]).to(self.device)

        # pad前的长度(超过pad_size的设为pad_size)
        seq_len = torch.LongTensor([_[2] for _ in datas]).to(self.device)
        mask = torch.LongTensor([_[3] for _ in datas]).to(self.device)
        return (x, seq_len, mask), y

    def __next__(self):
        if self.residue and self.index == self.n_batches:
            batches = self.batches[self.index * self.batch_size: len(self.batches)]
            self.index += 1
            batches = self._to_tensor(batches)
            return batches

        elif self.index > self.n_batches:
            self.index = 0
            raise StopIteration
        else:
            batches = self.batches[self.index * self.batch_size: (self.index + 1) * self.batch_size]
            self.index += 1
            batches = self._to_tensor(batches)
            return batches

    def __iter__(self):
        return self

    def __len__(self):
        if self.residue:
            return self.n_batches + 1
        else:
            return self.n_batches


def build_iterator(dataset, config):
    iter = DatasetIterater(dataset, config.batch_size, config.device)
    return iter


def get_time_dif(start_time):
    """获取已使用时间"""
    end_time = time.time()
    time_dif = end_time - start_time
    return timedelta(seconds=int(round(time_dif)))
