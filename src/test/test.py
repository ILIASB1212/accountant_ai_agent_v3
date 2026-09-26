import pytest

from langchain_core.messages import HumanMessage
from src.agentic_workflow.agent import graph


def run_agent(question: str):
    config = {
        "configurable": {
            "thread_id": "pytest-test"
        }
    }

    result = graph.invoke(
        {"messages": [HumanMessage(content=question)]},
        config=config
    )

    return result["messages"]


# ---------------------------------------------------------
# TEST 1 — Agent returns an answer
# ---------------------------------------------------------

def test_agent_returns_answer():
    messages = run_agent(
        "What is the accounting treatment for a purchase?"
    )

    assert len(messages) > 0

    final_message = messages[-1]

    assert final_message.content is not None
    assert len(final_message.content) > 0


# ---------------------------------------------------------
# TEST 2 — Accounting question
# ---------------------------------------------------------

def test_accounting_question():
    messages = run_agent(
        "What is the journal entry for an accounting service invoice "
        "of 2000 MAD HT?"
    )

    response = messages[-1].content.lower()

    assert len(response) > 0
    assert "2000" in response or "comptable" in response


# ---------------------------------------------------------
# TEST 3 — Moroccan tax question
# ---------------------------------------------------------

def test_tax_question():
    messages = run_agent(
        "What is the Moroccan VAT rate for a normal taxable transaction?"
    )

    response = messages[-1].content.lower()

    assert len(response) > 0

    # We don't force an exact answer here.
    # We only verify that the agent produced a tax-related response.
    assert any(
        word in response
        for word in ["tva", "taxe", "taux", "%"]
    )


# ---------------------------------------------------------
# TEST 4 — Agent uses a tool
# ---------------------------------------------------------

def test_agent_uses_tool():
    messages = run_agent(
        "What is account 4411 in the Moroccan chart of accounts?"
    )

    tool_messages = [
        message
        for message in messages
        if message.type == "tool"
    ]

    assert len(tool_messages) > 0


# ---------------------------------------------------------
# TEST 5 — Empty question
# ---------------------------------------------------------

def test_empty_question():
    messages = run_agent("")

    assert len(messages) > 0