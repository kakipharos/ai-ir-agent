import json
import os
from datetime import datetime
from difflib import SequenceMatcher
from .config import MEMORY_PATH
from .schema import ContextItem

class MemoryStore:
    def __init__(self, path: str = MEMORY_PATH):
        self.path = path
        os.makedirs(os.path.dirname(path), exist_ok=True)
        if not os.path.exists(path):
            self._write([])

    def _read(self) -> list[dict]:
        with open(self.path, "r", encoding="utf-8") as f:
            return json.load(f)

    def _write(self, data: list[dict]) -> None:
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def add(self, content: str, kind: str = "user_fact") -> None:
        data = self._read()
        data.append({
            "content": content.strip(),
            "kind": kind,
            "created_at": datetime.utcnow().isoformat()
        })
        self._write(data)

    def all(self) -> list[dict]:
        return self._read()

    def search(self, query: str, top_k: int = 5) -> list[ContextItem]:
        memories = self._read()
        scored = []
        q = query.lower()
        for m in memories:
            content = m["content"]
            ratio = SequenceMatcher(None, q, content.lower()).ratio()
            token_overlap = len(set(q.split()) & set(content.lower().split())) / max(1, len(set(q.split())))
            score = 0.5 * ratio + 0.5 * token_overlap
            if score > 0:
                scored.append((score, m))
        scored.sort(reverse=True, key=lambda x: x[0])
        return [
            ContextItem(
                source_type="memory",
                title=f"Memory: {m.get('kind', 'fact')}",
                content=m["content"],
                score=float(score),
                created_at=m.get("created_at", ""),
                metadata=m,
            )
            for score, m in scored[:top_k]
        ]
