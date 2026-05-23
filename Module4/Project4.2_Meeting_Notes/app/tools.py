from agents import function_tool


@function_tool
def clean_meeting_notes(notes: str) -> str:
    # This decorator converts this normal Python function into an agent tool.
    # The agent can call this tool when it wants to clean meeting notes.

    # Replace multiple spaces with single spaces.
    cleaned_notes = " ".join(notes.split())

    # Return cleaned meeting notes back to the agent.
    return cleaned_notes