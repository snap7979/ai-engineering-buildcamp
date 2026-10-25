from pydantic_ai import Agent
from trivia_tools import TriviaTools
import logfire
import dotenv
import questionary

instructions = """You are a trivia quizmaster. When asked to play trivia:
1. Use the available tools to fetch trivia questions
2. Ask the player one question at a time with multiple choice options
3. Wait for their answer before moving to the next question
4. When the player answers, explain why the correct answer is correct - add interesting context and facts
5. After all questions, give the final score
"""

trivia_tools = TriviaTools()
dotenv.load_dotenv("/workspaces/.codespaces/shared/.env")

logfire.configure()
logfire.instrument_pydantic_ai()

agent = Agent(
    "openai:gpt-4o-mini",
    name="agent",
    tools=[
        trivia_tools.get_categories,
        trivia_tools.get_questions,
    ],
    instructions=instructions,
)

def run(prompt):
    message_history = []

    while True:
        result = agent.run_sync(
            prompt,
            message_history=message_history
        )
        print(result.output)
        message_history = result.all_messages()

        prompt = input("You (write 'stop' to stop): ")
        if not prompt or prompt.lower().strip() == "stop":
            break

def ask_feedback():
    result = questionary.select(
        "How was the trivia session?",
        choices=["👍 Good", "👎 Bad", "Skip"],
    ).ask()

    if result is None or result == "Skip":
        return None

    return 1 if "Good" in result else -1