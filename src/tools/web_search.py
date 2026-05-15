import requests
from bs4 import BeautifulSoup
from datetime import datetime
from urllib.parse import quote_plus
from ..schema import ContextItem

def search_web(query: str, top_k: int = 5) -> list[ContextItem]:
    """Simple DuckDuckGo HTML search. For production, replace this with Tavily, SerpAPI, or another search API."""
    url = f"https://duckduckgo.com/html/?q={quote_plus(query)}"
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        resp = requests.get(url, headers=headers, timeout=10)
        resp.raise_for_status()
    except Exception as e:
        return [ContextItem(
            source_type="web",
            title="Web search failed",
            content=f"Could not search web: {e}",
            score=0.1,
            created_at=datetime.utcnow().isoformat(),
        )]

    soup = BeautifulSoup(resp.text, "html.parser")
    results = []
    for r in soup.select(".result")[:top_k]:
        title_el = r.select_one(".result__a")
        snippet_el = r.select_one(".result__snippet")
        if not title_el:
            continue
        title = title_el.get_text(" ", strip=True)
        link = title_el.get("href")
        snippet = snippet_el.get_text(" ", strip=True) if snippet_el else ""
        content = snippet or title
        results.append(ContextItem(
            source_type="web",
            title=title,
            content=content,
            url=link,
            score=0.65,
            created_at=datetime.utcnow().isoformat(),
        ))
    return results
