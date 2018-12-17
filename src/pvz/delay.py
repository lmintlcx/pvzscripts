# coding=utf-8

"""
Delay
"""

import time

from . import utils


# 大量占用 CPU, 默认不开启
high_precision = False


# 当前波次刷新时间点
refresh_time_point = 0


def wait_for_game_start():
    """
    选卡后等待直至正式开始战斗.
    """
    while utils.game_ui() != 3:
        time.sleep(0.01)


# 没什么卵用, 暂不开放接口
def enable_high_precision(on=True):
    """
    启用高精度键控, 缺点是会占满一个核心的 CPU 资源.

    @参数 on(bool): 是否启用
    """
    global high_precision
    high_precision = on


def thread_sleep_for(time_cs):
    """
    线程睡眠. 依赖于操作系统线程切换时间片精度, 误差较大.

    @参数 time_cs(float): 时间, 单位 cs, 精度 0.1.
    """
    if time_cs > 0.0:
        time.sleep(time_cs / 100)


def delay_a_little_time():
    """
    细微延时. 高精度情况下采用自旋等待, 否则阻塞等待.
    """
    if high_precision:
        pass
    else:
        thread_sleep_for(0.1)  # 1ms


def game_delay_for(time_cs):
    """
    游戏内部时钟延时. 相对于线程睡眠更精确.

    只能在战斗界面 `[[0x6A9EC0]+0x7FC] == 3` 使用. 游戏暂停时计时同样暂停.

    @参数 time_cs(int): 时间, 单位 cs, 精度 1.
    """
    if time_cs > 0:
        clock = utils.game_clock()
        while (utils.game_clock() - clock) < time_cs:
            delay_a_little_time()


def until_countdown(time_cs, hugewave=False):
    """
    等待直至本波刷新倒计时数值达到指定值. 调用时需要保证上一波已经刷出.

    @参数 time_cs(int): 倒计时数值, 单位 cs, 精度 1. 范围 [200, 1].

    @参数 hugewave(bool): 是否为旗帜波, 默认不是. 可用 (波数 % 10 == 0) 判断.

    @示例:

    >>> until_countdown(95)  # 非旗帜波 95cs 预判

    >>> until_countdown(55, True)  # 旗帜波 55cs 预判
    """
    if not hugewave:
        while utils.wave_countdown() > time_cs:
            delay_a_little_time()
    else:
        while utils.wave_countdown() > 5:
            delay_a_little_time()
        while utils.huge_wave_countdown() > time_cs:
            delay_a_little_time()


def until_relative_time_after_refresh(time_relative_cs, wave):
    """
    等待上一波刷新并且当前时间戳与本波刷新时间点的差值达到指定值.

    该函数只能在每波操作开始时执行一次. 用于重置本波刷新时间点数值.

    @参数 time_relative_cs(int): 相对时间, 单位 cs, 精度 1. 建议范围 [-200, 400].

    @参数 wave(int): 波数. 用于判断上一波是否已经刷出以及本波是否为旗帜波.

    @示例:

    >>> until_relative_time_after_refresh(-95, wave)  # 95cs 预判

    >>> until_relative_time_after_refresh(-55, wave)  # 55cs 预判

    >>> until_relative_time_after_refresh(-150, 20)  # 第 20 波炮炸珊瑚

    >>> until_relative_time_after_refresh(900 - 200 - 373, wave)  # 900cs 波长反应炸
    """
    global refresh_time_point

    # 等待设定预判波次的上一波刷出
    while utils.current_wave() < (wave - 1):
        delay_a_little_time()

    # 倒计时(大波倒计时)小于等于 200(750) 才算激活刷新
    huge_wave = wave % 10 == 0
    # until_countdown(200, huge_wave)
    until_countdown(750 if huge_wave else 200, huge_wave)

    # 获取当前时钟和倒计时数值
    clock = utils.game_clock()
    if huge_wave:
        countdown = utils.huge_wave_countdown()
    else:
        countdown = utils.wave_countdown()

    # 计算刷新时间点(倒计时归零时)的时钟数值
    refresh_time_point = clock + countdown

    # 等待目标相对时间和当前相对时间的差值
    # time_relative_cs - (-countdown)
    game_delay_for(time_relative_cs + countdown)


def until_relative_time(time_relative_cs):
    """
    等待直至当前时间戳与本波刷新时间点的差值达到指定值.

    该函数需要配合 until_relative_time_after_refresh() 使用.

    @参数 time_relative_cs(int): 相对时间, 单位 cs, 精度 1. 建议范围 [-200, 2300].

    @示例:

    >>> until_relative_time(-15)  # 刷新前 15cs

    >>> until_relative_time(1150 - 200 - 373)  # 1150cs 波长激活炸
    """
    while (utils.game_clock() - refresh_time_point) < time_relative_cs:
        delay_a_little_time()
