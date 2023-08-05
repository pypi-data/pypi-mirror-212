from .utils import get_nama
from nltk import NaiveBayesClassifier, classify
import random
from frasa import DATASET_DIR

class NBClassifier:
    def get_features(self):
        male_names, female_names = self._load_names()

        feature_set = list()

        for nameTuple in male_names:
            features = self._name_features(nameTuple[0])
            prob_cowok, prob_cewek = self._get_prob_distr(nameTuple)
            features['prob_cowok'] = prob_cowok
            features['prob_cewek'] = prob_cewek
            feature_set.append((features, 'Laki-Laki'))

        for nameTuple in female_names:
            features = self._name_features(nameTuple[0])
            prob_cowok, prob_cewek = self._get_prob_distr(nameTuple)
            features['prob_cowok'] = prob_cowok
            features['prob_cewek'] = prob_cewek
            feature_set.append((features, 'Perempuan'))

        return feature_set

    def train_and_test(self, training_percent=0.80):
        feature_set = self.get_features()
        random.shuffle(feature_set)

        name_count = len(feature_set)

        cut_point = int(name_count * training_percent)

        train_set = feature_set[:cut_point]
        test_set = feature_set[cut_point:]

        self.train(train_set)

        return self.test(test_set)

    def classify(self, name):
        feats = self._name_features(name)
        return self.classifier.classify(feats)

    def train(self, train_set):
        self.classifier = NaiveBayesClassifier.train(train_set)
        return self.classifier

    def test(self, test_set):
        return classify.accuracy(self.classifier, test_set)

    def _get_prob_distr(self, nameTuple):
        prob_cowok = (nameTuple[1] * 1.0) / (nameTuple[1] + nameTuple[2])
        if prob_cowok == 1.0:
            prob_cowok = 0.99
        elif prob_cowok == 0.0:
            prob_cowok = 0.01
        else:
            pass
        prob_cewek = 1.0 - prob_cowok
        return (prob_cowok, prob_cewek)

    def get_most_informative_features(self, n=10):
        return self.classifier.most_informative_features(n)

    def _load_names(self):
        return get_nama()

    def _name_features(self, name):
        name = name.upper()
        return {
            'last_letter': name[-1],
            'last_two': name[-2:],
            'last_three': name[-3:],
            'last_four': name[-4:],
            'last_five': name[-5:],
            'first_letter': name[0],
            # 'last_is_vowel': (name[-1] in 'AEIOU'), 
            # 'is_male_name': (name[-1] in self.load_male_names)
        }
        
    def get_probability(self, name):
        feats = self._name_features(name)
        
        prob_cowok = self.classifier.prob_classify(feats).prob('Laki-Laki')
        prob_cewek = self.classifier.prob_classify(feats).prob('Perempuan')
        
        return {'L': round(prob_cowok * 100, 2), 'P': round(prob_cewek * 100, 2)}

    def load_male_names(self, file_path):
        with open(file_path, 'r') as f:
            names = f.read().splitlines()
        return names
    
if __name__ != '__main__':
    NaiveBayes = NBClassifier()