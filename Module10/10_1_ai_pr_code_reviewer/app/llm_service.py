from openai import OpenAI

from app.config import (
    get_openai_api_key,
    get_openai_model,
)


def call_llm(
    system_prompt: str,
    user_prompt: str,
) -> str:
    # Create OpenAI client.
    client = OpenAI(
        api_key=get_openai_api_key()
    )

    # Call OpenAI chat completions API.
    response = client.chat.completions.create(
        model=get_openai_model(),

        temperature=0.2,

        messages=[
            {
                "role": "system",
                "content": system_prompt,
            },
            {
                "role": "user",
                "content": user_prompt,
            },
        ],
    )

    # Return generated text.
    return response.choices[0].message.content