from openai import OpenAI
from .config import OPENAI_API_KEY, OPENAI_BASE_URL, CHAT_MODEL, EMBEDDING_MODEL

def get_client() -> OpenAI:
    if not OPENAI_API_KEY:
        raise RuntimeError("OPENAI_API_KEY is missing. Add it to your .env file.")
    kwargs = {"api_key": OPENAI_API_KEY}
    if OPENAI_BASE_URL:
        kwargs["base_url"] = OPENAI_BASE_URL
    return OpenAI(**kwargs)

def chat_completion(messages, temperature: float = 0.2) -> str:
    client = get_client()
    response = client.chat.completions.create(
        model=CHAT_MODEL,
        messages=messages,
        temperature=temperature,
    )
    return response.choices[0].message.content or ""

def embed_texts(texts: list[str]) -> list[list[float]]:
    client = get_client()
    response = client.embeddings.create(
        model=EMBEDDING_MODEL,
        input=texts,
    )
    return [item.embedding for item in response.data]
