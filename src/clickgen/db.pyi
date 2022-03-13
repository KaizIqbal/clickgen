from pathlib import Path
from typing import Dict, List, Optional, Set

Data = List[Set[str]]
DATA: Data

class CursorDB:
    data: Dict[str, List[str]]
    def __init__(self, data: Data) -> None: ...
    def search_symlinks(self, key: str, find_similar: bool = ...) -> Optional[List[str]]: ...
    def rename_file(self, fp: Path) -> Optional[Path]: ...