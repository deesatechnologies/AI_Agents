def build_generation_prompt(user_prompt: str) -> str:
    # Prompt for AI content generation.
    return f"""
You are a professional AI assistant.

User Request:
{user_prompt}

Generate a high-quality professional response.
"""


def build_evaluation_prompt(
    user_prompt: str,
    ai_output: str,
) -> str:
    # Prompt for AI output evaluation.
    return f"""
You are an AI evaluator.

Evaluate the following AI response.

User Prompt:
{user_prompt}

AI Output:
{ai_output}

Score the output from 1-10 for:

1. Relevance
2. Clarity
3. Completeness
4. Professionalism
5. Hallucination Risk
   (10 means very safe/no hallucination)

Return STRICT JSON only.

Example:
{{
  "relevance": 8,
  "clarity": 9,
  "completeness": 7,
  "professionalism": 9,
  "hallucination_risk": 8,
  "overall_score": 8,
  "feedback": "Well-structured response with clear explanation."
}}
"""