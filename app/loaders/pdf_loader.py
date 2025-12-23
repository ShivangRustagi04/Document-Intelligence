import fitz  # PyMuPDF
from pypdf import PdfReader


def parse_pdf(file_obj):
    pages = []

    doc = fitz.open(stream=file_obj.read(), filetype="pdf")

    for i, page in enumerate(doc):
        text = page.get_text("text")


        blocks = page.get_text("blocks")
        block_text = ""
        for b in blocks:
            if isinstance(b[4], str):
                block_text += b[4] + "\n"

        pages.append({
            "page": i + 1,
            "text": text + "\n" + block_text
        })

    if not any("Overdue" in p["text"] for p in pages):
        file_obj.seek(0)
        reader = PdfReader(file_obj)
        for i, page in enumerate(reader.pages):
            extra_text = page.extract_text() or ""
            pages[i]["text"] += "\n" + extra_text

    return pages
