# -*- coding:utf-8 -*-

from flask import Flask
import time
import urllib2
import json

app = Flask(__name__)
APPID = 'wx8e697a61d0c72418'
APPSECRET = '5b021a1be63cfcbdae9af3768fc0a3ce'


class AccessToken(object):
    __access_token = {
        'access_token': '',
        'update_time': time.time(),
        'expires_in': 7200
    }

    @classmethod
    def get_access_token(cls):
        # 1. 是否存在  2. 是否过期 3. 返回token
        if not cls.__access_token.get('access_token') or \
                (time.time() - cls.__access_token.get('update_time') > cls.__access_token.get('expires_in')):

            url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s' % (
                APPID, APPSECRET)

            response = urllib2.urlopen(url)

            resp_data = response.read()

            resp_dict = json.loads(resp_data)

            if 'errcode' in resp_dict:
                raise Exception(resp_dict.get('errmsg'))

            cls.__access_token['access_token'] = resp_dict.get('access_token')
            cls.__access_token['expires_in'] = resp_dict.get('expires_in')
            cls.__access_token['update_time'] = time.time()

        return cls.__access_token.get('access_token')


@app.route('/get_qrcode/<scene_id>')
def hello_world(scene_id):
    # 获取带参数的二维码的过程包括两步，首先创建二维码ticket，然后凭借ticket到指定URL换取二维码。

    # 1. 发送请求, 获取ticket
    url = 'https://api.weixin.qq.com/cgi-bin/qrcode/create?access_token=' + AccessToken.get_access_token()
    params = {"expire_seconds": 604800, "action_name": "QR_SCENE", "action_info": {"scene": {"scene_id": scene_id}}}
    response = urllib2.urlopen(url, data=json.dumps(params))

    # 获取返回的数据(字符串)
    resp_data = response.read()
    # 将字符串转化成字典
    response_dict = json.loads(resp_data)
    # 从字典中获取ticket
    ticket = response_dict['ticket']
    # 通过ticket换取二维码
    qrcode_url = 'https://mp.weixin.qq.com/cgi-bin/showqrcode?ticket=' + ticket
    return "<image src='%s'>" % qrcode_url


if __name__ == '__main__':
    app.run(debug=True)
