from typing import Generator, Callable, Tuple
from langdash.chains import LDChainCached
from langdash.search.engine import Engine

def number_based_prompt(search: "MultichoiceSearch", key: int, document: str) -> Tuple[str, str]:
  return str(key), f"{key}. {document}\n"

class MultichoiceSearch(Engine):
  
  def __init__(self,
               prompt_chain: LDChainCached,
               document_prompt: Callable[["MultichoiceSearch", int, str], Tuple[str, str]] = number_based_prompt):
    self._prompt_chain = prompt_chain
    assert self._prompt_chain.argtype("prompts") == str, "prompt must have prompts argument"
    assert self._prompt_chain.argtype("query") == str, "prompt must have query argument"
    self._needs_update = False
    self._prompts = ""
    self._documents = []
    self._document_prompt = document_prompt
    self._keys = []
    self._key_tokens = []
  
  def add(self, text: str):
    self._documents.append(text)
    self._needs_update = True
  
  def _update_session(self):
    self._keys.clear()
    self._key_tokens.clear()
    self._prompts = ""
    for idx, document in enumerate(self._documents):
      key, prompt = self._document_prompt(self, idx, document)
      self._prompts += prompt
      self._keys.append(key)
  
  def search(self, text: str, max_documents: int = 1) -> Generator[Tuple[str, float], None, None]:
    if not self._documents:
      return
    
    if self._needs_update:
      self._update_session()
      self._needs_update = False
      
    _, session = self._prompt_chain.call(args={
      "prompts":self._prompts,
      "query":text
    }, return_session=True)
    
    if not self._key_tokens:
      for token in self._keys:
        tokens = session.tokenize(token)
        assert len(tokens) == 1
        self._key_tokens.append(tokens[0])
    
    tok_probs = session.next_token_probs()
    
    doc_probs = [0.] * len(self._documents)
    for idx, token in enumerate(self._key_tokens):
      doc_probs[idx] = float(tok_probs[token])
      
    doc_probs_sum = sum(doc_probs)
    for idx in range(len(doc_probs)):
      doc_probs[idx] /= doc_probs_sum
      
    doc_probs_with_text = list(zip(doc_probs, self._documents))
    doc_probs_with_text.sort(key=lambda x: x[0], reverse=True)
    if max_documents == -1:
      yield from iter(doc_probs_with_text)
    else:
      yield from iter(doc_probs_with_text[0:max_documents])