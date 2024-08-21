#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：API-flask 
@File    ：pwd.py
@IDE     ：PyCharm 
@Author  ：Jerry 497834876@qq.com
@Date    ：2024/8/21 下午2:29 
@explain : 文件说明： 

"""
from data import hash_password, verify_password, write_users_to_config, read_users_from_config

data = {
    'username': 'damin',
    'password': 'Jerry322',
    'email': 'admin@example.com',
    }

# 读取数据
