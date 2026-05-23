import gradio as gr

from app.llm_service import call_llm

from app.prompts import (
    build_summary_prompt,
)

from app.tools import (
    web_search,
)


def run_web_search_agent(user_query: str):
    """
    Main agent workflow.

    Workflow:
    User Query
    ↓
    Web Search Tool
    ↓
    AI Summarization
    ↓
    Final Response
    """

    # Validate user input.
    if not user_query or not user_query.strip():
        return "Please enter a search query."

    # Step 1 — Run web search tool.
    search_results = web_search(
        query=user_query,
        max_results=5,
    )

    # Step 2 — Build summarization prompt.
    prompt = build_summary_prompt(
        user_query=user_query,
        search_results=search_results,
    )

    # System prompt defines AI behavior.
    system_prompt = (
        "You are an intelligent AI web research agent."
    )

    # Step 3 — Generate final summarized response.
    final_response = call_llm(
        system_prompt=system_prompt,
        user_prompt=prompt,
    )

    # Return both search results and final summary.
    return f"""
# Web Search Results

{search_results}

---

# AI Summary

{final_response}
"""


with gr.Blocks() as demo:

    # Project title.
    gr.Markdown("# AI Web Search Agent")

    # Project description.
    gr.Markdown(
        "Search the web and generate AI-powered summaries."
    )

    # User query input.
    query_input = gr.Textbox(
        label="Enter Search Topic",

        placeholder=(
            "Example: Latest trends in AI Agents"
        ),

        lines=3,
    )

    # Search button.
    search_button = gr.Button(
        "Run Web Search Agent"
    )

    # Output display.
    output = gr.Markdown(
        label="Agent Response"
    )

    # Run workflow when button clicked.
    search_button.click(
        fn=run_web_search_agent,

        inputs=query_input,

        outputs=output,
    )


if __name__ == "__main__":
    # Launch local Gradio application.
    demo.launch()