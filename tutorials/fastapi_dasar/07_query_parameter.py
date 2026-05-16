"""
07 - Query Parameter (Filter & Pencarian)
==========================================

Query parameter = data tambahan di URL setelah tanda "?"
Analoginya: "Saya mau lihat menu, TAPI hanya yang pedas dan harga di bawah 30rb"

Contoh URL:
    /produk?kategori=makanan&harga_max=30000

Berbeda dengan path parameter:
- Path param  → /mahasiswa/A001      → WAJIB, bagian dari alamat
- Query param → /produk?kategori=... → OPSIONAL, untuk filter/pencarian

Cara jalankan:
    uvicorn 07_query_parameter:app --reload --port 8001
"""

from fastapi import FastAPI

app = FastAPI(title="Belajar Query Parameter")

# Database produk
produk_db = [
    {"id": 1, "nama": "Nasi Goreng", "kategori": "makanan", "harga": 25000},
    {"id": 2, "nama": "Mie Ayam", "kategori": "makanan", "harga": 20000},
    {"id": 3, "nama": "Es Teh", "kategori": "minuman", "harga": 5000},
    {"id": 4, "nama": "Jus Alpukat", "kategori": "minuman", "harga": 15000},
    {"id": 5, "nama": "Ayam Bakar", "kategori": "makanan", "harga": 35000},
    {"id": 6, "nama": "Es Jeruk", "kategori": "minuman", "harga": 8000},
    {"id": 7, "nama": "Soto Ayam", "kategori": "makanan", "harga": 22000},
]


@app.get("/produk")
def daftar_produk(
    kategori: str | None = None,
    harga_min: int = 0,
    harga_max: int = 999999,
    limit: int = 10,
):
    """Lihat daftar produk dengan FILTER.

    Query parameter ditulis sebagai parameter fungsi dengan default value.
    - Kalau ada default → opsional (query parameter)
    - Kalau tanpa default → wajib

    Contoh URL:
        /produk                         → semua produk
        /produk?kategori=minuman        → hanya minuman
        /produk?harga_max=20000         → harga ≤ 20rb
        /produk?kategori=makanan&limit=3 → 3 makanan pertama
    """
    hasil = produk_db

    # Filter berdasarkan kategori (jika diberikan)
    if kategori:
        hasil = [p for p in hasil if p["kategori"] == kategori]

    # Filter berdasarkan range harga
    hasil = [p for p in hasil if harga_min <= p["harga"] <= harga_max]

    # Batasi jumlah hasil
    hasil = hasil[:limit]

    return {
        "filter": {
            "kategori": kategori,
            "harga_min": harga_min,
            "harga_max": harga_max,
            "limit": limit,
        },
        "total": len(hasil),
        "produk": hasil,
    }


@app.get("/cari")
def cari_produk(q: str = ""):
    """Pencarian sederhana berdasarkan nama produk.

    Contoh: /cari?q=ayam → cari produk yang mengandung kata "ayam"
    """
    if not q:
        return {"pesan": "Ketik parameter 'q' untuk mencari. Contoh: /cari?q=nasi"}

    hasil = [p for p in produk_db if q.lower() in p["nama"].lower()]

    return {"kata_kunci": q, "total": len(hasil), "hasil": hasil}


@app.get("/produk/ringkasan")
def ringkasan(kategori: str | None = None):
    """Ringkasan statistik produk.

    /produk/ringkasan              → semua
    /produk/ringkasan?kategori=minuman → hanya minuman
    """
    data = produk_db
    if kategori:
        data = [p for p in data if p["kategori"] == kategori]

    if not data:
        return {"error": f"Kategori '{kategori}' tidak ditemukan"}

    harga_list = [p["harga"] for p in data]

    return {
        "kategori": kategori or "semua",
        "total_produk": len(data),
        "harga_termurah": min(harga_list),
        "harga_termahal": max(harga_list),
        "rata_rata_harga": sum(harga_list) // len(harga_list),
    }


# ============================================================
# PENJELASAN:
#
# Query parameter = parameter fungsi yang punya DEFAULT VALUE.
#
#   def fungsi(kategori: str | None = None, limit: int = 10):
#              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#              Semua ini jadi query parameter karena punya default
#
# Bandingkan dengan path parameter:
#   @app.get("/item/{item_id}")
#   def fungsi(item_id: int):    ← TANPA default = path param
#
# Cara pakai di URL:
#   ?key=value                   → satu parameter
#   ?key1=value1&key2=value2     → beberapa parameter
#
# Coba di browser:
#   http://127.0.0.1:8001/produk?kategori=minuman
#   http://127.0.0.1:8001/produk?harga_max=20000&limit=2
#   http://127.0.0.1:8001/cari?q=ayam
# ============================================================
