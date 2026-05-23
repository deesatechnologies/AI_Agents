import autogen

from app.config import (
    get_openai_api_key,
    get_deepseek_api_key,
    get_developer_model,
    get_reviewer_model,
    get_security_model,
    get_tester_model,
)

from app.prompts import (
    problem_analyst_prompt,
    solution_strategist_prompt,
    critic_agent_prompt,
    final_answer_agent_prompt,
)


def build_llm_config(model_name: str, temperature: float = 0.2):
    # If the model name starts with deepseek, use DeepSeek endpoint.
    if model_name.startswith("deepseek"):
        return {
            "config_list": [
                {
                    "model": model_name,
                    "api_key": get_deepseek_api_key(),
                    "base_url": "https://api.deepseek.com",
                }
            ],
            "temperature": temperature
        }

    # Otherwise use OpenAI endpoint.
    return {
        "config_list": [
            {
                "model": model_name,
                "api_key": get_openai_api_key(),
            }
        ],
        "temperature": temperature
    }


def get_agent_model_summary() -> str:
    # Display which model each problem-solving agent uses.
    return f"""
# Agent Model Configuration

| Agent | Model |
|---|---|
| Problem Analyst Agent | `{get_developer_model()}` |
| Solution Strategist Agent | `{get_reviewer_model()}` |
| Critic Agent | `{get_security_model()}` |
| Final Answer Agent | `{get_tester_model()}` |
"""


def create_problem_solving_group():
    # Read model names from .env.
    analyst_model = get_developer_model()
    strategist_model = get_reviewer_model()
    critic_model = get_security_model()
    final_model = get_tester_model()

    # Print model configuration in terminal for demo visibility.
    print("\n=== Problem Solving Agent Model Configuration ===")
    print(f"Problem Analyst Agent Model: {analyst_model}")
    print(f"Solution Strategist Agent Model: {strategist_model}")
    print(f"Critic Agent Model: {critic_model}")
    print(f"Final Answer Agent Model: {final_model}")

    # Create Problem Analyst Agent.
    problem_analyst = autogen.AssistantAgent(
        name="ProblemAnalystAgent",
        system_message=problem_analyst_prompt(),
        llm_config=build_llm_config(
            model_name=analyst_model,
            temperature=0.2
        ),
    )

    # Create Solution Strategist Agent.
    solution_strategist = autogen.AssistantAgent(
        name="SolutionStrategistAgent",
        system_message=solution_strategist_prompt(),
        llm_config=build_llm_config(
            model_name=strategist_model,
            temperature=0.3
        )
    )

    # Create Critic Agent.
    critic_agent = autogen.AssistantAgent(
        name="CriticAgent",
        system_message=critic_agent_prompt(),
        llm_config=build_llm_config(
            model_name=critic_model,
            temperature=0.1,
        )
    )

    # Create Final Answer Agent.
    final_answer_agent = autogen.AssistantAgent(
        name="FinalAnswerAgent",
        system_message=final_answer_agent_prompt(),
        llm_config=build_llm_config(
            model_name=final_model,
            temperature=0.2,
        )
    )

    # UserProxy starts the conversation.
    user_proxy = autogen.UserProxyAgent(
        name="UserProxy",
        human_input_mode="ALWAYS", #ALWAYS,NEVER
        code_execution_config=False,
    )

    # Create shared group chat.
    group_chat = autogen.GroupChat(
        agents=[
            user_proxy,
            problem_analyst,
            solution_strategist,
            critic_agent,
            final_answer_agent,
        ],
        messages=[],
        max_round=8
    )

    # GroupChatManager controls conversation flow.
    manager = autogen.GroupChatManager(
        groupchat=group_chat,
        llm_config=build_llm_config(
            model_name=analyst_model,
            temperature=0.2
        ),
    )

    return user_proxy, manager