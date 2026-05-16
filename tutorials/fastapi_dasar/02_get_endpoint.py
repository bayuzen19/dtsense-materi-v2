"""
02 - GET Endpoint (Mengambil Data)
===================================

GET = meminta/mengambil informasi dari server.
Analoginya: kamu MELIHAT menu restoran, bukan memesan.

Cara jalankan:
    uvicorn 02_get_endpoint:app --reload --port 8001
"""

from fastapi import FastAPI

app = FastAPI(title="Belajar GET Endpoint")

# Database sederhana (list of dict) — simpan di memori
menu_makanan = [
    {"id": 1, "nama": "Nasi Goreng", "harga": 25000},
    {"id": 2, "nama": "Mie Ayam", "harga": 20000},
    {"id": 3, "nama": "Soto Betawi", "harga": 30000},
    {"id": 4, "nama": "Gado-Gado", "harga": 18000},
]


@app.get("/menu")
def lihat_semua_menu():
    """GET /menu → Mengembalikan semua daftar makanan.

    Seperti: minta pelayan tunjukkan seluruh menu.
    """
    return {"total": len(menu_makanan), "menu": menu_makanan}


@app.get("/menu/termurah")
def menu_termurah():
    """GET /menu/termurah → Cari makanan paling murah.

    Server yang MEMPROSES data sebelum dikembalikan ke client.
    """
    termurah = min(menu_makanan, key=lambda m: m["harga"])
    return {"rekomendasi_hemat": termurah}


# ============================================================
# PENJELASAN:
#
# - Semua endpoint di file ini pakai @app.get(...)
# - GET artinya client hanya MINTA data, tidak mengirim data
# - Data dikembalikan dalam format JSON (dictionary Python)
# - Coba buka http://127.0.0.1:8001/docs lalu klik "Try it out"
#
# Contoh akses langsung di browser:
#   http://127.0.0.1:8001/menu
#   http://127.0.0.1:8001/menu/termurah
# ============================================================
