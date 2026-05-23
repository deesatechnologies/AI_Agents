import json
from pathlib import Path

from pypdf import PdfReader


KNOWLEDGE_BASE_FILE = "knowledge_base.json"


def extract_text_from_pdf(pdf_file_path: str) -> str:
    # Read the uploaded PDF file.
    reader = PdfReader(pdf_file_path)

    # Store extracted text from all pages.
    full_text = ""

    # Loop through every page.
    for page in reader.pages:
        # Extract text from current page.
        page_text = page.extract_text()

        # Add page text if extraction was successful.
        if page_text:
            full_text += page_text + "\n"

    return full_text


def chunk_text(text: str, chunk_size: int = 1000) -> list:
    # Split large document text into smaller chunks.
    chunks = []

    # Move through text in chunk_size blocks.
    for start in range(0, len(text), chunk_size):
        chunk = text[start:start + chunk_size]

        # Avoid saving empty chunks.
        if chunk.strip():
            chunks.append(chunk.strip())

    return chunks


def save_pdf_to_knowledge_base(pdf_file_path: str) -> int:
    # Extract text from PDF.
    extracted_text = extract_text_from_pdf(pdf_file_path)

    # Split document into chunks.
    chunks = chunk_text(extracted_text)

    # Prepare records for storage.
    records = []

    # Store source file name.
    source_name = Path(pdf_file_path).name

    # Create one record per chunk.
    for index, chunk in enumerate(chunks):
        records.append(
            {
                "source": source_name,
                "chunk_id": index + 1,
                "content": chunk,
            }
        )

    # Save chunks into JSON file.
    with open(KNOWLEDGE_BASE_FILE, "w", encoding="utf-8") as file:
        json.dump(records, file, indent=2)

    # Return number of chunks created.
    return len(records)


def load_knowledge_base() -> list:
    # If knowledge base file does not exist, return empty list.
    if not Path(KNOWLEDGE_BASE_FILE).exists():
        return []

    # Read saved document chunks.
    with open(KNOWLEDGE_BASE_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def search_knowledge_base(query: str, top_k: int = 3) -> list:
    # Load stored document chunks.
    records = load_knowledge_base()

    # Convert user query into lowercase words.
    query_words = query.lower().split()

    scored_chunks = []

    # Score each chunk based on keyword overlap.
    for record in records:
        content = record["content"].lower()

        # Count how many query words appear in chunk.
        score = sum(1 for word in query_words if word in content)

        # Keep chunks with at least one matching word.
        if score > 0:
            scored_chunks.append((score, record))

    # Sort chunks by highest score first.
    scored_chunks.sort(reverse=True, key=lambda item: item[0])

    # Return top matching chunks.
    return [record for score, record in scored_chunks[:top_k]]