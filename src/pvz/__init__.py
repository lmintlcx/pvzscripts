# coding=utf-8

"""
Python vs. Zombies
"""

__name__ = "pvz"
__version__ = "3.3.3"
__description__ = "Python vs. Zombies"
__date__ = "2019-03-14"
__status__ = "Production"
__author__ = "lmintlcx"
__copyright__ = "Copyright 2018-2019, lmintlcx"
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
from . import helper
from . import code
from . import tools

### documented api

## 调试日志

from .logger import enable_logger as EnableLogger

## 查找进程读写内存

from .process import find_pvz_1051 as FindPvZ
from .process import read_memory as ReadMemory
from .process import write_memory as WriteMemory
from .process import set_pvz_top_most as SetWindowTopMost

## 模拟鼠标点击

from .mouse import left_click as LeftClick
from .mouse import right_click as RightClick
from .mouse import special_button_click as ButtonClick

## 模拟键盘敲击

from .keyboard import press_esc as PressEsc
from .keyboard import press_space as PressSpace
from .keyboard import press_enter as PressEnter
from .keyboard import press_keys as PressKeys
from .keyboard import pause_game as PauseGame
from .keyboard import restore_game as RestoreGame

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

from .scene import get_mouse_lock as MouseLock
from .scene import safe_click as SafeClick
from .scene import click_seed as ClickSeed
from .scene import click_shovel as ClickShovel
from .scene import click_grid as ClickGrid

## 用卡用炮铲子操作

from .operate import use_seed as Card
from .operate import use_shovel as Shovel
from .operate import fire_cob as Pao
from .operate import skip_cob_index as SkipPao
from .operate import try_to_fire_cob as TryPao
from .operate import fire_cob_on_roof as RoofPao
from .operate import set_replace_cob_cannon as SetFixPao

## 子线程操作

from .threads import running_in_thread as RunningInThread
from .threads import auto_collect as StartAutoCollectThread
from .threads import auto_fill_ice as StartAutoFillIceThread
from .threads import activate_ice as Coffee
from .threads import immobilize_dancer as StartStopDancerThread
from .threads import nuts_fixer as StartNutsFixerThread

## 信息获取

from .utils import game_on as GameOn
from .utils import game_ui as GameUI
from .utils import game_mode as GameMode
from .utils import game_scene as GameScene
from .utils import game_paused as GamePaused
from .utils import game_clock as GameClock
from .utils import wave_countdown as WaveCountdown
from .utils import huge_wave_countdown as HugeWaveCountdown
from .utils import current_wave as CurrentWave
from .utils import get_zombie_spawning_types as GetZombieTypes
from .utils import get_zombie_spawning_appear_waves as GetZombieWaves

## 挂机辅助

from .helper import goto_main_ui as GotoMainUI
from .helper import goto_survival_endless as GotoEndless
from .helper import backup_user_data as Save
from .helper import restore_user_data as Load

## 功能修改

from .tools import background_running as BackgroundRunning
from .tools import set_quick_lineup as QuickLineup
from .tools import set_quick_pass as QuickPass
from .tools import jump_level as JumpLevel
from .tools import set_sun as SetSun
from .tools import set_money as SetMoney
from .tools import clear_fog as ClearFog
from .tools import zombie_no_falling as ZombieNoFalling
from .tools import set_music as SetMusic
from .tools import set_debug_mode as SetDebug
from .tools import set_zombies as SetZombies


__all__ = [
    # 调试日志
    "EnableLogger",
    # 查找进程读写内存
    "FindPvZ",
    "ReadMemory",
    "WriteMemory",
    "SetWindowTopMost",
    # 模拟鼠标点击
    "LeftClick",
    "RightClick",
    "ButtonClick",
    # 模拟键盘敲击
    "PressEsc",
    "PressSpace",
    "PressEnter",
    "PressKeys",
    "PauseGame",
    "RestoreGame",
    # 延时机制
    "Sleep",
    "Delay",
    "Countdown",
    "Prejudge",
    "Until",
    # 选卡/更新炮列表
    "SelectCards",
    "UpdatePaoList",
    # 场地相关点击函数
    "MouseLock",
    "SafeClick",
    "ClickSeed",
    "ClickShovel",
    "ClickGrid",
    # 用卡用炮铲子操作
    "Card",
    "Shovel",
    "Pao",
    "SkipPao",
    "TryPao",
    "RoofPao",
    "SetFixPao",
    # 子线程操作
    "RunningInThread",
    "StartAutoCollectThread",
    "StartAutoFillIceThread",
    "Coffee",
    "StartStopDancerThread",
    "StartNutsFixerThread",
    # 信息获取
    "GameOn",
    "GameUI",
    "GameMode",
    "GameScene",
    "GamePaused",
    "GameClock",
    "WaveCountdown",
    "HugeWaveCountdown",
    "CurrentWave",
    "GetZombieTypes",
    "GetZombieWaves",
    # 挂机辅助
    "GotoMainUI",
    "GotoEndless",
    "Save",
    "Load",
    # 功能修改
    "BackgroundRunning",
    "QuickLineup",
    "QuickPass",
    "JumpLevel",
    "SetSun",
    "SetMoney",
    "ClearFog",
    "ZombieNoFalling",
    "SetMusic",
    "SetDebug",
    "SetZombies",
]


### check operating system and python version

if platform.system() != "Windows":
    logger.critical(f"本包 (pvz) 只支持在 Windows 系统上运行.")

if sys.hexversion < 0x03050000:
    logger.critical(f"本包 (pvz) 要求 Python 版本 >=3.5.")


### start and exit works

# 游戏进程原始优先级
pvz_priority_class_original = win32.NORMAL_PRIORITY_CLASS


def on_start():
    # don't need actually, will set to 0.5ms if game started
    win32.timeBeginPeriod(1)  # res == TIMERR_NOERROR

    # this package is time-critical which needs real-time
    gc.disable()
    sys.setswitchinterval(0.001)

    win32.SetPriorityClass(win32.GetCurrentProcess(), win32.HIGH_PRIORITY_CLASS)

    logger.enable_logger(False)
    logger.set_logger_level("INFO")

    mouse.get_dpi_scale()

    if process.find_pvz_1051():

        global pvz_priority_class_original
        pvz_priority_class_original = win32.GetPriorityClass(process.pvz_handle)
        if pvz_priority_class_original != win32.REALTIME_PRIORITY_CLASS:
            win32.SetPriorityClass(process.pvz_handle, win32.HIGH_PRIORITY_CLASS)

        utils.update_game_base()
        ui = utils.game_ui()
        if ui in (2, 3):
            scene.update_game_scene()
            seeds.update_seeds_list() if ui == 3 else None
            cobs.update_cob_cannon_list()

    # else:
    #     logger.critical(f"游戏未开启或者游戏版本不受支持!")


def on_exit():
    win32.timeEndPeriod(1)  # res == TIMERR_NOERROR

    if process.is_valid():
        win32.SetPriorityClass(process.pvz_handle, pvz_priority_class_original)
        win32.CloseHandle(process.pvz_handle)


on_start()
atexit.register(on_exit)
