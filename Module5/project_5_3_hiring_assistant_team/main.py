import gradio as gr

from app.crew_setup import create_hiring_assistant_crew


def run_hiring_assistant(
    resume_text: str,
    job_description: str,
):
    # Validate resume input.
    if not resume_text or not resume_text.strip():
        return "Please paste the candidate resume."

    # Validate job description input.
    if not job_description or not job_description.strip():
        return "Please paste the job description."

    # Create the CrewAI hiring assistant team.
    crew = create_hiring_assistant_crew(
        resume_text=resume_text,
        job_description=job_description,
    )

    # Start the complete multi-agent workflow.
    result = crew.kickoff()

    # Return the final CrewAI output to the UI.
    return str(result)


with gr.Blocks() as demo:
    # Application title.
    gr.Markdown("# Hiring Assistant Team — CrewAI")

    # Application description.
    gr.Markdown(
        "Screen resumes, analyze skill gaps, and generate interview questions using a multi-agent HR workflow."
    )

    # Resume input.
    resume_input = gr.Textbox(
        label="Candidate Resume",
        placeholder="Paste candidate resume here...",
        lines=15
    )

    # Job description input.
    job_description_input = gr.Textbox(
        label="Job Description",
        placeholder="Paste job description here...",
        lines=15
    )

    # Button to start the CrewAI workflow.
    run_button = gr.Button("Run Hiring Assistant Team")

    # Output area.
    output = gr.Markdown(label="Hiring Assistant Output")

    # Connect button click to the Python function.
    run_button.click(
        fn=run_hiring_assistant,
        inputs=[
            resume_input,
            job_description_input,
        ],
        outputs=output
    )


if __name__ == "__main__":
    # Launch the local Gradio app.
    demo.launch()