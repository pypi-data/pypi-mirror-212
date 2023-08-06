from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.0.1.1'
DESCRIPTION = 'Conjugate - Simplify Verb Conjugation in Python'
LONG_DESCRIPTION = 'Conjugate is a powerful Python library that simplifies the process of verb conjugation, providing developers with an easy-to-use solution for generating accurate and contextually appropriate verb forms in various languages.'

# Setting up
setup(
    name="conjugate",
    version=VERSION,
    author="Aanjneya Moudgil",
    author_email="<aanjneya.moudgil@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=['pattern', 'googletrans'],
    keywords=['python', 'verbs', 'conjugate', 'german', 'api', 'conjugation', 'konjugation', 'verben'],
    classifiers=["Programming Language :: Python :: 3"]
)