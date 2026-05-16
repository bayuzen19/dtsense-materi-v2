"""Class RAGPipeline: menggabungkan semua komponen menjadi satu alur kerja."""

import os

from dotenv import load_dotenv

from src.models.document import Document
from src.processing.chunker import TextChunker
from src.processing.embedder import SimpleEmbedder
from src.processing.hf_embedder import HuggingFaceEmbedder
from src.retrieval.generator import SimpleGenerator
from src.retrieval.llm_generator import LLMGenerator
from src.retrieval.retriever import Retriever
from src.storage.vector_store import FaissVectorStore

load_dotenv()


class RAGPipeline:
    """Pipeline utama yang menggabungkan semua class menjadi satu alur.

    Alur kerja:
    1. Dokumen masuk melalui method add_document().
    2. Teks dokumen dipecah menjadi chunk oleh TextChunker.
    3. Setiap chunk diubah menjadi vector oleh Embedder (HuggingFace/Simple).
    4. Vector disimpan ke FaissVectorStore.
    5. Saat ada pertanyaan, Retriever mencari chunk relevan.
    6. Generator (LLM atau Simple) menyusun jawaban dari konteks.

    Parameter:
        chunk_size: ukuran chunk dalam jumlah kata.
        overlap: kata yang diulang antar chunk.
        use_llm: True = pakai Groq LLM, False = pakai generator sederhana.
        llm_model: nama model Groq (jika use_llm=True).
        embedding_model: nama model HuggingFace untuk embedding.
        use_simple_embedder: True = pakai SimpleEmbedder (tanpa download model).
    """

    def __init__(
        self,
        chunk_size: int = 30,
        overlap: int = 5,
        use_llm: bool = True,
        llm_model: str = "llama-3.3-70b-versatile",
        embedding_model: str = "all-MiniLM-L6-v2",
        use_simple_embedder: bool = False,
    ) -> None:
        # Buat chunker
        self.chunker = TextChunker(chunk_size=chunk_size, overlap=overlap)

        # Pilih embedder: HuggingFace (akurat) atau Simple (tanpa download)
        if use_simple_embedder:
            self.embedder = SimpleEmbedder(dimension=256)
        else:
            try:
                self.embedder = HuggingFaceEmbedder(model_name=embedding_model)
            except (ImportError, Exception):
                # Fallback jika sentence-transformers tidak terinstall
                print("[INFO] sentence-transformers tidak tersedia, pakai SimpleEmbedder.")
                self.embedder = SimpleEmbedder(dimension=256)

        # Buat vector store dan retriever
        self.vector_store = FaissVectorStore(embedder=self.embedder)
        self.retriever = Retriever(vector_store=self.vector_store)

        # Pilih generator: LLM (Groq) atau sederhana (tanpa API)
        api_key = os.getenv("GROQ_API_KEY")
        if use_llm and api_key:
            self.generator = LLMGenerator(model_name=llm_model, api_key=api_key)
        else:
            self.generator = SimpleGenerator()

        # Tempat mencatat dokumen yang sudah masuk
        self.documents: dict[str, Document] = {}
        self.chunk_counts: dict[str, int] = {}

    def add_document(self, title: str, content: str) -> int:
        """Menambahkan dokumen baru ke pipeline.

        Parameter:
            title: judul dokumen.
            content: isi teks dokumen.

        Return:
            Jumlah chunk yang dihasilkan dari dokumen ini.
        """
        doc = Document(title=title, content=content)

        if not doc.title:
            raise ValueError("title tidak boleh kosong")
        if not doc.content:
            raise ValueError("content tidak boleh kosong")

        # Hapus versi lama jika judul sudah ada
        if doc.title in self.documents:
            self.vector_store.remove_by_title(doc.title)

        # Pecah teks menjadi chunk
        chunks = self.chunker.split(doc.content)
        if not chunks:
            chunks = [doc.content]

        # Simpan ke vector store
        count = self.vector_store.add_chunks(doc.title, chunks)
        self.documents[doc.title] = doc
        self.chunk_counts[doc.title] = count
        return count

    def ask(self, question: str, top_k: int = 3) -> dict[str, object]:
        """Menjawab pertanyaan berdasarkan dokumen yang tersimpan.

        Parameter:
            question: pertanyaan pengguna.
            top_k: jumlah chunk yang diambil.

        Return:
            Dictionary berisi question, answer, dan retrieved_contexts.
        """
        cleaned = question.strip()
        if not cleaned:
            raise ValueError("question tidak boleh kosong")

        contexts = self.retriever.retrieve(question=cleaned, top_k=top_k)
        answer = self.generator.generate(question=cleaned, contexts=contexts)

        return {
            "question": cleaned,
            "answer": answer,
            "retrieved_contexts": contexts,
        }

    def list_documents(self) -> list[dict[str, object]]:
        """Mengembalikan daftar dokumen yang sudah tersimpan."""
        return [
            {
                "title": title,
                "content_length": len(doc.content),
                "chunk_count": self.chunk_counts.get(title, 0),
            }
            for title, doc in self.documents.items()
        ]

    def reset(self) -> None:
        """Menghapus semua dokumen dan vector."""
        self.documents.clear()
        self.chunk_counts.clear()
        self.vector_store.clear()
