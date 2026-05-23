import gradio as gr

from app.crew_setup import (
    create_product_launch_crew,
)


def run_product_launch_team(
    product_idea: str,
):
    """
    Main Gradio workflow function.
    """

    # Validate user input.
    if not product_idea or not product_idea.strip():
        return "Please enter a product idea."

    # Create CrewAI product launch team.
    crew = create_product_launch_crew(
        product_idea=product_idea
    )

    # Execute the complete workflow.
    result = crew.kickoff()

    # Return final result.
    return str(result)


with gr.Blocks() as demo:
    # Project title.
    gr.Markdown("# AI Product Launch Team — CrewAI")

    # Project description.
    gr.Markdown(
        "Multi-agent AI business workflow for product launch automation."
    )

    # Product idea input.
    product_input = gr.Textbox(
        label="Product Idea",

        placeholder=(
            "Example: AI-powered fitness coaching mobile app"
        ),

        lines=6,
    )

    # Run workflow button.
    run_button = gr.Button(
        "Run Product Launch Team"
    )

    # Output display.
    output = gr.Markdown(
        label="Business Workflow Output"
    )

    # Execute workflow.
    run_button.click(
        fn=run_product_launch_team,

        inputs=product_input,

        outputs=output,
    )


if __name__ == "__main__":
    # Launch local Gradio app.
    demo.launch()