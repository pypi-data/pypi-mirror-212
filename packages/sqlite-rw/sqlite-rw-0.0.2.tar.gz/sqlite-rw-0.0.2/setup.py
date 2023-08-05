# -*- coding:utf-8 -*-
'''
Author: xupingmao xupingmao@gmail.com
Date: 2023-03-11 13:44:52
LastEditors: xupingmao
LastEditTime: 2023-06-05 00:01:55
FilePath: \sqlite-rw\setup.py
Description: sqlite读写分离库
'''
import setuptools

with open("README.md", "r+", encoding="utf-8") as fp:
    long_description = fp.read()

setuptools.setup(
    name = "sqlite-rw",
    version = "0.0.2",
    author = "mark",
    author_email = "578749341@qq.com",
    description  = "sqlite读写分离库",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = "https://github.com/xupingmao/sqlite-rw",
    packages = setuptools.find_packages(),
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires = [
        "web.py >= 0.6.0"
    ]
)
