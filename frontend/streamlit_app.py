"""Frontend Streamlit: antarmuka web untuk berinteraksi dengan API RAG.

Cara menjalankan:
    streamlit run frontend/streamlit_app.py
"""

import json
import urllib.request
import urllib.error

import streamlit as st

API_BASE = "http://127.0.0.1:8000"


# ============================================================
# FUNGSI HELPER: komunikasi dengan backend API
# ============================================================


def call_api(method: str, endpoint: str, body: dict | None = None) -> dict:
    """Mengirim HTTP request ke backend FastAPI.

    Parameter:
        method: GET atau POST.
        endpoint: path endpoint (contoh: /health).
        body: data yang dikirim (untuk POST).

    Return:
        Dictionary hasil response dari API.
    """
    url = f"{API_BASE}{endpoint}"

    if body is not None:
        data = json.dumps(body).encode("utf-8")
        request = urllib.request.Request(
            url, data=data, method=method,
            headers={"Content-Type": "application/json"},
        )
    else:
        request = urllib.request.Request(url, method=method)

    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            return json.loads(response.read().decode())
    except urllib.error.HTTPError as e:
        return {"error": f"HTTP Error {e.code}: {e.reason}"}
    except urllib.error.URLError:
        return {"error": "Tidak bisa terhubung ke server. Pastikan API sudah berjalan."}


# ============================================================
# TAMPILAN STREAMLIT
# ============================================================

st.set_page_config(page_title="RAG OOP Demo", page_icon="📚", layout="wide")
st.title("📚 RAG OOP FastAPI Demo")
st.markdown("Aplikasi Retrieval-Augmented Generation menggunakan OOP dan FAISS")

# --- Sidebar: Status Server ---
with st.sidebar:
    st.header("⚙️ Status Server")
    if st.button("Cek Status"):
        health = call_api("GET", "/health")
        if "error" in health:
            st.error(health["error"])
        else:
            st.success(f"Status: {health['status']}")
            st.metric("Dokumen", health["total_documents"])
            st.metric("Chunk", health["total_chunks"])

# --- Tab 1: Tambah Dokumen ---
tab1, tab2, tab3 = st.tabs(["📄 Tambah Dokumen", "❓ Tanya", "📋 Daftar Dokumen"])

with tab1:
    st.subheader("Tambah Dokumen Baru")
    title = st.text_input("Judul Dokumen", placeholder="Contoh: Panduan Python OOP")
    content = st.text_area(
        "Isi Dokumen", height=200,
        placeholder="Ketik isi dokumen di sini...",
    )

    if st.button("Kirim Dokumen", type="primary"):
        if not title or not content:
            st.warning("Judul dan isi dokumen wajib diisi!")
        else:
            result = call_api("POST", "/documents", {"title": title, "content": content})
            if "error" in result:
                st.error(result["error"])
            else:
                st.success(
                    f"✅ {result['message']}: {result['title']} "
                    f"({result['chunks_created']} chunk)"
                )

# --- Tab 2: Tanya ---
with tab2:
    st.subheader("Ajukan Pertanyaan")
    question = st.text_input(
        "Pertanyaan", placeholder="Apa itu class dalam Python?"
    )

    if st.button("Kirim Pertanyaan", type="primary"):
        if not question:
            st.warning("Tulis pertanyaan terlebih dahulu!")
        else:
            result = call_api("POST", "/ask", {"question": question})
            if "error" in result:
                st.error(result["error"])
            else:
                st.markdown("### Jawaban")
                st.write(result["answer"])

                if result["retrieved_contexts"]:
                    st.markdown("### Konteks yang Ditemukan")
                    for ctx in result["retrieved_contexts"]:
                        with st.expander(
                            f"📎 {ctx['title']} (Chunk #{ctx['chunk_id']}, "
                            f"Skor: {ctx['score']:.4f})"
                        ):
                            st.write(ctx["content"])

# --- Tab 3: Daftar Dokumen ---
with tab3:
    st.subheader("Dokumen yang Tersimpan")
    if st.button("Refresh Daftar"):
        result = call_api("GET", "/documents")
        if "error" in result:
            st.error(result["error"])
        else:
            st.info(f"Total dokumen: {result['total']}")
            for doc in result["documents"]:
                st.markdown(
                    f"- **{doc['title']}** — "
                    f"{doc['content_length']} karakter, "
                    f"{doc['chunk_count']} chunk"
                )
