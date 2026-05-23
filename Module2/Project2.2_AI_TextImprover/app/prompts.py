def build_text_improvement_prompt(
    input_text: str,
    tone: str,
):
    # Build prompt dynamically based on selected tone.
    return f"""
You are an expert writing assistant.

Your job is to improve the text below.

Original Text:
{input_text}

Improvement Goals:
- Fix grammar mistakes
- Improve clarity
- Improve readability
- Improve sentence structure
- Improve professionalism

Selected Tone:
{tone}

Rules:
- Preserve original meaning
- Do not add fake information
- Keep response clean and polished
- Return only improved text
"""