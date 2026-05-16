"""PDF Loader: fungsi untuk membaca file PDF dan mengekstrak teksnya."""

from pathlib import Path

from pypdf import PdfReader


def extract_text_from_pdf(pdf_path: str) -> str:
    """Membaca file PDF dan mengembalikan isi teksnya.

    Parameter:
        pdf_path: path lengkap ke file PDF.

    Return:
        String berisi semua teks dari setiap halaman PDF.
    """
    reader = PdfReader(pdf_path)
    pages: list[str] = []

    for page in reader.pages:
        text = page.extract_text()
        if text and text.strip():
            pages.append(text.strip())

    return "\n\n".join(pages)


def load_documents_from_directory(directory: str) -> list[tuple[str, str]]:
    """Mencari semua file PDF di folder dan membaca isinya.

    Parameter:
        directory: path ke folder berisi file PDF.

    Return:
        List tuple (judul, konten) dari setiap PDF yang ditemukan.
    """
    folder = Path(directory)
    documents: list[tuple[str, str]] = []

    if not folder.exists():
        return documents

    for pdf_file in sorted(folder.glob("*.pdf")):
        content = extract_text_from_pdf(str(pdf_file))
        if content.strip():
            title = pdf_file.stem.replace("_", " ").title()
            documents.append((title, content))

    return documents
