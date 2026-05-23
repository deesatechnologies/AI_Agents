def build_extraction_prompt(document_text: str):
    # Build extraction prompt for structured information extraction.
    return f"""
You are an expert AI information extraction system.

Analyze the following document text and extract important business information.

Document Text:
{document_text}

Return ONLY valid JSON.

Required JSON format:

{{
    "document_type": "",
    "customer_name": "",
    "company_name": "",
    "invoice_number": "",
    "date": "",
    "email": "",
    "phone": "",
    "important_entities": [],
    "summary": ""
}}

Rules:
- Return only valid JSON
- Do not include markdown
- Do not include explanations
- If information missing, use "unknown"
"""