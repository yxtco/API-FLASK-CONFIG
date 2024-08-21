#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：API-flask 
@File    ：data.py
@IDE     ：PyCharm 
@Author  ：Jerry 497834876@qq.com
@Date    ：2024/8/21 上午11:26 
@explain : 文件说明： 

"""

import configparser
import hashlib


def hash_password(password):
    """对密码进行哈希处理"""
    hashed_password = hashlib.pbkdf2_hmac('sha256', password.encode(), b'Jerry322368', 100000)
    return hashed_password.hex()


def verify_password(plain_password, hashed_password):
    """验证密码是否正确"""
    test_hashed_password = hashlib.pbkdf2_hmac('sha256', plain_password.encode(), b'Jerry322368', 100000)
    return test_hashed_password.hex() == hashed_password


def write_users_to_config(users_data):
    """将用户数据写入 config.ini 文件"""
    config = configparser.ConfigParser()
    config.optionxform = str  # 设置 optionxform 为 str 类型以避免转换选项名称为小写

    for user, data in users_data.items():
        config[user] = data

    with open('config.ini', 'w', encoding='utf-8') as configfile:
        config.write(configfile)


def read_user_from_config(username):
    """从 config.ini 文件读取指定用户的用户数据"""
    config = configparser.ConfigParser()
    config.read('config.ini')

    if username in config.sections():
        return dict(config[username])
    else:
        return None
