def build_classification_prompt(customer_message: str) -> str:
    # This prompt asks the AI to classify the customer message.
    return f"""
You are an expert customer support ticket classifier.

Classify the following customer message.

Customer Message:
{customer_message}

Return the result in this exact format:

Category: <Billing/Login Issue/Technical Issue/Refund/Complaint/General Inquiry>
Priority: <Low/Medium/High/Critical>
Sentiment: <Calm/Confused/Frustrated/Angry>

Rules:
- Use only one category.
- Use only one priority.
- Use only one sentiment.
- Do not include extra explanation.
"""


def build_response_prompt(
    customer_message: str,
    category: str,
    priority: str,
    policy_guidance: str,
) -> str:
    # This prompt asks the AI to write a customer-friendly support response.
    return f"""
You are a professional customer support specialist.

Write a helpful response to the customer.

Customer Message:
{customer_message}

Ticket Category:
{category}

Priority:
{priority}

Company Policy Guidance:
{policy_guidance}

Requirements:
- Be polite and empathetic.
- Do not promise actions that are not allowed by policy.
- Ask for missing information if needed.
- Keep the response clear and professional.
"""


def build_escalation_prompt(
    customer_message: str,
    category: str,
    priority: str,
    draft_response: str,
) -> str:
    # This prompt asks the AI whether human escalation is needed.
    return f"""
You are a senior support operations manager.

Decide whether this support ticket should be escalated to a human.

Customer Message:
{customer_message}

Category:
{category}

Priority:
{priority}

Draft Response:
{draft_response}

Return only one word:
YES or NO

Escalate if:
- priority is High or Critical
- customer is angry
- issue involves billing mistake
- refund policy is unclear
- technical issue blocks business operations
"""