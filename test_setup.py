import os

from dotenv import load_dotenv
from openai import OpenAI


# Load variables from the .env file.
load_dotenv()


def get_llm_client():
   

    provider = os.getenv("MODEL_PROVIDER", "openai").lower()

    if provider == "openai":
        api_key = os.getenv("OPENAI_API_KEY")
        model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

        if not api_key:
            raise ValueError("OPENAI_API_KEY is missing in .env file.")

        client = OpenAI(api_key=api_key)

        return client, model, provider

    if provider == "deepseek":
        api_key = os.getenv("DEEPSEEK_API_KEY")
        model = os.getenv("DEEPSEEK_MODEL", "deepseek-chat")

        if not api_key:
            raise ValueError("DEEPSEEK_API_KEY is missing in .env file.")

        # DeepSeek supports OpenAI-compatible API format.
        # That is why we can use the OpenAI client and only change base_url.
        client = OpenAI(
            api_key=api_key,
            base_url="https://api.deepseek.com",
        )

        return client, model, provider

    raise ValueError(
        "Unsupported MODEL_PROVIDER. Use 'openai' or 'deepseek'."
    )


def main():
    client, model, provider = get_llm_client()

    print("=== AI Provider Test ===")
    print(f"Provider: {provider}")
    print(f"Model: {model}")
    print("========================\n")

    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": "You are a helpful AI assistant.",
            },
            {
                "role": "user",
                "content": "Explain what an LLM is in one simple sentence.",
            },
        ],
    )

    print(response.choices[0].message.content)


if __name__ == "__main__":
    main()