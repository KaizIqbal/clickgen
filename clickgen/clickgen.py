#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import tempfile
from contextlib import contextmanager
from pathlib import Path
from typing import List

from ._constants import CANVAS_SIZE
from ._typing import ImageSize, OptionalHotspot
from .builders.win import WinCursorBuilder
from .builders.x import XCursorBuilder
from .configs import Config, ThemeInfo, ThemeSettings
from .packagers.windows import WinPackager
from .packagers.x11 import XPackager
from .providers.bitmaps import Bitmaps
from .providers.themeconfig import CursorConfig


@contextmanager
def goto_cursors_dir(dir: Path):
    """ Temporary change directory to `cursors` using contextmanager. """

    CWD = os.getcwd()
    os.chdir(dir.absolute())
    try:
        yield
    except:
        raise Exception(f" Exception caught: {sys.exc_info()[0]}")
    finally:
        os.chdir(CWD)


def link_missing_cursors(cursors_dir: Path, root: str, symlink: List[str]) -> None:
    with goto_cursors_dir(cursors_dir):
        for link in symlink:
            try:
                os.symlink(root, link)
            except FileExistsError:
                continue


def create_theme(config: Config):
    info: ThemeInfo = config.info
    sett: ThemeSettings = config.settings

    bits_dir = Path(sett.bitmaps_dir)
    sizes: List[ImageSize] = []
    for s in sett.sizes:
        sizes.append(ImageSize(width=s, height=s))

    # Setup temporary directories
    x_config_dir: Path = Path(tempfile.mkdtemp(prefix="clickgen_x_configs_"))
    win_config_dir: Path = Path(tempfile.mkdtemp(prefix="clickgen_win_configs_"))

    xtmp: Path = Path(tempfile.mkdtemp(prefix="xbu"))
    wtmp: Path = Path(tempfile.mkdtemp(prefix="wbu"))

    bits = Bitmaps(bits_dir, hotspots=sett.hotspots, windows_cursors=sett.windows_cfg)

    # Creating 'XCursors'
    x_bitmaps = bits.x_bitmaps()
    for png in x_bitmaps.static:
        node = bits.db.cursor_node_by_name(png.split(".")[0])
        hotspot: OptionalHotspot = OptionalHotspot(*node["hotspots"])
        symlink: List[str] = node["symlink"]

        cfg_file: Path = CursorConfig(
            bits.x_bitmaps_dir, hotspot, sizes=sizes, config_dir=x_config_dir
        ).create_static(png)
        x = XCursorBuilder(cfg_file, xtmp)
        x.generate()

        if symlink:
            link_missing_cursors(x.cursors_dir, cfg_file.stem, symlink)

    for key, pngs in x_bitmaps.animated.items():
        node = bits.db.cursor_node_by_name(key)
        hotspot: OptionalHotspot = OptionalHotspot(*node["hotspots"])
        symlink: List[str] = node["symlink"]

        cfg_file: Path = CursorConfig(
            bits.x_bitmaps_dir, hotspot, sizes=sizes, config_dir=x_config_dir
        ).create_animated(key, pngs, sett.animation_delay)
        x = XCursorBuilder(cfg_file, xtmp)
        x.generate()

        if symlink:
            link_missing_cursors(x.cursors_dir, cfg_file.stem, symlink)

    XPackager(xtmp, info).save()

    # Creating 'Windows Cursors'
    win_bitmaps = bits.win_bitmaps()
    win_size: List[ImageSize] = [CANVAS_SIZE]
    for png in win_bitmaps.static:
        node = bits.db.cursor_node_by_name(png.split(".")[0])
        hotspot: OptionalHotspot = OptionalHotspot(*node["hotspots"])

        cfg_file: Path = CursorConfig(
            bits.win_bitmaps_dir,
            hotspot,
            sizes=win_size,
            config_dir=win_config_dir,
        ).create_static(png)
        WinCursorBuilder(cfg_file, wtmp).generate()

    for key, pngs in win_bitmaps.animated.items():
        node = bits.db.cursor_node_by_name(key)
        hotspot: OptionalHotspot = OptionalHotspot(*node["hotspots"])

        cfg_file: Path = CursorConfig(
            bits.win_bitmaps_dir, hotspot, sizes=win_size, config_dir=win_config_dir
        ).create_animated(key, pngs, delay=3)
        WinCursorBuilder(cfg_file, wtmp).generate()

    WinPackager(wtmp, info).save()
    print(x_config_dir)
    print(xtmp)
    print(win_config_dir)
    print(wtmp)
