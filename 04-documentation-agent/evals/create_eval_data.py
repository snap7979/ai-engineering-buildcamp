
import argparse
import asyncio
import json
from dataclasses import asdict
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv

from tools import create_documentation_tools_cached
from doc_agent import DocumentationAgentConfig, create_agent, run_agent
from tests.utils import collect_tools
from tests.cost_tracker import calculate_cost


EVALS_DIR = Path(__file__).parent


async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=None)
    args = parser.parse_args()

    # Load environment variables
    load_dotenv("/workspaces/.codespaces/shared/.env")

    # 1. Read evaluation questions
    df = pd.read_csv(EVALS_DIR / "questions.csv")

    if args.limit is not None:
        df = df.head(args.limit)

    # 2. Initialize the existing agent
    tools = create_documentation_tools_cached()
    config = DocumentationAgentConfig()
    agent = create_agent(config, tools)

    results = []
    output_file = EVALS_DIR / f"evals_run_{len(df)}.json"

    # 3. Run each evaluation question
    for i, (_, row) in enumerate(df.iterrows(), start=1):
        question = row["question"]
        print(f"\n[{i}/{len(df)}] {question}")

        try:
            result = await run_agent(agent, question)

            # Read token usage (attribute, not method)
            usage = result.usage

            cost = calculate_cost(
                config.model,
                usage.input_tokens,
                usage.output_tokens,
            )

            record = {
                "input": row.to_dict(),
                "rag_response": result.output.model_dump(mode="json"),
                "tools": [
                    asdict(tool)
                    for tool in collect_tools(result.all_messages())
                ],
                "cost": cost,
            }

            print(f"Cost: ${cost:.5f}")

        except Exception as error:
            print(f"ERROR: {error}")

            record = {
                "input": row.to_dict(),
                "rag_response": {"answer": ""},
                "tools": [],
                "cost": 0.0,
                "error": str(error),
            }

        results.append(record)

        # 4. Save results after each question
        output_file.write_text(
            json.dumps(results, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )

    total_cost = sum(item["cost"] for item in results)

    print(f"\nSaved {len(results)} results to {output_file}")
    print(f"Total estimated cost: ${total_cost:.5f}")


if __name__ == "__main__":
    asyncio.run(main())
