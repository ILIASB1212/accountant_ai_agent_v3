from guardrails import Guard
from guardrails_ai.detect_jailbreak import DetectJailbreak
from guardrails_ai.restricttotopic import RestrictToTopic
from langchain_core.messages import HumanMessage, AIMessage

# 1. Setup your Guardrails AI protection
protection = Guard().use(
    DetectJailbreak(threshold=0.8, on_fail="exception"),
    RestrictToTopic(
        valid_topics=[
            "economics", "finance", "accounting", "exchange rates", "tax", "moroccan law",
            "greetings and small talk",
            "general assistant conversation, such as asking what the assistant remembers about the user",
            "company historic client and deals and operations",
            "friendly conversation"
        ],
        invalid_topics=["politics", "religion", "violence", "adult content", "fraud"],
        disable_llm=False,  # local zero-shot classifier only — no extra latency/cost from an LLM fallback call
        on_fail="exception",
    )
    )

# 2. Define the Guardrail Node
def guardrail_node(state: dict) -> dict:
    context_message = state["messages"][-1]
 
    if not isinstance(context_message, HumanMessage):
        return {"messages": [], "blocked": False}
 
    user_text = context_message.content
 
    try:
        protection.validate(user_text)
        return {"messages": [], "blocked": False}
    except Exception as e:
        refusal = AIMessage(
            content="I cannot process this request due to safety or topic policies."
        )
        print(f"[guardrail] blocked input: {user_text!r}")
        print(f"[guardrail] reason: {e}")
        return {"messages": [refusal], "blocked": True}
