import numpy as np
import urllib.request

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer

from .rabin_karp import rabin_karp
from .jaccard import jaccard
from .cosine import cosine

class Plagiat:
  def __init__(self, format='Text', bahasa='indonesian'):
    self.dokumen_a = None
    self.dokumen_b = None
    self.format = format
    self.bahasa = bahasa
    self.n_gram = 5
    self.hashing = {"a": [], "b": []}
  
  def cosine(self, dokumen_a, dokumen_b, format='Text', bahasa='indonesian'):
    self.format = format
    self.bahasa = bahasa
    
    set_1 = self.preprocessing(self.baca_konten(dokumen_a))
    set_2 = self.preprocessing(self.baca_konten(dokumen_b))
    
    return cosine.calculate(set_1, set_2)
  
  def jaccard(self, dokumen_a, dokumen_b, format='Text', bahasa='indonesian'):
    self.format = format
    self.bahasa = bahasa
    
    set_1 = self.preprocessing(self.baca_konten(dokumen_a))
    set_2 = self.preprocessing(self.baca_konten(dokumen_b))
    
    return jaccard.calculate(set_1, set_2)
    
        
# def __init__(self, dokumen_a, dokumen_b, text=False, bahasa='indonesian', url=False, method='Rabin Karp'):
#     self.dokumen_a = dokumen_a
#     self.dokumen_b = dokumen_b
#     self.text = text
#     self.bahasa = bahasa
#     self.url = url
#     self.method = method
#     self.hashing = {"a": [], "b": []}
#     
#     self.content_1 = self.baca_konten(self.dokumen_a)
#     self.content_2 = self.baca_konten(self.dokumen_b)
#     self.hitung_hash(self.content_1, "a")
#     self.hitung_hash(self.content_2, "b")
  
  """ 
    Menghitung tingkat plagiarisme menggunakan Rumus Plagiarisme Rate

    Refefensi:
    https://www.researchgate.net/publication/319272358_Examination_of_Document_Similarity_Using_Rabin-Karp_Algorithm

    :param  hashing: kata yang sudah di hash
    :type   hashing: string
    
    :return (float) nilai persentase tingkat plagiarisme
    :type   p: float
  """
  def rabin_karp(self, dokumen_a, dokumen_b, format='Text', bahasa='indonesian'):
    
    self.content_1 = self.baca_konten(dokumen_a)
    self.content_2 = self.baca_konten(dokumen_b)
    
    self.hitung_hash(self.content_1, "a")
    self.hitung_hash(self.content_2, "b")
    
    th_a = len(self.hashing["a"])
    th_b = len(self.hashing["b"])
    a = self.hashing["a"]
    b = self.hashing["b"]
    sh = len(np.intersect1d(a, b))

    p = (float(2 * sh)/(th_a + th_b)) * 100
    return p

  """ 
    Menghitung nilai hash dari konten dokumen dan menambahkannya ke tabel hash tipe dokumen

    :param  content: konten dari dokumen
    :type   content: string
    
    :param  doc_type: indeks atau label dari dokumen
    :type   doc_type: string

    :return self.hashing[doc_type]: hashing yang telah di isi dengan konten dokumen
    :type   self.hashing[doc_type]: json
  """
  def hitung_hash(self, content, doc_type):
    text = self.preprocessing(content)
    text = "".join(text)

    text = rabin_karp(text, self.n_gram)
    for _ in range(len(content) - self.n_gram + 1):
      self.hashing[doc_type].append(text.hash)
      if text.next_window() == False:
        break
  
  """ 
    Baca teks dalam dokumen, dengan kondisi

    :param  file: bisa berupa URL atau path file
    :type   file: string
    
    :return mixed: isi dokumen
    :type   mixed: string
  """
  def baca_konten(self, file):
    if self.format == 'Text':
      return file
    elif self.format == 'URL':
      response = urllib.request.urlopen(file)
      return response.read().decode('utf-8')
    elif self.format == 'File':
      file = open(file, 'r+', encoding="utf-8")
      return file.read()
    
  """ 
    Proses pre-processing dengan Stopwords, Tokenisasi & Stemming

    :param  teks: kalimat atau paragraf
    :type   teks: string
    
    :return teks_bersih: teks yang telah di cleaning
    :type   teks_bersih: string
  """
  def preprocessing(self, teks):
    stop_words = set(stopwords.words(self.bahasa))
    tokens = word_tokenize(teks)
    teks_bersih = []
    porter = PorterStemmer()
    for w in tokens:
      if w not in stop_words:
        w = w.lower()
        word = porter.stem(w)
        teks_bersih.append(word)

    return teks_bersih