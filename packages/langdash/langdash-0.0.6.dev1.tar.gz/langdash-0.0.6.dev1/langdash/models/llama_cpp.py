from typing import Generator, List, Optional, Union
from math import inf
from dataclasses import dataclass

import torch
from llama_cpp import Llama, LlamaState, llama_token_to_str

from langdash.response import RespInfer
from langdash.llm import LLM
from langdash.llm_session import LLMGenerationSessionForRawText
from langdash.infer import InferArgs
import langdash.sampling as sampling

@dataclass
class LlamaExtraData:
  vocab: List[bytes]

class LlamaCppSession(LLMGenerationSessionForRawText["LlamaCppModel", LlamaState, torch.Tensor]):
  """
  Session for llama.cpp model.
  """
  
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    
    def load_model(llm: LlamaCppModel):
      model = Llama(model_path=llm._model_path)
      extras = LlamaExtraData(
        # TODO: figure out a better way of getting vocab mappings
        vocab=[
          llama_token_to_str(tokid)
          for tokid in model.n_vocab()
        ],
      )
      return model, extras
      
    self._llama, self._extras = self._ld.get_model_internal(self.llm, load_model)
    self._logits = None
    self._eot_token = Llama.token_eos()
  
  def _load_logits_from_llama(self):
    return torch.from_numpy(self._llama._scores[-1, :])
  
  def _eval(self, token: int):
    self._llama.eval([token])
    return self._load_logits_from_llama()
  
  def _eval_mult(self, tokens: List[int]):
    self._llama.eval(tokens)
    return self._load_logits_from_llama()
  
  def _next_token_probs(self):
    if self._next_token is None:
      if self._logits is None:
        raise ValueError("cannot predict next probability for empty input")
      logits = self._logits
    else:
      logits = self._eval(self._next_token[0])
    return sampling.logits_to_probs(logits).tolist()
  
  def set_state(self, state: Optional[LlamaState]):
    if state == None:
      self._llama.reset()
      self._logits = None
    else:
      self._llama.load_state(state)
      self._logits = self._load_logits_from_llama()
    
  def clone_state(self) -> LlamaState:
    return self._llama.save_state()

  def tokenize(self, text: str, add_special_tokens: bool = False) -> List[int]:
    return self._llama.tokenize(text, add_bos=add_special_tokens)
  
  def decode(self, tokens: List[int]) -> str:
    return self._llama.detokenize(tokens).decode("utf-8", errors="ignore")
  
  def _infer(self,
             end: Optional[Union[str, int]],
             args: Optional[InferArgs] = None) -> Generator[RespInfer, None, None]:
    generated = ""
    ctx: List[int] = []
    buffered_tokens = b""
    stops_at_eot = (
      (isinstance(end, str) and len(end) == 0) or
      (isinstance(end, int) and end == self._eot_token)
    )
    
    if self._logits is None:
      raise ValueError("no prompt provided for LlamaCppModel")
    
    for i in range(args.max_new_tokens):
      strip_left = 0
      
      if i == 0 and self._next_token is not None:
        tokstr = self._next_token[1]
        for logits_tokid, logits_tokstr in enumerate(self._extras.vocab):
          if not logits_tokstr.startswith(tokstr):
            self._logits[logits_tokid] = -inf
        strip_left = len(tokstr)
      
      if not stops_at_eot: # no early endoftext
        self._logits[self._eot_token] = -inf
        
      tokid = sampling.sample(self._logits, args, ctx)
      ctx.append(tokid)
      
      if tokid == end: # implies end is int
        break
      
      if stops_at_eot and tokid == 0:
        break
      else:
        tokstr_b = self._extras.vocab[tokid]
        
        try:
          if buffered_tokens:
            tokstr = (buffered_tokens + tokstr_b).decode("utf-8")
            buffered_tokens = b""
          else:
            tokstr = tokstr_b.decode("utf-8")
            if strip_left:
              tokstr = tokstr[strip_left:]
        
          self._next_token = (tokid, tokstr)
          
          generated += tokstr
          if isinstance(end, str) and end and generated.endswith(end):
            generated = generated[:-len(end)]
            break
          
          yield RespInfer(tokid=tokid, tokstr=tokstr, running_infer=generated)
        
        except UnicodeDecodeError:
          buffered_tokens += tokstr_b
          
        
      self._logits = self._eval(tokid)
    
    if buffered_tokens:
      generated += buffered_tokens.decode("utf-8", errors="ignore")
    yield RespInfer(tokid=-1, tokstr="", running_infer=generated)

class LlamaCppModel(LLM[LlamaCppSession]):
  """
  llama.cpp model.
  """
  
  Session = LlamaCppSession
  
  def __init__(self, model_path: str):
    self._model_path = model_path
  
  def session(self, **kwargs):
    return LlamaCppSession(self, **kwargs)
  