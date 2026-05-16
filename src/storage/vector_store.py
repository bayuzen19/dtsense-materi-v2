"""Class FaissVectorStore: menyimpan vector ke FAISS dan mencari yang relevan."""

from dataclasses import dataclass
from typing import Protocol

import faiss
import numpy as np


class Embedder(Protocol):
    """Protocol: interface yang harus dipenuhi oleh semua embedder."""

    dimension: int

    def embed(self, text: str) -> np.ndarray: ...


@dataclass
class StoredChunk:
    """Menyimpan data satu chunk beserta vector-nya.

    Attribute:
        doc_title: judul dokumen asal chunk ini.
        chunk_id: nomor urut chunk dalam dokumen.
        content: isi teks chunk.
        vector: representasi numerik chunk.
    """

    doc_title: str
    chunk_id: int
    content: str
    vector: np.ndarray


class FaissVectorStore:
    """Menyimpan chunk dan vector-nya ke index FAISS di memori.

    FAISS (Facebook AI Similarity Search) adalah library untuk mencari
    vector yang paling mirip secara cepat. Di sini kita pakai IndexFlatIP
    yang menghitung inner product (mirip cosine similarity kalau vector
    sudah dinormalisasi).

    Parameter:
        embedder: object yang punya method embed() dan attribute dimension.
                  Bisa SimpleEmbedder atau HuggingFaceEmbedder.
    """

    def __init__(self, embedder: Embedder) -> None:
        self.embedder = embedder
        self.chunks: list[StoredChunk] = []
        self.index = faiss.IndexFlatIP(embedder.dimension)

    def add_chunks(self, doc_title: str, chunk_texts: list[str]) -> int:
        """Menyimpan semua chunk dari satu dokumen.

        Parameter:
            doc_title: judul dokumen asal.
            chunk_texts: list potongan teks.

        Return:
            Jumlah chunk yang berhasil disimpan.
        """
        vectors: list[np.ndarray] = []

        for number, text in enumerate(chunk_texts, start=1):
            vector = self.embedder.embed(text)
            self.chunks.append(
                StoredChunk(
                    doc_title=doc_title,
                    chunk_id=number,
                    content=text,
                    vector=vector,
                )
            )
            vectors.append(vector)

        if vectors:
            matrix = np.vstack(vectors)
            self.index.add(matrix)

        return len(chunk_texts)

    def search(self, query: str, top_k: int = 3) -> list[dict[str, object]]:
        """Mencari chunk paling relevan terhadap pertanyaan.

        Parameter:
            query: teks pertanyaan.
            top_k: jumlah hasil yang dikembalikan.

        Return:
            List dictionary berisi judul, chunk_id, isi, dan score.
        """
        if not self.chunks:
            return []

        result_limit = min(top_k, len(self.chunks))
        query_vector = self.embedder.embed(query).reshape(1, -1)
        scores, indices = self.index.search(query_vector, result_limit)

        results: list[dict[str, object]] = []
        for score, idx in zip(scores[0], indices[0]):
            if idx < 0 or score <= 0:
                continue
            chunk = self.chunks[int(idx)]
            results.append({
                "title": chunk.doc_title,
                "chunk_id": chunk.chunk_id,
                "content": chunk.content,
                "score": round(float(score), 4),
            })

        return results

    def remove_by_title(self, doc_title: str) -> None:
        """Menghapus semua chunk milik satu dokumen lalu rebuild index."""
        self.chunks = [c for c in self.chunks if c.doc_title != doc_title]
        self._rebuild_index()

    def clear(self) -> None:
        """Menghapus seluruh isi store."""
        self.chunks.clear()
        self._rebuild_index()

    def _rebuild_index(self) -> None:
        """Membuat ulang index FAISS dari chunks yang tersisa."""
        self.index = faiss.IndexFlatIP(self.embedder.dimension)
        if self.chunks:
            matrix = np.vstack([c.vector for c in self.chunks]).astype(np.float32)
            self.index.add(matrix)
