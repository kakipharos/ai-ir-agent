# Demo Script

## 1. Show project structure

Explain that the project has separate modules for:
- agent
- memory
- retrieval
- web search
- context ranking

## 2. Add a sample document

```bash
echo "Transformers use self-attention to relate tokens in a sequence. Attention helps the model focus on relevant tokens." > data/documents/lecture_notes.txt
python -m src.cli index
```

## 3. Start chat

```bash
python -m src.cli chat
```

## 4. Turn on debug mode

```text
/debug on
```

## 5. Memory demo

```text
Remember that I prefer concise technical explanations.
```

Then ask:

```text
What do you remember about my preferences?
```

## 6. Document RAG demo

```text
Explain attention based on the local documents.
```

## 7. Web search demo

```text
Search the web for recent AI agent news and summarize it.
```

## 8. Explain novelty

Point out that the agent ranks memory, document chunks, and web results before answering.
