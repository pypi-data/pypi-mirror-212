#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
@author: Lambert
@file: setup.py.py
@time: 2023/4/16 10:24
@Description: 
"""

from setuptools import setup, find_packages

setup(
    name='black_tortoise',  # 应用名
    version='0.2',  # 版本号
    packages=find_packages(),  # 包括在安装包内的Python包
    include_package_data=True,  # 启用清单文件MANIFEST.in
    install_requires=[
        'faker >= 18.10.1',
        'loguru >= 0.7.0',
        'requests >= 2.31.0',
        'gmssl >= 3.2.2',
    ],  # 这个项目需要的其他库
    url='https://github.com/lizhen1412/black_tortoise',  # 项目主页
    license='LICENSE',  # 选择你的License
    author='Lambert',  # 你的名字
    author_email='595265454@qq.com',  # 你的邮箱
    description='玄武 SDK 是一个提供底层工具级的项目，类似于hutool 一样，提供很多的工具类',  # 简单描述你的项目
    long_description=open('README.md').read(),  # 从README.md中读取完整描述
    long_description_content_type="text/markdown",  # 设置文档内容类型
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    python_requires='>=3.6',  # 设定项目最低Python版本要求
)

if __name__ == '__main__':
    pass
