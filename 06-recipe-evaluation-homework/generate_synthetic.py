import csv
import json
from collections import Counter
from pathlib import Path
from typing import Literal

from pydantic import BaseModel
from pydantic_ai import Agent


APP_DIR = Path(__file__).resolve().parent
RECIPES_PATH = APP_DIR / "recipes.json"
OUTPUT_PATH = APP_DIR / "synthetic_scenarios.csv"
QUESTION_TYPES = ("factual", "how-to", "detail", "substitution", "comparison")
EXPECTED_RECIPE_COUNT = 15


class Question(BaseModel):
    question: str
    category: str
    type: Literal["factual", "how-to", "detail", "substitution", "comparison"]


class GeneratedQuestions(BaseModel):
    questions: list[Question]


GENERATION_INSTRUCTIONS = """You are creating test questions for evaluating a recipe assistant.
For the given recipe, generate exactly five realistic user questions: exactly one
factual question, one how-to question, one detail question, one substitution
question, and one comparison question. Keep every question grounded in the
provided recipe. Do not answer the questions. For each question, provide a concise
category describing its user intent and set type to exactly one of: factual,
how-to, detail, substitution, comparison.

Use the provided structured output format."""


def build_prompt(recipe: dict) -> str:
    ingredients = ", ".join(recipe["ingredients"])
    return f"""Generate the five questions for this recipe.

Recipe name: {recipe['name']}
Cuisine: {recipe['cuisine']}
Ingredients: {ingredients}
Instructions: {recipe['instructions']}"""


def validate_recipe_questions(recipe_name: str, generated: GeneratedQuestions) -> None:
    questions = generated.questions
    actual_types = Counter(question.type for question in questions)
    expected_types = Counter(QUESTION_TYPES)

    if len(questions) != len(QUESTION_TYPES) or actual_types != expected_types:
        raise ValueError(
            f"{recipe_name}: expected exactly one question of each type "
            f"{QUESTION_TYPES}; received {dict(actual_types)}"
        )

    if any(not question.question.strip() or not question.category.strip() for question in questions):
        raise ValueError(f"{recipe_name}: questions and categories must not be empty")


def generate_scenarios() -> list[Question]:
    with RECIPES_PATH.open(encoding="utf-8") as recipes_file:
        recipes = json.load(recipes_file)

    if len(recipes) != EXPECTED_RECIPE_COUNT:
        raise ValueError(
            f"Expected {EXPECTED_RECIPE_COUNT} recipes, found {len(recipes)}"
        )

    agent = Agent(
        "openai:gpt-4o-mini",
        output_type=GeneratedQuestions,
        instructions=GENERATION_INSTRUCTIONS,
    )
    scenarios = []

    for recipe in recipes:
        result = agent.run_sync(build_prompt(recipe))
        validate_recipe_questions(recipe["name"], result.output)
        scenarios.extend(
            sorted(result.output.questions, key=lambda question: QUESTION_TYPES.index(question.type))
        )

    expected_count = EXPECTED_RECIPE_COUNT * len(QUESTION_TYPES)
    if len(scenarios) != expected_count:
        raise ValueError(f"Expected {expected_count} questions, found {len(scenarios)}")

    return scenarios


def save_scenarios(scenarios: list[Question]) -> None:
    with OUTPUT_PATH.open("w", newline="", encoding="utf-8") as output_file:
        writer = csv.DictWriter(output_file, fieldnames=("question", "category", "type"))
        writer.writeheader()
        writer.writerows(question.model_dump() for question in scenarios)


def main() -> None:
    scenarios = generate_scenarios()
    save_scenarios(scenarios)
    print(f"Saved {len(scenarios)} questions to {OUTPUT_PATH.name}")


if __name__ == "__main__":
    main()