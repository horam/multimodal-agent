# Chunk Normalization

Chunk size normalization aims to keep embeddings:

- smaller
- more searchable
- less noisy
- cheaper (fewer tokens)

# Why Normalize?

You don't want:

- giant paragraphs embedded directly
- noisy logs going into RAG
- 3000-token embeddings for a simple chat

# Planned Behaviors

1. Split long text into semantic units
2. Strip noise (timestamps, logs, repeated content)
3. De-duplicate similar chunks
4. Add chunk metadata
