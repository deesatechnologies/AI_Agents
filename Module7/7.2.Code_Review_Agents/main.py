import gradio as gr

from app.autogen_setup import (
    create_code_review_group,
    get_agent_model_summary,
)


def run_code_review(code_input: str):
    # Validate user input.
    if not code_input or not code_input.strip():
        return "Please paste Python code for review."

    # Create AutoGen agents and group chat manager.
    user_proxy, manager = create_code_review_group()

    # Prompt that starts the multi-agent conversation.
    review_request = f"""
Review the following Python code collaboratively.

Code:
{code_input}

Workflow:
1. DeveloperAgent explains the code.
2. CodeReviewerAgent reviews code quality.
3. SecurityReviewerAgent reviews security risks.
4. TestingAgent suggests tests and improvements.

Each agent should clearly identify its role before responding.
Keep the discussion practical and professional.
"""

    # Start the AutoGen conversation.
    user_proxy.initiate_chat(
        manager,
        message=review_request
    )

    # Get conversation messages after agents finish.
    messages = manager.groupchat.messages

    # Start final output with model configuration.
    final_output = get_agent_model_summary()

    final_output += "\n---\n\n# Collaborative Code Review\n\n"

    # Convert AutoGen messages into readable Markdown.
    for message in messages:
        # Skip empty/internal messages.
        if "content" not in message:
            continue

        # Get speaker/agent name.
        speaker = message.get("name", "Unknown")

        # Get message content.
        content = message["content"]

        # Add speaker and content to final output.
        final_output += f"## {speaker}\n\n"
        final_output += f"{content}\n\n"

    return final_output


with gr.Blocks() as demo:
    # Page title.
    gr.Markdown("# Collaborative Code Review Agents — AutoGen")

    # Page description.
    gr.Markdown(
        "Multiple AI agents review Python code collaboratively. "
        "Each agent can use a different model/provider."
    )

    # Code input area.
    code_input = gr.Textbox(
        label="Python Code",
        placeholder="Paste Python code here...",
        lines=20,
    )

    # Button.
    run_button = gr.Button("Run Collaborative Review")

    # Output area.
    output = gr.Markdown(label="Collaborative Review Output")

    # Connect button to function.
    run_button.click(
        fn=run_code_review,
        inputs=code_input,
        outputs=output,
    )


if __name__ == "__main__":
    demo.launch()