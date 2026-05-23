import json

import gradio as gr
from openai import OpenAI

from app.config import (
    get_model_provider,
    get_openai_api_key,
    get_openai_model,
    get_deepseek_api_key,
    get_deepseek_model,
)


def get_client_and_model():
    """
    Creates AI client based on provider.
    """

    # Read provider from .env.
    provider = get_model_provider()

    # OpenAI setup.
    if provider == "openai":
        client = OpenAI(
            api_key=get_openai_api_key()
        )

        model = get_openai_model()

        return client, model, provider

    # DeepSeek setup.
    if provider == "deepseek":
        client = OpenAI(
            api_key=get_deepseek_api_key(),
            base_url="https://api.deepseek.com",
        )

        model = get_deepseek_model()

        return client, model, provider

    raise ValueError(
        "Unsupported MODEL_PROVIDER."
    )


def build_prompt(user_text):
    """
    Builds structured extraction prompt.
    """

    return f"""
Extract structured information from the following text.

Text:
{user_text}

Return ONLY valid JSON.

Required JSON structure:

{{
    "customer_name": "",
    "issue_type": "",
    "product": "",
    "priority": "",
    "summary": ""
}}

Rules:
- Return valid JSON only
- Do not include explanations
- Do not include markdown
- If value missing, use "unknown"
"""


def format_output(user_text):
    """
    Main business logic for structured extraction.
    """

    # Validate user input.
    if not user_text.strip():
        return "Please enter some text."

    # Build extraction prompt.
    prompt = build_prompt(user_text)

    # Create AI client.
    client, model, provider = get_client_and_model()

    print(f"\nUsing provider: {provider}")
    print(f"Using model: {model}")

    # Send prompt to AI model.
    response = client.chat.completions.create(
        model=model,

        messages=[
            {
                "role": "system",

                # System prompt defines AI behavior.
                "content": (
                    "You are an expert information extraction system."
                ),
            },
            {
                "role": "user",

                # User prompt contains extraction instructions.
                "content": prompt,
            },
        ],
    )

    # Extract AI response text.
    ai_output = response.choices[0].message.content

    print("\n=== TOKEN USAGE ===")

    print(
        "Prompt Tokens:",
        response.usage.prompt_tokens
    )

    print(
        "Completion Tokens:",
        response.usage.completion_tokens
    )

    print(
        "Total Tokens:",
        response.usage.total_tokens
    )

    # Try converting AI output into proper JSON.
    try:

        # Convert string JSON into Python dictionary.
        parsed_json = json.loads(ai_output)

        # Pretty-print JSON for better readability.
        formatted_json = json.dumps(
            parsed_json,
            indent=4,
        )

        return formatted_json

    # If JSON parsing fails, show raw output.
    except Exception as error:

        return (
            "JSON Parsing Failed.\n\n"
            f"Error: {error}\n\n"
            f"Raw Output:\n{ai_output}"
        )


# -----------------------------
# Gradio UI
# -----------------------------

with gr.Blocks() as demo:

    gr.Markdown(
        """
# AI Output Formatter

Convert unstructured AI output into structured JSON.
"""
    )

    user_input = gr.Textbox(
        label="Enter Unstructured Text",

        placeholder=(
            "Example: Customer John Smith reported "
            "payment issue while purchasing premium subscription."
        ),

        lines=8,
    )

    generate_button = gr.Button(
        "Generate Structured Output"
    )

    output = gr.Code(
        label="Structured JSON Output",

        language="json",
    )

    # Run format_output() when button clicked.
    generate_button.click(
        fn=format_output,

        inputs=user_input,

        outputs=output,
    )


if __name__ == "__main__":
    demo.launch()