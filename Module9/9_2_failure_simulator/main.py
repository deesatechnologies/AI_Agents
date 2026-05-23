import pandas as pd
import gradio as gr

from app.logger import (
    clear_logs,
    get_logs,
)

from app.workflow import run_failure_simulation


def run_simulator(
    user_input: str,
    failure_type: str,
):
    # Run failure simulation workflow.
    result = run_failure_simulation(
        user_input=user_input,
        failure_type=failure_type,
    )

    # Convert logs into dataframe.
    logs_df = pd.DataFrame(get_logs())

    # Return trace ID, final output, and logs.
    return (
        result["trace_id"],
        result["final_output"],
        logs_df,
    )


def clear_dashboard():
    # Clear logs.
    clear_logs()

    # Return empty UI values.
    return (
        "",
        "",
        pd.DataFrame(),
    )


with gr.Blocks() as demo:
    gr.Markdown("# Failure Simulator")

    gr.Markdown(
        "Inject failures into an AI workflow and observe how the system handles them."
    )

    user_input = gr.Textbox(
        label="User Input",
        placeholder="Example: Create a customer support response for delayed delivery.",
        lines=4,
    )

    failure_dropdown = gr.Dropdown(
        choices=[
            "No Failure",
            "Input Failure",
            "Tool Failure",
            "LLM Failure",
            "Output Validation Failure",
        ],
        label="Failure Type",
        value="No Failure",
    )

    run_button = gr.Button("Run Failure Simulation")

    clear_button = gr.Button("Clear Logs")

    trace_id_output = gr.Textbox(
        label="Trace ID",
    )

    final_output = gr.Markdown(
        label="Final Output",
    )

    logs_table = gr.Dataframe(
        label="Failure Logs",
    )

    run_button.click(
        fn=run_simulator,
        inputs=[
            user_input,
            failure_dropdown,
        ],
        outputs=[
            trace_id_output,
            final_output,
            logs_table,
        ],
    )

    clear_button.click(
        fn=clear_dashboard,
        outputs=[
            trace_id_output,
            final_output,
            logs_table,
        ],
    )


if __name__ == "__main__":
    demo.launch()