"""
Modul NLP Indonesia untuk Python
==================================

Frasa adalah kumpulan modul yang menyediakan berbagai fungsi Natural Language Processing (NLP) 
KHUSUS untuk Bahasa Indonesia beserta Bahasa Daerahnya. 

Repositori ini berisi semua kode sumber yang terkait dengan NLP.

Kunjungi http://frasa.id untuk informasi selengkapnya.
"""

import os

__name__ = "frasa"
__version__ = "0.1.53"
__license__ = 'MIT'
__author__ = 'Novianto Rahmadi'

PACKAGE_DIR = os.path.dirname(os.path.abspath(__file__))
DATASET_DIR = PACKAGE_DIR + '/datasets/corpus'
MODELS_DIR = PACKAGE_DIR + '/datasets/models'

from .base import *
from .sensor import *
from .preprocess import *