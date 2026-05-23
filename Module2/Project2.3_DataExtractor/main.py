import json

import gradio as gr
from pypdf import PdfReader

from app.llm_service import call_llm
from app.prompts import (
    build_extraction_prompt,
)


def extract_text_from_pdf(pdf_file):
    """
    Extract text from uploaded PDF file.

    PDFs are binary files.
    AI models cannot directly read them from our machine.

    So we first convert PDF into plain text.
    """

    # Create PDF reader object.
    reader = PdfReader(pdf_file)

    # Store all extracted text.
    extracted_text = ""

    # Loop through all pages in the PDF.
    for page in reader.pages:

        # Extract text from current page.
        page_text = page.extract_text()

        # Add page text into final document text.
        extracted_text += page_text + "\n"

    return extracted_text


def extract_data(
    raw_text,
    pdf_file,
):
    """
    Main workflow function.

    This function:
    - accepts text or PDF
    - extracts raw text
    - sends text to AI
    - returns structured JSON
    """

    # If user uploads PDF, extract text from it.
    if pdf_file is not None:

        try:
            document_text = extract_text_from_pdf(
                pdf_file
            )

        except Exception as error:
            return f"PDF Extraction Failed: {error}"

    # Otherwise use manually pasted text.
    elif raw_text and raw_text.strip():

        document_text = raw_text

    # If both inputs empty, stop execution.
    else:
        return "Please provide text or upload PDF."

    # Build extraction prompt.
    prompt = build_extraction_prompt(
        document_text
    )

    # System prompt controls AI behavior.
    system_prompt = (
        "You are an expert AI document extraction assistant."
    )

    # Send extraction request to AI.
    ai_output = call_llm(
        system_prompt=system_prompt,
        user_prompt=prompt,
    )

    # Try validating JSON response.
    try:

        # Convert JSON string into Python dictionary.
        parsed_json = json.loads(ai_output)

        # Pretty-format JSON output.
        formatted_json = json.dumps(
            parsed_json,
            indent=4,
        )

        return formatted_json

    except Exception as error:

        return (
            "JSON Parsing Failed.\n\n"
            f"Error: {error}\n\n"
            f"Raw Output:\n{ai_output}"
        )


with gr.Blocks() as demo:

    # Project title.
    gr.Markdown("# AI Data Extractor")

    # Project description.
    gr.Markdown(
        "Upload PDF or paste text to extract structured business information using AI."
    )

    # Text input option.
    raw_text_input = gr.Textbox(
        label="Paste Raw Text",

        placeholder=(
            "Paste invoice, contract, email, or any business document text..."
        ),

        lines=12,
    )

    # PDF upload option.
    pdf_input = gr.File(
        label="Upload PDF File",
        file_types=[".pdf"],
    )

    # Extraction button.
    extract_button = gr.Button(
        "Extract Structured Data"
    )

    # Output display.
    output = gr.Code(
        label="Structured JSON Output",
        language="json",
    )

    # Run extraction workflow.
    extract_button.click(
        fn=extract_data,

        inputs=[
            raw_text_input,
            pdf_input,
        ],

        outputs=output,
    )


if __name__ == "__main__":
    # Launch Gradio app locally.
    demo.launch()