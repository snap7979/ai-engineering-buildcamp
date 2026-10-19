from pydantic import BaseModel
from pydantic_ai import Agent
from tests.utils import collect_tools
from tests.cost_tracker import capture_usage


class JudgeCriterion(BaseModel):
    criterion_description: str
    passed: bool
    judgement: str


class JudgeFeedback(BaseModel):
    criteria: list[JudgeCriterion]
    feedback: str

judge_instructions = """
You are an expert judge evaluating the performance of an
AI agent.
""".strip()

def create_judge_agent():
    agent = Agent(
        name="judge",
        model="openai:gpt-4o-mini",
        instructions=judge_instructions,
        output_type=JudgeFeedback,
    )
    return agent

judge_user_prompt_template = """
Evaluate the agent's performance based on the following criteria:
<CRITERIA>
{criteria}
</CRITERIA>

The agent's final output was:
<AGENT_OUTPUT>
{output}
</AGENT_OUTPUT>

Tool calls:
<TOOL_CALLS>
{tool_calls}
</TOOL_CALLS>
""".strip()


async def assert_criteria(result, criteria):
    messages = result.new_messages()
    tool_calls = collect_tools(messages)
    output = str(result.output)



    judge_agent = create_judge_agent()

    judge_user_prompt = judge_user_prompt_template.format(
        criteria="\n".join(criteria),
        output=output,
        tool_calls="\n".join([str(tc) for tc in tool_calls]),
    )

    judge_result = await judge_agent.run(judge_user_prompt)

    provider = judge_agent.model.system
    model_name = judge_agent.model.model_name
    model = f"{provider}:{model_name}"

    capture_usage(model, judge_result)

    print("judge feedback:")
    print(judge_result.output.feedback)

    for criterion in judge_result.output.criteria:
        print(
            f"{criterion.criterion_description}: "
            f"{criterion.judgement}"
        )

        assert criterion.passed, (
            f"{criterion.criterion_description}: "
            f"{criterion.judgement}"
        )
