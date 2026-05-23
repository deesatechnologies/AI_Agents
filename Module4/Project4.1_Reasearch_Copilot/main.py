import os

import gradio as gr
from agents import Agent, Runner, set_default_openai_key

from app.config import get_openai_api_key, get_openai_model
from app.prompts import get_research_agent_instructions
from app.tools import web_search


# Set the OpenAI API key for the Agents SDK.
# The Agents SDK uses this key to call OpenAI models.
set_default_openai_key(get_openai_api_key())


def create_research_agent() -> Agent:
    # Create and return a Research Copilot agent.

    return Agent(
        # Agent name is useful for debugging and tracing.
        name="Research Copilot",

        # Model comes from .env through config.py.
        model=get_openai_model(),

        # Instructions define the agent's behavior.
        instructions=get_research_agent_instructions(),

        # Tools are functions the agent can use. Agent knows tools exists, what it does, and how to use it. LLM can decide whether to use the tool or not.
        tools=[
            web_search
        ]
    )

#The OpenAI Agents SDK supports async execution
async def run_research_copilot(topic: str) -> str:
    # This function is called by the Gradio UI.

    # Validate user input.
    if not topic or not topic.strip():
        return "Please enter a research topic."

    # Create the agent.
    research_agent = create_research_agent()

    # Build the user's request.
    user_prompt = f"""
Research this topic and produce a clear report:

{topic}
"""

    # Runner.run_sync executes the agent synchronously.
    # The SDK manages agent execution and tool usage internally.
    result = await Runner.run(
        research_agent,
        user_prompt,
    )

    # final_output contains the agent's final response.
    return result.final_output


with gr.Blocks() as demo:
    # Page title.
    gr.Markdown("# Research Copilot — OpenAI Agents SDK")

    # Page description.
    gr.Markdown(
        "Enter a topic. The agent can use a web search tool and generate a research report."
    )

    # Topic input box.
    topic_input = gr.Textbox(
        label="Research Topic",
        placeholder="Example: Future of AI agents in enterprise automation",
        lines=4,
    )

    # Button to run the agent.
    run_button = gr.Button("Run Research Copilot")

    # Output area.
    output = gr.Markdown(label="Research Report")

    # When button is clicked, run the agent.
    run_button.click(
        fn=run_research_copilot,
        inputs=topic_input,
        outputs=output,
    )


if __name__ == "__main__":
    # Launch local Gradio app.
    demo.launch()