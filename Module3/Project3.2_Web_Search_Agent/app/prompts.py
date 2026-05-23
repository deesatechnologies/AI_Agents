def build_summary_prompt(
    user_query: str,
    search_results: str,
):
    # Build summarization prompt using search results.
    return f"""
You are an expert AI research assistant.

User Query:
{user_query}

Search Results:
{search_results}

Your task:
- Summarize the information clearly
- Combine findings intelligently
- Remove duplicates
- Explain in beginner-friendly language
- Use bullet points where useful

Return a clean final answer.
"""