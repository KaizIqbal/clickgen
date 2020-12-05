#!/usr/bin/env python
# -*- coding: utf-8 -*-

import shutil
import tempfile
from os import makedirs, path
from pathlib import Path
from typing import List

from ._constants import CANVAS_SIZE
from ._typing import ImageSize, OptionalHotspot
from .builders.winbuilder import WinCursorsBuilder
from .builders.x11builder import X11CursorsBuilder, XCursorBuilder
from .configs import Config, ThemeInfo, ThemeSettings
from .packagers.windows import WindowsPackager
from .packagers.x11 import X11Packager
from .providers.bitmaps import Bitmaps
from .providers.themeconfig import CursorConfig, ThemeConfigsProvider


def create_theme(config: Config) -> None:
    """ Create cursors theme from `bitmaps`. """
    info: ThemeInfo = config.info
    sett: ThemeSettings = config.settings

    # Cursors '.in' files generator
    config_dir: str = ThemeConfigsProvider(
        bitmaps_dir=sett.bitmaps_dir,
        hotspots=sett.hotspots,
        sizes=sett.sizes,
    ).generate(sett.animation_delay)

    # Setup temporary directories
    xtmp: str = tempfile.mkdtemp(prefix="xbu")
    wtmp: str = tempfile.mkdtemp(prefix="wbu")

    # Building Themes
    WinCursorsBuilder(config_dir, wtmp).build()
    WindowsPackager(wtmp, info).pack()

    X11CursorsBuilder(config_dir, xtmp).build()
    X11Packager(xtmp, info).pack()

    # Move themes to @out_dir
    if not path.exists(sett.out_dir):
        makedirs(sett.out_dir)

    xdst: str = path.join(sett.out_dir, info.theme_name)
    if path.exists(xdst):
        shutil.rmtree(xdst)
    shutil.move(xtmp, xdst)

    wdst: str = path.join(sett.out_dir, f"{info.theme_name}-Windows")
    if path.exists(wdst):
        shutil.rmtree(wdst)
    shutil.move(wtmp, wdst)


def create_theme_with_db(config: Config):
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
    wtmp: str = tempfile.mkdtemp(prefix="wbu")

    bits = Bitmaps(bits_dir, hotspots=sett.hotspots, windows_cursors=sett.windows_cfg)

    # Creating 'XCursors'
    x_bitmaps = bits.x_bitmaps()
    for png in x_bitmaps.static:
        node = bits.db.cursor_node_by_name(png.split(".")[0])
        hotspot: OptionalHotspot = OptionalHotspot(*node["hotspots"])

        cfg_file: Path = CursorConfig(
            bits.x_bitmaps_dir, hotspot, sizes=sizes, config_dir=x_config_dir
        ).create_static(png)
        XCursorBuilder(cfg_file, xtmp).generate()

    for key, pngs in x_bitmaps.animated.items():
        node = bits.db.cursor_node_by_name(key)
        hotspot: OptionalHotspot = OptionalHotspot(*node["hotspots"])

        cfg_file: Path = CursorConfig(
            bits.x_bitmaps_dir, hotspot, sizes=sizes, config_dir=x_config_dir
        ).create_animated(key, pngs, sett.animation_delay)
        XCursorBuilder(cfg_file, xtmp).generate()

    # Creating 'Windows Cursors'
    win_bitmaps = bits.win_bitmaps()
    win_size: List[ImageSize] = [CANVAS_SIZE]
    for png in win_bitmaps.static:
        node = bits.db.cursor_node_by_name(png.split(".")[0])
        hotspot: OptionalHotspot = OptionalHotspot(*node["hotspots"])

        CursorConfig(
            bits.win_bitmaps_dir,
            hotspot,
            sizes=win_size,
            config_dir=win_config_dir,
        ).create_static(png)

    for key, pngs in win_bitmaps.animated.items():
        node = bits.db.cursor_node_by_name(key)
        hotspot: OptionalHotspot = OptionalHotspot(*node["hotspots"])

        CursorConfig(
            bits.win_bitmaps_dir, hotspot, sizes=win_size, config_dir=win_config_dir
        ).create_animated(key, pngs, delay=3)

    print(x_config_dir)
    print(xtmp)
    print(win_config_dir)
    print(wtmp)