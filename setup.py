import os

from setuptools import setup

setup(
    name="neoscore",
    version="0.0.1.dev0",
    author="Andrew Yoon",
    author_email="andrewyoon2@gmail.com",
    description="A vector graphics API for music notation",
    license="GPL-3",
    keywords="music graphics",
    url="https://github.com/ajyoon/neoscore",
    packages=["neoscore", "tests"],
    long_description=open(os.path.join(os.path.dirname(__file__), "README.md")).read(),
    classifiers=[],
    install_requires=["PyQt5"],
)
