from pydantic import BaseModel, Field
from pydantic_ai import Agent

from sql_tools import SQLTools, setup_database


class SQLResult(BaseModel):
    sql_query: str = Field(description="The SQL query executed")
    result_text: str = Field(description="The actual query result")
    row_count: int = Field(description="Number of result rows")


sql_tools = SQLTools()

agent = Agent(
    "openai:gpt-4o-mini",
    output_type=SQLResult,
    tools=[sql_tools.get_schema, sql_tools.run_sql],
    instructions=(
        "You are a SQL assistant for NYC taxi trip data. "
        "Always call get_schema first, then run_sql to answer the question. "
        "Use only the actual database results. "
        "Return the executed SQL, result text, and number of result rows. "
        "Never invent values. Only use read-only SELECT queries."
    ),
)


if __name__ == "__main__":
    setup_database()
    result = agent.run_sync(
        "What's the average trip distance for rides with 2 passengers?"
    )
    print(result.output.model_dump_json(indent=2))
