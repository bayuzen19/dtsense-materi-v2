"""
01 - Hello World FastAPI
========================

Ini adalah server API paling sederhana.
Hanya 5 baris kode kerja.

Cara jalankan:
    uvicorn 01_hello_world:app --reload --port 8001

Lalu buka: http://127.0.0.1:8001/docs
"""

from fastapi import FastAPI

# Buat aplikasi FastAPI (seperti buka restoran baru)
app = FastAPI(title="Server Pertamaku")


# Buat endpoint GET di path "/"
# GET = mengambil data (seperti lihat menu)
@app.get("/")
def halaman_utama():
    """Endpoint paling sederhana: kembalikan pesan sapaan."""
    return {"pesan": "Halo! Ini server pertamaku 🎉"}


# Endpoint kedua: informasi tentang server
@app.get("/info")
def tentang():
    """Informasi tentang server ini."""
    return {
        "nama_app": "Tutorial FastAPI",
        "versi": "1.0",
        "pembuat": "Murid DTSense",
    }


# ============================================================
# PENJELASAN:
#
# 1. `from fastapi import FastAPI` = import library FastAPI
# 2. `app = FastAPI()` = buat aplikasi baru
# 3. `@app.get("/")` = decorator yang bilang:
#    "kalau ada orang buka URL /, jalankan fungsi di bawah ini"
# 4. Fungsi return dictionary → otomatis jadi JSON
#
# JSON itu format data universal yang dipakai semua aplikasi
# untuk berkomunikasi. Bentuknya mirip dictionary Python.
# ============================================================
