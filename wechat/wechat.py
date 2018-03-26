# -*- coding:utf-8 -*-
from flask import Flask, request
import hashlib

WECHAT_TOKEN = "ITCAST"
app = Flask(__name__)


@app.route('/wechat8026',methods=['get','post'])
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
        return echostr

    return ''


if __name__ == '__main__':
    app.run(debug=True, port=8026)
