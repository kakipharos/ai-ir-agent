import os
import json
import pickle
import hashlib
from pathlib import Path
from typing import List
import numpy as np
from pypdf import PdfReader
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from .config import DOCUMENT_DIR, INDEX_DIR, USE_OPENAI_EMBEDDINGS
from .llm import embed_texts
from .schema import ContextItem

def read_file(path: Path) -> str:
    suffix = path.suffix.lower()
    if suffix in [".txt", ".md"]:
        return path.read_text(encoding="utf-8", errors="ignore")
    if suffix == ".pdf":
        reader = PdfReader(str(path))
        return "\n".join(page.extract_text() or "" for page in reader.pages)
    return ""

def chunk_text(text: str, chunk_size: int = 900, overlap: int = 150) -> list[str]:
    text = " ".join(text.split())
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        start = max(end - overlap, start + 1)
    return chunks

def file_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

class DocumentIndex:
    def __init__(self, document_dir: str = DOCUMENT_DIR, index_dir: str = INDEX_DIR):
        self.document_dir = Path(document_dir)
        self.index_dir = Path(index_dir)
        self.index_dir.mkdir(parents=True, exist_ok=True)
        self.meta_path = self.index_dir / "chunks.json"
        self.embed_path = self.index_dir / "embeddings.npy"
        self.tfidf_path = self.index_dir / "tfidf.pkl"

    def build(self) -> dict:
        self.document_dir.mkdir(parents=True, exist_ok=True)
        chunks = []
        for path in self.document_dir.rglob("*"):
            if path.suffix.lower() not in [".txt", ".md", ".pdf"]:
                continue
            text = read_file(path)
            for idx, chunk in enumerate(chunk_text(text)):
                chunks.append({
                    "id": f"{path.name}:{idx}",
                    "title": path.name,
                    "path": str(path),
                    "content": chunk,
                    "file_hash": file_hash(path),
                })

        self.meta_path.write_text(json.dumps(chunks, indent=2, ensure_ascii=False), encoding="utf-8")

        texts = [c["content"] for c in chunks]
        used_embeddings = False
        if texts and USE_OPENAI_EMBEDDINGS:
            try:
                vectors = embed_texts(texts)
                np.save(self.embed_path, np.array(vectors, dtype=np.float32))
                used_embeddings = True
            except Exception as e:
                print(f"Embedding indexing failed, falling back to TF-IDF. Reason: {e}")

        if texts and not used_embeddings:
            vectorizer = TfidfVectorizer(stop_words="english")
            matrix = vectorizer.fit_transform(texts)
            with open(self.tfidf_path, "wb") as f:
                pickle.dump({"vectorizer": vectorizer, "matrix": matrix}, f)

        return {"chunks": len(chunks), "used_embeddings": used_embeddings}

    def _load_chunks(self) -> list[dict]:
        if not self.meta_path.exists():
            return []
        return json.loads(self.meta_path.read_text(encoding="utf-8"))

    def search(self, query: str, top_k: int = 5) -> List[ContextItem]:
        chunks = self._load_chunks()
        if not chunks:
            return []

        texts = [c["content"] for c in chunks]

        if self.embed_path.exists() and USE_OPENAI_EMBEDDINGS:
            try:
                matrix = np.load(self.embed_path)
                qvec = np.array(embed_texts([query])[0], dtype=np.float32)
                scores = matrix @ qvec / (np.linalg.norm(matrix, axis=1) * np.linalg.norm(qvec) + 1e-10)
            except Exception:
                scores = self._tfidf_scores(query, texts)
        else:
            scores = self._tfidf_scores(query, texts)

        top_indices = np.argsort(scores)[::-1][:top_k]
        results = []
        for i in top_indices:
            if scores[i] <= 0:
                continue
            c = chunks[int(i)]
            results.append(ContextItem(
                source_type="document",
                title=c["title"],
                content=c["content"],
                score=float(scores[i]),
                metadata={"path": c["path"], "chunk_id": c["id"]}
            ))
        return results

    def _tfidf_scores(self, query: str, texts: list[str]):
        if self.tfidf_path.exists():
            with open(self.tfidf_path, "rb") as f:
                obj = pickle.load(f)
            vectorizer, matrix = obj["vectorizer"], obj["matrix"]
        else:
            vectorizer = TfidfVectorizer(stop_words="english")
            matrix = vectorizer.fit_transform(texts)
        q = vectorizer.transform([query])
        return cosine_similarity(q, matrix).flatten()
