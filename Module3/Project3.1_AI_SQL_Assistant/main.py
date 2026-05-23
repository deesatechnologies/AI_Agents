import gradio as gr

from app.llm_service import call_llm

from app.prompts import (
    build_sql_generation_prompt,
    build_sql_explanation_prompt,
    build_sql_optimization_prompt,
    build_sql_debug_prompt,
)


def process_sql_request(
    task_type: str,
    database_type: str,
    user_input: str,
):
    """
    Main workflow function.

    This function dynamically changes
    AI behavior based on selected task.
    """

    # Validate user input.
    if not user_input or not user_input.strip():
        return "Please enter SQL request or query."

    # System prompt controls overall assistant behavior.
    system_prompt = (
        "You are an expert AI SQL assistant "
        "with deep knowledge of databases, optimization, "
        "query debugging, and SQL education."
    )

    # Generate SQL workflow.
    if task_type == "Generate SQL":

        prompt = build_sql_generation_prompt(
            user_request=user_input,
            database_type=database_type,
        )

    # Explain SQL workflow.
    elif task_type == "Explain SQL":

        prompt = build_sql_explanation_prompt(
            sql_query=user_input
        )

    # Optimize SQL workflow.
    elif task_type == "Optimize SQL":

        prompt = build_sql_optimization_prompt(
            sql_query=user_input
        )

    # Debug SQL workflow.
    elif task_type == "Debug SQL":

        prompt = build_sql_debug_prompt(
            sql_query=user_input
        )

    else:
        return "Invalid task selected."

    # Send request to AI model.
    ai_output = call_llm(
        system_prompt=system_prompt,
        user_prompt=prompt,
    )

    return ai_output


with gr.Blocks() as demo:

    # Project title.
    gr.Markdown("# AI SQL Assistant")

    # Project description.
    gr.Markdown(
        "Generate, explain, optimize, and debug SQL queries using AI."
    )

    # Task selection dropdown.
    task_dropdown = gr.Dropdown(
        choices=[
            "Generate SQL",
            "Explain SQL",
            "Optimize SQL",
            "Debug SQL",
        ],

        label="Select Task",

        value="Generate SQL",
    )

    # Database selection dropdown.
    database_dropdown = gr.Dropdown(
        choices=[
            "PostgreSQL",
            "MySQL",
            "Oracle",
            "Snowflake",
            "SQL Server",
        ],

        label="Database Type",

        value="PostgreSQL",
    )

    # User input textbox.
    user_input = gr.Textbox(
        label="Enter Request or SQL Query",

        placeholder=(
            "Example: Generate SQL to find top 5 customers by revenue"
        ),

        lines=12,
    )

    # Process button.
    process_button = gr.Button(
        "Run AI SQL Assistant"
    )

    # Output display.
    output = gr.Markdown(
        label="AI SQL Response"
    )

    # Run workflow when button clicked.
    process_button.click(
        fn=process_sql_request,

        inputs=[
            task_dropdown,
            database_dropdown,
            user_input,
        ],

        outputs=output,
    )


if __name__ == "__main__":
    # Launch local Gradio app.
    demo.launch()