import os
import json
from pathlib import Path

from pypdf import PdfReader


def clean_text(text: str) -> str:
    """
    Basic cleanup:
    - strip leading/trailing spaces
    - collapse multiple whitespaces/newlines into single spaces
    """
    if not text:
        return ""
    # Replace newlines and tabs with spaces
    text = text.replace("\n", " ").replace("\t", " ")
    # Collapse multiple spaces
    while "  " in text:
        text = text.replace("  ", " ")
    return text.strip()


def extract_policy_pdf(
    pdf_path: str,
    output_json_path: str,
):
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"PDF not found at: {pdf_path}")

    reader = PdfReader(pdf_path)
    chunks = []

    for page_idx, page in enumerate(reader.pages):
        raw_text = page.extract_text()
        text = clean_text(raw_text)

        # some pages might be empty or only headers
        if not text:
            continue

        chunk = {
            "id": f"page_{page_idx+1}",
            "page": page_idx + 1,  # human-readable (1-based)
            "text": text,
        }
        chunks.append(chunk)

    # ensure output directory exists
    out_path = Path(output_json_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(chunks, f, ensure_ascii=False, indent=2)

    print(f"Saved {len(chunks)} chunks to {output_json_path}")


if __name__ == "__main__":
    PDF_PATH = "জ্বালানি নীতিমালা ২০২৫ (গেজেট).pdf"
    OUTPUT_JSON = "data/policy_chunks.json"

    extract_policy_pdf(PDF_PATH, OUTPUT_JSON)
