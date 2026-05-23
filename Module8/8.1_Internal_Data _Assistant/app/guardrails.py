import re


# SQL keywords that should never be allowed in this demo assistant.
BLOCKED_SQL_KEYWORDS = [
    "insert",
    "update",
    "delete",
    "drop",
    "alter",
    "truncate",
    "create",
    "replace",
    "merge",
    "grant",
    "revoke"
]


# Sensitive columns that should not be exposed in enterprise assistants.
BLOCKED_COLUMNS = [
    "email",
    "phone",
    "address",
    "username",
    "password",
    "api_key",
    "secret",
]


def validate_user_question(question: str):
    # Reject empty questions.
    if not question or not question.strip():
        return False, "Question cannot be empty."

    # Reject suspicious prompt-injection style requests.
    suspicious_phrases = [
        "ignore previous instructions",
        "bypass guardrails",
        "show secrets",
        "reveal api key",
        "drop table",
        "delete all"
    ]

    # Convert question to lowercase for easier matching.
    lower_question = question.lower()

    # Check for suspicious phrases.
    for phrase in suspicious_phrases:
        if phrase in lower_question:
            return False, "Request blocked by input guardrail."

    # If no issue found, allow question.
    return True, "Question allowed."


def validate_sql_query(sql_query: str):
    # Reject empty SQL.
    if not sql_query or not sql_query.strip():
        return False, "SQL query cannot be empty."

    # Normalize SQL for checks.
    normalized_sql = sql_query.lower().strip()

    # Only allow SELECT queries.
    if not normalized_sql.startswith("select"):
        return False, "Only SELECT queries are allowed."

    # Block multiple SQL statements using semicolon in middle.
    if ";" in normalized_sql.rstrip(";"):
        return False, "Multiple SQL statements are not allowed."

    # Block dangerous SQL keywords.
    for keyword in BLOCKED_SQL_KEYWORDS:
        pattern = rf"\b{keyword}\b"
        if re.search(pattern, normalized_sql):
            return False, f"Blocked SQL keyword detected: {keyword}"

    # Block sensitive columns.
    for column in BLOCKED_COLUMNS:
        pattern = rf"\b{column}\b"
        if re.search(pattern, normalized_sql):
            return False, f"Sensitive column access blocked: {column}"

    # Only allow querying the approved table.
    if "sales_orders" not in normalized_sql:
        return False, "Only sales_orders table is allowed in this demo."

    # If no issue found, allow SQL.
    return True, "SQL allowed."