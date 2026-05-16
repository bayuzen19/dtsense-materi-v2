"""Class SimpleEmbedder: mengubah teks menjadi vector angka sederhana."""

import string

import numpy as np


class SimpleEmbedder:
    """Mengubah teks menjadi vector numerik untuk disimpan di FAISS.

    Cara kerjanya sederhana:
    1. Teks dibersihkan (huruf kecil, tanda baca dihapus).
    2. Setiap kata dipetakan ke satu posisi di vector.
    3. Posisi ditentukan dari penjumlahan nilai karakter.
    4. Vector dinormalisasi agar panjangnya sama.

    Parameter:
        dimension: panjang vector yang dihasilkan.
        stopwords: kata-kata yang ingin diabaikan saat embedding.
    """

    def __init__(
        self,
        dimension: int = 256,
        stopwords: list[str] | None = None,
    ) -> None:
        self.dimension = dimension
        self.stopwords = set(stopwords or [])
        self._punctuation_table = str.maketrans("", "", string.punctuation)

    def clean_and_tokenize(self, text: str) -> list[str]:
        """Membersihkan teks lalu memecahnya menjadi list kata.

        Langkah:
        - Ubah ke huruf kecil.
        - Hapus tanda baca.
        - Buang stopwords.
        """
        cleaned = text.lower().translate(self._punctuation_table)
        tokens = cleaned.split()
        return [t for t in tokens if t and t not in self.stopwords]

    def _word_to_index(self, word: str) -> int:
        """Menentukan posisi vector untuk satu kata.

        Rumusnya: jumlahkan (posisi_karakter * kode_ascii_karakter),
        lalu ambil sisa bagi terhadap panjang vector.
        """
        total = 0
        for position, char in enumerate(word, start=1):
            total += position * ord(char)
        return total % self.dimension

    def embed(self, text: str) -> np.ndarray:
        """Mengubah teks menjadi vector float32 sepanjang `dimension`.

        Return:
            numpy array 1-dimensi berisi angka desimal.
        """
        vector = np.zeros(self.dimension, dtype=np.float32)

        for word in self.clean_and_tokenize(text):
            index = self._word_to_index(word)
            vector[index] += 1.0

        # Normalisasi agar semua vector punya panjang yang sama
        length = np.linalg.norm(vector)
        if length > 0:
            vector = vector / length

        return vector
