"""
04 - POST Endpoint (Mengirim Data)
===================================

POST = mengirim data ke server untuk diproses/disimpan.
Analoginya: kamu MEMESAN makanan (kirim pesanan ke dapur).

GET  = lihat menu (ambil data)
POST = pesan makanan (kirim data)

Cara jalankan:
    uvicorn 04_post_endpoint:app --reload --port 8001
"""

from fastapi import FastAPI

app = FastAPI(title="Belajar POST Endpoint")

# Database pesanan (simpan di memori)
daftar_pesanan: list[dict] = []


@app.get("/pesanan")
def lihat_pesanan():
    """GET: Lihat semua pesanan yang sudah masuk."""
    return {"total": len(daftar_pesanan), "pesanan": daftar_pesanan}


@app.post("/pesanan")
def buat_pesanan(data: dict):
    """POST: Kirim pesanan baru.

    Client mengirim data dalam format JSON di body request.
    Contoh body:
        {"nama": "Budi", "menu": "Nasi Goreng", "jumlah": 2}
    """
    # Tambah nomor urut otomatis
    nomor = len(daftar_pesanan) + 1
    pesanan_baru = {"nomor": nomor, **data}
    daftar_pesanan.append(pesanan_baru)

    return {"pesan": "Pesanan berhasil!", "pesanan": pesanan_baru}


@app.post("/hitung")
def hitung_total(data: dict):
    """POST: Hitung total harga.

    Body: {"harga_satuan": 25000, "jumlah": 3}
    """
    harga = data.get("harga_satuan", 0)
    jumlah = data.get("jumlah", 1)
    total = harga * jumlah

    return {"harga_satuan": harga, "jumlah": jumlah, "total": total}


# ============================================================
# PENJELASAN:
#
# @app.post("/pesanan") = endpoint yang MENERIMA data dari client
#
# Perbedaan GET vs POST:
# ┌──────┬──────────────────────────────────────────────┐
# │ GET  │ Ambil data. Tidak kirim body. Bisa di browser│
# │ POST │ Kirim data. Ada body JSON. Perlu tools/code  │
# └──────┴──────────────────────────────────────────────┘
#
# Untuk test POST, buka http://127.0.0.1:8001/docs
# → klik endpoint POST → "Try it out" → isi body → "Execute"
#
# Atau pakai curl di terminal:
#   curl -X POST http://127.0.0.1:8001/pesanan
#        -H "Content-Type: application/json"
#        -d '{"nama": "Budi", "menu": "Nasi Goreng"}'
# ============================================================
