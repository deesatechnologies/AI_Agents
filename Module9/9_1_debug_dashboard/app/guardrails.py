BLOCKED_WORDS = [
    "password",
    "api key",
    "secret",
    "token",
]


def validate_user_input(user_input: str):
    # Reject empty input.
    if not user_input or not user_input.strip():
        return False, "Input cannot be empty."

    lower_input = user_input.lower()

    # Block sensitive requests.
    for word in BLOCKED_WORDS:
        if word in lower_input:
            return False, f"Blocked sensitive request: {word}"

    return True, "Input allowed."