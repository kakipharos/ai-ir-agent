# AI IR Agent

Small AI agent project focused on information retrieval and context management.

The goal of this project was to better understand how modern AI agents retrieve and manage context instead of relying only on the language model’s internal knowledge.

The system combines:
- long-term memory
- local document retrieval (RAG)
- web search
- context ranking

---

## Features

- CLI chat interface
- Long-term memory stored in JSON
- Local document retrieval from PDF, TXT, and Markdown files
- Embedding-based retrieval using OpenAI-compatible models
- TF-IDF fallback retrieval when embeddings are unavailable
- Simple web search tool
- Context ranking system
- Debug mode for inspecting retrieved context

---

## Project Structure

ai-ir-agent/
├── data/
│   ├── documents/
│   └── memory/
├── demo/
├── src/
├── README.md
├── report.md
└── requirements.txt

---

## Setup

Clone the repository:

git clone https://github.com/kakipharos/ai-ir-agent.git
cd ai-ir-agent

Create a virtual environment:

python -m venv .venv

Activate the environment:

macOS/Linux:
source .venv/bin/activate

Windows:
.venv\Scripts\activate

Install dependencies:

pip install -r requirements.txt

Create a .env file:

cp .env.example .env

Add your API key:

OPENAI_API_KEY=your_api_key_here

If using Berget.AI or another OpenAI-compatible provider:

OPENAI_BASE_URL=your_provider_url
OPENAI_CHAT_MODEL=your_chat_model
OPENAI_EMBEDDING_MODEL=your_embedding_model

---

## Adding Documents

Place .txt, .md, or .pdf files inside:

data/documents/

Example:

echo "Transformers use attention mechanisms to connect tokens in a sequence." > data/documents/lecture_notes.txt

Build the retrieval index:

python -m src.cli index

---

## Running the Agent

Start the chat interface:

python -m src.cli chat

Useful commands:

/debug on
/debug off
/exit

Memory example:

Remember that I prefer concise technical answers.

---

## Example Questions

What do you remember about my preferences?

Explain attention mechanisms based on the local documents.

Search the web for recent AI agent news.

Compare the local document information with current web information.

---

## Architecture

User question
   ↓
Memory retrieval
Document retrieval
Web search
   ↓
Context ranking
   ↓
LLM response generation

The agent retrieves context from multiple sources before generating a response. Retrieved context is ranked before being added to the final prompt.

---

## Context Ranking

One part of the project was experimenting with context management.

The agent scores retrieved context based on:
- relevance
- source type
- freshness

Debug mode can be enabled to inspect which context items were selected.

---

## Why I Built This

This project was created to explore how AI agents use information retrieval systems to improve reasoning and answer quality.

Instead of building only a chatbot, I wanted to experiment with:
- memory systems
- retrieval pipelines
- tool usage
- context selection

A major focus of the project was understanding how retrieval affects the quality of generated answers.

---

## Demo

The demo video shows:
1. Running the agent
2. Adding and indexing documents
3. Memory retrieval
4. Web search
5. Context ranking in debug mode

Video link:
TODO

---

## Report

The project report is included in:

report.md
