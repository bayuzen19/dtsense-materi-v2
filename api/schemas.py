"""Schema (Pydantic model) untuk validasi request dan response API.

Pydantic memastikan data yang masuk ke API sesuai format yang diharapkan.
Jika data tidak valid, FastAPI otomatis mengembalikan pesan error yang jelas.
"""

from pydantic import BaseModel, Field


# ============================================================
# REQUEST SCHEMAS: data yang masuk dari client
# ============================================================

class DocumentRequest(BaseModel):
    """Request untuk menambahkan dokumen baru."""

    title: str = Field(min_length=1, description="Judul dokumen")
    content: str = Field(min_length=1, description="Isi teks dokumen")


class AskRequest(BaseModel):
    """Request untuk mengajukan pertanyaan."""

    question: str = Field(min_length=1, description="Pertanyaan pengguna")


# ============================================================
# RESPONSE SCHEMAS: data yang dikembalikan ke client
# ============================================================

class HealthResponse(BaseModel):
    """Response endpoint health check."""

    status: str
    total_documents: int
    total_chunks: int


class DocumentResponse(BaseModel):
    """Response setelah menambahkan dokumen."""

    message: str
    title: str
    chunks_created: int


class RetrievedContext(BaseModel):
    """Satu konteks yang ditemukan oleh retriever."""

    title: str
    chunk_id: int
    content: str
    score: float


class AskResponse(BaseModel):
    """Response untuk pertanyaan pengguna."""

    question: str
    answer: str
    retrieved_contexts: list[RetrievedContext]


class DocumentSummary(BaseModel):
    """Ringkasan satu dokumen yang tersimpan."""

    title: str
    content_length: int
    chunk_count: int


class DocumentsListResponse(BaseModel):
    """Response daftar semua dokumen."""

    total: int
    documents: list[DocumentSummary]
