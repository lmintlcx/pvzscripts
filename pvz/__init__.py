# coding=utf-8
"""
Python vs. Zombies
"""

__name__ = "pvz"
__version__ = "4.0.2"
__description__ = "Python vs. Zombies"
__date__ = "2020-09-13"
__status__ = "Production"
__author__ = "lmintlcx"
__copyright__ = "Copyright 2018-2020, lmintlcx"
__credits__ = ["no_doudle", "a418569882"]
__license__ = "GPL"
__maintainer__ = "lmintlcx"
__email__ = "lmintlcx@gmail.com"

import platform
import sys
import gc
import atexit

### 检查操作系统和 Python 版本

if platform.system() != "Windows":
    raise Exception("本项目 (pvz) 只支持在 Windows 系统上使用.")

if sys.hexversion < 0x030400f0:
    raise Exception("本项目 (pvz) 要求版本号 >=3.4.0 的 Python 运行环境.")

print("当前版本: %s" % __version__)
print("在线教程: https://pvz.lmintlcx.com/scripts/")

from .core import *
from .extra import *

### documented api

## 读写内存
from .core import read_memory as ReadMemory
from .core import write_memory as WriteMemory

## 模拟鼠标点击
from .core import left_click as LeftClick
from .core import right_click as RightClick
from .core import special_button_click as ButtonClick

## 模拟键盘敲击
from .core import press_esc as PressEsc
from .core import press_space as PressSpace
from .core import press_enter as PressEnter
from .core import press_keys as PressKeys

## 功能修改
from .extra import set_zombies as SetZombies

## 选卡/更新炮列表
from .extra import select_seeds_and_lets_rock as SelectCards
from .extra import update_cob_cannon_list as UpdatePaoList

## 阻塞延时
from .core import thread_sleep_for as Sleep
from .extra import game_delay_for as Delay
from .extra import until_relative_time_after_refresh as Prejudge
from .extra import until_relative_time as Until

## 场地点击
from .extra import get_mouse_lock as MouseLock
from .extra import safe_click as SafeClick
from .extra import click_seed as ClickSeed
from .extra import click_shovel as ClickShovel
from .extra import click_grid as ClickGrid

## 主要操作
from .extra import use_seed as Card
from .extra import use_shovel as Shovel
from .extra import fire_cob as Pao
from .extra import fire_cob_on_roof as RoofPao
from .extra import skip_cob_index as Skip

## 子线程操作
from .extra import running_in_thread as RunningInThread
from .extra import auto_collect as AutoCollect
from .extra import auto_fill_ice as IceSpots
from .extra import activate_ice as Coffee

__all__ = [
    # 读写内存
    "ReadMemory",
    "WriteMemory",
    # 模拟鼠标点击
    "LeftClick",
    "RightClick",
    "ButtonClick",
    # 模拟键盘敲击
    "PressEsc",
    "PressSpace",
    "PressEnter",
    "PressKeys",
    # 功能修改
    "SetZombies",
    # 选卡/更新炮列表
    "SelectCards",
    "UpdatePaoList",
    # 阻塞延时
    "Sleep",
    "Delay",
    "Prejudge",
    "Until",
    # 场地点击
    "MouseLock",
    "SafeClick",
    "ClickSeed",
    "ClickShovel",
    "ClickGrid",
    # 主要操作
    "Card",
    "Shovel",
    "Pao",
    "RoofPao",
    "Skip",
    # 子线程操作
    "RunningInThread",
    "AutoCollect",
    "IceSpots",
    "Coffee",
]

### 启动和退出时的特殊处理


def _on_start():
    # 其实不需要, 游戏启动后会变成 0.5ms
    timeBeginPeriod(1)  # res == TIMERR_NOERROR

    # 时间敏感
    gc.disable()
    sys.setswitchinterval(0.001)

    SetPriorityClass(GetCurrentProcess(), HIGH_PRIORITY_CLASS)

    get_dpi_scale()  # 自动获取缩放率
    # set_dpi_scale(1.25)  # 出错则手动设置

    if find_pvz():
        ui = game_ui()
        if ui in (2, 3):
            set_pvz_foreground()
            set_pvz_high_priority()
            update_game_scene()
            update_seeds_list() if ui == 3 else None
            update_cob_cannon_list()
    else:
        critical("游戏未开启或者游戏版本不受支持!")

    enable_logging(False)  # 是否输出调试日志
    set_logging_level("INFO")


def _on_exit():
    timeEndPeriod(1)  # res == TIMERR_NOERROR

    if is_valid():
        CloseHandle(pvz_handle)


_on_start()
atexit.register(_on_exit)
