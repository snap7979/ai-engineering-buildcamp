from pydantic import BaseModel
from pydantic_ai import Agent


class JudgeCriterion(BaseModel):
    criterion_description: str
    passed: bool
    judgement: str


class JudgeFeedback(BaseModel):
    criteria: list[JudgeCriterion]
    feedback: str


judge_agent = Agent(
    "openai:gpt-4o-mini",
    output_type=JudgeFeedback,
    instructions=(
        "You are an impartial SQL agent evaluator. "
        "Evaluate each criterion against the SQL query and result. "
        "Do not assume missing evidence. Explain your decisions."
    ),
)


async def evaluate_agent_performance(output, criteria):
    prompt = (
        f"SQL Agent output:\n{output.model_dump_json(indent=2)}\n\n"
        "Evaluate these criteria:\n"
        + "\n".join(f"- {criterion}" for criterion in criteria)
    )
    result = await judge_agent.run(prompt)
    return result.output


async def assert_criteria(output, criteria):
    feedback = await evaluate_agent_performance(output, criteria)
    for criterion in feedback.criteria:
        print(criterion)
        assert criterion.passed, criterion.judgement
    assert len(feedback.criteria) == len(criteria)
