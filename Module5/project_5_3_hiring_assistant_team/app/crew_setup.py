import yaml

from crewai import Agent, Task, Crew, Process

from app.config import get_openai_model


def load_yaml_file(file_path: str):
    # Open the YAML file from the given path.
    with open(file_path, "r") as file:

        # Convert the YAML content into a Python dictionary.
        return yaml.safe_load(file)


# Load all agent definitions from agents.yaml.
agents_config = load_yaml_file("app/agents.yaml")

# Load all task definitions from tasks.yaml.
tasks_config = load_yaml_file("app/tasks.yaml")


def create_hiring_assistant_crew(
    resume_text: str,
    job_description: str
):
    # Create the Resume Screener Agent.
    resume_screener_agent = Agent(
        role=agents_config["resume_screener_agent"]["role"],
        goal=agents_config["resume_screener_agent"]["goal"],
        backstory=agents_config["resume_screener_agent"]["backstory"],
        verbose=True,
        llm=get_openai_model()
    )

    # Create the Skill Gap Analyst Agent.
    skill_gap_analyst_agent = Agent(
        role=agents_config["skill_gap_analyst_agent"]["role"],
        goal=agents_config["skill_gap_analyst_agent"]["goal"],
        backstory=agents_config["skill_gap_analyst_agent"]["backstory"],
        verbose=True,
        llm=get_openai_model()
    )

    # Create the Interview Designer Agent.
    interview_designer_agent = Agent(
        role=agents_config["interview_designer_agent"]["role"],
        goal=agents_config["interview_designer_agent"]["goal"],
        backstory=agents_config["interview_designer_agent"]["backstory"],
        verbose=True,
        llm=get_openai_model()
    )

    # Create the resume screening task.
    resume_screening_task = Task(
        description=tasks_config["resume_screening_task"]["description"].format(
            resume_text=resume_text,
            job_description=job_description,
        ),
        expected_output=tasks_config["resume_screening_task"]["expected_output"],
        agent=resume_screener_agent
    )

    # Create the skill gap analysis task.
    skill_gap_analysis_task = Task(
        description=tasks_config["skill_gap_analysis_task"]["description"],
        expected_output=tasks_config["skill_gap_analysis_task"]["expected_output"],
        agent=skill_gap_analyst_agent
    )

    # Create the interview question generation task.
    interview_question_task = Task(
        description=tasks_config["interview_question_task"]["description"],
        expected_output=tasks_config["interview_question_task"]["expected_output"],
        agent=interview_designer_agent
    )

    # Create the CrewAI team.
    hiring_team = Crew(
        agents=[
            resume_screener_agent,
            skill_gap_analyst_agent,
            interview_designer_agent
        ],
        tasks=[
            resume_screening_task,
            skill_gap_analysis_task,
            interview_question_task
        ],
        process=Process.sequential,
        verbose=True
    )

    # Return the complete hiring assistant crew.
    return hiring_team