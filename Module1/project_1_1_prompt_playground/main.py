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
    Creates correct AI client based on provider.
    """

    # Read provider from .env file.
    provider = get_model_provider()

    # OpenAI provider setup.
    if provider == "openai":
        client = OpenAI(
            api_key=get_openai_api_key()
        )

        model = get_openai_model()

        return client, model, provider

    # DeepSeek provider setup.
    if provider == "deepseek":
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


def build_prompt(topic, prompt_style):
    """
    Builds different prompt styles.

    This demonstrates how prompts
    significantly affect AI outputs.
    """

    # Simple prompt style.
    if prompt_style == "Simple":
        return f"""
Explain:
{topic}
"""

    # Beginner-friendly teaching style.
    elif prompt_style == "Beginner Friendly":
        return f"""
Explain the following topic in very simple language.

Topic:
{topic}

Requirements:
- Use beginner-friendly language
- Use examples
- Avoid complex jargon
- Explain step-by-step
"""

    # Expert engineering style.
    elif prompt_style == "Expert Level":
        return f"""
Explain the following topic from an expert engineering perspective.

Topic:
{topic}

Requirements:
- Include architecture insights
- Include production considerations
- Include tradeoffs
- Include real-world examples
- Include scalability concerns
"""

    # Step-by-step structured explanation.
    elif prompt_style == "Step-by-Step":
        return f"""
Explain the following topic step-by-step.

Topic:
{topic}

Requirements:
1. Start with basics
2. Gradually increase complexity
3. Use practical examples
4. Explain WHY things work
5. Add real-world analogy
"""

    return f"Explain: {topic}"


def generate_response(topic, prompt_style):
    """
    Generates AI response using selected prompt style.
    """

    # Validate input.
    if not topic.strip():
        return "Please enter a topic."

    # Build selected prompt.
    prompt = build_prompt(
        topic=topic,
        prompt_style=prompt_style,
    )

    # Create AI client.
    client, model, provider = get_client_and_model()

    print(f"\nUsing provider: {provider}")
    print(f"Using model: {model}")

    # Send prompt to model.
    response = client.chat.completions.create(
        model=model,

        messages=[
            {
                "role": "system",

                # System prompt defines AI behavior.
                "content": (
                    "You are a highly skilled AI teacher."
                ),
            },
            {
                "role": "user",

                # User prompt contains actual instructions.
                "content": prompt,
            },
        ],
    )

    # Print token usage.
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

    # Return generated response.
    return response.choices[0].message.content


# -----------------------------
# Gradio UI
# -----------------------------

with gr.Blocks() as demo:

    gr.Markdown(
        """
# Prompt Playground

Experiment with different prompting styles
and compare AI outputs.
"""
    )

    topic_input = gr.Textbox(
        label="Enter Topic",

        placeholder=(
            "Example: What is an AI Agent?"
        ),

        lines=3,
    )

    prompt_style = gr.Dropdown(
        choices=[
            "Simple",
            "Beginner Friendly",
            "Expert Level",
            "Step-by-Step",
        ],

        label="Select Prompt Style",

        value="Simple",
    )

    generate_button = gr.Button(
        "Generate Response"
    )

    output = gr.Markdown(
        label="AI Response"
    )

    # When button clicked, run generate_response().
    generate_button.click(
        fn=generate_response,

        inputs=[
            topic_input,
            prompt_style,
        ],

        outputs=output,
    )


if __name__ == "__main__":
    demo.launch()