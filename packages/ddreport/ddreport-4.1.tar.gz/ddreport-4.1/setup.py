#!/usr/bin/env python
#-*- coding:utf-8 -*-

#############################################
# File Name: setup.py
# Author: duanliangcong
# Mail: 137562703@qq.com
# Created Time:  2022-11-02 15:00:00
#############################################

# pip install twine
# python setup.py sdist
# twine upload dist/*

#############################################
#################使用方法#####################
#############################################
'''
目录结构
UPSDIST
    ddreport        库文件夹
    MANIFEST.in     配置
    setup.py        当前文件

1.cmd进入UPSDIST目录
2.执行命令：python setup.py sdist
3.执行命令：twine upload dist/*
'''



#### 每次更新需要修改 version 字段

from setuptools import setup, find_packages, find_namespace_packages

setup(
    name = "ddreport",
    version = "4.1",
    keywords = ("pip", "pytest", "testReport"),
    description = "pytest测试报告",
    long_description = "1.request使用session；2.解决动态化参数中调用其他fixture不生效问题；3.解决响应头获取content-type失败后，无法确定响应内容类型问题",
    license = "MIT Licence",

    url = "https://gitee.com/duanliangcong/ddreport",
    author = "duanliangcong",
    author_email = "137562703@qq.com",
    entry_points={"pytest11": ["test_report=ddreport.testReport"]},

    packages = find_packages(),
    include_package_data = True,
    platforms = "any",
    install_requires = ["requests", "jsonpath", "deepdiff"],
)
