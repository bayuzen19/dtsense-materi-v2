"""Dependencies: membuat instance pipeline yang dipakai bersama oleh endpoints.

File ini bertanggung jawab:
1. Membuat satu instance RAGPipeline saat server mulai.
2. Memuat dokumen dari folder data/ jika ada.
"""

from pathlib import Path

from src.pipeline.rag_pipeline import RAGPipeline
from utils.pdf_loader import load_documents_from_directory


# Buat satu instance pipeline (Singleton Pattern sederhana)
# use_simple_embedder=False → pakai HuggingFace all-MiniLM-L6-v2
pipeline = RAGPipeline(
    chunk_size=30,
    overlap=5,
    use_llm=True,
    embedding_model="all-MiniLM-L6-v2",
    use_simple_embedder=False,
)


def load_initial_data() -> None:
    """Memuat dokumen PDF dari folder data/ saat server mulai."""
    data_path = Path(__file__).resolve().parent.parent / "data"
    if not data_path.exists():
        return

    documents = load_documents_from_directory(str(data_path))
    for title, content in documents:
        pipeline.add_document(title=title, content=content)
