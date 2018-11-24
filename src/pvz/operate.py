# coding=utf-8

"""
Operate
"""

import threading
import functools

from . import logger
from . import delay
from . import mouse
from . import cobs
from . import scene


# 完整的(不可分割的)鼠标操作前加锁
mouse_lock = threading.Lock()


def use_seed(seed, *crood):
    """
    用卡操作.

    @参数 seed(int/str): 卡槽第几格或者卡片名称.

    @参数 crood(float/tuple): 坐标, 两个分别表示 行/列 的数字或者一个 (行, 列) 元组, 数字可为小数.

    @示例:

    >>> use_seed(1, 2, 3)  # 将第 1 张卡片种在 2 行 3 列

    >>> use_seed("樱桃", (5, 9))  # 将卡槽中的樱桃种在 5 行 9 列
    """
    mouse_lock.acquire()
    mouse.safe_click()
    scene.click_seed(seed)
    scene.click_grid(*crood)
    mouse.safe_click()
    mouse_lock.release()

    logger.info(f"Use seed {seed} to {crood}.")


@functools.singledispatch
def fire_cob(*params):
    """
    用炮操作.

    @参数 params(int/tuple/list): 落点.

    用两个数字指定落点行数和列数, 为了避免炮落点位于自身附近点击失效可设置第三个延时参数或者调换连续两炮的顺序.

    落点参数还可以为一至多个格式为 (行, 列) 的元组, 或者一个包含了这些元组的列表.

    @示例:

    >>> fire_cob(2, 9)

    >>> fire_cob(5, 7, 30)  # 点炮身延迟 30cs 再发射

    >>> fire_cob((2, 9))

    >>> fire_cob((5, 4), (1, 4))  # 调整炮序

    >>> fire_cob([(2, 9), (5, 9), (2, 9), (5, 9)])
    """
    raise Exception("参数格数不对啊...")


@fire_cob.register(int)
def _(fall_row, fall_col, time_delay_cs=0):
    cob_count = len(cobs.cob_list)

    if cob_count == 0:
        raise Exception("你他娘的意大利炮呢...")

    cobs.cob_lock.acquire()
    cobs.cob_index %= cob_count
    cob_row = cobs.cob_list[cobs.cob_index][0]
    cob_col = cobs.cob_list[cobs.cob_index][1]
    fire_cob_by_crood(cob_row, cob_col, fall_row, fall_col, time_delay_cs)
    cobs.cob_index += 1
    cobs.cob_lock.release()


@fire_cob.register(tuple)
def _(*fall_grids):
    cob_count = len(cobs.cob_list)

    if cob_count == 0:
        raise Exception("你他娘的意大利炮呢...")

    cobs.cob_lock.acquire()
    for i in range(len(fall_grids)):
        cobs.cob_index %= cob_count
        cob_row = cobs.cob_list[cobs.cob_index][0]
        cob_col = cobs.cob_list[cobs.cob_index][1]
        fall_row = fall_grids[i][0]
        fall_col = fall_grids[i][1]
        fire_cob_by_crood(cob_row, cob_col, fall_row, fall_col)
        cobs.cob_index += 1
    cobs.cob_lock.release()


@fire_cob.register(list)
def _(fall_grids):
    fire_cob(*fall_grids)


# 炮身点击次数
click_count = 3

# TODO 无视内置炮列表直接指定炮位和落点的函数
def fire_cob_by_crood(cob_row, cob_col, fall_row, fall_col, time_delay_cs=0):
    mouse_lock.acquire()
    mouse.safe_click()
    for _ in range(click_count):
        scene.click_grid(cob_row, cob_col)
    if time_delay_cs > 0:
        delay.game_delay_for(time_delay_cs)
    scene.click_grid(fall_row, fall_col)
    mouse.safe_click()
    mouse_lock.release()

    logger.info(
        f"Fire Cob Cannon index {cobs.cob_index} from {(cob_row, cob_col)} to {(fall_row, fall_col)} delay {time_delay_cs}."
    )


def skip_cob_index(num):
    """
    跳过列表中一定数量的玉米炮, 通常用于 wave9/19 手动收尾.

    @参数 num(int): 数量.
    """
    cobs.cob_lock.acquire()
    cobs.cob_index += num
    cobs.cob_lock.release()

    logger.info(f"Skip cob index for {num}.")


def use_shovel(*crood):
    """
    用铲子操作.

    @参数 crood(float/tuple): 坐标, 两个分别表示 行/列 的数字或者一个 (行, 列) 元组, 数字可为小数.

    @示例:

    >>> use_shovel(2, 3)  # use_shovel((2, 3))  # 铲掉 2 行 3 列的植物
    """
    mouse_lock.acquire()
    mouse.safe_click()
    scene.click_shovel()
    scene.click_grid(*crood)
    mouse.safe_click()
    mouse_lock.release()

    logger.info(f"Use shovel to {crood}.")
