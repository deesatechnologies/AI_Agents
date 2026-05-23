import yaml

from crewai import (
    Agent,
    Task,
    Crew,
    Process
)

from app.config import (
    get_openai_model
)


# Load YAML file.
def load_yaml_file(file_path: str):

    # Open YAML file.
    with open(file_path, "r") as file:

        # Convert YAML into Python dictionary.
        return yaml.safe_load(file)


# Load agent configurations.
agents_config = load_yaml_file(
    "app/agents.yaml"
)

# Load task configurations.
tasks_config = load_yaml_file(
    "app/tasks.yaml"
)


def create_product_launch_crew(
    product_idea: str
):
    """
    Create complete CrewAI product launch team.
    """

    # ---------------------------------------------------
    # CREATE AGENTS
    # ---------------------------------------------------

    # Market Research Agent.
    market_research_agent = Agent(
        role=agents_config[
            "market_research_agent"
        ]["role"],

        goal=agents_config[
            "market_research_agent"
        ]["goal"],

        backstory=agents_config[
            "market_research_agent"
        ]["backstory"],

        verbose=True,

        llm=get_openai_model()
    )

    # Strategy Agent.
    strategy_agent = Agent(
        role=agents_config[
            "strategy_agent"
        ]["role"],

        goal=agents_config[
            "strategy_agent"
        ]["goal"],

        backstory=agents_config[
            "strategy_agent"
        ]["backstory"],

        verbose=True,

        llm=get_openai_model()
    )

    # Content Agent.
    content_agent = Agent(
        role=agents_config[
            "content_agent"
        ]["role"],

        goal=agents_config[
            "content_agent"
        ]["goal"],

        backstory=agents_config[
            "content_agent"
        ]["backstory"],

        verbose=True,

        llm=get_openai_model()
    )

    # ---------------------------------------------------
    # CREATE TASKS
    # ---------------------------------------------------

    # Market research task.
    market_research_task = Task(
        description=tasks_config[
            "market_research_task"
        ]["description"].format(
            product_idea=product_idea
        ),

        expected_output=tasks_config[
            "market_research_task"
        ]["expected_output"],

        agent=market_research_agent
    )

    # Strategy task.
    strategy_task = Task(
        description=tasks_config[
            "strategy_task"
        ]["description"],

        expected_output=tasks_config[
            "strategy_task"
        ]["expected_output"],

        agent=strategy_agent
    )

    # Content generation task.
    content_generation_task = Task(
        description=tasks_config[
            "content_generation_task"
        ]["description"],

        expected_output=tasks_config[
            "content_generation_task"
        ]["expected_output"],

        agent=content_agent
    )

    # ---------------------------------------------------
    # CREATE CREW
    # ---------------------------------------------------

    # Sequential execution:
    # Research → Strategy → Content.
    product_launch_team = Crew(
        agents=[
            market_research_agent,
            strategy_agent,
            content_agent
        ],

        tasks=[
            market_research_task,
            strategy_task,
            content_generation_task
        ],

        process=Process.sequential,

        verbose=True
    )

    return product_launch_team