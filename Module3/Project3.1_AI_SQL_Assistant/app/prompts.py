def build_sql_generation_prompt(user_request: str, database_type: str):
    # Prompt for SQL generation.
    return f"""
You are an expert SQL engineer.

Generate a SQL query based on the user's request.

Database Type:
{database_type}

User Request:
{user_request}

Requirements:
- Generate clean SQL
- Use readable formatting
- Add comments where useful
- Explain the query briefly
"""


def build_sql_explanation_prompt(sql_query: str):
    # Prompt for SQL explanation.
    return f"""
You are an expert SQL teacher.

Explain the following SQL query in beginner-friendly language.

SQL Query:
{sql_query}

Requirements:
- Explain step-by-step
- Explain each clause
- Explain joins if present
- Explain filters if present
- Keep language simple
"""


def build_sql_optimization_prompt(sql_query: str):
    # Prompt for SQL optimization.
    return f"""
You are an expert database performance engineer.

Optimize the following SQL query.

SQL Query:
{sql_query}

Requirements:
- Improve readability
- Improve performance
- Suggest indexing improvements
- Explain optimization changes
"""


def build_sql_debug_prompt(sql_query: str):
    # Prompt for SQL debugging.
    return f"""
You are an expert SQL debugger.

Analyze the following SQL query and identify possible issues.

SQL Query:
{sql_query}

Requirements:
- Identify syntax issues
- Identify logical issues
- Suggest fixes
- Explain corrections clearly
"""