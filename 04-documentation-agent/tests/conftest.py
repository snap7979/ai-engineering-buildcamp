
import pytest
from time import time

from tests.cost_tracker import reset_cost_file, display_total_usage
from tools import create_documentation_tools_cached
from doc_agent import (
    DocumentationAgentConfig,
    DEFAULT_INSTRUCTIONS,
    create_agent,
)


@pytest.fixture(scope="module")
def agent():
    t0 = time()

    tools = create_documentation_tools_cached()

    agent_config = DocumentationAgentConfig(
        instructions=DEFAULT_INSTRUCTIONS
    )

    agent = create_agent(agent_config, tools)

    t1 = time()
    print(f"loading agent took {t1 - t0}")

    return agent


def pytest_sessionstart(session):
    reset_cost_file()

def pytest_sessionfinish(session, exitstatus):
    display_total_usage()
