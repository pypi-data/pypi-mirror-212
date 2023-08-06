import os
import re
from frasa import PACKAGE_DIR

class Stopword:
    def __init__(self, path=None):
        self.dir = PACKAGE_DIR + '/datasets/corpus'
        if not path:
            path = os.path.join(self.dir, "indonesia", "stopword.txt")
        with open(path) as f:
            next(f)
            self.stopwords = f.read().split('\n')

    def get(self):
        return self.stopwords

    def remove(self, text):
        stopword = self.get()
        temp_result = []
        parts = []

        for match in re.finditer(r'[^.,?!\s]+|[.,?!]', text):
            parts.append(match.group())

        for word in parts:
            if word.casefold() not in stopword:
                temp_result.append(word)

        result_cand = ' '.join(temp_result)
        result = re.sub(r' ([^A-Za-z0-9])', r'\1', result_cand)

        return result