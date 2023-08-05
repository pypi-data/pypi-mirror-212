from typing import List
from langdash.infer import InferArgs

import torch
from torch.nn import functional as F

@torch.jit.script
def _sample_top_p(logits: torch.Tensor, top_p: float) -> torch.Tensor:
  assert 0.0 <= top_p <= 1.0, "top_p must be in [0.0, 1.0]"
  probs = F.softmax(logits, dim=-1)
  sorted_probs = torch.sort(probs, descending=True)[0]
  cumulative_probs = torch.cumsum(sorted_probs, dim=-1)
  cutoff = float(sorted_probs[torch.argmax((cumulative_probs > top_p).long())])
  probs[probs < cutoff] = 0
  return probs

@torch.jit.script
def _sample_typical(logits: torch.Tensor, mass: float) -> torch.Tensor:
  # https://github.com/huggingface/transformers/compare/main...cimeister:typicalsampling:typical-pr
  assert 0.0 <= mass <= 1.0, "typical mass must be in [0.0, 1.0]"
  
  probs = F.softmax(logits, dim=-1)
  normalized = -torch.log(probs)
  ent = torch.nansum(normalized * probs, dim=-1, keepdim=True)
  
  shifted_scores = torch.abs(logits - ent)
  sorted_scores, sorted_indices = torch.sort(shifted_scores, descending=False)
  sorted_logits = logits.gather(-1, sorted_indices)
  cumulative_probs = sorted_logits.softmax(dim=-1).cumsum(dim=-1)
  
  I = (cumulative_probs < mass).sum()
  probs[shifted_scores > sorted_scores[I]] = 0.
  return probs

def _output_probs(
  logits: torch.FloatTensor,
  args: InferArgs,
  ctx: List[int]
) -> torch.Tensor:
  # apply repetition penalty
  if args.rep_penalty != 1.0:
    rep_penalty = args.rep_penalty
    assert 0.0 <= rep_penalty, "rep_penalty must be in [0.0, inf]"
    for _, tok in zip(range(args.max_rep_ctx), reversed(ctx)):
      if logits[tok] < 0.0:
        logits[tok] *= rep_penalty
      else:
        logits[tok] /= rep_penalty
  
  # probabilities
  if args.typical_mass > 0.0:
    # typical
    probs = _sample_typical(logits, args.typical_mass)
  else:
    # top-p
    probs = _sample_top_p(logits, args.top_p)
  
  # apply temperature
  if args.temperature != 1.0:
    probs = probs.pow(1.0 / args.temperature)
    
  return probs

def sample(*args, **kwargs) -> int:
  """
  Sample from a distribution of tokens specified by *logits*.
  
  Args:
    logits (torch.FloatTensor): Logits to sample from.
    args (InferArgs): Sampling arguments.
    ctx (List[int]): List of tokens generated so far.
  
  Returns:
    The token sampled.
  """
  probs = _output_probs(*args, **kwargs)
  return int(torch.multinomial(probs, num_samples=1)[0])
  
def logits_to_probs(logits: torch.Tensor):
  """ Converts logit tensor to probability tensor using softmax. """
  return torch.nn.functional.softmax(logits, dim=-1)