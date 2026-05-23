from app.config import get_max_diff_chars


# File extensions we allow AI to review in this beginner demo.
ALLOWED_EXTENSIONS = [
    ".py",
    ".js",
    ".ts",
    ".java",
    ".sql",
    ".md",
]


# Files we do not want to review or send to AI.
BLOCKED_FILE_PATTERNS = [
    ".env",
    "package-lock.json",
    "poetry.lock",
    "uv.lock",
    "secrets",
    "credentials",
    "private_key",
]


# Secret-like strings we do not want to send to AI.
SECRET_PATTERNS = [
    "api_key",
    "apikey",
    "secret",
    "token",
    "password",
    "private_key",
]


def is_allowed_file(filename: str) -> bool:
    # Convert filename to lowercase for safe comparison.
    lower_name = filename.lower()

    # Block sensitive files by pattern.
    for blocked in BLOCKED_FILE_PATTERNS:
        if blocked in lower_name:
            return False

    # Allow only selected code/document extensions.
    return any(lower_name.endswith(ext) for ext in ALLOWED_EXTENSIONS)


def sanitize_patch(patch: str) -> str:
    # Remove lines that may contain secrets before sending to AI.
    safe_lines = []

    # Process patch line by line.
    for line in patch.splitlines():
        lower_line = line.lower()

        # Skip lines containing sensitive patterns.
        if any(pattern in lower_line for pattern in SECRET_PATTERNS):
            safe_lines.append("[REDACTED SENSITIVE LINE]")
            continue

        safe_lines.append(line)

    # Return sanitized patch.
    return "\n".join(safe_lines)


def validate_combined_diff(diff_text: str):
    # Block empty diffs.
    if not diff_text or not diff_text.strip():
        return False, "No reviewable code diff found."

    # Block very large diffs in beginner demo.
    if len(diff_text) > get_max_diff_chars():
        return False, (
            "PR diff is too large for this demo. "
            "Please reduce PR size or increase MAX_DIFF_CHARS."
        )

    # Diff is allowed.
    return True, "Diff allowed."