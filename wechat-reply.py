#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Jon.Chen 14:25 2018/1/27

from flask import Flask
from flask import request
from xml.etree import ElementTree as ET
from flask import render_template


app = Flask(__name__)

@app.route('/',methods=['GET', 'POST'])
def wechat():
    if request.method == 'GET':
        echostr = request.args.get('echostr')
        return echostr
    else:
        data = request.get_data()
        xml = ET.fromstring(data)
        ToUserName = xml.findtext('./ToUserName')
        FromUserName = xml.findtext('.//FromUserName')
        CreateTime = xml.findtext('.//CreateTime')
        MsgType = xml.findtext('.//MsgType')
        Content = xml.findtext('.//Content')
        MsgId = xml.findtext('.//MsgId')
        return render_template(
            'reply_text.html',
            ToUserName=ToUserName,
            FromUserName=FromUserName,
            CreateTime=CreateTime,
            Content=Content,)




if __name__ == '__main__' :
    app.run()