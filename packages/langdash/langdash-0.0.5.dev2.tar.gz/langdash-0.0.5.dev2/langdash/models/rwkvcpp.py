from typing import Generator, List, Optional, Tuple, Union
from math import inf
from dataclasses import dataclass
import copy

from langdash.response import RespInfer
from langdash.llm import LLM
from langdash.llm_session import LLMGenerationSessionForRawText, LLMState
from langdash.infer import InferArgs
import langdash.sampling as sampling

import os
import sys
import torch
import pathlib

_rwkv_lib: Optional[str] = None

RWKV_CPP_COMMIT = "9e2a0de8436a956c5ef80fbd5f4184311a7a568d"

def _load_rwkv_import():
  global _rwkv_lib
  
  import subprocess
  import shutil

  import langdash
  rwkv_cpp_folder = os.path.join(os.path.dirname(langdash.__file__), "extern/rwkv.cpp")

  if not os.path.isdir(rwkv_cpp_folder):
    print("rwkv.cpp isn't installed, clone and install? (requires git, cmake)")
    do_install = input("Type 'y' (without quotes) to install: ") == 'y'
    if not do_install:
      raise ImportError("rwkv.cpp is not installed")
    
    os.makedirs(rwkv_cpp_folder, exist_ok=True)
    git = shutil.which("git")
    if git == None:
      raise ImportError("git is needed for compiling rwkv.cpp")
    subprocess.check_call(
      [git, "clone", "--recursive", "https://github.com/saharNooby/rwkv.cpp", rwkv_cpp_folder]
    )
    subprocess.check_call(
      [git, "checkout", RWKV_CPP_COMMIT],
      cwd=rwkv_cpp_folder
    )
    subprocess.check_call(
      [git, "submodule", "update"],
      cwd=rwkv_cpp_folder
    )
    
  if 'win32' in sys.platform or 'cygwin' in sys.platform:
    file_name = 'rwkv.dll'
  elif 'darwin' in sys.platform:
    file_name = 'librwkv.dylib'
  else:
    file_name = 'librwkv.so'
  
  _rwkv_lib = os.path.join(rwkv_cpp_folder, file_name)
    
  if not os.path.isfile(_rwkv_lib):
    cmake = shutil.which("cmake")
    if cmake == None:
      raise ImportError("cmake is needed for compiling rwkv.cpp")
    subprocess.check_call(
      [cmake, "."],
      cwd=rwkv_cpp_folder
    )
    subprocess.check_call(
      [cmake, "--build", ".", "--config", "Release"],
      cwd=rwkv_cpp_folder
    )
  sys.path.append(os.path.join(rwkv_cpp_folder, "rwkv"))

_load_rwkv_import()

import tokenizers # type: ignore
import rwkv_cpp_model # type: ignore
import rwkv_cpp_shared_library # type: ignore

@dataclass
class RWKVCppState(LLMState):
  _logits: Optional[torch.Tensor] = None
  _state: Optional[torch.Tensor] = None
  _next_token: Optional[Tuple[int, str]] = None

class RWKVCppSession(LLMGenerationSessionForRawText["RWKVCppModel", RWKVCppState, torch.Tensor]):
  """
  Session for rwkv.cpp model.
  """
  
  _rwkv: rwkv_cpp_model.RWKVModel
  _tokenizer: tokenizers.Tokenizer
  
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    
    def load_model(llm: RWKVCppModel):
      assert _rwkv_lib is not None
      model = rwkv_cpp_model.RWKVModel(
        rwkv_cpp_shared_library.RWKVSharedLibrary(_rwkv_lib),
        llm._model_path
      )
      tokenizer = tokenizers.Tokenizer.from_file(llm._tokenizer_path)
      return model, tokenizer
      
    self._rwkv, self._tokenizer = self._ld.get_model_internal(self.llm, load_model)
    self._space_token = "\u0120"
    self._logits, self._state = None, None
    self._next_token = None
  
  def _eval(self, tokid: int) -> torch.Tensor:
    self._logits, self._state = self._rwkv.eval(tokid, self._state)
    return self._logits
  
  def set_state(self, state: Optional[RWKVCppState]):
    if state is None:
      self._logits, self._state = None, None
      self._next_token = None
    else:
      self._logits = copy.deepcopy(state._logits)
      self._state = copy.deepcopy(state._state)
      self._next_token = state._next_token
    
  def clone_state(self) -> RWKVCppState:
    return RWKVCppState(
      _logits = copy.deepcopy(self._logits),
      _state = copy.deepcopy(self._state),
      _next_token = self._next_token,
    )

  def tokenize(self, text: str, add_special_tokens: bool = False) -> List[int]:
    return self._tokenizer.encode(text, add_special_tokens=add_special_tokens).ids
  
  def decode(self, tokids: List[int]) -> str:
    return self._tokenizer.decode(tokids)
  
  def _next_token_probs(self) -> torch.Tensor:
    if self._next_token is None:
      if self._logits is None:
        raise ValueError("cannot predict next probability for empty input")
      logits = self._logits
    else:
      logits, _ = self._rwkv.eval(self._next_token[0], self._state)
    return sampling.logits_to_probs(logits)

  def _infer(
    self,
    end: Optional[Union[str, int]],
    args: InferArgs) -> Generator[RespInfer, None, None]:
    generated = ""
    ctx: List[int] = []
    buffered_tokens: List[int] = []
    
    assert args.min_new_tokens >= 0, "min_new_tokens must be at least 0"
    
    if isinstance(end, str):
      if len(end) == 0:
        end = 0
      elif args.min_new_tokens > 0:
        endtoks = self.tokenize(end)
        assert len(endtoks) == 1
        end = endtoks[0]
    
    if self._logits is None:
      raise ValueError("no prompt provided for RWKVCppModel")
    
    for i in range(args.max_new_tokens):
      strip_left = None
      
      if i == 0 and self._next_token is not None:
        tokid, tokstr = self._next_token

        if tokstr == " ":
          for logits_tokstr, logits_tokid in self._tokenizer.get_vocab().items():
            #https://github.com/openai/gpt-2/issues/80
            #starts with 0x120
            if not logits_tokstr.startswith(self._space_token):
              self._logits[logits_tokid] = -inf
        else:
          for logits_tokstr, logits_tokid in self._tokenizer.get_vocab().items():
            if not logits_tokstr.startswith(tokstr):
              self._logits[logits_tokid] = -inf
            
        if self._logits.isinf().all():
          # we don't need to heal tokens because no token that begins with _next_token
          self._logits, self._state = self._rwkv.eval(tokid, self._state)
        else:
          strip_left = tokstr
        
      if end != 0: # no early endoftext
        self._logits[0] = -inf
      elif args.min_new_tokens > 0 and i < args.min_new_tokens:
        self._logits[end] = -inf
      
      tokid = sampling.sample(self._logits, args, ctx)
      ctx.append(tokid)
      
      if tokid == end: # implies end is int
        break
      
      tokstr = self._tokenizer.decode([tokid])
      
      if "\ufffd" in tokstr:
        buffered_tokens.append(tokid)
        self._next_token = (tokid, "")
      else:
        if buffered_tokens:
          tokstr = self._tokenizer.decode(buffered_tokens)
          tokstr += self._tokenizer.decode([tokid])
          buffered_tokens.clear()
        else:
          if strip_left and tokstr.startswith(strip_left):
            tokstr = tokstr[len(strip_left):]
      
        self._next_token = (tokid, tokstr)
        
        generated += tokstr
        if isinstance(end, str) and end and generated.endswith(end):
          generated = generated[:-len(end)]
          break
        
        yield RespInfer(tokid=tokid, tokstr=tokstr, running_infer=generated)
        
      self._logits, self._state = self._rwkv.eval(tokid, self._state)
    
    if buffered_tokens:
      generated += self._tokenizer.decode(buffered_tokens)
    yield RespInfer(tokid=0, tokstr="", running_infer=generated)

class RWKVCppModel(LLM[RWKVCppSession]):
  """
  rwkv.cpp model
  """
  
  Session = RWKVCppSession
  
  def __init__(self, model_path: str, tokenizer_path: Optional[str] = None):
    """
    Creates a template for the RWKV language model (using the rwkv.cpp library).
    
    Args:
      model_path (str): Path to the model file.
      tokenizer_path (Optional[str]):
        Path to the tokenizer file.
        If None is given, the tokenizer is assumed to be the model_path / '20B_tokenizer.json'.
    """
    self._model_path = model_path
    if tokenizer_path is None:
      self._tokenizer_path = str(pathlib.Path(os.path.abspath(model_path)).parent / '20B_tokenizer.json')
    else:
      self._tokenizer_path = tokenizer_path
      