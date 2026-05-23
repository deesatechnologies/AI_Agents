import gradio as gr

from app.llm_service import call_llm

from app.prompts import (
    build_planning_prompt,
    build_execution_prompt,
    build_refinement_prompt,
)


def run_multi_step_agent(user_goal: str):
    """
    Main multi-step agent workflow.

    Workflow:
    Plan
    ↓
    Execute
    ↓
    Refine
    """

    # Validate user input.
    if not user_goal or not user_goal.strip():
        return "Please enter a goal."

    # System prompt defines overall agent behavior.
    system_prompt = (
        "You are an advanced AI task agent capable "
        "of planning, executing, and refining tasks."
    )

    # ---------------------------------------------------
    # STEP 1 — Planning
    # ---------------------------------------------------

    # Build planning prompt.
    planning_prompt = build_planning_prompt(
        user_goal
    )

    # Generate execution plan.
    plan_output = call_llm(
        system_prompt=system_prompt,
        user_prompt=planning_prompt,
    )

    # ---------------------------------------------------
    # STEP 2 — Execution
    # ---------------------------------------------------

    # Build execution prompt.
    execution_prompt = build_execution_prompt(
        user_goal=user_goal,
        plan_output=plan_output,
    )

    # Execute the plan.
    execution_output = call_llm(
        system_prompt=system_prompt,
        user_prompt=execution_prompt,
    )

    # ---------------------------------------------------
    # STEP 3 — Refinement
    # ---------------------------------------------------

    # Build refinement prompt.
    refinement_prompt = build_refinement_prompt(
        user_goal=user_goal,
        execution_output=execution_output,
    )

    # Improve and refine final output.
    refined_output = call_llm(
        system_prompt=system_prompt,
        user_prompt=refinement_prompt,
    )

    # Return complete workflow output.
    return f"""
# Step 1 — Planning Output

{plan_output}

---

# Step 2 — Execution Output

{execution_output}

---

# Step 3 — Refined Final Output

{refined_output}
"""


with gr.Blocks() as demo:

    # Project title.
    gr.Markdown("# Multi-Step Task Agent")

    # Project description.
    gr.Markdown(
        "AI Agent that plans, executes, and refines tasks iteratively."
    )

    # User goal input.
    goal_input = gr.Textbox(
        label="Enter Goal",

        placeholder=(
            "Example: Create a beginner roadmap for learning AI engineering"
        ),

        lines=5,
    )

    # Run button.
    run_button = gr.Button(
        "Run Multi-Step Agent"
    )

    # Output display.
    output = gr.Markdown(
        label="Agent Workflow Output"
    )

    # Execute workflow.
    run_button.click(
        fn=run_multi_step_agent,

        inputs=goal_input,

        outputs=output,
    )


if __name__ == "__main__":
    # Launch local Gradio application.
    demo.launch()