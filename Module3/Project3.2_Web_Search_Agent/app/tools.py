from duckduckgo_search import DDGS #importing the DDGS class from the duckduckgo_search module


def web_search(query: str, max_results: int = 5):
    """
    Web search tool.

    This function performs internet search
    using DuckDuckGo search engine.
    """

    # Store all search results.
    collected_results = []

    # Create DuckDuckGo search client.
    with DDGS() as ddgs:

        # Perform search query.
        results = ddgs.text(
            keywords=query,
            max_results=max_results,
        )

        # Loop through search results.
        for result in results:

            # Extract title.
            title = result.get("title", "")

            # Extract snippet/body.
            body = result.get("body", "")

            # Extract URL.
            href = result.get("href", "")

            # Build formatted result.
            formatted_result = f"""
Title: {title}

Snippet:
{body}

URL:
{href}
"""

            # Save result into list.
            collected_results.append(
                formatted_result
            )

    # Combine all results into one large text block.
    return "\n\n".join(collected_results)