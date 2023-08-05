# -*- coding: utf-8 -*-
from setuptools import setup

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()



setup(
    name='FileKit',
    version='1.0.6',
    author='孙亮',
    packages=['FileKit'],
    install_requires=[
        # 'some_dependency>=1.0.0',
    ],
    long_description=long_description,
    long_description_content_type='text/markdown',
)

