from agents import function_tool


@function_tool
def lookup_support_policy(issue_type: str) -> str:
    # This function becomes a tool available to the support agent.
    # The agent can call this tool to retrieve company support policy guidance.

    # Normalize the issue type so matching becomes easier.
    issue = issue_type.lower().strip()

    # Simulated company support policies.
    # In real systems, this could come from a database, API, or knowledge base.
    policies = {
        "refund": (
            "Refund policy: Customers are eligible for a full refund within "
            "14 days of purchase if they have used less than 20% of the service. "
            "Refund requests outside this window require human review."
        ),
        "billing": (
            "Billing policy: For duplicate charges, failed payments, or invoice issues, "
            "collect the customer email, invoice ID, and transaction date. "
            "Billing issues should be escalated if money was charged incorrectly."
        ),
        "login": (
            "Login policy: Ask the customer to reset their password first. "
            "If password reset fails or account is locked, escalate to technical support."
        ),
        "technical": (
            "Technical issue policy: Ask for error message, browser/device details, "
            "steps to reproduce, and screenshot if available. Critical outages require escalation."
        ),
        "cancellation": (
            "Cancellation policy: Customers can cancel anytime from account settings. "
            "If they request immediate cancellation and cannot access account settings, escalate."
        ),
        "upgrade": (
            "Upgrade policy: Customers can upgrade plans from billing settings. "
            "Enterprise upgrade requests should be routed to the sales team."
        ),
        "complaint": (
            "Complaint policy: Acknowledge the issue empathetically. "
            "High-frustration complaints or legal/compliance concerns require human escalation."
        ),
        "general": (
            "General inquiry policy: Answer the question clearly. "
            "If account-specific action is needed, ask for customer details and escalate."
        ),
    }

    # Match issue type in the issue to known policy.
    if "refund" in issue:
        return policies["refund"]

    if "billing" in issue or "payment" in issue or "charge" in issue:
        return policies["billing"]

    if "login" in issue or "password" in issue or "account access" in issue:
        return policies["login"]

    if "technical" in issue or "bug" in issue or "error" in issue:
        return policies["technical"]

    if "cancel" in issue:
        return policies["cancellation"]

    if "upgrade" in issue:
        return policies["upgrade"]

    if "complaint" in issue or "angry" in issue or "frustrated" in issue:
        return policies["complaint"]

    # Default fallback policy.
    return policies["general"]