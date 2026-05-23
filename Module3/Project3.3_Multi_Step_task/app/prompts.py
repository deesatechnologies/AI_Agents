def build_planning_prompt(user_goal: str):
    # Prompt for planning stage.
    return f"""
You are an expert AI planner.

Create a step-by-step execution plan for the following goal.

Goal:
{user_goal}

Requirements:
- Break work into logical steps
- Keep steps practical
- Explain reasoning briefly
- Use numbered steps
"""


def build_execution_prompt(
    user_goal: str,
    plan_output: str,
):
    # Prompt for execution stage.
    return f"""
You are an expert AI execution assistant.

Goal:
{user_goal}

Execution Plan:
{plan_output}

Now execute the plan and generate the best possible result.

Requirements:
- Follow the plan carefully
- Be detailed
- Use structured formatting
- Include practical insights
"""


def build_refinement_prompt(
    user_goal: str,
    execution_output: str,
):
    # Prompt for refinement stage.
    return f"""
You are an expert AI reviewer.

Goal:
{user_goal}

Current Output:
{execution_output}

Your task:
- Review the output critically
- Improve clarity
- Improve structure
- Improve completeness
- Fix weak areas
- Make the final result more professional

Return improved final version.
"""