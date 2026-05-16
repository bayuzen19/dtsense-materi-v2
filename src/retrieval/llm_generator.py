"""Class LLMGenerator: menyusun jawaban menggunakan LLM dari Groq.

Ini adalah versi 'cerdas' dari generator yang memanfaatkan Large Language Model
untuk menyusun jawaban yang natural dari konteks yang ditemukan.
"""

from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage


class LLMGenerator:
    """Menyusun jawaban menggunakan LLM (Groq) berdasarkan konteks retrieval.

    Class ini mendemonstrasikan:
    - Bagaimana menghubungkan LLM ke pipeline RAG.
    - Penggunaan system prompt untuk mengatur perilaku model.
    - Composition: class ini memakai object ChatGroq di dalamnya.

    Parameter:
        model_name: nama model di Groq (default: llama-3.3-70b-versatile).
        temperature: kreativitas jawaban (0 = faktual, 1 = kreatif).
        max_tokens: batas panjang jawaban.
        api_key: Groq API key (opsional, bisa dari environment variable).
    """

    def __init__(
        self,
        model_name: str = "llama-3.3-70b-versatile",
        temperature: float = 0.3,
        max_tokens: int = 512,
        api_key: str | None = None,
    ) -> None:
        self.model_name = model_name
        self.llm = ChatGroq(
            model=model_name,
            temperature=temperature,
            max_tokens=max_tokens,
            api_key=api_key,  # None = baca dari env GROQ_API_KEY
        )

    def generate(self, question: str, contexts: list[dict[str, object]]) -> str:
        """Membuat jawaban menggunakan LLM berdasarkan konteks.

        Alur:
        1. Gabungkan isi konteks menjadi satu teks referensi.
        2. Buat system prompt yang mengarahkan LLM.
        3. Kirim ke Groq dan terima jawaban.

        Parameter:
            question: pertanyaan pengguna.
            contexts: list chunk hasil retrieval.

        Return:
            String jawaban dari LLM.
        """
        if not contexts:
            return "Maaf, informasi belum ditemukan pada dokumen yang tersedia."

        # Gabungkan konteks menjadi referensi
        context_text = "\n\n".join(
            f"[Sumber: {ctx['title']}, Chunk #{ctx['chunk_id']}]\n{ctx['content']}"
            for ctx in contexts
        )

        # System prompt: instruksi untuk LLM
        system_prompt = (
            "Kamu adalah asisten yang menjawab pertanyaan HANYA berdasarkan "
            "konteks yang diberikan. Jika konteks tidak mengandung jawaban, "
            "katakan bahwa informasi tidak ditemukan. Jawab dalam Bahasa Indonesia "
            "yang jelas dan ringkas."
        )

        # Human message: konteks + pertanyaan
        human_message = (
            f"Konteks:\n{context_text}\n\n"
            f"Pertanyaan: {question}\n\n"
            f"Jawab berdasarkan konteks di atas:"
        )

        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=human_message),
        ]

        try:
            response = self.llm.invoke(messages)
            return response.content
        except Exception as e:
            # Fallback: jika LLM gagal, gabungkan konteks secara manual
            fallback = " ".join(str(ctx["content"]) for ctx in contexts[:2])
            return (
                f"[LLM Error: {type(e).__name__}] "
                f"Berikut konteks yang ditemukan: {fallback}"
            )
