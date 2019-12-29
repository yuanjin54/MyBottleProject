# -*- coding:utf-8 -*-
import json
import codecs


def write_json(obj, path):
    with open(path, 'w') as f:
        json.dump(obj, f)
    print('write data successfully...')


def read_json(path):
    with open(path, 'r') as f:
        data = json.load(f)
    return data
