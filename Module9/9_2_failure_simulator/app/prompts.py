def build_response_prompt(user_input: str) -> str:
    # Build prompt for normal AI response.
    return f"""
You are a helpful AI assistant.

User request:
{user_input}

Generate a clear, useful, and professional response.
"""