import os

from dotenv import load_dotenv


# Load variables from .env file during local development.
load_dotenv()


def get_openai_api_key() -> str:
    # Read OpenAI key from environment.
    api_key = os.getenv("OPENAI_API_KEY")

    # Stop if key is missing.
    if not api_key:
        raise ValueError("OPENAI_API_KEY is missing.")

    return api_key


def get_openai_model() -> str:
    # Read OpenAI model from environment.
    return os.getenv("OPENAI_MODEL", "gpt-4o-mini")


def get_github_token() -> str:
    # Read GitHub token from environment.
    token = os.getenv("GITHUB_TOKEN")

    # Stop if token is missing.
    if not token:
        raise ValueError("GITHUB_TOKEN is missing.")

    return token


def get_github_webhook_secret() -> str:
    # Secret used to verify webhook really came from GitHub.
    return os.getenv("GITHUB_WEBHOOK_SECRET", "")


def get_max_diff_chars() -> int:
    # Maximum amount of diff text sent to AI.
    return int(os.getenv("MAX_DIFF_CHARS", "12000"))