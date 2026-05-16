"""Class TextChunker: memecah teks panjang menjadi potongan kecil."""


class TextChunker:
    """Memecah teks menjadi chunk berdasarkan jumlah kata.

    Parameter:
        chunk_size: jumlah kata maksimal per chunk.
        overlap: jumlah kata yang diulang antar chunk agar konteks tidak terputus.
    """

    def __init__(self, chunk_size: int = 30, overlap: int = 5) -> None:
        if chunk_size <= 0:
            raise ValueError("chunk_size harus lebih besar dari 0")
        if overlap < 0:
            raise ValueError("overlap tidak boleh negatif")
        if overlap >= chunk_size:
            raise ValueError("overlap harus lebih kecil dari chunk_size")

        self.chunk_size = chunk_size
        self.overlap = overlap

    def split(self, text: str) -> list[str]:
        """Memecah teks menjadi list potongan kata.

        Return:
            List string, masing-masing berisi sebagian kata dari teks asli.
        """
        words = text.split()
        if not words:
            return []

        step = self.chunk_size - self.overlap
        chunks: list[str] = []

        for start in range(0, len(words), step):
            chunk_words = words[start : start + self.chunk_size]
            if not chunk_words:
                break
            chunks.append(" ".join(chunk_words))
            if start + self.chunk_size >= len(words):
                break

        return chunks
