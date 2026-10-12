from pydantic_ai import Agent
from pydantic_ai.mcp import FastMCPClient, MCPToolset
from fastmcp.client.transports import PythonStdioTransport

from toyaikit.chat.interface import StdOutputInterface
from toyaikit.chat.runners import PydanticAIRunner


transport = PythonStdioTransport(
    script_path="../faq-mcp/main.py",
    cwd="../faq-mcp",
    python_cmd="../faq-mcp/.venv/bin/python"
)

mcp_client = FastMCPClient(transport)

mcp_toolset = MCPToolset(mcp_client)



developer_prompt = """
You're a course teaching assistant.
You're given a question from a course student and your task is to answer it.

If you want to look up the answer, explain why before making the call.
Use as many keywords from the user question as possible when making first requests.

Make multiple searches. Try to expand your search by using new keywords based on the results you
get from the search.

At the end, make a clarifying question based on what you presented and ask if there are
other areas that the user wants to explore.
""".strip()


agent = Agent(
    name="faq_agent",
    instructions=developer_prompt,
    toolsets=[mcp_toolset],
    model="openai-chat:gpt-4o-mini"
)


chat_interface = StdOutputInterface()

runner = PydanticAIRunner(
    chat_interface=chat_interface,
    agent=agent
)


if __name__ == "__main__":
    import asyncio
    asyncio.run(runner.run())
