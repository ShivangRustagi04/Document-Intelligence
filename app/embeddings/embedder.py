from sklearn.feature_extraction.text import TfidfVectorizer

class Embedder:
    def __init__(self):
        self.vectorizer = TfidfVectorizer()

    def fit_transform(self, texts):
        return self.vectorizer.fit_transform(texts).toarray()

    def transform(self, texts):
        return self.vectorizer.transform(texts).toarray()
