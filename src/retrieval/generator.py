"""Class SimpleGenerator: menyusun jawaban dari konteks yang ditemukan."""


class SimpleGenerator:
    """Menyusun jawaban sederhana dari konteks hasil retrieval.

    Generator ini tidak memakai LLM eksternal. Tujuannya agar murid
    bisa fokus pada alur RAG tanpa perlu API key atau koneksi internet.
    """

    def generate(self, question: str, contexts: list[dict[str, object]]) -> str:
        """Membuat jawaban berdasarkan konteks yang ditemukan.

        Logika:
        - Jika tidak ada konteks, jawab bahwa informasi belum ditemukan.
        - Jika ada konteks, gabungkan isi dari chunk terbaik sebagai jawaban.

        Parameter:
            question: pertanyaan pengguna.
            contexts: list chunk hasil retrieval.

        Return:
            String jawaban akhir.
        """
        if not contexts:
            return "Maaf, informasi belum ditemukan pada dokumen yang tersedia."

        best_score = float(contexts[0]["score"])
        if best_score < 0.05:
            return "Maaf, informasi belum ditemukan pada dokumen yang tersedia."

        # Ambil isi dari 2 chunk terbaik
        top_contents = [str(ctx["content"]) for ctx in contexts[:2]]
        combined = " ".join(top_contents)

        return (
            f"Berdasarkan dokumen yang tersedia, berikut jawaban untuk "
            f"'{question}': {combined}"
        )
