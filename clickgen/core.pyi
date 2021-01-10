from pathlib import Path
from typing import Any, List, Literal, Optional, Tuple, TypeVar, Union

from PIL.Image import Image as Image

Size = Tuple[int, int]
LikePath = TypeVar("LikePath", str, Path)
Positions: Any

class Bitmap:
    animated: bool
    png: Path
    grouped_png: List[Path]
    key: str
    x_hot: int
    y_hot: int
    size: Tuple[int, int]
    width: int
    height: int
    compress: Literal[0, 1, 2, 3, 4, 5, 6, 7, 8, 9] = ...
    def __init__(
        self, png: Union[LikePath, List[LikePath]], hotspot: Tuple[int, int]
    ) -> None: ...
    def __enter__(self) -> Bitmap: ...
    def __exit__(self, *args: Any) -> None: ...
    def resize(
        self, size: Size, resample: int = ..., save: bool = ...
    ) -> Optional[Union[Image, List[Image]]]: ...
    def reproduce(
        self,
        size: Size = ...,
        canvas_size: Size = ...,
        position: Positions = ...,
        save: Any = ...,
    ) -> Optional[Union[Image, List[Image]]]: ...
    def rename(self, key: str) -> None: ...
    def copy(self, path: Optional[LikePath] = ...) -> Bitmap: ...

class CursorAlias:
    bitmap: Bitmap
    prefix: str
    alias_dir: Path
    alias_file: Path
    def __init__(self, bitmap: Bitmap) -> None: ...
    def __enter__(self) -> CursorAlias: ...
    def __exit__(self, *args: Any) -> None: ...
    @classmethod
    def from_bitmap(
        cls: Any, png: Union[LikePath, List[LikePath]], hotspot: Tuple[int, int]
    ) -> CursorAlias: ...
    def create(self, sizes: Union[Size, List[Size]], delay: int = ...) -> Path: ...
    def check_alias(self) -> None: ...
    def extension(self) -> str: ...
    def extension(self, ext: str) -> Path: ...
    def extension(self, ext: Optional[str] = ...) -> Union[str, Path]: ...
    def copy(self, dst: Optional[LikePath] = ...) -> CursorAlias: ...
    def rename(self, key: str) -> Path: ...
    def reproduce(
        self,
        size: Size = ...,
        canvas_size: Size = ...,
        position: Positions = ...,
        delay: int = ...,
    ) -> CursorAlias: ...
