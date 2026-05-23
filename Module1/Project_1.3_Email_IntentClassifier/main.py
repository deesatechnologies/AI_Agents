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

    # Read provider from .env file.
    provider = get_model_provider()

    # OpenAI configuration.
    if provider == "openai":

        # Create OpenAI client using API key.
        client = OpenAI(
            api_key=get_openai_api_key()
        )

        # Read model name from config.
        model = get_openai_model()

        return client, model, provider

    # DeepSeek configuration.
    if provider == "deepseek":

        # DeepSeek supports OpenAI-compatible APIs.
        client = OpenAI(
            api_key=get_deepseek_api_key(),
            base_url="https://api.deepseek.com",
        )

        model = get_deepseek_model()

        return client, model, provider

    # Stop execution if provider invalid.
    raise ValueError(
        "Unsupported MODEL_PROVIDER."
    )


def build_prompt(email_text):
    """
    Builds classification prompt.

    This prompt tells the AI:
    - what categories exist
    - what output structure to return
    """

    return f"""
Analyze the following email and classify it.

Email:
{email_text}

Possible categories:
- Support
- Sales
- Spam
- Billing
- Complaint
- Feedback
- Job Application

Also determine:
- priority
- short summary

Return ONLY valid JSON.

Required JSON format:

{{
    "category": "",
    "priority": "",
    "summary": ""
}}

Priority rules:
- High
- Medium
- Low

Rules:
- Return JSON only
- No explanations
- No markdown
"""


def classify_email(email_text):
    """
    Main business logic for email classification.
    """

    # Validate user input.
    if not email_text.strip():
        return "Please enter email content."

    # Build prompt for classification.
    prompt = build_prompt(email_text)

    # Create AI client.
    client, model, provider = get_client_and_model()

    print(f"\nUsing provider: {provider}")
    print(f"Using model: {model}")

    # Send classification request to AI model.
    response = client.chat.completions.create(
        model=model,

        messages=[
            {
                "role": "system",

                # System prompt defines AI behavior.
                "content": (
                    "You are an expert email classification system."
                ),
            },
            {
                "role": "user",

                # User prompt contains classification instructions.
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

    # Validate and pretty-format JSON.
    try:

        # Convert JSON string into Python dictionary.
        parsed_json = json.loads(ai_output)

        # Pretty-print JSON.
        formatted_json = json.dumps(
            parsed_json,
            indent=4,
        )

        return formatted_json

    except Exception as error:

        # Show raw output if parsing fails.
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
# AI Email Intent Classifier

Classify emails into business categories using AI.
"""
    )

    email_input = gr.Textbox(
        label="Paste Email Content",

        placeholder=(
            "Example: Hello team, I am unable to "
            "access my subscription dashboard after payment."
        ),

        lines=10,
    )

    classify_button = gr.Button(
        "Classify Email"
    )

    output = gr.Code(
        label="Classification Result",

        language="json",
    )

    # Run classification when button clicked.
    classify_button.click(
        fn=classify_email,

        inputs=email_input,

        outputs=output,
    )


if __name__ == "__main__":
    demo.launch()