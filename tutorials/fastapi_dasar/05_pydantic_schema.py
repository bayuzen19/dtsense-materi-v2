"""
05 - Pydantic Schema (Validasi Data Otomatis)
==============================================

Masalah: di file sebelumnya, client bisa kirim data apa saja.
Bagaimana kalau mereka kirim data yang salah format?

Solusi: Pydantic memvalidasi data SEBELUM masuk ke fungsi kita.
Analoginya: pelayan cek pesanan dulu sebelum diantar ke dapur.
"Maaf, menu 'Laptop' tidak ada di restoran kami."

Cara jalankan:
    uvicorn 05_pydantic_schema:app --reload --port 8001
"""

from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI(title="Belajar Pydantic Schema")


# ============================================================
# SCHEMA = cetakan/aturan format data yang WAJIB dipenuhi
# ============================================================

class PesananRequest(BaseModel):
    """Schema untuk data pesanan yang masuk.

    Jika client tidak mengirim field yang wajib, atau tipe datanya salah,
    FastAPI OTOMATIS menolak dan mengembalikan pesan error yang jelas.
    """

    nama_pemesan: str = Field(description="Nama yang memesan")
    menu: str = Field(description="Nama menu yang dipesan")
    jumlah: int = Field(ge=1, le=100, description="Jumlah porsi (1-100)")
    catatan: str = Field(default="", description="Catatan tambahan (opsional)")


class PesananResponse(BaseModel):
    """Schema untuk response yang dikembalikan ke client."""

    pesan: str
    nomor_pesanan: int
    detail: PesananRequest


# ============================================================
# ENDPOINTS
# ============================================================

daftar_pesanan: list[dict] = []


@app.post("/pesanan", response_model=PesananResponse)
def buat_pesanan(data: PesananRequest):
    """Buat pesanan baru DENGAN VALIDASI.

    Coba kirim data yang salah di /docs:
    - Tanpa field 'menu' → error 422
    - jumlah = -5 → error 422 (harus >= 1)
    - jumlah = "abc" → error 422 (harus integer)

    Semua pengecekan dilakukan OTOMATIS oleh Pydantic!
    """
    nomor = len(daftar_pesanan) + 1
    daftar_pesanan.append(data.model_dump())

    return PesananResponse(
        pesan="Pesanan diterima!",
        nomor_pesanan=nomor,
        detail=data,
    )


@app.get("/pesanan")
def lihat_pesanan():
    """Lihat semua pesanan."""
    return {"total": len(daftar_pesanan), "pesanan": daftar_pesanan}


# ============================================================
# PENJELASAN:
#
# BaseModel = class dari Pydantic untuk mendefinisikan "aturan data"
#
# Field(...) bisa menambahkan:
#   - ge=1      → minimal nilainya 1 (greater or equal)
#   - le=100    → maksimal 100 (less or equal)
#   - default="" → opsional, kalau tidak diisi pakai ""
#
# response_model=PesananResponse
#   → FastAPI juga memvalidasi data KELUAR (response)
#   → Dokumentasi /docs otomatis menampilkan format response
#
# TANPA Pydantic: kita harus tulis if-else manual untuk setiap validasi
# DENGAN Pydantic: deklarasi sekali, validasi otomatis selamanya
# ============================================================
