from .lemma import Lemmatisasi
from .token import Token
from .stopword import Stopword
from .sentimen import Sentimen
from .tweet import Tweet

if __name__ != '__main__':
    lemma = Lemmatisasi()
    token = Token()
    stopword = Stopword()
    sentimen = Sentimen()
    tweet = Tweet