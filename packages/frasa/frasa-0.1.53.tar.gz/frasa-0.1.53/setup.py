from setuptools import setup, find_packages

from codecs import open
from os import path

HERE = path.abspath(path.dirname(__file__))

with open(path.join(HERE, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()
    
setup(
    name="frasa",
    version="0.1.53",
    description="Koleksi NLP Pribadi untuk Bahasa Indonesia.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/novay/frasa",
    author="Novianto Rahmadi",
    author_email="novay@btekno.id",
    license="MIT",
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Operating System :: OS Independent"
    ],
    packages=find_packages(), 
    package_data={'frasa': [
        'datasets/models/frasa-gender.pickle', 
        'datasets/corpus/sensor/alphabetic_unicode.json', 
        'datasets/corpus/sensor/sensor-kata.csv', 
        'datasets/corpus/sensor/sensor-aturan.csv', 
        'datasets/corpus/sensor/sensor-pengganti.csv', 
        'datasets/corpus/indonesia/stopword.txt', 
        'datasets/corpus/indonesia/lemma/clitics.txt', 
        'datasets/corpus/indonesia/lemma/dict.json', 
        'datasets/corpus/indonesia/lemma/root.txt',
        'datasets/models/nusax/*.pkl',
    ]}
)