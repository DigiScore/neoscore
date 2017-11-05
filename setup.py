import os
from setuptools import setup


setup(
    name="brown",
    version="0.0.1.dev0",
    author="Andrew Yoon",
    author_email="andrewyoon2@gmail.com",
    description="A vector graphics API for music notation",
    license="GPL-3",
    keywords="music graphics",
    url="https://github.com/ajyoon/brown",
    packages=['brown', 'tests'],
    long_description=open(os.path.join(os.path.dirname(__file__),
                                       'README.md')).read(),
    classifiers=[
    ], install_requires=['PyQt5']
)
