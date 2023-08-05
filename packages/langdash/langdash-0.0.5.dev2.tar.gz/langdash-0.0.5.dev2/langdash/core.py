import gc
from typing import Dict, Callable, TypeVar
from langdash.llm import LLM
from langdash.llm_session import LLMSession, T_LLM
from langdash.chains import LDChain, LDText, LDFormatArg, LDArg, LDReturns, LDChoice

T_ModelInternal = TypeVar("T_ModelInternal")

class Langdash:
  """
  Core Langdash instance.
  """
  _models: Dict[str, LLM]
  
  def __init__(self):
    self._models = {}
    self._cached_models = {}
  
  def get_model_internal(self,
                         model: T_LLM,
                         default: Callable[[T_LLM], T_ModelInternal]) -> T_ModelInternal:
    if model in self._cached_models:
      return self._cached_models[model]
    gc.collect()
    self._cached_models[model] = default(model)
    return self._cached_models[model]
  
  def register_model(self, name: str, model: LLM):
    """
    Register a new language model to the Langdash instance.
    
    Args:
      name (str): The name of the model.
      model (LLM): The LLM object.
    """
    if name in self._models:
      raise KeyError(f"model '{name}' already exists")
    self._models[name] = model
    
  def session_for_model(self, model: str, **kwargs) -> LLMSession:
    """
    Create a new session for a given model.
    
    Args:
      model (str): The name of the model to be used.
      default_infer_args (InferArgs): Default inference arguments.
      track_called_chains (bool): Whether or not to track the nodes called in each chain. Defaults to `True`.
      token_healing (bool): Whether or not to heal tokens.
      global_args (LDNodeArgs): Global arguments which can be read by every chain.
    
    Returns:
      (LLMSession) The session object.
    """
    return self._models[model].session(ld=self, **kwargs)
      
  def chain(self, *args, **kwargs) -> LDChain:
    """
    Chain a list of nodes together.

    Args:
      nodes (List[Union["LDNode", str]]):
        A list of nodes or constant text nodes (represented by strings) to chain together.
      args (TypeDict):
        A dictionary of argument types for the chain function.
      returns (TypeDict):
        A dictionary of return value types for the chain function.

    Returns:
      (LDChain) The chain of nodes.
    """
    return LDChain(self, *args, **kwargs)
    
  def text(self, *args, **kwargs):
    """
    Creates a raw text node.
    
    Args:
      text (str): The raw text.
      
    Returns:
      The text node.
    """
    return LDText(self, *args, **kwargs)
    
  def format_args(self, *args, **kwargs):
    """
    Creates a format argument node.
    
    Args:
      text (str): The format text.
      
    Returns:
      The format text node.
    """
    return LDFormatArg(self, *args, **kwargs)
    
  def arg(self, *args, **kwargs):
    """
    Creates a new argument node with the specified argument.
    
    Args:
      arg (str): The argument.
      padleft (str):
        The padding string to use for the left side of the argument.
      padright (str):
        The padding string to use for the right side of the argument.
    
    Returns:
      The newly created argument node.
    """
    return LDArg(self, *args, **kwargs)
    
  def returns(self, *args, **kwargs):
    """
    Create a new return node for the specified return value.

    Args:
      returns (str): The name of the return value.
      end (str):
        Where to stop the inference. Either a string, or a token id.
        If None is passed, the inference will continue forever (for streaming).
      padleft (str):
        The left padding value for the return. If the generated string starts with
        *padleft* then it will be stripped.
      infer_args (Optional[InferArgs]):
        Optional inference arguments for generation.

    Returns:
      The return node.
    """
    return LDReturns(self, *args, **kwargs)

  def choice(self, *args, **kwargs):
    """
    Creates a new choice node with the specified choices, and returns to the .
    
    Args:
      returns (str): The name of the return value.
      choices (List[str]): List of choice strings
      padleft (str):
        Left padding for every choice string.
      padright (str):
        Right padding for every choice string.
    
    Returns:
      The newly created choice node.
    """
    return LDChoice(self, *args, **kwargs)
    