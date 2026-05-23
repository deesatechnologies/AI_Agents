import gradio as gr

from app.llm_service import call_llm
from app.prompts import (
    build_text_improvement_prompt,
)


def improve_text(
    input_text: str,
    tone: str,
):
    """
    Main workflow function.

    This function:
    - validates input
    - builds prompt
    - calls AI
    - returns improved text
    """

    # Validate input text.
    if not input_text or not input_text.strip():
        return "Please enter some text."

    # Create prompt using selected tone.
    prompt = build_text_improvement_prompt(
        input_text=input_text,
        tone=tone,
    )

    # System prompt controls AI behavior globally.
    system_prompt = (
        "You are an expert AI writing assistant. "
        "You improve writing quality professionally."
    )

    # Call the AI model.
    improved_output = call_llm(
        system_prompt=system_prompt,
        user_prompt=prompt,
    )

    # Return final improved text.
    return improved_output


with gr.Blocks() as demo:

    # Project title.
    gr.Markdown("# AI Text Improver")

    # Project description.
    gr.Markdown(
        "Improve grammar, clarity, tone, and professionalism using AI."
    )

    # User input textbox.
    input_text = gr.Textbox(
        label="Enter Text",

        placeholder=(
            "Paste text that you want to improve..."
        ),

        lines=12,
    )

    # Dropdown for tone selection.
    tone_dropdown = gr.Dropdown(
        choices=[
            "Professional",
            "Friendly",
            "Technical",
            "Concise",
            "Confident",
        ],

        label="Select Tone",

        value="Professional",
    )

    # Button to trigger AI improvement.
    improve_button = gr.Button(
        "Improve Text"
    )

    # Output area.
    output = gr.Markdown(
        label="Improved Output"
    )

    # Run improve_text() when button clicked.
    improve_button.click(
        fn=improve_text,

        inputs=[
            input_text,
            tone_dropdown,
        ],

        outputs=output,
    )


if __name__ == "__main__":
    # Launch Gradio application locally.
    demo.launch()