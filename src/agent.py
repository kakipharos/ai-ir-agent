from .llm import chat_completion
from .memory import MemoryStore
from .retrieval import DocumentIndex
from .context_manager import ContextManager
from .tools.web_search import search_web

SYSTEM_PROMPT = """You are an AI Information Retrieval Agent.

Your job is to answer using retrieved context when available.
You have access to:
- long-term memory
- local document retrieval
- web search results

Rules:
1. Prefer retrieved context over unsupported assumptions.
2. Mention which source types were used.
3. If context is insufficient, say what is missing.
4. Keep answers clear and useful.
"""

class IRAgent:
    def __init__(self):
        self.memory = MemoryStore()
        self.docs = DocumentIndex()
        self.context_manager = ContextManager()
        self.debug = False

    def should_search_web(self, query: str) -> bool:
        q = query.lower()
        triggers = [
            "latest", "recent", "today", "news", "current", "this week",
            "web", "internet", "search online", "search the web", "now"
        ]
        return any(t in q for t in triggers)

    def should_save_memory(self, query: str) -> bool:
        q = query.lower().strip()
        triggers = ["remember that", "remember:", "save this", "note that", "my preference", "i prefer"]
        return any(t in q for t in triggers)

    def extract_memory(self, query: str) -> str:
        lowered = query.lower()
        for marker in ["remember that", "remember:", "save this", "note that"]:
            if marker in lowered:
                idx = lowered.index(marker) + len(marker)
                return query[idx:].strip(" :.")
        return query.strip()

    def retrieve_context(self, query: str):
        items = []
        items.extend(self.memory.search(query, top_k=4))
        items.extend(self.docs.search(query, top_k=5))
        if self.should_search_web(query):
            items.extend(search_web(query, top_k=5))
        return self.context_manager.select(items)

    def answer(self, query: str) -> str:
        if self.should_save_memory(query):
            memory_text = self.extract_memory(query)
            self.memory.add(memory_text)
            return f"Saved to memory: {memory_text}"

        selected_context = self.retrieve_context(query)
        context_text = self.context_manager.format_for_prompt(selected_context)

        if self.debug:
            print("\n[DEBUG] Selected context")
            for item in selected_context:
                print(
                    f"- {item.source_type} | {item.title} | "
                    f"raw={item.score:.3f} final={item.metadata.get('final_score')}"
                )
            print()

        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": (
                f"User question:\n{query}\n\n"
                f"Retrieved context:\n{context_text}\n\n"
                "Answer the user. Include a short 'Sources used' line."
            )}
        ]
        return chat_completion(messages)
