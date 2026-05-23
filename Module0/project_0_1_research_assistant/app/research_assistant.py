from app.llm_client import call_llm
from app.prompts import build_research_prompt


def generate_research_summary(topic: str) -> str:
    """
    Main business logic for the research assistant.

    Step 1: Accept topic from user.
    Step 2: Build a strong prompt.
    Step 3: Send prompt to LLM.
    Step 4: Return model response.
    """

    prompt = build_research_prompt(topic)

    result = call_llm(prompt)

    return result