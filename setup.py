import os

from setuptools import find_packages
from setuptools import setup


setup(
    name='backend-design',
    author='Dan Davison',
    author_email='dandavison7@gmail.com',
    description="Create backend design specifications",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'pygraphviz',
    ],
)
