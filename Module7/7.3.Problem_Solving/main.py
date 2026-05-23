import gradio as gr

from app.autogen_setup import (
    create_problem_solving_group,
    get_agent_model_summary
)


def solve_problem(problem_text: str):
    # Validate user input.
    if not problem_text or not problem_text.strip():
        return "Please enter a problem to solve."

    # Create AutoGen problem-solving group.
    user_proxy, manager = create_problem_solving_group()

    # This prompt starts the collaborative reasoning conversation.
    problem_request = f"""
Solve the following problem collaboratively.

Problem:
{problem_text}

Workflow:
1. ProblemAnalystAgent should analyze and break down the problem.
2. SolutionStrategistAgent should propose a step-by-step solution.
3. CriticAgent should identify weaknesses, risks, and missing assumptions.
4. FinalAnswerAgent should create the final polished answer.

Important:
- Keep the discussion practical.
- Avoid unnecessary repetition.
- The final answer should be clear, structured, and actionable.
"""

    # Start AutoGen multi-agent conversation.
    user_proxy.initiate_chat(
        manager,
        message=problem_request
    )

    # Get all messages from the group chat.
    messages = manager.groupchat.messages

    # Start output with model configuration.
    final_output = get_agent_model_summary()

    # Add separator.
    final_output += "\n---\n\n# Collaborative Problem Solving Conversation\n\n"

    # Convert conversation messages into readable Markdown.
    for message in messages:
        # Skip messages without content.
        if "content" not in message:
            continue

        # Get agent name.
        speaker = message.get("name", "Unknown")

        # Get message content.
        content = message["content"]

        # Add speaker heading.
        final_output += f"## {speaker}\n\n"

        # Add message content.
        final_output += f"{content}\n\n"

    return final_output


with gr.Blocks() as demo:
    # Page title.
    gr.Markdown("# Problem Solving Agents — AutoGen")

    # Page description.
    gr.Markdown(
        "Multiple AI agents collaborate to solve complex problems step-by-step."
    )

    # Problem input area.
    problem_input = gr.Textbox(
        label="Problem",
        placeholder=(
            "Example: Our customer support team receives 500 tickets per day. "
            "How can we use AI to reduce response time without reducing quality?"
        ),
        lines=10
    )

    # Button to start solving.
    run_button = gr.Button("Solve Problem")

    # Output area.
    output = gr.Markdown(label="Problem Solving Output")

    # Connect button to Python function.
    run_button.click(
        fn=solve_problem,
        inputs=problem_input,
        outputs=output
    )


if __name__ == "__main__":
    # Launch local Gradio app.
    demo.launch()