#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from typing import Dict
from os import path
from clickgen.configs import Config, ThemeInfo, ThemeSettings
import pytest


@pytest.fixture
def ti() -> ThemeInfo:
    return ThemeInfo(theme_name="foo", author="bar")


@pytest.fixture
def ts() -> ThemeSettings:
    return ThemeSettings(
        bitmaps_dir="foo", sizes=[1, 2], hotspots={"a": {"xhot": 1, "yhot": 2}}
    )


def test_theme_info(ti) -> None:
    assert isinstance(ti, ThemeInfo)

    assert ti.comment == None
    assert isinstance(ti.theme_name, str)
    assert isinstance(ti.author, str)
    assert ti.url == "Unknown Source!"


def test_theme_settings(ts) -> None:
    assert isinstance(ts, ThemeSettings)

    assert isinstance(ts.sizes[0], int)

    assert ts.animation_delay == 50
    assert ts.out_dir == os.getcwd()

    assert isinstance(ts.hotspots, Dict)
    assert ts.hotspots.get("a") == pytest.approx({"xhot": 1, "yhot": 2})
    assert isinstance(ts.hotspots.get("a").get("xhot"), int)
    assert ts.hotspots.get("a").get("xhot") == 1
    assert isinstance(ts.hotspots.get("a").get("yhot"), int)
    assert ts.hotspots.get("a").get("yhot") == 2


def test_config(ti, ts) -> None:
    c = Config(ti, ts)

    # check paths
    assert path.isabs(c.settings.bitmaps_dir)
    assert path.isabs(c.settings.out_dir)