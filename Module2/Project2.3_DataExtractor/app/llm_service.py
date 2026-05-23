from openai import OpenAI

from app.config import (
    get_model_provider,
    get_openai_api_key,
    get_openai_model,
    get_deepseek_api_key,
    get_deepseek_model,
)


def get_client_and_model():
    # Read the provider name from the .env file.
    provider = get_model_provider()

    # If the provider is OpenAI, create an OpenAI client.
    if provider == "openai":
        client = OpenAI(api_key=get_openai_api_key())
        model = get_openai_model()
        return client, model, provider

    # If the provider is DeepSeek, create a DeepSeek client.
    # DeepSeek supports OpenAI-compatible API format.
    if provider == "deepseek":
        client = OpenAI(
            api_key=get_deepseek_api_key(),
            base_url="https://api.deepseek.com",
        )
        model = get_deepseek_model()
        return client, model, provider

    # If the provider is neither openai nor deepseek, stop the program.
    raise ValueError("Unsupported MODEL_PROVIDER. Use 'openai' or 'deepseek'.")


def call_llm(system_prompt: str, user_prompt: str) -> str:
    # Get the correct client, model, and provider.
    client, model, provider = get_client_and_model()

    # Print provider details so students can see which model is being used.
    print(f"\nUsing provider: {provider}")
    print(f"Using model: {model}")

    # Send request to the selected LLM.
    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                # System prompt defines the AI's role and behavior.
                "role": "system",
                "content": system_prompt,
            },
            {
                # User prompt contains the actual task.
                "role": "user",
                "content": user_prompt,
            },
        ],
    )

    # Print token usage so students understand API usage and cost.
    print("\n=== TOKEN USAGE ===")
    print("Prompt Tokens:", response.usage.prompt_tokens)
    print("Completion Tokens:", response.usage.completion_tokens)
    print("Total Tokens:", response.usage.total_tokens)

    # Return only the generated text.
    return response.choices[0].message.content