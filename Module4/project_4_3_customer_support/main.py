import gradio as gr

from agents import Agent, Runner, set_default_openai_key

from app.config import (
    get_openai_api_key,
    get_openai_model,
)

from app.prompts import (
    get_support_agent_instructions,
)

from app.tools import (
    lookup_support_policy,
)


# Set OpenAI API key for the Agents SDK.
# The SDK uses this key to call OpenAI models.
set_default_openai_key(get_openai_api_key())


def create_customer_support_agent() -> Agent:
    # Create the customer support agent.

    return Agent(
        # Agent name helps identify this agent during debugging/tracing.
        name="Customer Support Agent",

        # Model name comes from .env through config.py.
        model=get_openai_model(),

        # Instructions define the behavior and responsibilities of the agent.
        instructions=get_support_agent_instructions(),

        # Tools available to this agent.
        tools=[
            lookup_support_policy
        ]
    )


async def handle_customer_message(customer_message: str) -> str:
    # This function is called by the Gradio UI.

    # Validate user input.
    if not customer_message or not customer_message.strip():
        return "Please paste a customer message."

    # Create the support agent.
    support_agent = create_customer_support_agent()

    # Build the task for the agent.
    user_prompt = f"""
Analyze this customer support message and generate a support response.

Customer Message:
{customer_message}
"""

    # Run the agent asynchronously.
    # In Gradio, async Runner.run avoids event loop errors.
    result = await Runner.run(
        support_agent,
        user_prompt,
    )

    # Return the final response from the agent.
    return result.final_output


with gr.Blocks() as demo:
    # Page title.
    gr.Markdown("# Customer Support Agent — OpenAI Agents SDK")

    # Page description.
    gr.Markdown(
        "Paste a customer message. The AI agent will classify the issue, "
        "check support policy, draft a response, and recommend escalation."
    )

    # Customer message input box.
    customer_input = gr.Textbox(
        label="Customer Message",
        placeholder=(
            "Example: I was charged twice this month and I need a refund immediately."
        ),
        lines=10,
    )

    # Button to run the support agent.
    run_button = gr.Button("Analyze Support Request")

    # Output area.
    output = gr.Markdown(label="Support Agent Output")

    # When button is clicked, call the async agent function.
    run_button.click(
        fn=handle_customer_message,
        inputs=customer_input,
        outputs=output,
    )


if __name__ == "__main__":
    # Launch local Gradio application.
    demo.launch()