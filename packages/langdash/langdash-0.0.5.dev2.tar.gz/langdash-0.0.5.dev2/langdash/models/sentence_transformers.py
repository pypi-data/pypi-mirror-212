from sentence_transformers import SentenceTransformer
import torch
from langdash.llm import EmbeddingLLM
from langdash.llm_session import LLMEmbeddingSession

class SentenceTransformersSession(LLMEmbeddingSession["SentenceTransformersModel", torch.Tensor]):
  """
  Session for sentence_transformers embedding model.
  """
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
      
    self._model = self._ld.get_model_internal(
      self.llm,
      lambda llm: SentenceTransformer(llm._model_name)
    )
  
  def embedding_size(self) -> int:
    return self._model.get_sentence_embedding_dimension()
  
  def infer(self, text: str) -> torch.Tensor:
    return self._model.encode([text])

class SentenceTransformersModel(EmbeddingLLM[SentenceTransformersSession]):
  """
  sentence_transformers embedding model.
  """
  Session = SentenceTransformersSession

  def __init__(self, model_name: str):
    self._model_name = model_name
