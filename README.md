# AI IR Agent: Context-Aware Agent with Memory, RAG, Web Search, and Context Ranking

This project implements a small AI agent focused on **Information Retrieval (IR)**.  
The agent improves its answers by retrieving context from:

1. Long-term working memory
2. Local documents using RAG-style retrieval
3. Web search
4. Tool actions, such as saving new memory

The main idea is that an AI agent should not only answer from the model's internal knowledge. It should actively collect relevant context before answering.

## Features

- CLI chat interface
- Long-term memory stored in `data/memory/memory.json`
- Local document retrieval from `data/documents`
- PDF, TXT, and Markdown document loading
- Embedding-based retrieval when an OpenAI-compatible embedding model is available
- TF-IDF fallback retrieval if embeddings are unavailable
- Simple web search tool using DuckDuckGo HTML search
- Context ranking based on relevance, freshness, and source type
- Debug mode showing which context items were selected

## Architecture

```text
User question
   ↓
Agent decides retrieval needs
   ↓
Memory search + Document search + Web search
   ↓
Context Manager ranks context
   ↓
LLM receives selected context
   ↓
Final answer with sources
```

## Setup

```bash
git clone <your-repo-link>
cd ai-ir-agent

python -m venv .venv
source .venv/bin/activate   # macOS/Linux
# .venv\Scripts\activate  # Windows

pip install -r requirements.txt

cp .env.example .env
```

Edit `.env` and add your API key:

```bash
OPENAI_API_KEY=your_key_here
```

If using Berget.AI or another OpenAI-compatible endpoint, also set:

```bash
OPENAI_BASE_URL=your_provider_base_url
OPENAI_CHAT_MODEL=your_chat_model
OPENAI_EMBEDDING_MODEL=your_embedding_model
```

## Add Documents

Put `.txt`, `.md`, or `.pdf` files inside:

```text
data/documents/
```

Example:

```bash
echo "Transformers use attention to connect tokens in a sequence." > data/documents/lecture_notes.txt
```

Then build the document index:

```bash
python -m src.cli index
```

## Run the Agent

```bash
python -m src.cli chat
```

Useful commands inside chat:

```text
/memory remember that I prefer concise answers
/debug on
/debug off
/exit
```

## Demo Questions

Try these:

```text
Remember that I prefer concise technical answers.
```

```text
What do you remember about my preferences?
```

```text
Explain attention based on the documents.
```

```text
Search the web for recent AI agent news and summarize it.
```

```text
Compare the local document information with current web information.
```

## What Makes This an IR Agent?

The system retrieves information before answering. It uses multiple context sources and ranks them before sending them to the model. This is different from a normal chatbot because the answer depends on external context gathered by tools.

## Report and Video

The report template is in `report.md`.

For the video, demonstrate:

1. Installing/running the project
2. Adding a document and indexing it
3. Asking a document-based question
4. Saving and retrieving memory
5. Running a web-search question
6. Showing debug output from the context ranking system
