# embedder.py

from sentence_transformers import SentenceTransformer


class Embedder:
    """
    Simple wrapper around a multilingual SentenceTransformer model.
    Works for Bangla + English text.
    """

    def __init__(self):
        # Multilingual model – supports Bengali and English
        self.model = SentenceTransformer(
            "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
        )

    def embed_one(self, text: str):
        """
        Compute a single embedding for one string.
        Returns: list[float]
        """
        return self.model.encode(text).tolist()

    def embed_many(self, texts):
        """
        Compute embeddings for a list of strings.
        Returns: list[list[float]]
        """
        return self.model.encode(list(texts)).tolist()
