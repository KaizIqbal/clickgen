from clickgen.parser import open_blob as open_blob
from clickgen.parser.png import DELAY as DELAY
from clickgen.writer.windows import to_win as to_win
from clickgen.writer.x11 import to_x11 as to_x11
from pathlib import Path
from typing import Any, Dict, List, TypeVar, Union

class ThemeSection:
    name: str
    comment: str
    website: str
    def __init__(self, name, comment, website) -> None: ...
    def __lt__(self, other): ...
    def __le__(self, other): ...
    def __gt__(self, other): ...
    def __ge__(self, other): ...

def parse_toml_theme_section(d: Dict[str, Any], **kwargs) -> ThemeSection: ...

class ConfigSection:
    bitmaps_dir: Path
    out_dir: Path
    platforms: List[str]
    x11_sizes: List[int]
    win_size: int
    def __init__(self, bitmaps_dir, out_dir, platforms, x11_sizes, win_size) -> None: ...
    def __lt__(self, other): ...
    def __le__(self, other): ...
    def __gt__(self, other): ...
    def __ge__(self, other): ...

def parse_toml_config_section(fp: str, d: Dict[str, Any], **kwargs) -> ConfigSection: ...
T = TypeVar('T')

class CursorSection:
    x11_cursor_name: str
    x11_cursor: bytes
    x11_symlinks: List[str]
    win_cursor_name: Union[str, None]
    win_cursor: Union[bytes, None]
    def __init__(self, x11_cursor_name, x11_cursor, x11_symlinks, win_cursor_name, win_cursor) -> None: ...
    def __lt__(self, other): ...
    def __le__(self, other): ...
    def __gt__(self, other): ...
    def __ge__(self, other): ...

def parse_toml_cursors_section(d: Dict[str, Any], config: ConfigSection) -> List[CursorSection]: ...

class ClickgenConfig:
    theme: ThemeSection
    config: ConfigSection
    cursors: List[CursorSection]
    def __init__(self, theme, config, cursors) -> None: ...
    def __lt__(self, other): ...
    def __le__(self, other): ...
    def __gt__(self, other): ...
    def __ge__(self, other): ...

def parse_toml_file(fp: str, **kwargs) -> ClickgenConfig: ...
