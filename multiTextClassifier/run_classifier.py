# coding: UTF-8
import time
import torch
import numpy as np
from train_eval import train, init_network
from importlib import import_module
import argparse
import os
import joblib
from utils import build_dataset, build_iterator, get_time_dif, build_dataset_csv_train, build_dataset_csv_test

parser = argparse.ArgumentParser(description='Chinese Text Classification')
# parser.add_argument('--model', type=str, required=True, help='choose a model: Bert, ERNIE')
parser.add_argument('--model', type=str, default='bert', help='choose a model: Bert, ERNIE')
parser.add_argument('--feature', type=str, default='price_level', help='choose 1 feature from 20 features')
args = parser.parse_args()

if __name__ == '__main__':
    dataset = 'dzdp'  # 数据集
    model_name = args.model  # bert
    x = import_module('models.' + model_name)
    config = x.Config(dataset, args)
    if not os.path.exists(config.dir_path):
        os.makedirs(config.dir_path)
    np.random.seed(1)
    torch.manual_seed(1)
    torch.cuda.manual_seed_all(1)
    torch.backends.cudnn.deterministic = True  # 保证每次结果一样

    start_time = time.time()
    print("Loading data...")

    if not os.path.exists(config.train_data_pkl):
        print('train pkl not exits , need preprocessing... ')
        train_data = build_dataset_csv_train(config)  # 已经处理好存在本地，每次处理太花时间
        joblib.dump(train_data, config.train_data_pkl)
        print('the train pkl has been saved ')
    else:
        print('train pkl exits ,just load...')
        train_data = joblib.load(config.train_data_pkl)

    if not os.path.exists(config.dev_data_pkl):
        print('dev pkl not exits , need preprocessing... ')
        dev_data = build_dataset_csv_test(config)  # 已经处理好存在本地，每次处理太花时间
        joblib.dump(dev_data, config.dev_data_pkl)
        print('the dev pkl has been saved ')
    else:
        print('dev pkl exits ,just load...')
        dev_data = joblib.load(config.dev_data_pkl)

    len_train = len(train_data) - (len(train_data) % config.batch_size) - 1
    print(len_train)
    train_data = train_data[:len_train]

    len_dev = len(dev_data) - (len(dev_data) % config.batch_size) - 1
    print(len_dev)
    dev_data = dev_data[:len_dev]
    test_data = dev_data

    print('all data prepared..')
    train_iter = build_iterator(train_data, config)
    dev_iter = build_iterator(test_data, config)
    test_iter = build_iterator(test_data, config)
    time_dif = get_time_dif(start_time)
    print("Time usage:", time_dif)

    # train
    model = x.Model(config).to(config.device)
    train(config, model, train_iter, dev_iter, test_iter)
