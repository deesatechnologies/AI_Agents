SENSITIVE_TERMS = [
    "password",
    "api key",
    "secret",
    "token",
    "private key",
    "credit card",
    "ssn",
]


def validate_user_question(question: str):
    # Block empty questions.
    if not question or not question.strip():
        return False, "Question cannot be empty."

    # Convert question to lowercase for easier checks.
    lower_question = question.lower()

    # Block prompt injection attempts.
    blocked_phrases = [
        "ignore previous instructions",
        "bypass guardrails",
        "reveal secrets",
        "show passwords",
        "show api keys",
        "system prompt",
    ]

    # Check for unsafe phrases.
    for phrase in blocked_phrases:
        if phrase in lower_question:
            return False, "Question blocked by input guardrail."

    # Block direct sensitive-data requests.
    for term in SENSITIVE_TERMS:
        if term in lower_question:
            return False, f"Sensitive information request blocked: {term}"

    return True, "Question allowed."


def sanitize_retrieved_text(text: str) -> str:
    # Remove lines that contain sensitive terms.
    safe_lines = []

    # Process text line by line.
    for line in text.splitlines():
        lower_line = line.lower()

        # Skip sensitive lines.
        if any(term in lower_line for term in SENSITIVE_TERMS):
            continue

        safe_lines.append(line)

    # Return cleaned text.
    return "\n".join(safe_lines)


def validate_final_answer(answer: str):
    # Convert answer to lowercase.
    lower_answer = answer.lower()

    # Block final answer if sensitive terms appear.
    for term in SENSITIVE_TERMS:
        if term in lower_answer:
            return False, f"Final answer blocked because it may expose: {term}"

    return True, "Answer allowed."