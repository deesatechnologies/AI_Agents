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


    provider = get_model_provider()

    # OpenAI configuration
    if provider == "openai":
        client = OpenAI(
            api_key=get_openai_api_key()
        )

        model = get_openai_model()

        return client, model, provider

    # DeepSeek configuration
    if provider == "deepseek":
        client = OpenAI(
            api_key=get_deepseek_api_key(),
            base_url="https://api.deepseek.com",
        )

        model = get_deepseek_model()

        return client, model, provider

    raise ValueError(
        "Unsupported MODEL_PROVIDER. "
        "Use 'openai' or 'deepseek'."
    )


#Build the prompt for the AI model
def build_email_prompt(
    email_type: str,
    tone: str,
    purpose: str,
    additional_context: str,
) -> str:
   

    return f"""
You are an expert professional email writer.

Generate a high-quality email using the following information.

Email Type:
{email_type}

Tone:
{tone}

Purpose:
{purpose}

Additional Context:
{additional_context}

Instructions:
1. Generate a strong subject line.
2. Write a professional email body.
3. Keep formatting clean and readable.
4. Match the requested tone.
5. Avoid robotic wording.
6. Make the email practical and realistic.

Return output using this structure:

Subject:
<subject line>

Email:
<email body>
"""


def generate_email(
    email_type: str,
    tone: str,
    purpose: str,
    additional_context: str,
) -> str:
    """
    Main business logic for email generation.
    """

    # Basic validation
    if not purpose.strip():
        return "Please enter the purpose of the email."

    # Build prompt
    prompt = build_email_prompt(
        email_type=email_type,
        tone=tone,
        purpose=purpose,
        additional_context=additional_context,
    )

    # Get correct AI provider client
    client, model, provider = get_client_and_model()

    print(f"\nUsing provider: {provider}")
    print(f"Using model: {model}")

    # Send request to AI model
    response = client.chat.completions.create(
        model=model,

        messages=[
            {
                "role": "system",

                # System prompt defines AI behavior.
                # It tells the model HOW it should behave.
                "content": (
                    "You are an expert professional email writer."
                ),
            },
            {
                "role": "user",

                # User prompt contains actual task instructions.
                "content": prompt,
            },
        ],
    )

    # Print token usage for learning purposes.
    # This helps students understand API cost.
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

    # Return AI-generated email
    return response.choices[0].message.content


# -----------------------------
# Gradio UI
# -----------------------------

demo = gr.Interface(
    fn=generate_email,

    inputs=[
        gr.Dropdown(
            choices=[
                "Professional",
                "Sales",
                "Support",
                "Interview",
                "Follow-Up",
                "Meeting Request",
            ],

            label="Email Type",

            value="Professional",
        ),

        gr.Dropdown(
            choices=[
                "Professional",
                "Friendly",
                "Formal",
                "Confident",
                "Persuasive",
            ],

            label="Tone",

            value="Professional",
        ),

        gr.Textbox(
            label="Purpose of the Email",

            placeholder=(
                "Example: Request feedback "
                "after technical interview."
            ),

            lines=4,
        ),

        gr.Textbox(
            label="Additional Context",

            placeholder=(
                "Example: Mention that "
                "I enjoyed learning about the team."
            ),

            lines=4,
        ),
    ],

    outputs=gr.Markdown(
        label="Generated Email"
    ),

    title="AI Email Generator",

    description=(
        "Generate professional emails using AI."
    ),
)


if __name__ == "__main__":
    demo.launch()