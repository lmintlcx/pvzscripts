# coding=utf-8

"""
Python vs. Zombies
"""

__name__ = "pvz"
__version__ = "3.1.4"
__description__ = "Python vs. Zombies"
__date__ = "2018-11-25"
__status__ = "Development"  # Prototype -> Development -> Production
__author__ = "lmintlcx"
__copyright__ = "Copyright 2018, lmintlcx"
__credits__ = ["no_doudle", "a4l8569882"]
__license__ = "GPL"
__maintainer__ = "lmintlcx"
__email__ = "lmintlcx@gmail.com"


import platform
import sys
import gc
import atexit

from . import logger
from . import win32
from . import process
from . import utils
from . import delay
from . import mouse
from . import keyboard
from . import seeds
from . import cobs
from . import scene
from . import operate
from . import threads
from . import code


### documented api

## 查找进程读写内存

from .process import find_pvz_1051 as FindPvZ
from .process import read_memory as ReadMemory
from .process import write_memory as WriteMemory

## 模拟鼠标点击

from .mouse import left_click as LeftClick
from .mouse import right_click as RightClick
from .mouse import safe_click as SafeClick
from .mouse import special_button_click as ButtonClick

## 延时机制

from .delay import thread_sleep_for as Sleep
from .delay import game_delay_for as Delay
from .delay import until_countdown as Countdown
from .delay import until_relative_time_after_refresh as Prejudge
from .delay import until_relative_time as Until

## 选卡/更新炮列表

from .seeds import select_seeds_and_lets_rock as SelectCards
from .cobs import update_cob_cannon_list as UpdatePaoList

## 场地相关点击函数

from .scene import click_seed as ClickSeed
from .scene import click_shovel as ClickShovel
from .scene import click_grid as ClickGrid

## 用卡用炮铲子操作

from .operate import use_seed as Card
from .operate import fire_cob as Pao
from .operate import skip_cob_index as SkipPao
from .operate import use_shovel as Shovel

## 子线程操作

from .threads import running_in_thread as RunningInThread
from .threads import auto_collect as StartAutoCollectThread
from .threads import auto_fill_ice as StartAutoFillIceThread
from .threads import activate_ice as Coffee
from .threads import immobilize_dancer as StartStopDancerThread


__all__ = [
    "FindPvZ",
    "ReadMemory",
    "WriteMemory",
    "LeftClick",
    "RightClick",
    "SafeClick",
    "ButtonClick",
    "Sleep",
    "Delay",
    "Countdown",
    "Prejudge",
    "Until",
    "SelectCards",
    "UpdatePaoList",
    "ClickSeed",
    "ClickShovel",
    "ClickGrid",
    "Card",
    "Pao",
    "SkipPao",
    "Shovel",
    "RunningInThread",
    "StartAutoCollectThread",
    "StartAutoFillIceThread",
    "Coffee",
    "StartStopDancerThread",
]


### check operating system and python version

if platform.system() != "Windows":
    raise Exception("This package only works on Windows.")

if sys.hexversion < 0x03050000:
    raise Exception("Python 3.5 or newer is required to run this package.")

# # Hello World
# win32.MessageBoxW(
#     None,
#     win32.LPCWSTR("Hello PvZ!"),
#     win32.LPCWSTR("test"),
#     win32.UINT(0x00000001)
#     )


### start and exit works

pvz_priority_class_original = win32.NORMAL_PRIORITY_CLASS


def on_start():
    # don't need actually, will set to 0.5ms if game started
    win32.timeBeginPeriod(1)  # res == TIMERR_NOERROR

    # this package is time-critical which needs real-time
    gc.disable()

    win32.SetPriorityClass(win32.GetCurrentProcess(), win32.HIGH_PRIORITY_CLASS)

    # disable log
    logger.enable_logger(False)  # TODO
    logger.set_logger_level("INFO")

    mouse.get_dpi_scale()

    if process.find_pvz_1051():
        global pvz_priority_class_original
        pvz_priority_class_original = win32.GetPriorityClass(process.pvz_handle)
        if pvz_priority_class_original != win32.REALTIME_PRIORITY_CLASS:
            win32.SetPriorityClass(process.pvz_handle, win32.HIGH_PRIORITY_CLASS)

        if utils.game_ui() in (2, 3):
            global slots_count, game_scene
            slots_count = process.read_memory("int", 0x6A9EC0, 0x768, 0x144, 0x24)
            game_scene = process.read_memory("int", 0x6A9EC0, 0x768, 0x554C)
            cobs.update_cob_cannon_list()
            seeds.update_seeds_list()  # utils.game_ui() in (3,)
            scene.update_game_scene()


def on_exit():
    win32.timeEndPeriod(1)  # res == TIMERR_NOERROR

    if process.is_valid():
        win32.SetPriorityClass(process.pvz_handle, pvz_priority_class_original)
        win32.CloseHandle(process.pvz_handle)


on_start()
atexit.register(on_exit)
