# coding=utf-8

"""
Operate
"""

import threading
import functools

from . import logger
from . import delay
from . import utils
from . import mouse
from . import seeds
from . import cobs
from . import scene
from . import threads


# 进行完整的(不可分割的)鼠标操作时加锁
mouse_lock = threading.Lock()

###
###
###


def use_seed(seed, *crood):
    """
    用卡操作.

    @参数 seed(int/str): 卡槽第几格或者卡片名称.

    @参数 crood(int/tuple): 坐标, 两个分别表示 行/列 的数字或者一个 (行, 列) 元组, 数字均为整数.

    @示例:

    >>> use_seed(1, 2, 3)  # use_seed(1, (2, 3))  # 将卡槽中的第 1 张卡片种在 2 行 3 列

    >>> use_seed("樱桃", 5, 9)  # use_seed("樱桃", (5, 9))  # 将樱桃种在 5 行 9 列
    """
    if isinstance(seed, str):
        seed_type = seeds.get_seed_by_name(seed)
        slot_index = seeds.get_index_by_seed(seed_type)
    else:  # int
        seed_type = seeds.get_seed_by_index(seed)
        slot_index = seed

    # 墓碑/咖啡豆 理想种植坐标偏上约 30px
    if seed_type in (11, 35, 11 + 48, 35 + 48):
        row_fix = -0.3
    else:
        row_fix = 0
    if isinstance(crood[0], tuple):
        row, col = crood[0]
    else:
        row, col = crood
    row += row_fix

    mouse_lock.acquire()
    mouse.safe_click()
    scene.click_seed(slot_index)
    scene.click_grid((row, col))
    mouse.safe_click()
    mouse_lock.release()

    logger.info(f"Use seed {seed} to {crood}.")


###
###
###


def use_shovel(*crood):
    """
    用铲子操作.

    @参数 crood(float/tuple): 坐标, 两个分别表示 行/列 的数字或者一个 (行, 列) 元组, 数字可为小数.

    @示例:

    >>> use_shovel(2, 3)  # use_shovel((2, 3))  # 铲掉 2 行 3 列的普通植物

    >>> use_shovel(5.1, 6)  # use_shovel((5 + 0.1, 6))  # 铲掉 5 行 6 列的南瓜头
    """
    mouse_lock.acquire()
    mouse.safe_click()
    scene.click_shovel()
    scene.click_grid(*crood)
    mouse.safe_click()
    mouse_lock.release()

    logger.info(f"Use shovel to {crood}.")


###
###
###


@functools.singledispatch
def fire_cob(*params):
    """
    用炮操作.

    @参数 params(float/tuple/list): 落点.

    用两个数字指定落点行数和列数, 为了避免炮落点位于自身附近点击失效可设置第三个延时参数或者调换连续两炮的顺序.

    落点参数还可以为一至多个格式为 (行, 列) 的元组, 或者一个包含了这些元组的列表.

    @示例:

    >>> fire_cob(2, 9)

    >>> fire_cob(5, 7, 30)  # 点炮身延迟 30cs 再发射

    >>> fire_cob((2, 7.8))

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
    cob_row, cob_col = cobs.cob_list[cobs.cob_index]
    fire_cob_by_crood(cob_row, cob_col, fall_row, fall_col, time_delay_cs)
    cobs.cob_index += 1
    cobs.cob_index %= cob_count
    cobs.cob_lock.release()


@fire_cob.register(tuple)
def _(*fall_grids):
    cob_count = len(cobs.cob_list)
    
    if cob_count == 0:
        raise Exception("你他娘的意大利炮呢...")

    cobs.cob_lock.acquire()
    for grid in fall_grids:
        cob_row, cob_col = cobs.cob_list[cobs.cob_index]
        fall_row, fall_col = grid
        fire_cob_by_crood(cob_row, cob_col, fall_row, fall_col)
        cobs.cob_index += 1
        cobs.cob_index %= cob_count
    cobs.cob_lock.release()


@fire_cob.register(list)
def _(fall_grids):
    fire_cob(*fall_grids)


###
###
###


def skip_cob_index(num):
    """
    跳过列表中一定数量的玉米炮, 通常用于 wave9/19 手动收尾.

    @参数 num(int): 数量.
    """
    cobs.cob_lock.acquire()
    cobs.cob_index += num
    cobs.cob_index %= len(cobs.cob_list)
    cobs.cob_lock.release()

    logger.info(f"Skip cob index for {num}.")


###
###
###


@functools.singledispatch
def try_to_fire_cob(*params):
    """
    自动找炮发射. 此函数开销较大不适合精确键控. 参数格式同 `Pao()`.

    @返回值 (bool): 成功返回 True, 无炮可用或者中途无炮导致发射不完全则返回 False.
    """
    raise Exception("参数格数不对啊...")


@try_to_fire_cob.register(int)
def _(fall_row, fall_col, time_delay_cs=0):
    cob = cobs.get_an_available_cob()
    if cob is not None:
        cob_row, cob_col = cob
        fire_cob_by_crood(cob_row, cob_col, fall_row, fall_col, time_delay_cs)
        delay.game_delay_for(1)  # 等待内存数据更新
        return True
    else:
        return False


@try_to_fire_cob.register(tuple)
def _(*fall_grids):
    for grid in fall_grids:
        fall_row, fall_col = grid
        if not try_to_fire_cob(fall_row, fall_col):
            return False
    return True


@try_to_fire_cob.register(list)
def _(fall_grids):
    return try_to_fire_cob(*fall_grids)


###
###
###


FLYING_TIME = 373

# TODO 开销略大
@threads.running_in_thread
@functools.singledispatch
def fire_cob_on_roof(*params):
    """
    屋顶修正飞行时间发炮. 此函数开销较大不适合精确键控. 只适用于前场 (7~9 列).
    """
    raise Exception("参数格数不对啊...")


@fire_cob_on_roof.register(int)
def _(fall_row, fall_col):
    clock = utils.game_clock()  # 参照时钟
    cob_count = len(cobs.cob_list)

    if cob_count == 0:
        raise Exception("你他娘的意大利炮呢...")

    cobs.cob_lock.acquire()
    cob_row, cob_col = cobs.cob_list[cobs.cob_index]
    cobs.cob_index += 1
    cobs.cob_index %= cob_count
    cobs.cob_lock.release()

    flying_time = cobs.get_cob_flying_time(cob_col, fall_col)
    while (utils.game_clock() - clock) < (FLYING_TIME - flying_time):
        delay.delay_a_little_time()
    fire_cob_by_crood(cob_row, cob_col, fall_row, fall_col)


@fire_cob_on_roof.register(tuple)
def _(*fall_grids):
    clock = utils.game_clock()  # 参照时钟
    cob_count = len(cobs.cob_list)

    if cob_count == 0:
        raise Exception("你他娘的意大利炮呢...")

    # (flying_time, cob_row, cob_col, fall_row, fall_col) x n
    operate_list = []

    cobs.cob_lock.acquire()
    for grid in fall_grids:
        cob_row, cob_col = cobs.cob_list[cobs.cob_index]
        fall_row, fall_col = grid
        flying_time = cobs.get_cob_flying_time(cob_col, fall_col)
        operate_list.append((flying_time, cob_row, cob_col, fall_row, fall_col))
        cobs.cob_index += 1
        cobs.cob_index %= cob_count
    cobs.cob_lock.release()

    operate_list.sort()  # 根据飞行时间排序
    for op in reversed(operate_list):  # 逆序发射
        flying_time, cob_row, cob_col, fall_row, fall_col = op
        while (utils.game_clock() - clock) < (FLYING_TIME - flying_time):
            delay.delay_a_little_time()
        fire_cob_by_crood(cob_row, cob_col, fall_row, fall_col)


@fire_cob_on_roof.register(list)
def _(fall_grids):
    return fire_cob_on_roof(*fall_grids)


###
###
###


# 更换的玉米炮
cob_cannon_to_be_replaced = None


def set_replace_cob_cannon(*crood):
    """
    设置要更换的玉米炮. 下一次该门炮发射后会自动替换并在可用时更新炮列表相关数据.

    @参数 crood(int/tuple): 坐标, 两个分别表示 行/列 的数字或者一个 (行, 列) 元组.
    """
    if isinstance(crood[0], tuple):
        row, col = crood[0]
    else:
        row, col = crood

    global cob_cannon_to_be_replaced
    cob_cannon_to_be_replaced = (row, col)


# 炮身点击次数
click_count = 3

# 无视内置炮列表直接指定炮位和落点的函数
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

    # 如果正在发射的炮需要更换的话
    global cob_cannon_to_be_replaced
    if (cob_row, cob_col) == cob_cannon_to_be_replaced:
        threads.replace_cob_cannon(cob_cannon_to_be_replaced)
        cob_cannon_to_be_replaced = None

    logger.info(
        f"Fire Cob Cannon {cobs.cob_index}"
        f" from {(cob_row, cob_col)}"
        f" to {(fall_row, fall_col)}"
        f" delay {time_delay_cs}."
    )
