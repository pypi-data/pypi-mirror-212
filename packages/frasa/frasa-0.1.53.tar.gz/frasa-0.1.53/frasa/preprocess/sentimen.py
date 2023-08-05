import pickle
from frasa import MODELS_DIR
from .token import Token

class Sentimen:        
    def models(self, lang, string):
        
        model = MODELS_DIR + '/nusax/'+ lang +'_model.pkl'
        with open(model, 'rb') as file:
            model = pickle.load(file)
        
        vectorizer = MODELS_DIR + '/nusax/'+ lang +'_vectorizer.pkl'
        with open(vectorizer, 'rb') as file:
            vectorizer = pickle.load(file)
                
        input = " ".join(Token().tokenize(string))
        sentimen = model.predict(vectorizer.transform([input]).toarray())
        
        return sentimen[0]

    def indo(self, string):
        return self.models('indo', string)

    def aceh(self, string):
        return self.models('aceh', string)

    def bali(self, string):
        return self.models('bali', string)

    def banjar(self, string):
        return self.models('banjar', string)

    def batak(self, string):
        return self.models('batak', string)

    def bugis(self, string):
        return self.models('bugis', string)

    def jawa(self, string):
        return self.models('jawa', string)

    def madura(self, string):
        return self.models('madura', string)

    def minang(self, string):
        return self.models('minang', string)

    def ngaju(self, string):
        return self.models('ngaju', string)

    def sunda(self, string):
        return self.models('sunda', string)
    
    # def download(self, lang):
        