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

    if provider == "openai":
        client = OpenAI(api_key=get_openai_api_key())
        model = get_openai_model()
        return client, model, provider

    if provider == "deepseek":
        client = OpenAI(
            api_key=get_deepseek_api_key(),
            base_url="https://api.deepseek.com",
        )
        model = get_deepseek_model()
        return client, model, provider

    raise ValueError("Unsupported MODEL_PROVIDER. Use 'openai' or 'deepseek'.")


def call_llm(prompt: str) -> str:
    """
    Sends a prompt to the selected AI model and returns the response text.
    """

    client, model, provider = get_client_and_model()

    print(f"Using provider: {provider}")
    print(f"Using model: {model}")

    # Send chat messages to the AI model and generate an AI response
    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": "You are a helpful AI research assistant.",
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
    )

    print("\n=== Token Usage ===")
    print("Prompt tokens:", response.usage.prompt_tokens)
    print("Completion tokens:", response.usage.completion_tokens)
    print("Total tokens:", response.usage.total_tokens)

    return response.choices[0].message.content