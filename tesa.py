#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：API-flask 
@File    ：tesa.py
@IDE     ：PyCharm 
@Author  ：Jerry 497834876@qq.com
@Date    ：2024/8/21 下午1:55 
@explain : 文件说明： 

"""
import requests
import time

url = "http://127.0.0.1:5000/douyin"

payload = {}
headers = {
    'Authorization': 'Basic eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJuYW1lIjoibmFtZSIsImV4cCI6MTcyNDIyNjk2MX0.4U-D7ylvYHUnoufAqf7cLejEO5dwPzjXxSdXmgJKUzA',
    'User-Agent': 'Apifox/1.0.0 (https://apifox.com)',
    'Accept': '*/*',
    'Host': '127.0.0.1:5000',
    'Connection': 'keep-alive'
    }

for i in range(30):
    response = requests.request("GET", url, headers = headers, data = payload)
    response.encoding = 'utf-8'

    print(f"Response {i + 1}: {response.text.encode('utf-8').decode('unicode_escape')}")  #解码名文显示返回数据
    time.sleep(1)
response = requests.request("GET", url, headers = headers, data = payload)

