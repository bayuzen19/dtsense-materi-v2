"""Class Document: menyimpan satu dokumen teks."""


class Document:
    """Mewakili satu dokumen yang masuk ke sistem RAG.

    Attribute:
        title: judul dokumen.
        content: isi teks dokumen.
    """

    def __init__(self, title: str, content: str) -> None:
        self.title = title.strip()
        self.content = content.strip()

    def word_count(self) -> int:
        """Menghitung jumlah kata dalam dokumen."""
        return len(self.content.split())

    def preview(self, max_words: int = 15) -> str:
        """Mengambil beberapa kata pertama sebagai preview."""
        words = self.content.split()
        return " ".join(words[:max_words])

    def to_dict(self) -> dict[str, str]:
        """Mengubah object Document menjadi dictionary."""
        return {"title": self.title, "content": self.content}

    def __repr__(self) -> str:
        return f"Document(title='{self.title}', words={self.word_count()})"
