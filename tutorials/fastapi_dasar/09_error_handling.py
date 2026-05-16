"""
09 - Error Handling & Status Code
===================================

Di dunia nyata, banyak hal bisa salah:
- Data tidak ditemukan (404)
- Format data salah (422)
- Server error (500)

FastAPI harus memberitahu client APA yang salah secara jelas.
Analoginya: pelayan bilang "Maaf, menu itu habis" bukan diam saja.

Cara jalankan:
    uvicorn 09_error_handling:app --reload --port 8001
"""

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field

app = FastAPI(title="Belajar Error Handling & Status Code")


# ============================================================
# DATABASE
# ============================================================

buku_db = {
    1: {"id": 1, "judul": "Python Dasar", "penulis": "Andi", "stok": 5},
    2: {"id": 2, "judul": "FastAPI Pro", "penulis": "Budi", "stok": 0},
    3: {"id": 3, "judul": "Data Science", "penulis": "Citra", "stok": 12},
}


# ============================================================
# SCHEMA
# ============================================================

class BukuBaru(BaseModel):
    judul: str = Field(min_length=1, max_length=100)
    penulis: str = Field(min_length=1)
    stok: int = Field(ge=0, description="Stok tidak boleh negatif")


# ============================================================
# PENJELASAN STATUS CODE:
#
# 200 = OK (berhasil, default untuk GET)
# 201 = Created (berhasil dibuat, untuk POST)
# 404 = Not Found (data tidak ditemukan)
# 409 = Conflict (data sudah ada / bentrok)
# 422 = Unprocessable Entity (format data salah)
# 500 = Internal Server Error (kesalahan server)
# ============================================================


@app.get("/buku/{buku_id}")
def ambil_buku(buku_id: int):
    """Ambil buku berdasarkan ID.

    Jika buku tidak ditemukan → raise HTTPException dengan status 404.
    """
    if buku_id not in buku_db:
        # HTTPException = cara resmi FastAPI untuk mengembalikan error
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Buku dengan ID {buku_id} tidak ditemukan",
        )

    return buku_db[buku_id]


@app.post("/buku", status_code=status.HTTP_201_CREATED)
def tambah_buku(data: BukuBaru):
    """Tambah buku baru.

    - status_code=201 → memberitahu client bahwa data BERHASIL DIBUAT
    - Jika judul sudah ada → 409 Conflict
    """
    # Cek apakah judul sudah ada
    for buku in buku_db.values():
        if buku["judul"].lower() == data.judul.lower():
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Buku '{data.judul}' sudah ada di database!",
            )

    # Buat ID baru
    new_id = max(buku_db.keys()) + 1 if buku_db else 1
    buku_baru = {"id": new_id, **data.model_dump()}
    buku_db[new_id] = buku_baru

    return buku_baru


@app.post("/buku/{buku_id}/pinjam")
def pinjam_buku(buku_id: int):
    """Pinjam buku (kurangi stok).

    Contoh beberapa error yang mungkin terjadi:
    - Buku tidak ditemukan → 404
    - Stok habis → 400 Bad Request
    """
    if buku_id not in buku_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Buku #{buku_id} tidak ditemukan",
        )

    buku = buku_db[buku_id]

    if buku["stok"] <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Buku '{buku['judul']}' stoknya habis! Tidak bisa dipinjam.",
        )

    buku["stok"] -= 1
    return {
        "pesan": f"Berhasil pinjam '{buku['judul']}'!",
        "sisa_stok": buku["stok"],
    }


@app.delete("/buku/{buku_id}")
def hapus_buku(buku_id: int):
    """Hapus buku. Return 404 jika tidak ditemukan."""
    if buku_id not in buku_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Buku #{buku_id} tidak ditemukan",
        )

    buku_dihapus = buku_db.pop(buku_id)
    return {"pesan": f"Buku '{buku_dihapus['judul']}' berhasil dihapus"}


# ============================================================
# PENJELASAN:
#
# 1. HTTPException → cara FastAPI mengirim error ke client
#    raise HTTPException(status_code=404, detail="Pesan error")
#
# 2. status_code di decorator → set kode sukses default
#    @app.post("/buku", status_code=201)  ← response sukses = 201
#
# 3. Status code yang WAJIB diingat:
#    ┌──────┬─────────────────────────────────────────────┐
#    │ 200  │ OK - Berhasil (default GET, PUT, DELETE)    │
#    │ 201  │ Created - Data baru berhasil dibuat (POST)  │
#    │ 400  │ Bad Request - Request tidak valid           │
#    │ 404  │ Not Found - Data tidak ditemukan            │
#    │ 409  │ Conflict - Data bentrok/duplikat            │
#    │ 422  │ Validation Error - Pydantic gagal validasi  │
#    │ 500  │ Server Error - Bug di server                │
#    └──────┴─────────────────────────────────────────────┘
#
# 4. Pydantic otomatis return 422 jika data tidak sesuai schema
#    (kita tidak perlu coding manual untuk ini)
#
# Coba di http://127.0.0.1:8001/docs:
#   GET /buku/999      → 404 Not Found
#   POST /buku tanpa field wajib → 422
#   POST /buku/2/pinjam → 400 (stok habis)
# ============================================================
