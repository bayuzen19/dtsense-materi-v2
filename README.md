# 📚 RAG OOP FastAPI — Materi Pembelajaran

Materi lengkap untuk belajar **Object-Oriented Programming (OOP)**, **FastAPI**,
dan **Retrieval-Augmented Generation (RAG)** dari NOL. Cocok untuk pemula dan
mahasiswa non-IT sekalipun.

Teknologi: Python · FastAPI · FAISS · HuggingFace Embeddings · LangChain + Groq LLM · Streamlit

---

## 🏗 Struktur Project

```
oop_fastapi/
├── src/                              # Source code utama (OOP)
│   ├── models/
│   │   └── document.py              # Class Document (judul, konten, word_count)
│   ├── processing/
│   │   ├── chunker.py               # Class TextChunker (pecah teks jadi potongan)
│   │   ├── embedder.py              # Class SimpleEmbedder (embedding tanpa library)
│   │   └── hf_embedder.py           # Class HuggingFaceEmbedder (all-MiniLM-L6-v2)
│   ├── storage/
│   │   └── vector_store.py          # Class FaissVectorStore (simpan & cari vektor)
│   ├── retrieval/
│   │   ├── retriever.py             # Class Retriever (cari dokumen relevan)
│   │   ├── generator.py             # Class SimpleGenerator (tanpa LLM)
│   │   └── llm_generator.py         # Class LLMGenerator (Groq + Llama 3.3)
│   └── pipeline/
│       └── rag_pipeline.py          # Class RAGPipeline (orkestrasi seluruh alur)
├── api/                              # Layer API (FastAPI)
│   ├── main.py                      # Endpoint: /health, /documents, /ask, /reset
│   ├── schemas.py                   # Pydantic request/response models
│   └── dependencies.py              # Pipeline singleton & loader
├── frontend/                         # Layer UI (Streamlit)
│   └── streamlit_app.py             # Web app: upload PDF, tanya jawab
├── tutorials/                        # 📖 Tutorial FastAPI dari NOL
│   └── fastapi_dasar/               # 9 file progresif (hello world → full CRUD)
│       ├── 01_hello_world.py
│       ├── 02_get_endpoint.py
│       ├── 03_path_parameter.py
│       ├── 04_post_endpoint.py
│       ├── 05_pydantic_schema.py
│       ├── 06_mini_project.py
│       ├── 07_query_parameter.py
│       ├── 08_put_delete.py
│       ├── 09_error_handling.py
│       └── README.md
├── utils/                            # Fungsi-fungsi pembantu
│   └── pdf_loader.py                # Baca PDF, load dari folder
├── data/                             # Dokumen sampel
│   └── sample_documents.pdf         # PDF 6 halaman (OOP, FastAPI, RAG)
├── notebooks/                        # Materi pembelajaran interaktif
│   └── 01_oop_rag_fastapi_easy.ipynb
├── .env                              # API key (GROQ_API_KEY)
├── .gitignore
├── requirements.txt                  # Semua dependencies
└── README.md                         # File ini
```

---

## 🎯 Apa yang Dipelajari

### OOP (Object-Oriented Programming)

| Konsep | File |
|--------|------|
| Class dan Object | `src/models/document.py` |
| Attribute dan Method | `src/processing/chunker.py` |
| Encapsulation | `src/processing/embedder.py` |
| Protocol / Interface | `src/storage/vector_store.py` |
| Composition (class pakai class lain) | `src/storage/vector_store.py` |
| Polymorphism (beda embedder, cara pakai sama) | `src/pipeline/rag_pipeline.py` |
| Orchestration Pattern | `src/pipeline/rag_pipeline.py` |

### FastAPI

| Konsep | File |
|--------|------|
| Hello World & konsep API | `tutorials/fastapi_dasar/01_hello_world.py` |
| GET endpoint | `tutorials/fastapi_dasar/02_get_endpoint.py` |
| Path parameter (URL dinamis) | `tutorials/fastapi_dasar/03_path_parameter.py` |
| POST endpoint | `tutorials/fastapi_dasar/04_post_endpoint.py` |
| Pydantic validasi | `tutorials/fastapi_dasar/05_pydantic_schema.py` |
| Mini project gabungan | `tutorials/fastapi_dasar/06_mini_project.py` |
| Query parameter & filter | `tutorials/fastapi_dasar/07_query_parameter.py` |
| PUT & DELETE (CRUD lengkap) | `tutorials/fastapi_dasar/08_put_delete.py` |
| Error handling & status code | `tutorials/fastapi_dasar/09_error_handling.py` |
| API production-style | `api/main.py` |

### RAG (Retrieval-Augmented Generation)

| Konsep | File |
|--------|------|
| Chunking (pecah teks) | `src/processing/chunker.py` |
| Embedding (teks → angka) | `src/processing/hf_embedder.py` |
| Vector Store (simpan & cari) | `src/storage/vector_store.py` |
| Retrieval (ambil yang relevan) | `src/retrieval/retriever.py` |
| Generation (jawab pakai LLM) | `src/retrieval/llm_generator.py` |
| Pipeline end-to-end | `src/pipeline/rag_pipeline.py` |

---

## � Panduan Implementasi Step-by-Step (Urutan Ngoding)

Ikuti urutan ini saat membangun project dari NOL. Setiap langkah membangun
di atas langkah sebelumnya.

---
### 📌 Konsep Dasar: Function (Fungsi)

Sebelum belajar class, kamu harus paham **function** dulu.

**Function = resep yang bisa dipakai berulang-ulang.**

Bayangkan kamu punya resep "Buat Kopi":
1. Ambil gelas
2. Masukkan kopi 2 sendok
3. Tuang air panas
4. Aduk

Tanpa function, setiap kali mau buat kopi kamu tulis 4 langkah itu lagi.
Dengan function, cukup tulis SEKALI, lalu panggil kapanpun mau bikin kopi.

```python
# TANPA function (capek, nulis berulang):
print("Halo, Budi! Selamat datang.")
print("Halo, Siti! Selamat datang.")
print("Halo, Dedi! Selamat datang.")

# DENGAN function (tulis sekali, pakai berkali-kali):
def sapa(nama):
    print(f"Halo, {nama}! Selamat datang.")

sapa("Budi")   # → Halo, Budi! Selamat datang.
sapa("Siti")   # → Halo, Siti! Selamat datang.
sapa("Dedi")   # → Halo, Dedi! Selamat datang.
```

**Anatomi function:**
```python
def nama_function(parameter1, parameter2):
    """Penjelasan singkat fungsi ini ngapain."""
    # lakukan sesuatu
    hasil = parameter1 + parameter2
    return hasil   # ← kembalikan hasilnya

# Panggil:
jawaban = nama_function(5, 3)   # jawaban = 8
```

| Bagian | Artinya |
|--------|---------|
| `def` | "Saya mau bikin function baru" |
| `nama_function` | Nama resepnya (terserah kamu) |
| `(parameter)` | Bahan yang dibutuhkan resep |
| `return` | Hasil jadinya |

---

### 📌 Konsep Dasar: Class (Kelas)

**Class = cetakan/blueprint untuk membuat sesuatu.**

Bayangkan class itu seperti **formulir kosong**:
- Formulir "Data Mahasiswa" punya kolom: nama, NIM, jurusan
- Setiap mahasiswa mengisi formulir itu → jadi **object** (data nyata)

```python
# CLASS = cetakan/formulir
class Mahasiswa:
    def __init__(self, nama, nim, jurusan):
        # Attribute = kolom-kolom di formulir
        self.nama = nama
        self.nim = nim
        self.jurusan = jurusan

    # Method = aksi yang bisa dilakukan
    def perkenalan(self):
        return f"Hai, saya {self.nama} dari {self.jurusan}"

# OBJECT = formulir yang sudah diisi (data nyata)
budi = Mahasiswa("Budi", "A001", "Informatika")
siti = Mahasiswa("Siti", "A002", "Data Science")

print(budi.nama)           # → Budi
print(siti.perkenalan())   # → Hai, saya Siti dari Data Science
```

**Penjelasan bagian-bagian class:**

| Bagian | Artinya | Analogi |
|--------|---------|---------|
| `class Mahasiswa:` | Buat cetakan baru | Buat formulir kosong |
| `__init__(self, ...)` | Dijalankan saat object dibuat | Saat isi formulir |
| `self` | Merujuk ke object itu sendiri | "Saya" |
| `self.nama = nama` | Simpan data ke object | Isi kolom "Nama" |
| `def perkenalan(self)` | Aksi yang bisa dilakukan object | Kemampuan mahasiswa |

**Perbedaan function biasa vs method (function di dalam class):**

```python
# Function biasa — berdiri sendiri, tidak punya "pemilik"
def hitung_luas(panjang, lebar):
    return panjang * lebar

# Method — milik sebuah class, punya akses ke data object via self
class Persegi:
    def __init__(self, sisi):
        self.sisi = sisi

    def hitung_luas(self):          # ← method
        return self.sisi * self.sisi  # bisa akses self.sisi

kotak = Persegi(5)
print(kotak.hitung_luas())  # → 25
```

**Kenapa pakai class? Kenapa tidak function biasa saja?**

| Situasi | Pakai Function | Pakai Class |
|---------|---------------|-------------|
| Hitung 2+3 | ✅ Cukup | Berlebihan |
| Simpan data mahasiswa + aksi | Ribet | ✅ Rapi |
| Banyak data + banyak aksi yang saling terkait | Sangat ribet | ✅ Terorganisir |
| Project besar (seperti ini) | Kacau | ✅ Wajib |

**Intinya**: Class = data + aksi dibungkus jadi satu paket. Kalau cuma perlu aksi tanpa
menyimpan data, cukup function biasa.

---
### Step 1: Buat folder project dan struktur dasar

```
mkdir oop_fastapi
cd oop_fastapi
mkdir src src/models src/processing src/storage src/retrieval src/pipeline
mkdir api frontend utils data tutorials notebooks
```

Kenapa banyak folder? Karena kita memisahkan tanggung jawab:
- `src/` → semua class OOP (logika utama)
- `api/` → endpoint HTTP (pintu masuk dari luar)
- `frontend/` → tampilan web
- `utils/` → fungsi bantu yang bukan class

---

### Step 2: Buat `src/models/document.py` — Class pertama

**Tujuan**: Belajar membuat class, `__init__`, method, attribute.

```python
class Document:
    def __init__(self, title: str, content: str):
        self.title = title
        self.content = content

    def word_count(self) -> int:
        return len(self.content.split())

    def preview(self, max_chars: int = 100) -> str:
        return self.content[:max_chars] + "..."
```

**Konsep OOP**: Class = cetakan. Object = hasil cetakan.
`Document("FastAPI", "...")` → membuat object dari class Document.

---

### Step 3: Buat `src/processing/chunker.py` — Pecah teks

**Tujuan**: Teks panjang dipotong-potong supaya bisa dicari per bagian.

```python
class TextChunker:
    def __init__(self, chunk_size: int = 30, overlap: int = 5):
        self.chunk_size = chunk_size
        self.overlap = overlap

    def split(self, text: str) -> list[str]:
        words = text.split()
        chunks = []
        start = 0
        while start < len(words):
            end = start + self.chunk_size
            chunk = " ".join(words[start:end])
            chunks.append(chunk)
            start += self.chunk_size - self.overlap
        return chunks
```

**Konsep OOP**: Attribute (`chunk_size`) menyimpan konfigurasi.
Method (`split`) melakukan aksi.

---

### Step 4: Buat `src/processing/embedder.py` — Ubah teks jadi angka

**Tujuan**: Komputer tidak bisa membaca teks. Kita ubah teks jadi array angka (vektor).

```python
class SimpleEmbedder:
    def __init__(self, dimension: int = 256):
        self.dimension = dimension

    def embed(self, text: str) -> list[float]:
        # Setiap kata diubah jadi angka berdasarkan posisi huruf
        ...
```

**Konsep OOP**: Encapsulation — detail cara embed disembunyikan di dalam class.
User cukup panggil `embedder.embed("teks")` tanpa tahu rumus di dalamnya.

---

### Step 5: Buat `src/processing/hf_embedder.py` — Embedding serius

**Tujuan**: Ganti embedding buatan sendiri dengan model AI sungguhan (HuggingFace).

```python
from sentence_transformers import SentenceTransformer

class HuggingFaceEmbedder:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)
        self.dimension = self.model.get_sentence_embedding_dimension()

    def embed(self, text: str) -> list[float]:
        return self.model.encode(text).tolist()
```

**Konsep OOP**: Polymorphism — `SimpleEmbedder` dan `HuggingFaceEmbedder` punya
method `.embed()` yang sama, tapi cara kerjanya berbeda. Bisa ditukar-tukar!

---

### Step 6: Buat `src/storage/vector_store.py` — Simpan & cari vektor

**Tujuan**: Menyimpan semua vektor embedding ke FAISS, lalu mencari yang paling mirip.

```python
import faiss
import numpy as np

class FaissVectorStore:
    def __init__(self, embedder):
        self.embedder = embedder
        self.index = faiss.IndexFlatL2(embedder.dimension)
        self.texts = []

    def add(self, text: str): ...
    def search(self, query: str, top_k: int = 3) -> list[str]: ...
```

**Konsep OOP**: Composition — `FaissVectorStore` MEMILIKI `embedder` di dalamnya.
Satu class memakai class lain. Protocol/Interface memastikan embedder apapun bisa dipakai
selama punya `.dimension` dan `.embed()`.

---

### Step 7: Buat `src/retrieval/retriever.py` — Cari dokumen relevan

**Tujuan**: Membungkus vector_store.search() supaya lebih mudah dipakai.

```python
class Retriever:
    def __init__(self, vector_store):
        self.vector_store = vector_store

    def retrieve(self, query: str, top_k: int = 3) -> list[str]:
        return self.vector_store.search(query, top_k)
```

**Konsep OOP**: Separation of Concerns — setiap class punya SATU tugas.
Retriever tugasnya HANYA mencari. Tidak tahu cara embed atau simpan.

---

### Step 8: Buat `src/retrieval/llm_generator.py` — Jawab pakai AI

**Tujuan**: Ambil potongan teks yang relevan, kirim ke LLM, dapat jawaban lengkap.

```python
from langchain_groq import ChatGroq

class LLMGenerator:
    def __init__(self, model_name: str = "llama-3.3-70b-versatile"):
        self.llm = ChatGroq(model_name=model_name)

    def generate(self, query: str, contexts: list[str]) -> str:
        # Gabung konteks + pertanyaan → kirim ke LLM → dapat jawaban
        ...
```

**Konsep OOP**: Class ini bertanggung jawab HANYA untuk generate jawaban.
Tidak tahu cara cari dokumen. Terima beres dari Retriever.

---

### Step 9: Buat `src/pipeline/rag_pipeline.py` — Gabungkan semuanya

**Tujuan**: Satu class yang mengorkestrasikan seluruh alur dari A-Z.

```python
class RAGPipeline:
    def __init__(self, ...):
        self.chunker = TextChunker(...)
        self.embedder = HuggingFaceEmbedder(...)
        self.vector_store = FaissVectorStore(self.embedder)
        self.retriever = Retriever(self.vector_store)
        self.generator = LLMGenerator(...)

    def add_document(self, title, content): ...
    def ask(self, question) -> str: ...
```

**Konsep OOP**: Orchestration Pattern — pipeline merangkai semua class menjadi alur kerja.
Ini seperti "manajer" yang mendelegasikan tugas ke bawahannya.

Alur: Teks → Chunker → Embedder → VectorStore → Retriever → Generator → Jawaban

---

### Step 10: Buat `api/schemas.py` — Definisikan format data API

**Tujuan**: Tentukan format JSON yang diterima dan dikembalikan oleh API.

```python
from pydantic import BaseModel

class AskRequest(BaseModel):
    question: str

class AskResponse(BaseModel):
    answer: str
    contexts: list[str]
```

---

### Step 11: Buat `api/dependencies.py` — Singleton pipeline

**Tujuan**: Buat SATU instance pipeline yang dipakai bersama oleh semua endpoint.

```python
from src.pipeline.rag_pipeline import RAGPipeline

pipeline = RAGPipeline(use_llm=True, use_simple_embedder=False)
```

---

### Step 12: Buat `api/main.py` — Endpoint FastAPI

**Tujuan**: Pintu masuk HTTP. Client kirim request → server proses → kirim response.

```python
from fastapi import FastAPI
app = FastAPI()

@app.post("/ask")
def ask(request: AskRequest):
    answer = pipeline.ask(request.question)
    return {"answer": answer}
```

---

### Step 13: Buat `frontend/streamlit_app.py` — Tampilan web

**Tujuan**: UI sederhana dimana user bisa upload PDF dan bertanya.
Streamlit berkomunikasi dengan FastAPI via HTTP request.

---

### 🗺️ Peta Hubungan Antar File

```
User bertanya "Apa itu OOP?"
         │
         ▼
┌─────────────────────┐
│  frontend/          │  ← User klik tombol "Tanya"
│  streamlit_app.py   │
└────────┬────────────┘
         │ HTTP POST /ask
         ▼
┌─────────────────────┐
│  api/main.py        │  ← Terima request, panggil pipeline
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│  pipeline/          │  ← Orkestrasi semua langkah
│  rag_pipeline.py    │
└────────┬────────────┘
         │
    ┌────┴─────────────────────────────────┐
    ▼                                      ▼
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│ retriever.py │→ │vector_store  │→ │ hf_embedder  │
│ (cari)       │  │ (FAISS)      │  │ (teks→angka) │
└──────────────┘  └──────────────┘  └──────────────┘
    │
    ▼
┌──────────────┐
│llm_generator │  ← Dapat konteks relevan, generate jawaban
│ (Groq LLM)   │
└──────────────┘
         │
         ▼
    "OOP adalah paradigma pemrograman yang menggunakan
     class dan object untuk mengorganisir kode..."
```

---

## �🚀 Cara Menjalankan (Step-by-Step)

### Langkah 1: Buat Virtual Environment

Virtual environment = "ruang kerja terisolasi" supaya library project ini
tidak bentrok dengan project Python lainnya.

**Windows:**
```bash
cd F:\programming\ngajar\dtsense\oop_fastapi
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
cd /path/to/oop_fastapi
python3 -m venv venv
source venv/bin/activate
```

> Setelah aktif, terminal akan menampilkan `(venv)` di depan prompt.

### Langkah 2: Install Dependencies

```bash
pip install -r requirements.txt
```

> Proses ini akan mengunduh semua library yang dibutuhkan (~500MB untuk model HuggingFace).

### Langkah 3: Setup API Key (untuk LLM)

Buat file `.env` di root project:

```
GROQ_API_KEY=gsk_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

> Dapatkan gratis di https://console.groq.com/keys
> Jika tidak punya API key, sistem tetap jalan tapi pakai SimpleGenerator (tanpa LLM).

### Langkah 4: Jalankan Backend (FastAPI)

```bash
uvicorn api.main:app --reload
```

Buka http://127.0.0.1:8000/docs → dokumentasi API interaktif.

### Langkah 5: Jalankan Frontend (Streamlit)

Buka terminal baru (tetap di folder project, venv aktif):

```bash
streamlit run frontend/streamlit_app.py
```

Buka http://localhost:8501 → Web app untuk upload PDF dan tanya jawab.

---

## 📖 Tutorial FastAPI (Untuk Pemula Total)

Folder `tutorials/fastapi_dasar/` berisi 9 file yang bisa dijalankan SENDIRI-SENDIRI:

```bash
cd tutorials/fastapi_dasar
uvicorn 01_hello_world:app --reload --port 8001
```

Buka http://127.0.0.1:8001/docs dan eksperimen langsung!

Urutan belajar:
1. **01** → Apa itu API? Endpoint pertama
2. **02** → GET: mengambil data
3. **03** → Path parameter: URL dinamis
4. **04** → POST: mengirim data
5. **05** → Pydantic: validasi otomatis
6. **06** → Mini project: gabungan 01-05
7. **07** → Query parameter: filter & pencarian
8. **08** → PUT & DELETE: CRUD lengkap
9. **09** → Error handling & status code

---

## 📓 Notebook Pembelajaran

Buka `notebooks/01_oop_rag_fastapi_easy.ipynb` untuk materi interaktif:

1. Dasar Python (variabel, fungsi)
2. Membuat class pertama
3. OOP: attribute, method, `__init__`
4. Class Document
5. Chunking (pecah teks)
6. Embedding (teks → vektor angka)
7. FAISS (pencarian vektor)
8. RAG Pipeline lengkap
9. Frontend ↔ Backend

---

## ⚙️ Kompatibilitas

| Komponen | Versi |
|----------|-------|
| Python | 3.10 – 3.14 |
| FastAPI | ≥ 0.115.0 |
| sentence-transformers | ≥ 3.0.0 |
| Model embedding | all-MiniLM-L6-v2 (~80MB, 384 dimensi) |
| LLM | Llama 3.3 70B via Groq (gratis) |

---

## 📋 Catatan Penting

- **API Key Groq GRATIS** — daftar di https://console.groq.com
