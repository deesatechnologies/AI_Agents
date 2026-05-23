def build_analysis_prompt(user_question: str) -> str:
    # Prompt for workflow analysis step.
    return f"""
Analyze the following business question carefully.

Question:
{user_question}

Provide:
- intent
- possible business area
- important keywords
"""


def build_summary_prompt(user_question: str, analysis: str) -> str:
    # Prompt for final response generation.
    return f"""
User Question:
{user_question}

Analysis:
{analysis}

Generate a professional business response.
"""