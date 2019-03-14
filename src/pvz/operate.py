# coding=utf-8

"""
Operate
"""

import functools
import random

from . import logger
from . import process
from . import delay
from . import utils
from . import mouse
from . import seeds
from . import cobs
from . import scene
from . import threads


###
###
###


def use_seed(seed, *crood):
    """
    用卡操作.

    @参数 seed(int/str): 卡槽第几格或者卡片名称.

    @参数 crood(int/tuple): 坐标, 两个分别表示 行/列 的数字或者一个 (行, 列) 元组, 数字均为整数.

    @示例:

    >>> Card(1, (2, 3))  # 将卡槽中的第 1 张卡片种在 2 行 3 列

    >>> Card("樱桃", (5, 9))  # 将樱桃种在 5 行 9 列

    >>> Card(1, 2, 3)  # 不推荐

    >>> Card("樱桃", 5, 9)  # 不推荐
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

    scene.mouse_lock.acquire()
    scene.safe_click()
    scene.click_seed(slot_index)
    scene.click_grid((row, col))
    scene.safe_click()
    scene.mouse_lock.release()

    if isinstance(seed, str):
        logger.info(f"向 {crood} 种植 {seed} 卡片.")
    else:  # int
        logger.info(f"向 {crood} 种植卡槽第 {seed} 张卡片.")


###
###
###


def use_shovel(*croods):
    """
    用铲子操作.

    @参数 croods(float/tuple): 坐标, 两个分别表示 行/列 的数字或者一至多个 (行, 列) 元组, 数字可为小数.

    @示例:

    >>> Shovel((3, 4))  # 铲掉 3 行 4 列的普通植物

    >>> Shovel((5 + 0.1, 6))  # 铲掉 5 行 6 列的南瓜头

    >>> Shovel((1, 9), (2, 9), (5, 9), (6, 9))  # 铲掉所有 9 列垫材

    >>> Shovel(1, 2)  # 不推荐
    """

    scene.mouse_lock.acquire()
    scene.safe_click()

    if isinstance(croods[0], tuple):
        for crood in croods:
            scene.click_shovel()
            scene.click_grid(crood)
    else:  # float/int
        scene.click_shovel()
        scene.click_grid(*croods)

    scene.safe_click()
    scene.mouse_lock.release()

    logger.info(f"对格子 {croods} 使用铲子.")


###
###
###


@functools.singledispatch
def fire_cob(*croods):
    """
    用炮操作.

    @参数 croods(float/tuple/list): 落点, 一至多个格式为 (行, 列) 的元组, 或者一个包含了这些元组的列表.

    为了避免炮落点位于自身附近点击失效可设置额外的延时参数(发射单门炮时)或者调换连续两炮的顺序(发射多门炮时).

    @示例:

    >>> Pao((2, 9))

    >>> Pao((2, 9), (5, 9), (2, 9), (5, 9))

    >>> Pao((5, 7), 30)  # 点炮身延迟 30cs 再发射

    >>> Pao((5, 4), (1, 4))  # 调整炮序

    >>> Pao(2, 9)  # 不推荐

    >>> Pao(5, 7, 30)  # 不推荐

    >>> Pao([(2, 9), (5, 9), (2, 9), (5, 9)])  # 不推荐
    """
    logger.error("参数格式不正确.")


@fire_cob.register(int)
def _(fall_row, fall_col, time_delay_cs=0):
    cob_count = len(cobs.cob_list)

    if cob_count == 0:
        logger.error("炮列表为空.")

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
        logger.error("炮列表为空.")

    if len(fall_grids) == 2 and isinstance(fall_grids[1], int):
        cobs.cob_lock.acquire()
        cob_row, cob_col = cobs.cob_list[cobs.cob_index]
        fall_row, fall_col = fall_grids[0]
        time_delay_cs = fall_grids[1]
        fire_cob_by_crood(cob_row, cob_col, fall_row, fall_col, time_delay_cs)
        cobs.cob_index += 1
        cobs.cob_index %= cob_count
        cobs.cob_lock.release()
        return

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
    按炮列表顺序跳过即将发射的一定数量的玉米炮, 通常用于 wave9/19 手动收尾.

    @参数 num(int): 数量.
    """
    cobs.cob_lock.acquire()
    cobs.cob_index += num
    cobs.cob_index %= len(cobs.cob_list)
    cobs.cob_lock.release()

    logger.info(f"跳过炮列表中的 {num} 门炮.")


###
###
###


@functools.singledispatch
def try_to_fire_cob(*croods):
    """
    自动找炮发射.

    此函数有一定开销, 不可连续使用(间隔至少 1cs). 参数格式同 `Pao()`.

    @返回值 (bool): 成功返回 True, 无炮可用或者中途无炮导致发射不完全则返回 False.
    """
    logger.error("参数格式不正确.")


@try_to_fire_cob.register(int)
def _(fall_row, fall_col, time_delay_cs=0):
    available_cobs = cobs.get_available_cobs()
    if available_cobs == []:
        return False  # 无炮可用, 发射失败
    else:
        if len(available_cobs) > 1:
            index = random.randint(0, len(available_cobs) - 1)
            cob_row, cob_col = available_cobs[index]
        else:
            cob_row, cob_col = available_cobs[0]
        fire_cob_by_crood(cob_row, cob_col, fall_row, fall_col, time_delay_cs)
        return True  # 发射成功


@try_to_fire_cob.register(tuple)
def _(*fall_grids):

    # TryPao((fall_row, fall_col), time_delay_cs)
    if len(fall_grids) == 2 and isinstance(fall_grids[1], int):
        fall_row, fall_col = fall_grids[0]
        time_delay_cs = fall_grids[1]
        return try_to_fire_cob(fall_row, fall_col, time_delay_cs)

    available_cobs = cobs.get_available_cobs()
    if available_cobs == []:
        return False  # 无炮可用, 发射失败
    else:
        random.shuffle(available_cobs)  # 打乱
        for i in range(min(len(available_cobs), len(fall_grids))):  # 发炮次数取可用炮数和落点数的较小值
            cob_row, cob_col = available_cobs[i]
            fall_row, fall_col = fall_grids[i]
            time_delay_cs = 0
            fire_cob_by_crood(cob_row, cob_col, fall_row, fall_col, time_delay_cs)
        return len(available_cobs) >= len(fall_grids)  # 可用炮数小于落点数则发射失败


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
def fire_cob_on_roof(*croods):
    """
    屋顶修正飞行时间发炮.

    此函数开销较大(开新线程)不适合精确键控. 只适用于前场 (约 7~9 列). 参数格式大体与 `Pao()` 相同 (缺少额外的点炮延时参数).
    """
    logger.error("参数格式不正确.")


@fire_cob_on_roof.register(int)
def _(fall_row, fall_col):
    clock = utils.game_clock()  # 参照时钟
    cob_count = len(cobs.cob_list)

    if cob_count == 0:
        logger.error("炮列表为空.")

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
        logger.error("炮列表为空.")

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
    设置要更换的玉米炮, 下一次该门炮发射后会自动替换并在可用时更新炮列表相关数据.

    @参数 crood(int/tuple): 坐标, 两个分别表示 行/列 的数字或者一个 (行, 列) 元组.
    """
    if isinstance(crood[0], tuple):
        row, col = crood[0]
    else:
        row, col = crood

    global cob_cannon_to_be_replaced
    cob_cannon_to_be_replaced = (row, col)


# 炮身点击次数
CLICK_COUNT = 3

# 无视内置炮列表直接指定炮位和落点的函数
def fire_cob_by_crood(cob_row, cob_col, fall_row, fall_col, time_delay_cs=0):

    # 如果开了日志
    if not logger.pvz_logger.disabled:
        cob_index = cobs.cob_list_detailed[cobs.cob_list.index((cob_row, cob_col))][3]
        cob_status = process.read_memory("int", utils.plants_offset + 0x3C + 0x14C * cob_index)
        if cob_status == 35:  # 空炮
            print(f"玉米炮 {(cob_row, cob_col)} 空炮中, 请检查脚本写法.")
        elif cob_status == 36:  # 装填
            print(f"玉米炮 {(cob_row, cob_col)} 装填中, 请检查脚本写法.")
        elif cob_status == 38:  # 发炮
            print(f"玉米炮 {(cob_row, cob_col)} 发炮中, 请检查脚本写法.")
        else:  # 37 有炮
            pass

    scene.mouse_lock.acquire()
    scene.safe_click()
    for _ in range(CLICK_COUNT):
        scene.click_grid(cob_row, cob_col)
    if time_delay_cs > 0:
        delay.game_delay_for(time_delay_cs)
    scene.click_grid(fall_row, fall_col)
    scene.safe_click()
    scene.mouse_lock.release()

    # 如果正在发射的炮需要更换的话
    global cob_cannon_to_be_replaced
    if (cob_row, cob_col) == cob_cannon_to_be_replaced:
        threads.replace_cob_cannon(cob_cannon_to_be_replaced)
        cob_cannon_to_be_replaced = None

    if time_delay_cs in (0, 0.0):
        logger.info(f"从 {(cob_row, cob_col)} 向 {(fall_row, fall_col)} 发射玉米炮.")
    else:
        logger.info(f"从 {(cob_row, cob_col)} 向 {(fall_row, fall_col)} 发射玉米炮, 点炮延时 {time_delay_cs}.")
