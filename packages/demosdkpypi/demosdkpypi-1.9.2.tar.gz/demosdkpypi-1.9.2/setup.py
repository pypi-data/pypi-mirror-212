from setuptools import setup, find_packages
import sys

if sys.version_info < (3, 7):
    raise RuntimeError("my demo requires Python 3.7+")
current_version = '1.9.2'

setup(
    name='demosdkpypi',
    version=current_version,
    author='Bharti',
    author_email='bharti.sagar@skyflow.com',
    packages=find_packages(),
    url='https://github.com/skyflowapi/skyflow-python/',
    description='demo SDK for the Python programming language',
    long_description=open('README.md').read(),
    install_requires=[],
    python_requires=">=3.7"
)
