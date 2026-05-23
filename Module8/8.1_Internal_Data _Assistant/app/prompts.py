def build_sql_generation_prompt(question: str) -> str:
    # This prompt asks the AI to generate SQL from a business question.
    return f"""
You are a careful enterprise data assistant.

Convert the user's business question into a safe SQLite SELECT query.

Available table:

sales_orders(
    order_id INTEGER,
    customer_name TEXT,
    region TEXT,
    product TEXT,
    order_amount REAL,
    order_status TEXT
)

User Question:
{question}

Rules:
- Return only SQL.
- Use only SELECT.
- Use only the sales_orders table.
- Do not use INSERT, UPDATE, DELETE, DROP, ALTER, CREATE, TRUNCATE.
- Do not include markdown.
- Do not include explanation.
- Do not use SELECT *.
- Only select business-safe columns: order_id, customer_name, region, product, order_amount, order_status.
"""


def build_summary_prompt(question: str, sql_query: str, query_result: str) -> str:
    # This prompt asks the AI to summarize database results for business users.
    return f"""
You are a helpful internal business data assistant.

User Question:
{question}

SQL Query Used:
{sql_query}

Query Result:
{query_result}

Summarize the result in simple business language.

Rules:
- Be concise.
- Do not expose sensitive information.
- Explain what the result means.
- If there are no rows, say no matching records were found.
"""