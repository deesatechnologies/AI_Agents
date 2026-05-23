import gradio as gr

from app.crew_setup import (
    create_software_engineering_crew
)


def run_software_team(user_requirement: str):
    """
    Main Gradio workflow function.
    """

    # Validate user input.
    if not user_requirement or not user_requirement.strip():
        return "Please enter a software requirement."

    # Create CrewAI software team.
    crew = create_software_engineering_crew(
        user_requirement=user_requirement
    )

    # Execute the crew workflow.crew.kickoff() starts execution of the CrewAI workflow, orchestrates all agents and tasks according to the configured process, and returns the final workflow output
    result = crew.kickoff()

    # Return final result.
    return str(result)


with gr.Blocks() as demo:
    # Project title.
    gr.Markdown("# AI Software Engineering Team — CrewAI")

    # Project description.
    gr.Markdown(
        "Multi-agent AI software engineering workflow using CrewAI."
    )

    # User requirement input.
    requirement_input = gr.Textbox(
        label="Software Requirement",

        placeholder=(
            "Example: Create a Python calculator application "
            "with add, subtract, multiply, and divide operations."
        ),

        lines=6,
    )

    # Run button.
    run_button = gr.Button(
        "Run AI Software Team"
    )

    # Output display.
    output = gr.Markdown(
        label="Software Engineering Output"
    )

    # Execute workflow.
    run_button.click(
        fn=run_software_team,

        inputs=requirement_input,

        outputs=output,
    )


if __name__ == "__main__":
    # Launch local Gradio application.
    demo.launch()