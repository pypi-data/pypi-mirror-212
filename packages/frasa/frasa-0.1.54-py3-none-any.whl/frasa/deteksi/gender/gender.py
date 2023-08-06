import pickle
from frasa import MODELS_DIR
from .classify import NaiveBayes
import json

class Gender:
    def __init__(self):
        self.model = self.models()
        
    def models(self):
        filename = MODELS_DIR + '/frasa-gender.pickle'
        try:
            with open(filename, 'rb') as file:
                model = pickle.load(file)
        
        except FileNotFoundError:
            model = NaiveBayes
            model.train_and_test()

            with open(filename, 'wb') as file:
                pickle.dump(model, file)
                
        return model

    def probabilitas(self, nama):
        return self.models().get_probability(nama)
    
    def info(self, nama, only=None):
        gender = self.models().classify(nama)
        prob = self.probabilitas(nama)
        data = {'nama': nama, 'gender': gender, 'prob': prob}

        if only is not None:
            return {k: v for k, v in data.items() if k in only}
        else:
            return data