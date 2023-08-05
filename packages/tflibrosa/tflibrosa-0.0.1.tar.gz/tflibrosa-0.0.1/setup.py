# -*- coding: utf-8 -*-
from setuptools import setup
from io import open

def readme():
    with open('README.md', encoding="utf-8-sig") as f:
        README = f.read()
    return README


setup(
    name='tflibrosa',
    version='0.0.1',    
    description='Re-implementation of some librosa function for tensorflow. Reproduction from torchlibrosa.',
    author='Shiro-LK',
    author_email='shirosaki94@gmail.com',
    license='MIT License',
    packages=['tflibrosa'],
    long_description=readme(),
    long_description_content_type="text/markdown",
    install_requires=['numpy', 
                      "pytest", "tensorflow", "librosa"
                      ],
    url='https://github.com/Shiro-LK/tflibrosa',
    download_url='https://github.com/Shiro-LK/tflibrosa.git',
    keywords=["tflibrosa", "tensorflow", "librosa"],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)
