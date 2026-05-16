"""
03 - Path Parameter (URL Dinamis)
==================================

Path parameter = bagian URL yang berubah-ubah.
Analoginya: "Saya mau lihat menu nomor 2" → /menu/2

Cara jalankan:
    uvicorn 03_path_parameter:app --reload --port 8001
"""

from fastapi import FastAPI

app = FastAPI(title="Belajar Path Parameter")

# Data mahasiswa
mahasiswa_db = {
    "A001": {"nama": "Budi Santoso", "jurusan": "Informatika", "semester": 5},
    "A002": {"nama": "Siti Rahayu", "jurusan": "Sistem Informasi", "semester": 3},
    "A003": {"nama": "Dedi Kurniawan", "jurusan": "Data Science", "semester": 7},
}


@app.get("/mahasiswa")
def semua_mahasiswa():
    """Lihat semua mahasiswa yang terdaftar."""
    return {"total": len(mahasiswa_db), "data": mahasiswa_db}


@app.get("/mahasiswa/{nim}")
def cari_mahasiswa(nim: str):
    """Cari satu mahasiswa berdasarkan NIM.

    {nim} di URL akan menjadi parameter fungsi.
    Contoh: GET /mahasiswa/A001 → nim = "A001"
    """
    if nim not in mahasiswa_db:
        return {"error": f"Mahasiswa dengan NIM '{nim}' tidak ditemukan"}

    return {"nim": nim, "data": mahasiswa_db[nim]}


@app.get("/mahasiswa/{nim}/jurusan")
def jurusan_mahasiswa(nim: str):
    """Ambil HANYA jurusan dari satu mahasiswa.

    Contoh: GET /mahasiswa/A001/jurusan → {"jurusan": "Informatika"}
    """
    if nim not in mahasiswa_db:
        return {"error": f"NIM '{nim}' tidak ditemukan"}

    return {"nim": nim, "jurusan": mahasiswa_db[nim]["jurusan"]}


# ============================================================
# PENJELASAN:
#
# Path parameter ditulis dengan {kurung_kurawal} di URL:
#   @app.get("/mahasiswa/{nim}")
#
# FastAPI otomatis:
# 1. Ambil nilai dari URL (misal /mahasiswa/A001 → nim="A001")
# 2. Masukkan ke parameter fungsi
# 3. Validasi tipe data (str, int, dll)
#
# Coba di browser:
#   http://127.0.0.1:8001/mahasiswa/A001
#   http://127.0.0.1:8001/mahasiswa/A999  ← tidak ada
# ============================================================
