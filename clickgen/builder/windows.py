#!/usr/bin/env python
# -*- coding: utf-8 -*-


from clickgen.configs.core import ConfigProvider


class WindowsBuilder:
    """ Generate `x11` cursors """

    def __init__(self, config: ConfigProvider) -> None:
        self._config = config
