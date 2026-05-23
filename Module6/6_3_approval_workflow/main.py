import gradio as gr

from app.graph_workflow import (
    build_initial_approval_graph,
    build_final_decision_graph,
)


# Build graphs once when application starts.
initial_graph = build_initial_approval_graph()
final_graph = build_final_decision_graph()


def start_approval_workflow(request_text: str):
    # Validate input.
    if not request_text or not request_text.strip():
        return "Please enter a business request.", None

    # Initial workflow state.
    initial_state = {
        "request_text": request_text,
        "risk_level": "",
        "risk_reason": "",
        "recommended_action": "",
        "human_decision": "",
        "final_result": "",
    }

    # Run first phase of the graph.
    updated_state = initial_graph.invoke(initial_state)

    # Return output and store state in Gradio state.
    return updated_state["final_result"], updated_state


def submit_human_decision(human_decision: str, current_state):
    # If there is no current workflow state, show error.
    if current_state is None:
        return "Please run the approval workflow first.", None

    # If the request was already auto-approved, no human decision is needed.
    if current_state["risk_level"].lower() == "low":
        return (
            "This request was already auto-approved. Human decision is not required.",
            current_state
        )

    # Update state with human decision.
    current_state["human_decision"] = human_decision

    # Run final decision graph.
    final_state = final_graph.invoke(current_state)

    # Return final result and updated state.
    return final_state["final_result"], final_state


with gr.Blocks() as demo:
    gr.Markdown("# Approval Workflow — LangGraph")

    gr.Markdown(
        "AI analyzes request risk. Low-risk requests are auto-approved. "
        "Medium/high-risk requests require human approval."
    )

    request_input = gr.Textbox(
        label="Business Request",
        placeholder=(
            "Example: Approve a $500 refund for a customer who was charged twice."
        ),
        lines=6
    )

    start_button = gr.Button("Analyze Request")

    output = gr.Markdown(label="Workflow Output")

    human_decision = gr.Radio(
        choices=[
            "Approved",
            "Rejected"
        ],
        label="Human Decision",
        value="Approved"
    )

    decision_button = gr.Button("Submit Human Decision")

    workflow_state = gr.State(None)

    start_button.click(
        fn=start_approval_workflow,
        inputs=request_input,
        outputs=[
            output,
            workflow_state,
        ]
    )

    decision_button.click(
        fn=submit_human_decision,
        inputs=[
            human_decision,
            workflow_state
        ],
        outputs=[
            output,
            workflow_state
        ]
    )


if __name__ == "__main__":
    demo.launch()