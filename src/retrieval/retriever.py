"""Class Retriever: mengambil konteks paling relevan dari vector store."""

from src.storage.vector_store import FaissVectorStore


class Retriever:
    """Mencari chunk yang paling relevan terhadap pertanyaan pengguna.

    Class ini membungkus proses pencarian di vector store agar
    pipeline utama tidak perlu tahu detail FAISS.

    Parameter:
        vector_store: object FaissVectorStore tempat chunk disimpan.
    """

    def __init__(self, vector_store: FaissVectorStore) -> None:
        self.vector_store = vector_store

    def retrieve(self, question: str, top_k: int = 3) -> list[dict[str, object]]:
        """Mengambil top_k chunk paling mirip dengan pertanyaan.

        Parameter:
            question: teks pertanyaan.
            top_k: jumlah chunk yang dikembalikan.

        Return:
            List dictionary berisi title, chunk_id, content, dan score.
        """
        return self.vector_store.search(query=question, top_k=top_k)
