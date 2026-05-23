import pandas as pd
import gradio as gr

from app.logger import (
    clear_logs,
    get_all_logs,
)

from app.workflow import run_debuggable_workflow


async def run_workflow(question: str):
    # Execute workflow.
    result = await run_debuggable_workflow(question)

    # Fetch workflow logs.
    logs = get_all_logs()

    # Convert logs into dataframe.i.e tabular format
    dataframe = pd.DataFrame(logs)

    # Return workflow result and dashboard table.
    return (
        result["trace_id"],
        result["final_output"],
        dataframe,
    )


def reset_dashboard():
    # Clear workflow logs.
    clear_logs()

    # Return empty dashboard.
    return (
        "",
        "",
        pd.DataFrame(),
    )


with gr.Blocks() as demo:
    gr.Markdown("# AI Debug Dashboard")

    gr.Markdown(
        "Track AI workflow execution, tracing, logging, "
        "latency, and observability."
    )

    question_input = gr.Textbox(
        label="Business Question",
        placeholder="Example: Analyze declining customer retention.",
        lines=4,
    )

    run_button = gr.Button("Run Workflow")

    clear_button = gr.Button("Clear Dashboard")

    trace_id_output = gr.Textbox(
        label="Trace ID",
    )

    final_output = gr.Markdown(
        label="Final AI Response",
    )

    dashboard_table = gr.Dataframe(
        label="Execution Dashboard",
    )

    run_button.click(
        fn=run_workflow,
        inputs=question_input,
        outputs=[
            trace_id_output,
            final_output,
            dashboard_table,
        ],
    )

    clear_button.click(
        fn=reset_dashboard,
        outputs=[
            trace_id_output,
            final_output,
            dashboard_table,
        ],
    )


if __name__ == "__main__":
    demo.launch()