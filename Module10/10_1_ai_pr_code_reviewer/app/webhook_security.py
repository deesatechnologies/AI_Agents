import hmac
import hashlib


def verify_github_signature(
    payload_body: bytes,
    signature_header: str,
    webhook_secret: str,
) -> bool:
    # If no secret configured, skip verification for local beginner testing.
    # For production, always configure webhook secret.
    if not webhook_secret:
        return True

    # GitHub sends signature like: sha256=<hash>
    if not signature_header:
        return False

    # Create expected HMAC signature using webhook secret.
    expected_signature = "sha256=" + hmac.new(
        webhook_secret.encode("utf-8"),
        payload_body,
        hashlib.sha256,
    ).hexdigest()

    # Securely compare expected signature with received signature.
    return hmac.compare_digest(
        expected_signature,
        signature_header,
    )