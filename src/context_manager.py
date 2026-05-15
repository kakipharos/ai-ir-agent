from datetime import datetime
from .schema import ContextItem

SOURCE_WEIGHT = {
    "document": 1.00,
    "memory": 0.90,
    "web": 0.85,
}

class ContextManager:
    def __init__(self, max_items: int = 8, max_chars: int = 6000):
        self.max_items = max_items
        self.max_chars = max_chars

    def freshness_score(self, item: ContextItem) -> float:
        try:
            created = datetime.fromisoformat(item.created_at.replace("Z", ""))
            age_days = max(0, (datetime.utcnow() - created).days)
            return max(0.2, 1.0 - min(age_days, 365) / 365)
        except Exception:
            return 0.6

    def rank(self, items: list[ContextItem]) -> list[ContextItem]:
        ranked = []
        for item in items:
            source_weight = SOURCE_WEIGHT.get(item.source_type, 0.7)
            freshness = self.freshness_score(item)
            final_score = (0.70 * item.score) + (0.20 * source_weight) + (0.10 * freshness)
            item.metadata["final_score"] = round(final_score, 4)
            item.metadata["freshness_score"] = round(freshness, 4)
            item.metadata["source_weight"] = source_weight
            ranked.append(item)
        return sorted(ranked, key=lambda x: x.metadata["final_score"], reverse=True)

    def select(self, items: list[ContextItem]) -> list[ContextItem]:
        ranked = self.rank(items)
        selected = []
        total_chars = 0
        for item in ranked:
            size = len(item.content)
            if len(selected) >= self.max_items:
                break
            if total_chars + size > self.max_chars:
                continue
            selected.append(item)
            total_chars += size
        return selected

    def format_for_prompt(self, items: list[ContextItem]) -> str:
        if not items:
            return "No external context was retrieved."
        blocks = []
        for i, item in enumerate(items, 1):
            url = f"\nURL: {item.url}" if item.url else ""
            blocks.append(
                f"[Context {i}]\n"
                f"Source type: {item.source_type}\n"
                f"Title: {item.title}{url}\n"
                f"Score: {item.metadata.get('final_score', item.score)}\n"
                f"Content:\n{item.content}"
            )
        return "\n\n".join(blocks)
