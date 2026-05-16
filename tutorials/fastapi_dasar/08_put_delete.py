"""
08 - PUT & DELETE (Update dan Hapus Data)
==========================================

Sekarang kita lengkapi CRUD:
- C = Create  → POST   (sudah dipelajari)
- R = Read    → GET    (sudah dipelajari)
- U = Update  → PUT    ← INI
- D = Delete  → DELETE ← INI

Analoginya di restoran:
- POST   = pesan makanan baru
- GET    = lihat pesanan
- PUT    = ubah pesanan ("ganti minumannya jadi es jeruk")
- DELETE = batalkan pesanan

Cara jalankan:
    uvicorn 08_put_delete:app --reload --port 8001
"""

from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI(title="Belajar PUT & DELETE (CRUD Lengkap)")


# ============================================================
# SCHEMA
# ============================================================

class KontakBaru(BaseModel):
    """Data untuk membuat kontak baru."""
    nama: str = Field(min_length=1, max_length=50)
    telepon: str = Field(min_length=8, max_length=15)
    email: str = Field(default="")


class KontakUpdate(BaseModel):
    """Data untuk mengupdate kontak.

    Semua field opsional — hanya kirim yang mau diubah.
    """
    nama: str | None = None
    telepon: str | None = None
    email: str | None = None


# ============================================================
# DATABASE SEDERHANA (list di memori)
# ============================================================

kontak_db: list[dict] = [
    {"id": 1, "nama": "Budi", "telepon": "081234567890", "email": "budi@email.com"},
    {"id": 2, "nama": "Siti", "telepon": "089876543210", "email": "siti@email.com"},
    {"id": 3, "nama": "Dedi", "telepon": "082111222333", "email": ""},
]


# ============================================================
# HELPER: cari kontak berdasarkan ID
# ============================================================

def cari_kontak(kontak_id: int) -> dict | None:
    """Cari kontak berdasarkan ID. Return None jika tidak ketemu."""
    for kontak in kontak_db:
        if kontak["id"] == kontak_id:
            return kontak
    return None


# ============================================================
# C - CREATE (POST)
# ============================================================

@app.post("/kontak")
def tambah_kontak(data: KontakBaru):
    """Tambah kontak baru."""
    new_id = max(k["id"] for k in kontak_db) + 1 if kontak_db else 1
    kontak_baru = {"id": new_id, **data.model_dump()}
    kontak_db.append(kontak_baru)
    return {"pesan": "Kontak ditambahkan!", "data": kontak_baru}


# ============================================================
# R - READ (GET)
# ============================================================

@app.get("/kontak")
def semua_kontak():
    """Lihat semua kontak."""
    return {"total": len(kontak_db), "kontak": kontak_db}


@app.get("/kontak/{kontak_id}")
def satu_kontak(kontak_id: int):
    """Lihat satu kontak berdasarkan ID."""
    kontak = cari_kontak(kontak_id)
    if not kontak:
        return {"error": f"Kontak #{kontak_id} tidak ditemukan"}
    return kontak


# ============================================================
# U - UPDATE (PUT)
# ============================================================

@app.put("/kontak/{kontak_id}")
def update_kontak(kontak_id: int, data: KontakUpdate):
    """Update data kontak yang sudah ada.

    PUT = ganti/update data yang SUDAH ADA.
    Hanya field yang dikirim yang akan diubah.

    Contoh: PUT /kontak/1
    Body: {"nama": "Budi Santoso", "email": "budi.baru@email.com"}
    → Hanya nama dan email yang berubah, telepon tetap.
    """
    kontak = cari_kontak(kontak_id)
    if not kontak:
        return {"error": f"Kontak #{kontak_id} tidak ditemukan"}

    # Update hanya field yang dikirim (bukan None)
    data_update = data.model_dump(exclude_none=True)
    for key, value in data_update.items():
        kontak[key] = value

    return {"pesan": "Kontak berhasil diupdate!", "data": kontak}


# ============================================================
# D - DELETE (DELETE)
# ============================================================

@app.delete("/kontak/{kontak_id}")
def hapus_kontak(kontak_id: int):
    """Hapus kontak berdasarkan ID.

    DELETE = hapus data. Hati-hati, tidak bisa di-undo!

    Contoh: DELETE /kontak/2 → hapus kontak Siti
    """
    kontak = cari_kontak(kontak_id)
    if not kontak:
        return {"error": f"Kontak #{kontak_id} tidak ditemukan"}

    kontak_db.remove(kontak)
    return {"pesan": f"Kontak '{kontak['nama']}' berhasil dihapus!"}


# ============================================================
# BONUS: DELETE semua (hati-hati!)
# ============================================================

@app.delete("/kontak")
def hapus_semua():
    """Hapus SEMUA kontak. Hati-hati!"""
    jumlah = len(kontak_db)
    kontak_db.clear()
    return {"pesan": f"Semua kontak ({jumlah}) berhasil dihapus!"}


# ============================================================
# PENJELASAN:
#
# HTTP Method lengkap (CRUD):
# ┌────────┬────────────┬─────────────────────────────────┐
# │ Method │ Operasi    │ Contoh                          │
# ├────────┼────────────┼─────────────────────────────────┤
# │ POST   │ Create     │ POST /kontak (buat baru)        │
# │ GET    │ Read       │ GET /kontak/1 (lihat data)      │
# │ PUT    │ Update     │ PUT /kontak/1 (ubah data)       │
# │ DELETE │ Delete     │ DELETE /kontak/1 (hapus data)    │
# └────────┴────────────┴─────────────────────────────────┘
#
# Test semua endpoint di: http://127.0.0.1:8001/docs
# ============================================================
