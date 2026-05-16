"""
06 - Mini Project: API Catatan Sederhana
=========================================

Sekarang kita gabungkan semua yang sudah dipelajari:
- GET endpoint (ambil data)
- POST endpoint (kirim data)
- Path parameter (URL dinamis)
- Pydantic schema (validasi data)

Mini project ini adalah API catatan/notes sederhana.

Cara jalankan:
    uvicorn 06_mini_project:app --reload --port 8001
"""

from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI(
    title="API Catatan Sederhana",
    description="Mini project gabungan semua konsep FastAPI dasar",
)


# ============================================================
# SCHEMA (aturan format data)
# ============================================================

class CatatanBaru(BaseModel):
    """Data yang dikirim saat membuat catatan baru."""

    judul: str = Field(min_length=1, max_length=100)
    isi: str = Field(min_length=1)
    kategori: str = Field(default="umum")


class CatatanResponse(BaseModel):
    """Data catatan yang dikembalikan ke client."""

    id: int
    judul: str
    isi: str
    kategori: str
    panjang_isi: int


# ============================================================
# DATABASE SEDERHANA (list di memori)
# ============================================================

catatan_db: list[dict] = [
    {"id": 1, "judul": "Belanja", "isi": "Beli susu dan roti", "kategori": "pribadi"},
    {"id": 2, "judul": "Meeting", "isi": "Rabu jam 10 pagi", "kategori": "kerja"},
]


# ============================================================
# ENDPOINTS
# ============================================================

@app.get("/catatan")
def semua_catatan():
    """GET /catatan → Lihat semua catatan."""
    return {"total": len(catatan_db), "catatan": catatan_db}


@app.get("/catatan/{catatan_id}")
def satu_catatan(catatan_id: int):
    """GET /catatan/1 → Lihat catatan dengan ID tertentu."""
    for catatan in catatan_db:
        if catatan["id"] == catatan_id:
            return catatan
    return {"error": f"Catatan #{catatan_id} tidak ditemukan"}


@app.get("/catatan/kategori/{nama_kategori}")
def filter_kategori(nama_kategori: str):
    """GET /catatan/kategori/kerja → Filter catatan berdasarkan kategori."""
    hasil = [c for c in catatan_db if c["kategori"] == nama_kategori]
    return {"kategori": nama_kategori, "total": len(hasil), "catatan": hasil}


@app.post("/catatan", response_model=CatatanResponse)
def tambah_catatan(data: CatatanBaru):
    """POST /catatan → Tambah catatan baru.

    Body contoh:
        {"judul": "Belajar", "isi": "Belajar FastAPI jam 8", "kategori": "belajar"}
    """
    # Buat ID baru
    new_id = max(c["id"] for c in catatan_db) + 1 if catatan_db else 1

    # Simpan ke "database"
    catatan_baru = {
        "id": new_id,
        "judul": data.judul,
        "isi": data.isi,
        "kategori": data.kategori,
    }
    catatan_db.append(catatan_baru)

    return CatatanResponse(
        id=new_id,
        judul=data.judul,
        isi=data.isi,
        kategori=data.kategori,
        panjang_isi=len(data.isi),
    )


@app.get("/statistik")
def statistik():
    """GET /statistik → Ringkasan data catatan."""
    kategori_list = set(c["kategori"] for c in catatan_db)
    return {
        "total_catatan": len(catatan_db),
        "kategori_unik": list(kategori_list),
        "jumlah_kategori": len(kategori_list),
    }


# ============================================================
# SELAMAT! 🎉
#
# Kamu sudah memahami fondasi FastAPI:
# ✅ GET  → mengambil data
# ✅ POST → mengirim data
# ✅ Path parameter → URL dinamis
# ✅ Pydantic → validasi otomatis
#
# Selanjutnya: lihat bagaimana ini dipakai di project RAG
# di file api/main.py (project utama)
# ============================================================
