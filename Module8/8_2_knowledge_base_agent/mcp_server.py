import json

from mcp.server.fastmcp import FastMCP

from app.document_store import search_knowledge_base

from app.guardrails import (
    validate_user_question,
    sanitize_retrieved_text,
)


# Create MCP server.
mcp = FastMCP("knowledge-base-server")


@mcp.tool()
def search_company_knowledge_base(question: str) -> str:
    # This MCP tool searches uploaded company documents.

    # Validate the question before searching.
    allowed, message = validate_user_question(question)

    # Block unsafe questions.
    if not allowed:
        return json.dumps(
            {
                "status": "blocked",
                "reason": message,
                "chunks": [],
            }
        )

    # Search local knowledge base.
    chunks = search_knowledge_base(question)

    # If no chunks found, return empty result.
    if not chunks:
        return json.dumps(
            {
                "status": "not_found",
                "reason": "No matching document content found.",
                "chunks": [],
            }
        )

    safe_chunks = []

    # Sanitize each retrieved chunk.
    for chunk in chunks:
        safe_chunks.append(
            {
                "source": chunk["source"],
                "chunk_id": chunk["chunk_id"],
                "content": sanitize_retrieved_text(chunk["content"]),
            }
        )

    # Return safe search result.
    return json.dumps(
        {
            "status": "success",
            "reason": "Relevant chunks found.",
            "chunks": safe_chunks,
        },
        indent=2,
    )


if __name__ == "__main__":
    # Start MCP server using stdio transport.
    mcp.run()