from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.1.9'
DESCRIPTION = 'A package with lots of features'

# Setting up
setup(
    name="netora-python",
    version=VERSION,
    author="JacksonLin",
    author_email="jacksonlam.macau@gmail.com",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=['yt-dlp'],
    keywords=['python', 'features', 'youtube', 'youtube downloader'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Microsoft :: Windows",
    ]
)