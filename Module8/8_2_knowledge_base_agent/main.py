import json

import gradio as gr

from app.document_store import save_pdf_to_knowledge_base

from app.guardrails import (
    validate_user_question,
    validate_final_answer,
)

from app.llm_service import call_llm

from app.mcp_client import search_documents_with_mcp

from app.prompts import build_answer_prompt


def upload_pdf(pdf_file) -> str:
    # Validate file upload.
    if pdf_file is None:
        return "Please upload a PDF file."

    # Gradio gives uploaded file path.
    pdf_file_path = pdf_file.name

    # Extract PDF text and save chunks.
    chunk_count = save_pdf_to_knowledge_base(pdf_file_path)

    # Return success message.
    return f"PDF uploaded and indexed successfully. Created {chunk_count} chunks."


async def ask_knowledge_base(question: str) -> str:
    # Validate user question using guardrails.
    allowed, message = validate_user_question(question)

    # Block unsafe question.
    if not allowed:
        return f"Blocked: {message}"

    # Search documents using MCP tool.
    mcp_result = await search_documents_with_mcp(question)

    # Parse MCP result.
    try:
        parsed_result = json.loads(mcp_result)
    except Exception:
        return f"MCP result parsing failed:\n\n{mcp_result}"

    # Stop if MCP tool blocked the request.
    if parsed_result["status"] == "blocked":
        return f"Blocked by MCP guardrail: {parsed_result['reason']}"

    # Stop if no document chunks found.
    if parsed_result["status"] == "not_found":
        return "I could not find relevant information in the uploaded documents."

    # Combine retrieved chunks into context.
    context = ""

    for chunk in parsed_result["chunks"]:
        context += f"""
Source: {chunk["source"]}
Chunk ID: {chunk["chunk_id"]}
Content:
{chunk["content"]}

---
"""

    # Build answer prompt.
    answer_prompt = build_answer_prompt(
        question=question,
        context=context,
    )

    # System prompt for answer generation.
    system_prompt = (
        "You are a secure company knowledge base assistant. "
        "Answer only from provided document context."
    )

    # Call LLM to answer based on document context.
    answer = call_llm(
        system_prompt=system_prompt,
        user_prompt=answer_prompt,
    )

    # Validate final answer before showing user.
    final_allowed, final_message = validate_final_answer(answer)

    # Block unsafe final answer.
    if not final_allowed:
        return f"Final answer blocked by output guardrail: {final_message}"

    # Return transparent result for teaching.
    return f"""
# Knowledge Base Answer

## Question
{question}

## Retrieved Context
```json
{json.dumps(parsed_result, indent=2)}
Answer

{answer}
"""

# UI with Gradio
with gr.Blocks() as demo:

    # Title
    gr.Markdown("# Knowledge Base Agent — MCP + Guardrails")

    # Description
    gr.Markdown(
        "Upload a company PDF and ask questions. "
        "The assistant searches uploaded documents using an MCP tool."
    )

    # PDF upload component
    pdf_input = gr.File(
        label="Upload Company PDF",
        file_types=[".pdf"],
    )

    # Upload button
    upload_button = gr.Button("Upload and Index PDF")

    # Upload status display
    upload_status = gr.Markdown(label="Upload Status")

    # Question textbox
    question_input = gr.Textbox(
        label="Ask a Question",
        placeholder="Example: What is the refund policy?",
        lines=4,
    )

    # Ask button
    ask_button = gr.Button("Ask Knowledge Base")

    # Final output area
    output = gr.Markdown(label="Knowledge Base Output")

    # When upload button is clicked:
    # call upload_pdf()
    # pass pdf_input as input
    # display returned result in upload_status
    upload_button.click(
        fn=upload_pdf,
        inputs=pdf_input,
        outputs=upload_status,
    )

    # When ask button is clicked:
    # call ask_knowledge_base()
    # pass question_input as input
    # display returned result in output
    ask_button.click(
        fn=ask_knowledge_base,
        inputs=question_input,
        outputs=output,
    )

# =====================================================
# Main
# =====================================================

if __name__ == "__main__":
    demo.launch()
