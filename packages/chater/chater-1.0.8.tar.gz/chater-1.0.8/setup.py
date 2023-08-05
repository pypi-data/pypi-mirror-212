from pathlib import Path

from setuptools import setup, find_packages

setup(
    name='chater',
    version='1.0.8',
    packages=find_packages(),
    author='Sricor',
    author_email='josricor@outlook.com',
    description='Using ChatGPT in Python',
    long_description=open(Path("README.md"), encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    license='MIT',
    install_requires=[
        'requests',
        'pydantic'
    ]
)
