# Frasa NLP: Deteksi
#
# Copyright (C) 2023 Frasa Project
# Author: Novianto Rahmadi <novay@btekno.id>
# URL: <https://frasa.id/>
# For license information, see LICENSE.TXT

"""
Frasa Deteksi

Modul untuk melakukan deteksi pada beberapa hal seperti
- Prediksi Gender dari nama seseorang
- Prediksi Bahasa Daerah yang digunakan
- Prediksi Topik dalam suatu kalimat
- Prediksi Kesimpulan dari suatu dokumen
- Prediksi Tingkat Kesamaan dari beberapa dokumen
"""

# from frasa.deteksi.gender import model_gender, probabilitas
# from frasa.deteksi.plagiat.plagiat import Periksa
# import json

# class Periksa:
#     def __init__(self, text_1, text_2):
#         self.text_1 = text_1
#         self.text_2 = text_2
        


from .gender.gender import Gender
from .plagiat.plagiat import Plagiat

if __name__ != '__main__':
    gender = Gender()
    plagiat = Plagiat()