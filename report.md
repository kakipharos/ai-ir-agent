# Building a Context-Aware AI Agent for Information Retrieval

**GitHub repository:** <insert link>  
**Video demo:** <insert link>

## 1. Introduction

This project implements an AI agent that focuses on Information Retrieval (IR). The goal is to understand how agents collect and manage context before answering questions or performing tasks. Instead of relying only on the language model's internal knowledge, the system retrieves relevant information from memory, local documents, and the web.

## 2. System Design

The agent is designed around a retrieval-first architecture. When the user asks a question, the system searches three context sources: long-term memory, local documents, and web results. Each source returns candidate context items. A context manager then ranks these items by relevance, freshness, and source type. The highest-ranked context is included in the final prompt to the language model.

The system includes the following components:

- **Working memory:** stores user preferences and useful long-term facts.
- **Document retrieval:** chunks and indexes local documents for RAG-style search.
- **Web search:** retrieves current external information.
- **Context ranking:** selects the most useful context under a limited context budget.

This design is inspired by agent architecture concepts such as memory, tool use, context compaction, and skills.

## 3. Implementation

The project is implemented in Python and uses an OpenAI-compatible API for language model calls. The code is modular: memory, document retrieval, web search, and context ranking are implemented as separate modules. Documents can be placed in `data/documents`, indexed, and searched by the agent. The agent also supports a debug mode that prints selected context items and their scores.

If an embedding model is available, the system uses embeddings for semantic search. If not, it falls back to local TF-IDF retrieval. This makes the project easier to run across different OpenAI-compatible providers.

## 4. Evaluation

The system was tested with three types of questions. First, memory questions were used to verify that stored user preferences could be retrieved later. Second, document questions were used to confirm that the agent could answer using local notes. Third, web questions were used to test retrieval of recent information. The debug mode showed that the context manager selected different sources depending on the question.

The main limitation is that the web search tool is simple and depends on public search result pages. A future version could use a dedicated search API and stronger citation handling.

## 5. Reflection

AI coding tools were useful for generating boilerplate code, improving the README, and checking architectural alternatives. However, the system still required manual understanding and verification. I had to check whether the retrieval flow made sense, whether context was actually used in the prompt, and whether the code could run with an API key. This showed that AI tools are helpful assistants, but the developer still needs to understand the architecture, debug the system, and evaluate the final result.

## References

- OpenAI API documentation
- OpenClaw documentation on memory, tools, skills, heartbeat, and compaction
- Course material on AI agents and Information Retrieval
