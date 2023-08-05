import numpy as np
from collections import Counter

class cosine:
    def calculate(dokumen_a, dokumen_b):
        """ Menghitung Cosine Similarity
        
        Referensi Paper:
        https://www.researchgate.net/publication/344010599_Measurement_of_Text_Similarity_A_Survey
        
        Cosine Similarity = dot product(v1, v2) / (||v1|| * ||v2||)
        Dimana:
            - dot product(v1, v2): Hasil dari perkalian dot (inner product) antara dua vektor v1 dan v2
            - ||v1|| dan ||v2||: panjang (norm) dari vektor v1 dan v2 masing-masing

        Returns:
            float: Nilai similaritas Cosine antara dua teks.
        """
        # Menghitung frekuensi kata dalam dokumen
        doc1_word_freq = Counter(dokumen_a)
        doc2_word_freq = Counter(dokumen_b)

        # Menghitung dot product antara vektor frekuensi kata
        dot_product = 0
        for word in doc1_word_freq.keys():
            if word in doc2_word_freq:
                dot_product += doc1_word_freq[word] * doc2_word_freq[word]

        # Menghitung panjang vektor frekuensi kata
        doc1_norm = np.sqrt(sum(np.square(list(doc1_word_freq.values()))))
        doc2_norm = np.sqrt(sum(np.square(list(doc2_word_freq.values()))))

        # Menghitung similaritas Cosine
        similarity = dot_product / (doc1_norm * doc2_norm)

        return similarity