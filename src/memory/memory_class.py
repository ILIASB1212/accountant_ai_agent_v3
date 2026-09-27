import os
from mem0 import MemoryClient  
from dotenv import load_dotenv

from datetime import datetime


load_dotenv()

MEM0_API_KEY = os.environ["MEM0_API_KEY"]

mem_client = MemoryClient(api_key=MEM0_API_KEY)


class Memory:
    def __init__(self,user_prompt:str,user_id:str,agent_id:str,limit:int=5):
        self.user_prompt = user_prompt
        self.user_id = user_id
        self.limit = limit
        self.agent_id = agent_id

    def retrive(self):
        results = mem_client.search(
                filters={'user_id': self.user_id, 'agent_id': self.agent_id},
                query=self.user_prompt,
                limit=self.limit,
            )
        return results
    def store_memory(self,memory_data: dict[str, str]):
        """Store a new memory in Mem0."""
        mem_client.add(
            user_id=memory_data["user_id"],
        agent_id=memory_data["agent_id"],
            messages=[
            {
                "role": "user",
                "content": memory_data["text"],
            },
            {
                "role": "assistant",
                "content": memory_data["llm_output"],
            },
        ],
        )
    def format_context_for_systeme(self, memories: list[dict]) -> str:
        """ format the memory responce to be passed to systeme prompt as configurable"""
        
        if not memories:
            return ""
        return "\n".join(f"- {m}" for m in memories)

    def build_prompt(self, memories: list[dict]) -> str:
        """Deprecated: baked a rival system persona + the raw user turn into
        one HumanMessage, which then got permanently written into the
        LangGraph checkpointer's thread history on every call. Kept only for
        reference; use format_context() + chat_node's config instead."""
        memory_block = ""
        if memories:
            context = "\n".join(f"- {m}" for m in memories)
            memory_block = f"Known user context:\n{context}\n\n"

        system = (
            "You are a helpful support agent. Use the known user context when relevant, "
            "and avoid asking for information already present there."
        )
        return f"{system}\n\n{memory_block}User: {self.user_prompt}\nAssistant:"

    def semantic_memory_for_facts(self,llm_output: str) -> dict [str, str] | None:
        return {"user_id": self.user_id, "agent_id": self.agent_id, "text": self.user_prompt,"llm_output": llm_output,"timestamp": datetime.now().isoformat()}