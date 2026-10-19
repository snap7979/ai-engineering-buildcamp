import pytest

from sql_agent import agent


@pytest.mark.asyncio(loop_scope="module")
async def test_passenger_count():
    result = await agent.run(
        "How many trips had more than 5 passengers?"
    )

    output = result.output

    assert output.sql_query.strip()
    assert "22413" in output.result_text.replace(",", "")


@pytest.mark.asyncio(loop_scope="module")
async def test_tool_calls_order():
    from utils import collect_tools

    result = await agent.run(
        "What is the most common payment type?"
    )

    tools = collect_tools(result)
    print(f"\nTools called: {tools}")

    assert tools[0] == "get_schema"
    assert "run_sql" in tools


@pytest.mark.asyncio(loop_scope="module")
async def test_highest_average_fare_hour():
    from judge import assert_criteria

    result = await agent.run(
        "Which hour of the day has the highest average fare amount? "
        "Use the pickup hour, group by hour, and order by average fare descending."
    )

    print("\nSQL Agent output:", result.output.model_dump_json(indent=2))

    await assert_criteria(result.output, [
        "The SQL correctly calculates average fare by pickup hour.",
        "The result identifies the hour with the highest average fare.",
        "The result includes the actual average fare amount.",
    ])


@pytest.mark.asyncio(loop_scope="module")
@pytest.mark.parametrize("question,expected_column", [
    ("What is the average tip amount for credit card payments?", "tip_amount"),
    ("Which pickup location has the most trips?", "PULocationID"),
    ("What is the average fare for trips longer than 10 miles?", "trip_distance"),
    ("How many trips had zero passengers recorded?", "passenger_count"),
    ("What is the busiest day of the week for taxi trips?", "tpep_pickup_datetime"),
])
async def test_more_sql_scenarios(question, expected_column):
    from utils import collect_tools

    result = await agent.run(question)
    output = result.output
    tools = collect_tools(result)

    assert tools[0] == "get_schema"
    assert "run_sql" in tools
    assert expected_column.lower() in output.sql_query.lower()
    assert output.result_text.strip()
