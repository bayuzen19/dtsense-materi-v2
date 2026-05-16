"""Class HuggingFaceEmbedder: embedding menggunakan model HuggingFace ringan.

Model default: sentence-transformers/all-MiniLM-L6-v2
- Ukuran: ~80MB (ringan, cepat download)
- Dimensi output: 384
- Kualitas: sangat bagus untuk pencarian semantik
"""

import numpy as np
from sentence_transformers import SentenceTransformer


class HuggingFaceEmbedder:
    """Mengubah teks menjadi vector menggunakan model HuggingFace.

    Berbeda dengan SimpleEmbedder yang memakai rumus karakter sederhana,
    class ini menggunakan model AI yang sudah dilatih pada jutaan kalimat.
    Hasilnya jauh lebih akurat untuk menangkap makna teks.

    Parameter:
        model_name: nama model dari HuggingFace Hub.
                    Default 'all-MiniLM-L6-v2' (ringan, cepat, bagus).
    """

    def __init__(self, model_name: str = "all-MiniLM-L6-v2") -> None:
        self.model_name = model_name
        self.model = SentenceTransformer(model_name)
        self.dimension = self.model.get_sentence_embedding_dimension()

    def embed(self, text: str) -> np.ndarray:
        """Mengubah satu teks menjadi vector float32.

        Parameter:
            text: kalimat atau paragraf yang ingin di-embedding.

        Return:
            numpy array 1-dimensi (panjang = self.dimension).
        """
        vector = self.model.encode(text, normalize_embeddings=True)
        return vector.astype(np.float32)

    def embed_batch(self, texts: list[str]) -> np.ndarray:
        """Mengubah banyak teks sekaligus (lebih efisien).

        Parameter:
            texts: list kalimat/paragraf.

        Return:
            numpy array 2-dimensi (baris = jumlah teks, kolom = dimensi).
        """
        vectors = self.model.encode(texts, normalize_embeddings=True)
        return vectors.astype(np.float32)
