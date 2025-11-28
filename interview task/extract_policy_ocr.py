import os
import json
from pathlib import Path

from pdf2image import convert_from_path
import pytesseract
import pytesseract



# IMPORTANT: set this to your Tesseract exe path on Windows
# e.g. "C:/Program Files/Tesseract-OCR/tesseract.exe"
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"




def clean_text(text: str) -> str:
    if not text:
        return ""
    text = text.replace("\n", " ").replace("\t", " ")
    while "  " in text:
        text = text.replace("  ", " ")
    return text.strip()


def extract_policy_pdf_ocr(
    pdf_path: str,
    output_json_path: str = "data/policy_chunks_ocr.json",
    dpi: int = 300,
):
    pdf_path = Path(pdf_path)
    if not pdf_path.exists():
        raise FileNotFoundError(pdf_path)

    # Convert each page to an image
    pages = convert_from_path(str(pdf_path), dpi=dpi)

    chunks = []
    for i, img in enumerate(pages):
        print(f"OCR page {i+1}/{len(pages)}...")
        text = pytesseract.image_to_string(img, lang="ben")  # Bangla OCR
        text = clean_text(text)
        if not text:
            continue

        chunks.append(
            {
                "id": f"page_{i+1}",
                "page": i + 1,
                "text": text,
            }
        )

    out_path = Path(output_json_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(chunks, f, ensure_ascii=False, indent=2)

    print(f"Saved {len(chunks)} OCR chunks to {output_json_path}")


if __name__ == "__main__":
    PDF_PATH = "জ্বালানি নীতিমালা ২০২৫ (গেজেট).pdf"
    OUTPUT_JSON = "data/policy_chunks_ocr.json"
    extract_policy_pdf_ocr(PDF_PATH, OUTPUT_JSON)
