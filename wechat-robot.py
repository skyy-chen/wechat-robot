#! usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask
from flask import request
from xml.etree import ElementTree as ET
from flask import render_template
from urllib import urlopen
from json import loads


app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def wechat():
    if request.method == 'GET':
        echostr = request.args.get('echostr')
        return echostr
    else:
        data = request.get_data()
        xml = ET.fromstring(data)
        ToUserName = xml.findtext('.//ToUserName')
        FromUserName = xml.findtext('.//FromUserName')
        CreateTime = xml.findtext('.//CreateTime')
        MsgType = xml.findtext('.//MsgType')
        Content = xml.findtext('.//Content')
        MsgId = xml.findtext('.//MsgId')
        if u'你是谁' in Content:
            return render_template(
                'sendmsg.html',
                ToUserName=ToUserName,
                FromUserName=FromUserName,
                CreateTime=CreateTime,
                MsgType=MsgType,
                Content=u'我是你的朋友瘦子君啊', )
        html = urlopen('http://op.juhe.cn/robot/index?info=%s&key=ab335a381ee61e8e95e2b5a32c364d66'
                       % Content.encode('utf-8')).read()
        result = loads(html)
        Content = result['result']['text']
        return render_template(
                'index.html',
                ToUserName=ToUserName,
                FromUserName=FromUserName,
                CreateTime=CreateTime,
                MsgType=MsgType,
                Content=Content,)


if __name__ == '__main__':
    app.run()
