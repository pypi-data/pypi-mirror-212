import numpy as np
from gensim.models.fasttext import FastText
from sentence_transformers import SentenceTransformer
from sklearn.base import (
    BaseEstimator,
    TransformerMixin,
)
from sklearn.feature_extraction.text import CountVectorizer


class FastTextVectorizer(BaseEstimator, TransformerMixin):
    def __init__(self, model_path, max_features=None):
        self.model = FastText.load(model_path)
        self.max_features = max_features

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        return np.array([self.get_sentence_vector(s) for s in X])

    def get_sentence_vector(self, sentence):
        words = sentence.split()
        if self.max_features:
            words = words[: self.max_features]
        vectors = [self.model.wv[word] for word in words]
        if not vectors:
            return np.zeros(self.model.vector_size)
        return np.mean(vectors, axis=0)


class SentenceTransformerVectorizer(BaseEstimator, TransformerMixin):
    def __init__(self, model_name_or_path):
        self.model = SentenceTransformer(model_name_or_path)

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        return np.array([self.model.encode(s) for s in X])
