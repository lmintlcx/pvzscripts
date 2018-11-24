# coding=utf-8

"""
Utils
"""

from . import process


def game_on():
    """
    @返回值 (bool): 游戏是否开启, 没开则会尝试查找一次.
    """
    if process.is_valid():
        return True
    else:
        return process.find_pvz_1051()


# 13. Survival: Endless
def game_mode():
    """
    @返回值 (int): 游戏模式
    """
    return process.read_memory("int", 0x6A9EC0, 0x7F8)


# 1: 主界面, 2: 选卡, 3: 正常游戏, 4: 僵尸进屋, 7: 模式选择
def game_ui():
    """
    @返回值 (int): 游戏界面
    """
    return process.read_memory("int", 0x6A9EC0, 0x7FC)


# 0: 白天, 1: 黑夜, 2: 泳池, 3: 浓雾, 4: 屋顶, 5: 月夜
def game_scene():
    """
    @返回值 (int): 游戏场景
    """
    return process.read_memory("int", 0x6A9EC0, 0x768, 0x554C)


def game_paused():
    """
    @返回值 (bool): 游戏是否暂停
    """
    return process.read_memory("bool", 0x6A9EC0, 0x768, 0x164)


def mouse_in_game():
    """
    @返回值 (bool): 鼠标是否在游戏窗口内部
    """
    return process.read_memory("bool", 0x6A9EC0, 0x768, 0x59)
    # return read_memory("bool", 0x6A9EC0, 0x768, 0x138, 0x18)


def mouse_have_something():
    """
    @返回值 (bool): 鼠标是否选中卡炮或铲子
    """
    return process.read_memory("int", 0x6A9EC0, 0x768, 0x138, 0x30) in (1, 6, 8)


def game_clock():
    """
    @返回值 (int): 一个内部时钟, 游戏暂停时停止计时.
    """
    return process.read_memory("int", 0x6A9EC0, 0x768, 0x5568)


def wave_countdown():
    """
    @返回值 (int): 下一波刷新倒计时, 触发刷新时重置为 200, 减少至 0 刷出下一波.
    """
    return process.read_memory("int", 0x6A9EC0, 0x768, 0x559C)


def huge_wave_countdown():
    """
    @返回值 (int): 大波刷新倒计时, 对于旗帜波, 刷新倒计时减少至 4 后停滞, 由该值代替减少.
    """
    return process.read_memory("int", 0x6A9EC0, 0x768, 0x55A4)


def current_wave():
    """
    @返回值 (int): 当前波数
    """
    return process.read_memory("int", 0x6A9EC0, 0x768, 0x557C)


def dance_clock():
    """
    @返回值 (int): 一个内部时钟, 可用于判断舞王/伴舞的舞蹈/前进.
    """
    return process.read_memory("int", 0x6A9EC0, 0x838)
