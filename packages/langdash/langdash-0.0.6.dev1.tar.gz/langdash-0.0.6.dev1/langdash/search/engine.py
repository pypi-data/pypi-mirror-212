from typing import Generator, Tuple

class Engine:
  
  def add(self, text: str):
    raise NotImplementedError("add")
  
  def search(self, text: str, max_documents: int = 1) -> Generator[Tuple[str, float], None, None]:
    raise NotImplementedError("search")