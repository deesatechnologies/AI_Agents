def lookup_support_policy(category: str) -> str:
    # Normalize category for easier matching.
    normalized_category = category.lower().strip()

    # Policy for billing issues.
    if "billing" in normalized_category:
        return (
            "Billing policy: Ask for invoice ID, customer email, "
            "transaction date, and payment method. Escalate if customer "
            "claims incorrect charge or duplicate charge."
        )

    # Policy for login issues.
    if "login" in normalized_category:
        return (
            "Login policy: Ask the customer to reset password first. "
            "If password reset fails or account is locked, escalate to technical support."
        )

    # Policy for technical issues.
    if "technical" in normalized_category:
        return (
            "Technical policy: Ask for error message, browser/device details, "
            "steps to reproduce, and screenshot. Escalate business-blocking issues."
        )

    # Policy for refund issues.
    if "refund" in normalized_category:
        return (
            "Refund policy: Full refunds are allowed within 14 days of purchase "
            "if usage is below 20%. Requests outside this policy require human review."
        )

    # Policy for complaints.
    if "complaint" in normalized_category:
        return (
            "Complaint policy: Acknowledge the concern empathetically. "
            "Escalate angry customers, legal concerns, or repeated unresolved complaints."
        )

    # Default policy.
    return (
        "General support policy: Answer clearly, ask for missing details, "
        "and escalate if the issue cannot be resolved safely."
    )