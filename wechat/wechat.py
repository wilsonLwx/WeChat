# -*- coding:utf-8 -*-
from flask import Flask, request
import xmltodict
import hashlib
import time
# 解决编码问题

import sys

reload(sys)
sys.setdefaultencoding('utf-8')

WECHAT_TOKEN = "ITCAST"
app = Flask(__name__)


@app.route('/wechat8026', methods=['get', 'post'])
def wechat8026():
    args = request.args
    # 1. 获取参数
    signature = args.get("signature")
    timestamp = args.get("timestamp")
    nonce = args.get("nonce")
    echostr = args.get("echostr")

    # 2. 校验参数
    # 1）将token、timestamp、nonce三个参数进行字典序排序
    temp = [timestamp, nonce, WECHAT_TOKEN]
    temp.sort()

    # 2）将三个参数字符串拼接成一个字符串进行sha1加密
    temp = "".join(temp)
    sig = hashlib.sha1(temp).hexdigest()

    # 3) 开发者获得加密后的字符串可与signature对比
    if signature == sig:
        # 代表是来自于微信的请求
        if request.method == 'get':
            return echostr
        else:
            # 获取xml数据
            '''
            <xml>
            <ToUserName><![CDATA[toUser]]></ToUserName>
            <FromUserName><![CDATA[fromUser]]></FromUserName>
            <CreateTime>12345678</CreateTime>
            <MsgType><![CDATA[text]]></MsgType>
            <Content><![CDATA[你好]]></Content>
            </xml>
            '''
            request_data = request.data
            # 将xml数据转换成字典
            request_dict = xmltodict.parse(request_data)['xml']
            if request_dict['MsgType'] == 'text':
                # 拼接内容节点
                response = {
                    'ToUserName': request_dict['FromUserName'],
                    'FromUserName': request_dict['ToUserName'],
                    'CreateTime': time.time(),
                    'MsgType': 'text',
                    'Content': request_dict['Content'],
                }
                # 将字典转换成xml格式
                response = xmltodict.unparse({'xml': response})
                print request_dict['Content']
                # 返回xml数据
                return response

            elif 'voice' == request_dict['MsgType']:

                print '接收到了语音消息'

                # 拼接xml的内容节点

                response = {
                    'ToUserName': request_dict['FromUserName'],
                    'FromUserName': request_dict['ToUserName'],
                    'CreateTime': time.time(),
                    'MsgType': 'text',
                    'Content': request_dict['Recognition'],
                }

                print request_dict['Recognition']
                response = xmltodict.unparse({'xml': response})
                return response
            else:
                response = {
                    'ToUserName': request_dict['FromUserName'],
                    'FromUserName': request_dict['ToUserName'],
                    'CreateTime': time.time(),
                    'MsgType': 'text',
                    'Content': '呵呵,不认识！',

                }
                # 拼接根节点
                response = xmltodict.unparse({'xml': response})
                print request_dict['Content']
                return response
    return ''


if __name__ == '__main__':
    app.run(debug=True, port=8026)
