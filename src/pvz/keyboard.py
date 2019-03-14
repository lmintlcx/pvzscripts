# coding=utf-8

"""
Keyboard
"""

from . import win32
from . import process
from . import utils


def press_esc():
    """
    敲击 退出 键.
    """
    win32.PostMessageW(process.pvz_hwnd, win32.WM_KEYDOWN, win32.VK_ESCAPE, 0)
    win32.PostMessageW(process.pvz_hwnd, win32.WM_KEYUP, win32.VK_ESCAPE, 0)


def press_space():
    """
    敲击 空格 键.
    """
    win32.PostMessageW(process.pvz_hwnd, win32.WM_KEYDOWN, win32.VK_SPACE, 0)
    win32.PostMessageW(process.pvz_hwnd, win32.WM_KEYUP, win32.VK_SPACE, 0)


def press_enter():
    """
    敲击 回车 键.
    """
    win32.PostMessageW(process.pvz_hwnd, win32.WM_KEYDOWN, win32.VK_RETURN, 0)
    win32.PostMessageW(process.pvz_hwnd, win32.WM_KEYUP, win32.VK_RETURN, 0)


def press_left():
    """
    敲击 左方向 键.
    """
    win32.PostMessageW(process.pvz_hwnd, win32.WM_KEYDOWN, win32.VK_LEFT, 0)
    win32.PostMessageW(process.pvz_hwnd, win32.WM_KEYUP, win32.VK_LEFT, 0)


def press_up():
    """
    敲击 上方向 键.
    """
    win32.PostMessageW(process.pvz_hwnd, win32.WM_KEYDOWN, win32.VK_UP, 0)
    win32.PostMessageW(process.pvz_hwnd, win32.WM_KEYUP, win32.VK_UP, 0)


def press_right():
    """
    敲击 右方向 键.
    """
    win32.PostMessageW(process.pvz_hwnd, win32.WM_KEYDOWN, win32.VK_RIGHT, 0)
    win32.PostMessageW(process.pvz_hwnd, win32.WM_KEYUP, win32.VK_RIGHT, 0)


def press_down():
    """
    敲击 下方向 键.
    """
    win32.PostMessageW(process.pvz_hwnd, win32.WM_KEYDOWN, win32.VK_DOWN, 0)
    win32.PostMessageW(process.pvz_hwnd, win32.WM_KEYUP, win32.VK_DOWN, 0)


def press_key(key):
    """
    敲击按键. 可选值 '0' - '9' 'A' - 'Z'.
    """
    code = ord(key)
    win32.PostMessageW(process.pvz_hwnd, win32.WM_KEYDOWN, code, 0)
    win32.PostMessageW(process.pvz_hwnd, win32.WM_KEYUP, code, 0)


def press_keys(keys):
    """
    敲击一系列按键.

    @参数 keys(str): 按键字符串, 由 '0' - '9' 'A' - 'Z' 组成.

    @示例:

    >>> PressKeys("FUTURE")  # 智慧树指令, 使僵尸带上眼镜
    """
    for k in keys:
        press_key(k.upper())


def pause_game():
    """
    暂停游戏.
    """
    if utils.game_ui() == 3 and not utils.game_paused():
        press_space()


def restore_game():
    """
    恢复游戏.
    """
    if utils.game_ui() == 3 and utils.game_paused():
        press_space()
