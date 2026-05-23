from duckduckgo_search import DDGS
from agents import function_tool

#@function_tool is a decorator provided by the OpenAI Agents SDK. Converts a function into a tool that can be used by the agent.
@function_tool
def web_search(query: str) -> str:
    # This function becomes a tool available to the OpenAI Agent.
    # The agent can call this function when it needs web information.

    # Create an empty list to store formatted search results.
    collected_results = []

    # DDGS is the DuckDuckGo search client.
    with DDGS() as ddgs:

        # Search the web using the user's query.
        results = ddgs.text(
            keywords=query,
            max_results=5,
        )

        # Loop through each search result.
        for result in results:

            # Extract the title from the search result.
            title = result.get("title", "")

            # Extract the short snippet/body from the search result.
            body = result.get("body", "")

            # Extract the source URL from the search result.
            href = result.get("href", "")

            # Format one search result as readable text.
            formatted_result = f"""
Title: {title}

Snippet:
{body}

URL:
{href}
"""

            # Add the formatted result to our results list.
            collected_results.append(formatted_result)

    # If no results were found, return a clear message.
    if not collected_results:
        return "No search results found."

    # Combine all results into one text block.
    return "\n\n".join(collected_results)