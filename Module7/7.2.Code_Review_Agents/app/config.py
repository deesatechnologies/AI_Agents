import os

from dotenv import load_dotenv


# Load all environment variables from .env file.
load_dotenv()


def get_openai_api_key() -> str:
    # Read OpenAI API key from .env.
    api_key = os.getenv("OPENAI_API_KEY")

    # Stop program if key is missing.
    if not api_key:
        raise ValueError("OPENAI_API_KEY is missing in .env file.")

    return api_key


def get_deepseek_api_key() -> str:
    # Read DeepSeek API key from .env.
    api_key = os.getenv("DEEPSEEK_API_KEY")

    # Stop program if key is missing.
    if not api_key:
        raise ValueError("DEEPSEEK_API_KEY is missing in .env file.")

    return api_key


def get_openai_model() -> str:
    # Default OpenAI model.
    return os.getenv("OPENAI_MODEL", "gpt-4o-mini")


def get_deepseek_model() -> str:
    # Default DeepSeek model.
    return os.getenv("DEEPSEEK_MODEL", "deepseek-chat")


def get_developer_model() -> str:
    # Model used by Developer Agent.
    return os.getenv("DEVELOPER_MODEL", get_openai_model())


def get_reviewer_model() -> str:
    # Model used by Code Reviewer Agent.
    return os.getenv("REVIEWER_MODEL", get_openai_model())


def get_security_model() -> str:
    # Model used by Security Reviewer Agent.
    return os.getenv("SECURITY_MODEL", get_deepseek_model())


def get_tester_model() -> str:
    # Model used by Testing Agent.
    return os.getenv("TESTER_MODEL", get_openai_model())