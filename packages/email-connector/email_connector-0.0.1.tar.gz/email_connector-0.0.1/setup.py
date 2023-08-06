# @Author: nero
# @Date: 2023/6/8 9:25
# @File: setup
# @Project: my_sitpackage

import setuptools
from setuptools import setup

# with open("README.md", "r") as fh:
#     long_description = fh.read()

setup(
    name='email_connector',
    version='0.0.1',
    packages=setuptools.find_packages(),
    url='',  # https://github.com/pypa/sampleproject
    license='MIT',
    author='Margo',
    author_email='935929075@qq.com',
    description='A small example package',
    # long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=['yamail >= 1.0.2', 'imbox >= 0.9.8'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
