# 🚀 Tutorial FastAPI untuk Pemula

Folder ini berisi materi pengantar FastAPI yang disusun **step-by-step**.
Jalankan setiap file Python satu per satu dari yang paling kecil nomornya.

---

## Apa itu API?

Bayangkan kamu di restoran:
- **Kamu** = pengguna (client/frontend)
- **Pelayan** = API
- **Dapur** = server/backend

Kamu TIDAK langsung masak di dapur. Kamu pesan lewat pelayan (API),
pelayan antar pesanan ke dapur, dapur masak, pelayan antar hasilnya ke meja kamu.

Dalam programming:
- **Frontend** (Streamlit/website) = kamu di meja
- **API** (FastAPI) = pelayan yang terima dan antar pesanan
- **Backend** (Python logic) = dapur yang memproses data

---

## Urutan Belajar

| No | File | Topik |
|----|------|-------|
| 1 | `01_hello_world.py` | Server pertama — cuma 5 baris |
| 2 | `02_get_endpoint.py` | Mengambil data (seperti lihat menu) |
| 3 | `03_path_parameter.py` | URL dinamis (seperti pilih meja) |
| 4 | `04_post_endpoint.py` | Mengirim data (seperti pesan makanan) |
| 5 | `05_pydantic_schema.py` | Validasi data otomatis (cek pesanan valid) |
| 6 | `06_mini_project.py` | Mini project: API Catatan Sederhana |

---

## Cara Menjalankan

Untuk setiap file:
```bash
cd tutorials/fastapi_dasar
uvicorn 01_hello_world:app --reload --port 8001
```

Lalu buka browser di: http://127.0.0.1:8001/docs

> **Tips:** Swagger UI di `/docs` itu seperti "buku menu interaktif" —
> kamu bisa langsung coba semua endpoint tanpa tools tambahan.

---

## Kenapa FastAPI?

| Keunggulan | Penjelasan Sederhana |
|------------|---------------------|
| Cepat | Secepat bahasa Go/NodeJS |
| Otomatis validasi | Salah format? Langsung ditolak + pesan error jelas |
| Dokumentasi gratis | Buka `/docs` = buku manual otomatis |
| Type hints | Python biasa, tapi lebih aman dari typo |
