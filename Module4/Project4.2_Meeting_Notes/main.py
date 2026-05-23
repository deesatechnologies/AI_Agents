import gradio as gr

from agents import Agent, Runner, set_default_openai_key

from app.config import (
    get_openai_api_key,
    get_openai_model,
)

from app.prompts import (
    get_meeting_agent_instructions,
)

from app.tools import (
    clean_meeting_notes,
)


# Set OpenAI API key for the Agents SDK.
# The Agents SDK uses this key to call OpenAI models.
set_default_openai_key(get_openai_api_key())


def create_meeting_agent() -> Agent:
    # Create an OpenAI Agents SDK agent for meeting analysis.

    return Agent(
        # Agent name helps identify this agent during debugging/tracing.
        name="Meeting Notes Assistant",

        # Model name comes from .env through config.py.
        model=get_openai_model(),

        # Instructions define agent behavior.
        instructions=get_meeting_agent_instructions(),

        # Tools available to this agent.
        tools=[
            clean_meeting_notes
        ]
    )


async def process_meeting_notes(meeting_notes: str) -> str:
    # This function is called by the Gradio UI.

    # Validate user input before calling the agent.
    if not meeting_notes or not meeting_notes.strip():
        return "Please paste meeting notes."

    # Create the meeting agent.
    meeting_agent = create_meeting_agent()

    # Build the user request for the agent.
    user_prompt = f"""
Convert the following meeting notes into action items, decisions, and risks.

Meeting Notes:
{meeting_notes}
"""

    # Runner.run is async.
    # This is preferred inside Gradio because Gradio runs async internally.
    result = await Runner.run(
        meeting_agent,
        user_prompt,
    )

    # Return the agent's final response.
    return result.final_output


with gr.Blocks() as demo:
    # Page title.
    gr.Markdown("# Meeting Notes → Action Items — OpenAI Agents SDK")

    # Page description.
    gr.Markdown(
        "Paste meeting notes and let the AI agent extract summaries, tasks, owners, deadlines, decisions, and blockers."
    )

    # Meeting notes input.
    notes_input = gr.Textbox(
        label="Meeting Notes",
        placeholder=(
            "Example: John will prepare the sales report by Friday. "
            "Sarah will coordinate with design team. "
            "Backend deployment is delayed due to infrastructure issues."
        ),
        lines=15,
    )

    # Button to run the agent.
    process_button = gr.Button("Generate Action Items")

    # Output area.
    output = gr.Markdown(label="Meeting Analysis")

    # When button is clicked, call the async agent function.
    process_button.click(
        fn=process_meeting_notes,
        inputs=notes_input,
        outputs=output,
    )


if __name__ == "__main__":
    # Launch local Gradio application.
    demo.launch()