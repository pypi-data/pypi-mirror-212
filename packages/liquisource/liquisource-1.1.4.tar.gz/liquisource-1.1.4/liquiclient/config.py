#!/usr/local/bin/python3
# coding: utf8
import sys
from jproperties import Properties
import os

config = Properties()


# 获取配置信息
def get_config(filepath):
    with open(filepath, 'rb') as prop:
        config.load(prop)


# 默认找项目路径的文件
def auto_config():
    current_working_directory = os.getcwd()
    print(current_working_directory)


# 获取配置的某一个key
def get_property(name):
    if len(name) == 0:
        return config
    return config[str(name[0])].data


# 获取根据租户分库分表
def get_tenant_shard(key):
    kfuin = get_property("parameter.tenant")
    return key + "_" + kfuin
