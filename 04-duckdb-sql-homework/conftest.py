import pytest

from sql_agent import agent
from judge import judge_agent
from cost_tracker import capture_usage, display_total_usage, usage_totals


@pytest.fixture(autouse=True, scope="session")
def track_agent_costs():
    original_run = agent.run
    original_judge_run = judge_agent.run

    async def tracked_agent_run(*args, **kwargs):
        result = await original_run(*args, **kwargs)
        capture_usage("openai:gpt-4o-mini", result)
        return result

    async def tracked_judge_run(*args, **kwargs):
        result = await original_judge_run(*args, **kwargs)
        capture_usage("openai:gpt-4o-mini", result)
        return result

    usage_totals.clear()
    agent.run = tracked_agent_run
    judge_agent.run = tracked_judge_run

    yield

    agent.run = original_run
    judge_agent.run = original_judge_run
    display_total_usage()
