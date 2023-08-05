import faiss
from typing import Generator, Tuple
  
from langdash.llm_session import LLMEmbeddingSession
from langdash.search.engine import Engine

class EmbeddingSearch(Engine):
  
  def __init__(
    self,
    embd_session: LLMEmbeddingSession,
  ):
    self._embd_session = embd_session
    self._embds = faiss.IndexFlatIP(self._embd_session.embedding_size())
    self._documents = []
  
  def add(self, text: str):
    self._documents.append(text)
    self._embds.add(self._embd_session.infer(text))
    
  def search(self, text: str, max_documents: int = 1) -> Generator[Tuple[str, float], None, None]:
    embd = self._embd_model.encode([text])
    if max_documents == -1:
      max_documents = len(self._documents)
    D, I = self._embds.search(embd, max_documents)
    for d, i in zip(D[0], I[0]):
      yield self._documents[i], d
