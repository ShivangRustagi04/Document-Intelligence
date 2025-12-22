import faiss
import numpy as np

class VectorStore:
    def __init__(self, dim):
        self.index = faiss.IndexFlatL2(dim)
        self.texts = []

    def add(self, embeddings, texts):
        self.index.add(np.array(embeddings).astype("float32"))
        self.texts.extend(texts)

    def search(self, query_embedding, k=3):
        D, I = self.index.search(np.array([query_embedding]).astype("float32"), k)
        return [(self.texts[i], 1/(1+d)) for i, d in zip(I[0], D[0])]
