"""Main: aplikasi FastAPI dengan semua endpoint RAG.

Cara menjalankan server:
    uvicorn api.main:app --reload

Setelah berjalan, buka http://127.0.0.1:8000/docs untuk melihat dokumentasi.
"""

from contextlib import asynccontextmanager
from collections.abc import AsyncGenerator

from fastapi import FastAPI, HTTPException

from api.dependencies import load_initial_data, pipeline
from api.schemas import (
    AskRequest,
    AskResponse,
    DocumentRequest,
    DocumentResponse,
    DocumentsListResponse,
    DocumentSummary,
    HealthResponse,
    RetrievedContext,
)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Lifecycle event: memuat data saat server mulai."""
    load_initial_data()
    yield


app = FastAPI(
    title="RAG OOP FastAPI",
    description="Sistem Retrieval-Augmented Generation menggunakan OOP + FAISS.",
    version="2.0.0",
    lifespan=lifespan,
)


# ===========================================================
# ENDPOINTS
# ===========================================================


@app.get("/health", response_model=HealthResponse)
def health_check():
    """Memeriksa status server."""
    docs = pipeline.list_documents()
    total_chunks = sum(d["chunk_count"] for d in docs)
    return HealthResponse(
        status="healthy",
        total_documents=len(docs),
        total_chunks=total_chunks,
    )


@app.post("/documents", response_model=DocumentResponse)
def add_document(request: DocumentRequest):
    """Menambahkan dokumen baru ke sistem RAG."""
    chunks_created = pipeline.add_document(
        title=request.title, content=request.content
    )
    return DocumentResponse(
        message="Dokumen berhasil ditambahkan",
        title=request.title,
        chunks_created=chunks_created,
    )


@app.post("/ask", response_model=AskResponse)
def ask_question(request: AskRequest):
    """Menjawab pertanyaan berdasarkan dokumen yang tersimpan."""
    result = pipeline.ask(question=request.question)
    contexts = [
        RetrievedContext(
            title=str(ctx["title"]),
            chunk_id=int(ctx["chunk_id"]),
            content=str(ctx["content"]),
            score=float(ctx["score"]),
        )
        for ctx in result["retrieved_contexts"]
    ]
    return AskResponse(
        question=str(result["question"]),
        answer=str(result["answer"]),
        retrieved_contexts=contexts,
    )


@app.get("/documents", response_model=DocumentsListResponse)
def list_documents():
    """Menampilkan daftar semua dokumen yang tersimpan."""
    docs = pipeline.list_documents()
    summaries = [
        DocumentSummary(
            title=str(d["title"]),
            content_length=int(d["content_length"]),
            chunk_count=int(d["chunk_count"]),
        )
        for d in docs
    ]
    return DocumentsListResponse(total=len(summaries), documents=summaries)


@app.post("/reset")
def reset_pipeline():
    """Menghapus semua dokumen dan memulai dari awal."""
    pipeline.reset()
    return {"message": "Semua data berhasil dihapus"}
