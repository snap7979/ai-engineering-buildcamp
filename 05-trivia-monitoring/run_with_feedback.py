import logfire

from trivia_agent import run, ask_feedback

with logfire.span("trivia_session"):
    run("Let's play 5 easy questions from Science & Nature")

    feedback = ask_feedback()

    if feedback is not None:
        logfire.info(
            "trivia_feedback",
            feedback=feedback,
        )