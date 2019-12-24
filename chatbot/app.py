# !/usr/bin/env Python
# coding=utf-8

from flask import Flask, render_template, request, make_response
from flask import jsonify

import sys
import time
import hashlib
import threading

# def heartbeat():
#     print (time.strftime('%Y-%m-%d %H:%M:%S - heartbeat', time.localtime(time.time())))
#     timer = threading.Timer(60, heartbeat)
#     timer.start()
# timer = threading.Timer(60, heartbeat)
# timer.start()
#
# try:
#     import xml.etree.cElementTree as ET
# except ImportError:
#     import xml.etree.ElementTree as ET

import re
from chatbot.chatbot import ChatBot

zhPattern = re.compile(u'[\u4e00-\u9fa5]+')
ct_bot = ChatBot()
print('chatbot initialization finished...')
app = Flask(__name__, static_url_path="/static")


@app.route('/message', methods=['POST'])
def reply():
    req_msg = request.form['msg']
    print(req_msg)
    answer = ct_bot.answer(req_msg)
    answer = answer.strip()
    # 如果接受到的内容为空，则给出相应的恢复
    # if res_msg == '':
    #     res_msg = ''

    return jsonify({'text': answer})


@app.route("/")
def index():
    return render_template("index.html")


# 启动APP
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9996)
