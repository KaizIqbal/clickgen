#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ._typing import WindowsCursorsConfig, ImageSize

# -- Bitmaps Constants

CANVAS_SIZE: ImageSize = ImageSize(width=32, height=32)
LARGE_SIZE: ImageSize = ImageSize(width=20, height=20)
NORMAL_SIZE: ImageSize = ImageSize(width=16, height=16)

WINDOWS_CURSORS: WindowsCursorsConfig = {
    "Alternate": {"xcursor": "right_ptr", "placement": "top_left"},
    "Busy": {"xcursor": "wait"},
    "Cross": {"xcursor": "cross"},
    "Default": {"xcursor": "left_ptr", "placement": "top_left"},
    "Diagonal_1": {"xcursor": "fd_double_arrow"},
    "Diagonal_2": {"xcursor": "bd_double_arrow"},
    "Handwriting": {"xcursor": "pencil"},
    "Help": {"xcursor": "help", "placement": "top_left"},
    "Horizontal": {"xcursor": "sb_h_double_arrow"},
    "IBeam": {"xcursor": "xterm", "placement": "top_left"},
    "Link": {"xcursor": "hand2", "placement": "top_left"},
    "Move": {"xcursor": "hand1"},
    "Unavailiable": {"xcursor": "circle", "placement": "top_left"},
    "Vertical": {"xcursor": "sb_v_double_arrow"},
    "Work": {"xcursor": "left_ptr_watch", "placement": "top_left"},
}