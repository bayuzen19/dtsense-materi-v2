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

## 🚀 Cara Menjalankan (Step-by-Step)

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
