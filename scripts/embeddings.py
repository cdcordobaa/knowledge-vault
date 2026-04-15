#!/usr/bin/env python3
"""
Embeddings — Local vector embeddings via sentence-transformers.
Default model: all-MiniLM-L6-v2 (384 dimensions, ~80MB, no API key).

Usage:
  from embeddings import embed_text, embed_batch
  vec = embed_text("some text")
  vecs = embed_batch(["text1", "text2"])
"""

import os

EMBEDDING_MODEL = os.environ.get("EMBEDDING_MODEL", "all-MiniLM-L6-v2")
EMBEDDING_DIM = 384

_model = None


def _get_model():
    global _model
    if _model is None:
        from sentence_transformers import SentenceTransformer
        _model = SentenceTransformer(EMBEDDING_MODEL)
    return _model


def embed_text(text):
    """Embed a single text string. Returns list[float]."""
    if not text or not text.strip():
        return [0.0] * EMBEDDING_DIM
    model = _get_model()
    return model.encode(text, normalize_embeddings=True).tolist()


def embed_batch(texts):
    """Embed a batch of texts. Returns list[list[float]]."""
    if not texts:
        return []
    model = _get_model()
    # Replace empty strings with a placeholder to avoid errors
    cleaned = [t if t and t.strip() else "empty" for t in texts]
    return model.encode(cleaned, normalize_embeddings=True, show_progress_bar=False).tolist()
