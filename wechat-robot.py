#! usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask
from flask import request
from xml.etree import ElementTree as ET
from flask import render_template
from urllib import urlopen
from json import loads


app = Flask(__name__)


@app.route('/weixin', methods=['GET', 'POST'])
def wechat():
    # 接收和返回GET请求，与微信服务器建立连接
    if request.method == 'GET':
        echostr = request.args.get('echostr')
        return echostr
    else:
        data = request.get_data()
        # 用xml.etree模块解析XML类型数据
        xml = ET.fromstring(data)
        ToUserName = xml.findtext('.//ToUserName')  # 也可以写成xml.find('ToUserName').text
        FromUserName = xml.findtext('.//FromUserName')
        CreateTime = xml.findtext('.//CreateTime')
        MsgType = xml.findtext('.//MsgType')
        Content = xml.findtext('.//Content')
        MsgId = xml.findtext('.//MsgId')
        if u'你是谁' in Content:
            return render_template(
                'reply_text.html',
                ToUserName=ToUserName,
                FromUserName=FromUserName,
                CreateTime=CreateTime,
                MsgType=MsgType,
                Content=u'我是你的朋友瘦子君啊^@^', )
        session = urlopen('http://op.juhe.cn/robot/index?info=%s&key=ab335a381ee61e8e95e2b5a32c364d66'
                        % Content.encode('utf-8')).read()
        # 处理聚合接口调用返回的json格式数据，将json转换为字典数据
        result = loads(session)
        Content = result['result']['text']
        return render_template(
                'reply_text.html',
                ToUserName=ToUserName,
                FromUserName=FromUserName,
                CreateTime=CreateTime,
                MsgType=MsgType,
                Content=Content,)


if __name__ == '__main__':
    app.run(debug=True)
