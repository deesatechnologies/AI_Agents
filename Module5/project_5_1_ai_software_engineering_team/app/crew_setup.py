import yaml

from crewai import (
    Agent,
    Task,
    Crew,
    Process,
)

from app.config import (
    get_openai_model
)


# Load YAML configuration file.
def load_yaml_file(file_path: str):
    # Open YAML file.
    with open(file_path, "r") as file:

        # Convert YAML into Python dictionary.
        return yaml.safe_load(file)


# Load agents configuration.
agents_config = load_yaml_file(
    "app/agents.yaml"
)

# Load tasks configuration.
tasks_config = load_yaml_file(
    "app/tasks.yaml"
)


def create_software_engineering_crew(
    user_requirement: str
):
    """
    Create complete CrewAI software engineering team.
    """

    # ---------------------------------------------------
    # CREATE AGENTS
    # ---------------------------------------------------

    # Developer Agent.
    developer_agent = Agent(
        role=agents_config["developer_agent"]["role"],

        goal=agents_config["developer_agent"]["goal"],

        backstory=agents_config["developer_agent"]["backstory"],

        verbose=True,

        llm=get_openai_model()
    )

    # Reviewer Agent.
    reviewer_agent = Agent(
        role=agents_config["reviewer_agent"]["role"],

        goal=agents_config["reviewer_agent"]["goal"],

        backstory=agents_config["reviewer_agent"]["backstory"],

        verbose=True,

        llm=get_openai_model()
    )

    # Tester Agent.
    tester_agent = Agent(
        role=agents_config["tester_agent"]["role"],

        goal=agents_config["tester_agent"]["goal"],

        backstory=agents_config["tester_agent"]["backstory"],

        verbose=True,

        llm=get_openai_model()
    )

    # ---------------------------------------------------
    # CREATE TASKS
    # ---------------------------------------------------

    # Code generation task.
    code_generation_task = Task(
        description=tasks_config[
            "code_generation_task"
        ]["description"].format(
            user_requirement=user_requirement
        ),

        expected_output=tasks_config[
            "code_generation_task"
        ]["expected_output"],

        agent=developer_agent
    )

    # Code review task.
    code_review_task = Task(
        description=tasks_config[
            "code_review_task"
        ]["description"],

        expected_output=tasks_config[
            "code_review_task"
        ]["expected_output"],

        agent=reviewer_agent
    )

    # Testing task.
    testing_task = Task(
        description=tasks_config[
            "testing_task"
        ]["description"],

        expected_output=tasks_config[
            "testing_task"
        ]["expected_output"],

        agent=tester_agent
    )

    # ---------------------------------------------------
    # CREATE CREW
    # ---------------------------------------------------

    # Sequential process means:
    # tasks execute one after another.
    software_team = Crew(
        agents=[
            developer_agent,
            reviewer_agent,
            tester_agent
        ],

        tasks=[
            code_generation_task,
            code_review_task,
            testing_task
        ],

        process=Process.sequential,

        verbose=True,
    )

    return software_team