import autogen

from app.config import (
    get_openai_api_key,
    get_deepseek_api_key,
    get_developer_model,
    get_reviewer_model,
    get_security_model,
    get_tester_model
)

from app.prompts import (
    developer_agent_prompt,
    code_reviewer_prompt,
    security_reviewer_prompt,
    testing_agent_prompt
)


def build_llm_config(model_name: str, temperature: float = 0.2):
    # If model name starts with deepseek, use DeepSeek endpoint.
    # temperature low means more deterministic
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
    # This text will be displayed in UI so students can see which model each agent uses.
    return f"""
# Agent Model Configuration

| Agent | Model |
|---|---|
| Developer Agent | `{get_developer_model()}` |
| Code Reviewer Agent | `{get_reviewer_model()}` |
| Security Reviewer Agent | `{get_security_model()}` |
| Testing Agent | `{get_tester_model()}` |
"""


def create_code_review_group():
    # Read model names from .env.
    developer_model = get_developer_model()
    reviewer_model = get_reviewer_model()
    security_model = get_security_model()
    tester_model = get_tester_model()

    # Print models in terminal for teaching/demo purpose.
    print("\n=== Agent Model Configuration ===")
    print(f"Developer Agent Model: {developer_model}")
    print(f"Code Reviewer Agent Model: {reviewer_model}")
    print(f"Security Reviewer Agent Model: {security_model}")
    print(f"Testing Agent Model: {tester_model}")

    # Create Developer Agent.
    developer_agent = autogen.AssistantAgent(
        name="DeveloperAgent",
        system_message=developer_agent_prompt(),
        llm_config=build_llm_config(
            model_name=developer_model,
            temperature=0.3
        )
    )

    # Create Code Reviewer Agent.
    code_reviewer_agent = autogen.AssistantAgent(
        name="CodeReviewerAgent",
        system_message=code_reviewer_prompt(),
        llm_config=build_llm_config(
            model_name=reviewer_model,
            temperature=0.2
        )
    )

    # Create Security Reviewer Agent.
    security_reviewer_agent = autogen.AssistantAgent(
        name="SecurityReviewerAgent",
        system_message=security_reviewer_prompt(),
        llm_config=build_llm_config(
            model_name=security_model,
            temperature=0.1
        )
    )

    # Create Testing Agent.
    testing_agent = autogen.AssistantAgent(
        name="TestingAgent",
        system_message=testing_agent_prompt(),
        llm_config=build_llm_config(
            model_name=tester_model,
            temperature=0.2
        )
    )

    # User Proxy starts the conversation.
    #a special AutoGen agent that represents the user/human side of the conversation.

    user_proxy = autogen.UserProxyAgent(
        name="UserProxy",  #agent name
        human_input_mode="NEVER", #NEVER,ALWAYS, TERMINATE are other mode . whether AutoGen pauses and asks the real human for input.
        code_execution_config=False #“Do NOT execute Python code.”
    )

    # Create shared group chat. It stores agents and conversation messages
    group_chat = autogen.GroupChat(
        agents=[
            user_proxy,
            developer_agent,
            code_reviewer_agent,
            security_reviewer_agent,
            testing_agent,
        ],
        messages=[],
        max_round=6 #the maximum number of conversation rounds allowed in the AutoGen group chat.
    )

    # Manager controls the group conversation: agent communication, turn-taking, message routing, discussion progression
    manager = autogen.GroupChatManager(
        groupchat=group_chat,
        llm_config=build_llm_config(
            model_name=developer_model,
            temperature=0.2
        )
    )

    return user_proxy, manager