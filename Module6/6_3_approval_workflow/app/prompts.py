def build_risk_analysis_prompt(request_text: str) -> str:
    # This prompt asks the AI to analyze the business request.
    return f"""
You are an enterprise risk analysis assistant.

Analyze the following business request.

Business Request:
{request_text}

Classify the risk level.

Return the result in this exact format:

Risk Level: <Low/Medium/High>
Reason: <short reason>
Recommended Action: <Auto Approve/Human Review>

Rules:
- Low risk means safe to auto-approve.
- Medium risk means human review is preferred.
- High risk means human review is required.
- Do not include extra explanation.
"""