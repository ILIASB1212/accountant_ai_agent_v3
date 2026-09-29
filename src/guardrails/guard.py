from guardrails import Guard
from guardrails_ai.detect_jailbreak import DetectJailbreak
from guardrails_ai.restricttotopic import RestrictToTopic
from langchain_core.messages import HumanMessage, AIMessage

# 1. Setup your Guardrails AI protection
protection = Guard().use_many(
    DetectJailbreak(threshold=0.9, on_fail="exception"),
    RestrictToTopic(
        valid_topics=["economics","finance", "accounting", "exchange rates", "tax", "moroccan law"],
        disable_llm=True,  # local zero-shot classifier only — no extra latency/cost from an LLM fallback call
        on_fail="exception",
    ),
)

# 2. Define the Guardrail Node
def guardrail_node(state: dict) -> dict:
    last_message = state["messages"][-1]
 
    if not isinstance(last_message, HumanMessage):
        return {"messages": [], "blocked": False}
 
    user_text = last_message.content
 
    try:
        protection.validate(user_text)
        return {"messages": [], "blocked": False}
    except Exception as e:
        refusal = AIMessage(
            content="I cannot process this request due to safety or topic policies."
        )
        return {"messages": [refusal], "blocked": True}
