# -*- coding: utf-8 -*-
# @Author  : zhousf
# @Date    : 2023/6/6 
# @Function:
"""

构建项目
python -m pip install --user --upgrade setuptools wheel
上传文件至Pypi
python -m pip install --user --upgrade twine
检查语法是否正确
python setup.py check
构建项目
python setup.py sdist bdist_wheel
cmd中输入Pypi的账户与密码
twine upload --repository-url https://upload.pypi.org/legacy/ dist/*


"""

from __future__ import print_function
from setuptools import setup, find_packages
import version

with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    name="zhousf-lib",
    version=version.__version__,
    author="zhousf",
    author_email="442553199@qq.com",
    description="a python library of zhousf",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    url="https://github.com/MrZhousf/ZhousfLib",
    packages=find_packages(),
    py_modules=['zhousflib'],
    install_requires=[
        "numpy <= 1.24.3",
        ],
    classifiers=[
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        'Programming Language :: Python :: Implementation :: CPython',
    ],
)



