# coding=utf-8

"""
Mouse
"""

import time
import ctypes
import random

from . import logger
from . import win32
from . import process

#

dpi_scale = 1.0


def get_dpi_scale():
    """
    获取 DPI 缩放比例.
    """
    screen = win32.GetDC(None)
    if screen is not None:
        virtual_width = win32.GetDeviceCaps(screen, win32.HORZRES)
        physical_width = win32.GetDeviceCaps(screen, win32.DESKTOPHORZRES)
        win32.ReleaseDC(None, screen)
        scale = physical_width / virtual_width
    else:
        scale = 1.0

    global dpi_scale
    dpi_scale = scale
    logger.info(f"Get DPI scale {scale}.")


def MAKELONG(low, high):
    if dpi_scale != 1.0:
        low, high = int(low / dpi_scale), int(high / dpi_scale)
    # else:
    #     low, high = int(low), int(high)
    return ((high & 0xFFFF) << 16) | (low & 0xFFFF)


# 参数 x, y 分别为横坐标和纵坐标.
# 游戏以窗口化运行, 窗口内容分辨率为 800 x 600.
# 左上角 (0, 0), 右下角 (799, 599).

PVZ_WINDOW_WIDTH = 800
PVZ_WINDOW_HEIGHT = 600


def left_down(x, y):
    """
    鼠标左键按下.
    """
    coord = MAKELONG(x, y)
    win32.PostMessageW(process.pvz_hwnd, win32.WM_LBUTTONDOWN, win32.MK_LBUTTON, coord)


def left_up(x, y):
    """
    鼠标左键弹起.
    """
    coord = MAKELONG(x, y)
    win32.PostMessageW(process.pvz_hwnd, win32.WM_LBUTTONUP, win32.MK_LBUTTON, coord)


def left_click(x, y):
    """
    鼠标左键单击.

    @参数 x(int): 横坐标, 单位像素. 建议范围 [0, 799].

    @参数 y(int): 纵坐标, 单位像素. 建议范围 [0, 599].

    @示例:

    >>> left_click(108, 42)  # 左键单击卡槽第一张卡片的位置
    """
    coord = MAKELONG(x, y)
    win32.PostMessageW(process.pvz_hwnd, win32.WM_LBUTTONDOWN, win32.MK_LBUTTON, coord)
    win32.PostMessageW(process.pvz_hwnd, win32.WM_LBUTTONUP, win32.MK_LBUTTON, coord)


click = left_click


def right_down(x, y):
    """
    鼠标右键按下.
    """
    coord = MAKELONG(x, y)
    win32.PostMessageW(process.pvz_hwnd, win32.WM_RBUTTONDOWN, win32.MK_RBUTTON, coord)


def right_up(x, y):
    """
    鼠标右键弹起.
    """
    coord = MAKELONG(x, y)
    win32.PostMessageW(process.pvz_hwnd, win32.WM_RBUTTONUP, win32.MK_RBUTTON, coord)


def right_click(x, y):
    """
    鼠标右键单击.

    @参数 x(int): 横坐标, 单位像素. 建议范围 [0, 799].

    @参数 y(int): 纵坐标, 单位像素. 建议范围 [0, 599].

    @示例:

    >>> right_click(399, 299)  # 右键单击场地中间位置
    """
    coord = MAKELONG(x, y)
    win32.PostMessageW(process.pvz_hwnd, win32.WM_RBUTTONDOWN, win32.MK_RBUTTON, coord)
    win32.PostMessageW(process.pvz_hwnd, win32.WM_RBUTTONUP, win32.MK_RBUTTON, coord)


# safe click


def safe_click():
    """
    安全右键. 用于避免操作冲突.
    """
    right_click(0, 0)


# special button click


def special_button_click(x, y):
    """
    适用于模仿者按钮和菜单按钮的特殊点击.

    @参数 x(int): 横坐标, 单位像素. 建议范围 [0, 799].

    @参数 y(int): 纵坐标, 单位像素. 建议范围 [0, 599].

    @示例:

    >>> special_button_click(490, 550)  # 选卡界面左键单击模仿者卡片
    """
    point = win32.POINT()
    win32.GetCursorPos(ctypes.byref(point))
    x_0 = point.x
    y_0 = point.y
    rect = win32.RECT()
    win32.GetWindowRect(process.pvz_hwnd, ctypes.byref(rect))
    border_width = (rect.right - rect.left - PVZ_WINDOW_WIDTH) / 2
    title_height = rect.bottom - rect.top - border_width - PVZ_WINDOW_HEIGHT
    x_1 = int(rect.left + border_width + x)
    y_1 = int(rect.top + title_height + y)

    win32.SetCursorPos(x_1, y_1)
    time.sleep(0.01)
    win32.SetCursorPos(x_1, y_1)
    time.sleep(0.01)
    win32.SetCursorPos(x_1, y_1)

    window_hwnd = win32.WindowFromPoint(point)
    if window_hwnd == process.pvz_hwnd.value:
        left_click(x, y)
        time.sleep(0.01)
    else:
        left_click(x, y)
        time.sleep(0.02)
        left_click(0, 0)

    win32.SetCursorPos(x_0, y_0)


def move_to_click(x, y, click=True):
    """
    光标移动到目标位置再点击.
    """
    point = win32.POINT()
    win32.GetCursorPos(ctypes.byref(point))
    x_0 = point.x
    y_0 = point.y
    rect = win32.RECT()
    win32.GetWindowRect(process.pvz_hwnd, ctypes.byref(rect))
    border_width = (rect.right - rect.left - PVZ_WINDOW_WIDTH) / 2
    title_height = rect.bottom - rect.top - border_width - PVZ_WINDOW_HEIGHT
    x_1 = int(rect.left + border_width + x)
    y_1 = int(rect.top + title_height + y)

    distance = pow(pow((x_1 - x_0), 2) + pow((y_1 - y_0), 2), 0.5)
    speed = random.randint(12, 36)  # px/cs
    steps = int(distance / speed)
    for i in range(steps):
        time.sleep(0.01)
        x_tmp = int(x_0 + (x_1 - x_0) * i / steps)
        y_tmp = int(y_0 + (y_1 - y_0) * i / steps)
        win32.SetCursorPos(x_tmp, y_tmp)
    time.sleep(0.01)
    win32.SetCursorPos(x_1, y_1)
    time.sleep(0.05)
    if click:
        left_click(x, y)
    delay = random.randint(10, 20)  # 随机延时
    time.sleep(delay / 100)
