"""
Three LLM judge checks for evaluating the documentation agent:

1. Answer Correctness  – does the agent's answer contain the reference answer?
2. Instruction Following – does the agent follow its system-prompt instructions?
3. Trajectory Optimality – was the tool-call sequence efficient?
"""

import os
import sys
import json
from typing import Literal, Any, Dict

from pydantic import BaseModel, Field
from pydantic_ai import Agent

# Allow imports from project root
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from doc_agent import SIMPLE_INSTRUCTIONS


# ---------------------------------------------------------------------------
# Output models
# ---------------------------------------------------------------------------

class CorrectnessResult(BaseModel):
    """Result of the answer-correctness check."""

    reasoning: str = Field(
        description="Step-by-step reasoning about whether the agent's answer covers the reference answer."
    )
    score: Literal["good", "bad"] = Field(
        description="'good' if the answer semantically contains the reference answer, 'bad' otherwise."
    )


class InstructionFollowingResult(BaseModel):
    """Result of the instruction-following check."""

    reasoning: str = Field(
        description="Step-by-step reasoning about whether the agent followed its instructions."
    )
    score: Literal["good", "bad"] = Field(
        description="'good' if the agent followed the instructions, 'bad' otherwise."
    )


class TrajectoryResult(BaseModel):
    """Result of the trajectory-optimality check."""

    reasoning: str = Field(
        description="Step-by-step reasoning about the optimality of the tool-call trajectory."
    )
    score: Literal["good", "bad"] = Field(
        description="'good' if the trajectory was reasonably optimal, 'bad' if clearly wasteful."
    )
    suggestion: str = Field(
        description="Concrete suggestion for how the agent could have been more efficient, or 'none' if the trajectory was already optimal."
    )


# ---------------------------------------------------------------------------
# Check 1 – Answer correctness
# ---------------------------------------------------------------------------

CORRECTNESS_INSTRUCTIONS = """
You are an expert evaluator. Your task is to decide whether an AI agent's
answer SEMANTICALLY CONTAINS the reference answer.

Rules:
- The agent's answer does NOT need to be word-for-word identical to the
  reference answer. It must convey the same key information.
- If the reference answer is a code snippet, the agent's answer must include
  equivalent code (variable names may differ, but the logic must match).
- If the agent's answer provides additional correct information beyond the
  reference, that is fine — it should still be marked "good".
- If the agent's answer is missing the core information from the reference
  answer, or contradicts it, mark it "bad".

Be strict: the core facts from the reference answer MUST appear in the
agent's response.
""".strip()

# Calibration version; the baseline judge remains wired to CORRECTNESS_INSTRUCTIONS.
CORRECTNESS_INSTRUCTIONS_V2 = """
You are an expert evaluator. Decide whether an AI agent's answer semantically
answers the user's question and covers the essential information in the
reference answer.

Rules:
- Identify the specific subject, action, and outcome required by the question
  and reference answer. Check that the response conveys those essential facts;
  topical similarity or a generic statement is not enough when a technical
  detail is required.
- Accept accurate paraphrases and equivalent code when they preserve the
  essential meaning. Do not require wording to match exactly.
- Before claiming that a required fact is missing, check the full answer and
  verify that the fact is not expressed elsewhere in different words.
- Do not require optional links, citations, or supplementary details unless
  the question or reference makes them essential to the requested answer.
- Additional information is acceptable when it is supported and does not
  contradict the essential answer. If an extra technical claim cannot be
  verified from the question, reference, and answer provided, do not
  automatically treat it as either correct or incorrect; note that limitation
  and base the score on the verifiable essential content.
- Mark "bad" when essential information is absent or contradicted. Mark
  "good" when the essential answer is present and not contradicted by
  verifiable evidence.
- Evaluate answer correctness only. Do not score instruction following,
  tool-use compliance, or trajectory efficiency.

In your reasoning, state the essential facts checked and cite what the answer
does or does not say. Distinguish observed omissions or contradictions from
claims that cannot be verified with the available evidence.
""".strip()

CORRECTNESS_PROMPT = """
User Question:
{question}

Reference Answer (ground truth):
{reference_answer}

Agent's Answer:
{agent_answer}
""".strip()


def create_correctness_judge(
    instructions: str = CORRECTNESS_INSTRUCTIONS,
) -> Agent:
    return Agent(
        name="correctness_judge",
        model="openai:gpt-4o-mini",
        instructions=instructions,
        output_type=CorrectnessResult,
    )


def format_correctness_prompt(entry: Dict[str, Any]) -> str:
    return CORRECTNESS_PROMPT.format(
        question=entry["input"]["question"],
        reference_answer=entry["input"]["reference_answer"],
        agent_answer=entry["rag_response"]["answer"],
    )


# ---------------------------------------------------------------------------
# Check 2 – Instruction following
# ---------------------------------------------------------------------------

INSTRUCTION_FOLLOWING_INSTRUCTIONS = """
You evaluate whether a documentation agent followed its instructions.

Evidence rules:
1. Use actual tool calls to assess search and retrieval.
2. Do not claim missing searches when search calls are recorded.
3. Require user-specific adaptation only when the user supplied
   specific variables, data, or setup.
4. Apply code-formatting rules only to code actually present.
5. Do not require fenced Markdown code blocks unless explicitly
   required by the agent's instructions.
6. Do not penalize missing code examples unless you have evidence
   that relevant examples were available in retrieved documents.
7. Agent self-checks are claims, not independent evidence.
8. For every bad score, identify the exact violated instruction
   and the supporting observable evidence.
9. Do not invent requirements or infer violations from
   information that was not provided.

Score good if no important violation is demonstrated by the
available evidence. A good score does not prove compliance
with requirements that cannot be observed.
""".strip()

INSTRUCTION_FOLLOWING_PROMPT = """
=== AGENT INSTRUCTIONS (system prompt) ===
{instructions}

=== USER QUESTION ===
{question}

=== AGENT ANSWER ===
{agent_answer}

=== ACTUAL TOOL CALLS ===
{tools}

=== AGENT SELF-CHECKS ===
{self_checks}
""".strip()


def create_instruction_judge() -> Agent:
    return Agent(
        name="instruction_judge",
        model="openai:gpt-4o-mini",
        instructions=INSTRUCTION_FOLLOWING_INSTRUCTIONS,
        output_type=InstructionFollowingResult,
    )


def format_instruction_prompt(entry: Dict[str, Any]) -> str:
    checks = entry["rag_response"].get("checks", [])
    checks_str = "\n".join(
        f"- [{'+' if c['passed'] else '-'}] {c['rule']}: {c['explanation']}"
        for c in checks
    )
    tools_str = "\n".join(
        f"{i}. {tool['name']}({tool['args']})"
        for i, tool in enumerate(entry.get("tools", []), 1)
    ) or "(no tool calls)"

    return INSTRUCTION_FOLLOWING_PROMPT.format(
        tools=tools_str,
        instructions=SIMPLE_INSTRUCTIONS,
        question=entry["input"]["question"],
        agent_answer=entry["rag_response"]["answer"],
        self_checks=checks_str or "(none)",
    )


# ---------------------------------------------------------------------------
# Check 3 – Trajectory optimality
# ---------------------------------------------------------------------------

TRAJECTORY_INSTRUCTIONS = """
You evaluate the efficiency of a documentation agent's tool calls.

Available tools:
- search(query): finds relevant documentation.
- get_file(filename): retrieves a documentation file.

Typical workflow:
1. Search for relevant documentation.
2. Retrieve one or more relevant files.
3. Produce the final answer.

Evaluation rules:
- Multiple DIFFERENT get_file calls are allowed.
- Do not assume files contain duplicate information.
- Do not penalize multiple files based on count alone.
- Additional searches are allowed when relevant.
- Flag repeated identical calls when clearly unnecessary.
- Flag clearly irrelevant searches or retrievals.
- You cannot see retrieved document contents.
- Never invent tool calls that are absent from the trajectory.
- Do not evaluate answer formatting or writing style here.
- Do not claim that fewer files would suffice without evidence.

Score "bad" only for a clearly observable inefficiency.
Otherwise score "good", meaning no clear inefficiency was detected.

Explain the evidence behind the score.
Provide a concrete improvement suggestion when applicable.
""".strip()

TRAJECTORY_PROMPT = """
User Question:
{question}

Tool Call Trajectory:
{tools}

Agent's Final Answer:
{agent_answer}
""".strip()


def create_trajectory_judge() -> Agent:
    return Agent(
        name="trajectory_judge",
        model="openai:gpt-4o-mini",
        instructions=TRAJECTORY_INSTRUCTIONS,
        output_type=TrajectoryResult,
    )


def format_trajectory_prompt(entry: Dict[str, Any]) -> str:
    tools_parts = []
    for i, t in enumerate(entry["tools"], 1):
        tools_parts.append(f"{i}. {t['name']}({t['args']})")
    tools_str = "\n".join(tools_parts) or "(no tool calls)"

    return TRAJECTORY_PROMPT.format(
        question=entry["input"]["question"],
        tools=tools_str,
        agent_answer=entry["rag_response"]["answer"],
    )
