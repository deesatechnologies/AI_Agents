BLOCKED_TERMS = [
    "password",
    "api key",
    "secret",
    "token",
]


def validate_input(user_input: str):
    # Check if input is empty.
    if not user_input or not user_input.strip():
        return False, "Input cannot be empty."

    # Convert input to lowercase.
    lower_input = user_input.lower()

    # Block sensitive requests.
    for term in BLOCKED_TERMS:
        if term in lower_input:
            return False, f"Blocked unsafe term: {term}"

    # Input is safe.
    return True, "Input validation passed."


def validate_output(output: str):
    # Check if output is empty.
    if not output or not output.strip():
        return False, "Output is empty."

    # Block invalid simulated output.
    if "INVALID_OUTPUT" in output:
        return False, "Output validation failed because invalid marker was found."

    # Output is safe.
    return True, "Output validation passed."