# coding=utf-8

"""
Tools
"""

from . import process
from . import code
from . import utils

# https://github.com/lmintlcx/pvztools


def background_running(on=True):
    """
    允许后台运行.

    @参数 on(bool): 是否开启.
    """
    if utils.game_on():
        if on:
            process.write_memory("short", 0x00EB, 0x0054EBA8)
        else:
            process.write_memory("short", 0x2E74, 0x0054EBA8)


def clear_fog(on=True):
    """
    清除浓雾.

    @参数 on(bool): 是否开启.
    """
    if utils.game_on():
        if on:
            process.write_memory("unsigned short", 0xD231, 0x0041A68D)
        else:
            process.write_memory("unsigned short", 0xF23B, 0x0041A68D)
