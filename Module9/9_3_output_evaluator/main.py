import json
import pandas as pd
import gradio as gr

from app.logger import (
    clear_logs,
    get_logs,
)

from app.workflow import run_output_evaluation


def evaluate_output(user_prompt: str):
    # Run evaluation workflow.
    result = run_output_evaluation(user_prompt)

    # Convert logs into dataframe.
    logs_df = pd.DataFrame(get_logs())

    # Return all dashboard outputs.
    return (
        result["ai_output"],
        json.dumps(
            result["evaluation"],
            indent=2,
        ),
        logs_df,
    )


def clear_dashboard():
    # Clear evaluation logs.
    clear_logs()

    # Reset dashboard.
    return (
        "",
        "",
        pd.DataFrame(),
    )


with gr.Blocks() as demo:
    gr.Markdown("# AI Output Evaluator")

    gr.Markdown(
        "Generate AI responses and automatically evaluate their quality."
    )

    user_prompt = gr.Textbox(
        label="User Prompt",
        placeholder="Example: Explain benefits of cloud computing.",
        lines=4,
    )

    evaluate_button = gr.Button("Generate + Evaluate")

    clear_button = gr.Button("Clear Dashboard")

    ai_output = gr.Markdown(
        label="AI Output",
    )

#Create a code-display box in the UI using gr.Code
    evaluation_output = gr.Code(
        label="Evaluation Scores",
        language="json",
    )

    logs_table = gr.Dataframe(
        label="Evaluation Logs",
    )

    evaluate_button.click(
        fn=evaluate_output,
        inputs=user_prompt,
        outputs=[
            ai_output,
            evaluation_output,
            logs_table,
        ],
    )

    clear_button.click(
        fn=clear_dashboard,
        outputs=[
            ai_output,
            evaluation_output,
            logs_table,
        ],
    )


if __name__ == "__main__":
    demo.launch()