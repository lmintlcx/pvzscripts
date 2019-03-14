# coding=utf-8

"""
Delay
"""

import time

from . import logger
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


def wait_for_game_stop():
    """
    等待战斗结束进入选卡界面.
    """

    while utils.game_ui() != 2:
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
    线程睡眠. 实际睡眠时间依赖于操作系统线程切换时间片精度.

    @参数 time_cs(float): 时间, 单位 cs, 精度 0.1.
    """

    if time_cs > 0.0:
        time.sleep(time_cs / 100)
    elif time_cs == 0.0:
        pass
    else:
        logger.error(f"线程睡眠时间不能小于零.")


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
    elif time_cs == 0:
        pass
    else:
        logger.error(f"游戏延时时间不能小于零.")


def until_countdown(time_cs, hugewave=False):
    """
    等待直至刷新倒计时数值达到指定值.

    调用时需要保证上一波已经刷出. 该函数仅保留兼容旧式写法, 已不推荐使用.

    @参数 time_cs(int): 倒计时数值, 单位 cs, 精度 1. 建议范围 [200, 1].

    第一波最早 599, 旗帜波最早 750.

    @参数 hugewave(bool): 是否为旗帜波, 默认不是. 可用 (波数 % 10 == 0) 判断.

    @示例:

    >>> Countdown(100)  # 非旗帜波 100cs 预判

    >>> Countdown(55, True)  # 旗帜波 55cs 预判

    >>> Countdown(95, wave % 10 == 0)  # 第 wave 波 95cs 预判
    """

    if not hugewave:
        while utils.wave_countdown() > time_cs:
            delay_a_little_time()
    else:
        while utils.wave_countdown() > 5:  # 这里用 5 而不用 4, 为了支持大波 750cs 预判
            delay_a_little_time()
        while utils.huge_wave_countdown() > time_cs:
            delay_a_little_time()


# 倒计时(大波倒计时/初始倒计时)小于等于 200(750/599) 才算激活刷新
refresh_trigger = [750 if wave % 10 == 0 else 599 if wave == 1 else 200 for wave in range(1, 21)]


def until_relative_time_after_refresh(time_relative_cs, wave):
    """
    读内存获取刷新状况, 等待直至与设定波次刷新时间点的差值达到指定值.

    该函数须在每波操作开始时执行一次. 通常用于预判(在设定波次刷新前调用), 也可以在设定波次刷新之后调用.

    @参数 time_relative_cs(int): 与刷新时间点的相对时间, 单位 cs, 精度 1. 建议范围 [-200, 400].

    第一波最早 -599, 旗帜波最早 -750. 为了方便可统一给每波设置 -200 (此时不会检查参数合理性).

    @参数 wave(int): 波数. 用于判断刷新状况以及本波是否为旗帜波.

    @示例:

    >>> Prejudge(-95, wave)  # 95cs 预判

    >>> Prejudge(-150, 20)  # 第 20 波炮炸珊瑚时机

    >>> Prejudge(900 - 200 - 373, wave)  # 900cs 波长反应炸时机
    """

    # 设定波次的刷新时间点
    global refresh_time_point

    now_wave = utils.current_wave()

    # 设定波次还未刷出
    if now_wave < wave:

        # 等待设定预判波次的上一波刷出
        if now_wave < wave - 1:
            while utils.current_wave() < (wave - 1):
                delay_a_little_time()

        # 等到本波触发刷新
        is_huge_wave = wave % 10 == 0
        until_countdown(refresh_trigger[wave - 1], is_huge_wave)

        # 计算实际倒计时数值
        wave_countdown = utils.wave_countdown()
        huge_wave_countdown = utils.huge_wave_countdown()
        if is_huge_wave:
            if wave_countdown in (4, 5):
                countdown = huge_wave_countdown
            else:
                countdown = wave_countdown - 5 + 750
        else:
            countdown = utils.wave_countdown()

        # 计算刷新时间点(倒计时变为下一波初始值时)的时钟数值
        clock = utils.game_clock()
        refresh_time_point = clock + countdown

        # 等待 目标相对时间 和 当前相对时间(即倒计时数值负值) 的差值
        time_to_wait = time_relative_cs + countdown
        if time_to_wait >= 0:
            game_delay_for(time_to_wait)
        else:
            if time_relative_cs not in (-200, -599, -750):
                logger.error(f"第 {wave} 波设定时间 {time_relative_cs} 已经过去, 当前相对时间 {time_relative_cs - time_to_wait}.")

    # 设定波次已经刷出
    elif now_wave == wave:

        # 获取当前时钟/倒计时数值/倒计时初始数值
        clock = utils.game_clock()
        countdown = utils.wave_countdown()
        init_countdown = utils.wave_init_countdown()

        if countdown <= 200:
            logger.warning(f"设定波次 {wave} 的下一波即将刷新, 请调整脚本写法.")

        # 计算刷新时间点(倒计时变为下一波初始值时)的时钟数值
        refresh_time_point = clock - (init_countdown - countdown)

        # 等到设定时间
        time_to_wait = time_relative_cs - (init_countdown - countdown)
        if time_to_wait >= 0:
            game_delay_for(time_to_wait)
        else:
            if time_relative_cs not in (-200, -599, -750):
                logger.error(f"第 {wave} 波设定时间 {time_relative_cs} 已经过去, 当前相对时间 {time_relative_cs - time_to_wait}.")

    # 设定波次的下一波已经刷出
    else:
        logger.error(f"设定波次 {wave} 的下一波已经刷新, 请调整脚本写法.")


def until_relative_time(time_relative_cs):
    """
    等待直至当前时间戳与本波刷新时间点的差值达到指定值.

    该函数需要配合 Prejudge() 使用. 多个 Until() 连用时注意调用顺序必须符合时间先后顺序.

    @参数 time_relative_cs(int): 相对时间, 单位 cs, 精度 1. 建议范围 [-200, 2300].

    @示例:

    >>> Until(-95)  # 刷新前 95cs

    >>> Until(180)  # 刷新后 180cs

    >>> Until(-150)  # 炮炸珊瑚可用时机

    >>> Until(444 - 373)  # 444cs 生效炮发射时机

    >>> Until(601 + 20 - 298)  # 加速波下一波 20cs 预判冰点咖啡豆时机

    >>> Until(601 + 5 - 100 - 320)  # 加速波下一波 5cs 预判冰复制冰种植时机

    >>> Until(1200 - 200 - 373)  # 1200cs 波长激活炸时机

    >>> Until(4500 - 5)  # 收尾波拖满时红字出现时机

    >>> Until(5500)  # 最后一大波白字出现时机
    """

    # while (utils.game_clock() - refresh_time_point) < time_relative_cs:
    #     delay_a_little_time()

    time_to_wait = time_relative_cs - (utils.game_clock() - refresh_time_point)
    if time_to_wait >= 0:
        game_delay_for(time_to_wait)
    else:
        logger.error(f"设定时间 {time_relative_cs} 已经过去, 当前相对时间 {time_relative_cs - time_to_wait}.")
