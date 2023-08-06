# -*- coding: utf-8 -*-
# author: 华测-长风老师
# file name：setup.py
"""
python3 setup.py sdist bdist_wheel
python3 -m twine upload dist/*
Could not find 'apksigner.jar' in ["C:\\Users\\wxy\\SDK\\platform-tools\\apksigner.jar","C:\\Users\\wxy\\SDK\\emulator\\apksigner.jar","C:\\Users\\wxy\\SDK\\cmdline-tools\\latest\\bin\\apksigner.jar","C:\\Users\\wxy\\SDK\\tools\\apksigner.jar","C:\\Users\\wxy\\SDK\\tools\\bin\\apksigner.jar","C:\\Users\\wxy\\SDK\\apksigner.jar"]
"""
from setuptools import setup, find_packages

setup(
    name="hctest_record",
    version="1.2",
    description="获取用例运行中的数据，并保存起来",
    author="cf",
    author_email="dingjun_baby@yeah.net",
    url="https://github.com/pypa/sampleproject",
    packages=find_packages(),
    package_data={},
    install_requires=[
        "requests"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
