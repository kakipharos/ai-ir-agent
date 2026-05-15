from dataclasses import dataclass, field
from typing import Optional, Dict, Any
from datetime import datetime

@dataclass
class ContextItem:
    source_type: str
    title: str
    content: str
    score: float = 0.0
    url: Optional[str] = None
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    metadata: Dict[str, Any] = field(default_factory=dict)

    def short(self, max_chars: int = 500) -> str:
        text = self.content.replace("\n", " ").strip()
        return text[:max_chars] + ("..." if len(text) > max_chars else "")
