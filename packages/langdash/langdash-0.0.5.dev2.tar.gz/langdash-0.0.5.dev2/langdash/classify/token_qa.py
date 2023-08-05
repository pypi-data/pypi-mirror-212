from typing import Union, List, Tuple, Dict, Optional
from langdash.chains import LDChainCached, LDResult, LDNodeArgs

class TokenQA:
  
  def __init__(self,
               prompt_chain: LDChainCached,
               classes: Dict[str, Union[str, List[str]]]):
    self._prompt_chain = prompt_chain
    assert self._prompt_chain.argtype("query") == str, "prompt must have query argument"
    
    self._classes = classes
    self._classes_tok: Optional[Dict[str, List[int]]] = None
    self._token_list_set = False

  def _strs_to_token_list(session, str_or_list) -> List[int]:
    str_list = str_or_list if isinstance(str_or_list, list) else [str_or_list]
    token_list = []
    for str_ in str_list:
      token = session.tokenize(str_)
      assert len(token) == 1
      token_list.append(token[0])
    return token_list
  
  def query(self,
            query: str,
            additional_args: Optional[LDNodeArgs] = None,
            return_result: bool = False) \
    -> Union[Dict[str, float], Tuple[Dict[str, float], LDResult]]:
    args={"query":query}
    if additional_args is not None:
      args.update(additional_args)
    result, session = self._prompt_chain.call(
      args=args,
      return_session=True
    )
    if not self._token_list_set:
      self._classes_tok = {}
      for k, v in self._classes.items():
        self._classes_tok[k] = TokenQA._strs_to_token_list(session, v)
      self._token_list_set = True
      
    tok_probs = session.next_token_probs()
    
    prob = {}
    for k, toks in self._classes_tok.items():
      prob[k] = sum(map(lambda tok: float(tok_probs[tok]), toks))
    prob_sum = sum(prob.values())
    for k, v in prob.items():
      prob[k] = v / prob_sum
    
    if return_result:
      return prob, result
    return prob