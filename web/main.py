# -*- coding: utf-8 -*-
from bottle import get, post, request, route, run, template, static_file
from speakingExtraction import ExtractionModel

import sys
import os
import warnings

warnings.filterwarnings("ignore")

root_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(root_path)


@get('/')
def index():
    return template('pages/helloWorld.html')


# 自动言论抽取
@post('/speaking-extraction')
def speakingExtraction():
    requestion = request.POST.decode('utf-8')
    data = []
    result = {}
    # print(username)
    example1 = [1, "习近平", "指出", "既要决胜全面建成小康社会，又要开启全面建设社会主义现代化国家新征程"]
    data.append(example1)
    example2 = [2, "奥巴马", "提出", "两项不受布什现有教育政策框架限制,也不以特定利益团体为优惠对象的教育主张,即对学前教育提出“0岁至5岁教育计划”"]
    data.append(example2)
    example3 = [3, "马化腾", "认为", "发展产业互联网,将为实体经济高质量发展提供历史机遇和技术条件,提供新引擎和新动力,对实体经济产生全方位、深层次、革命性的影响"]
    data.append(example3)
    example4 = [4, "刘强东", "表示", "五环外的营收及活跃用户 截至2019年6月30日,京东过去12个月的活跃用户数为3.213亿,继续保持增长"]
    data.append(example4)

    try:
        # 获取文本内容
        text = requestion.get('text')
        if text is not None and text.strip() != '':
            text = text.strip()
            if text != 'test':
                model = ExtractionModel.SpeakingExtractionModel()
                data = model.extract()
            if len(data) < 1:
                result["data"] = None
                result["code"] = 2
                result["msg"] = 'The result is null!'
            else:
                result["data"] = data
                result["code"] = 1
                result["msg"] = 'success'
        else:
            result["data"] = None
            result["code"] = 2
            result["msg"] = 'The result is null!'
    except Exception as e:
        result["data"] = None
        result["code"] = 0
        result["msg"] = 'The model exception, {}'.format(e)
        print('exception:', e)
    return result


# 自动摘要提取
@post('/abstract')
def getAbstract():
    return None


run(host="0.0.0.0", port=8868, server="tornado")