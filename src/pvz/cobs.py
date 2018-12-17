# coding=utf-8

"""
Cobs
"""

import threading
import random

from . import logger
from . import process


# [cd, row, col, index, status]
cob_list_detailed = []

# (row, col) x n
cob_list = []

# index of current cob in list
cob_index = 0

# 修改以上变量时加锁
cob_lock = threading.Lock()


def update_cob_cannon_list(cobs=None):
    """
    更新玉米加农炮列表.
    
    选卡时自动调用, 空参数则自动找炮. 若需要自定义炮组请在选卡函数后面使用.

    如果出现炮落点位于自身附近快速点击无法发射的现象可通过调整炮序解决.

    @参数 cobs(list): 加农炮列表, 包括若干个 (行, 列) 元组, 以后轮坐标为准.

    @示例:

    >>> update_cob_cannon_list()

    >>> update_cob_cannon_list([(3, 1), (4, 1), (3, 3), (4, 3), (1, 5), (2, 5), (3, 5), (4, 5), (5, 5), (6, 5)])
    """

    global cob_list, cob_list_detailed, cob_index

    if cobs is not None:
        cob_lock.acquire()
        cob_list = cobs
        cob_index = 0
        cob_lock.release()

    else:
        cob_lock.acquire()

        cob_list_detailed = []
        plant_count_max = process.read_memory("unsigned int", 0x6A9EC0, 0x768, 0xB0)
        plant_offset = process.read_memory("unsigned int", 0x6A9EC0, 0x768, 0xAC)
        for i in range(plant_count_max):
            plant_disappeared = process.read_memory("bool", plant_offset + 0x141 + 0x14C * i)
            plant_crushed = process.read_memory("bool", plant_offset + 0x142 + 0x14C * i)
            plant_type = process.read_memory("int", plant_offset + 0x24 + 0x14C * i)
            if not plant_disappeared and not plant_crushed and plant_type == 47:
                cob_row = process.read_memory("int", plant_offset + 0x1C + 0x14C * i)
                cob_col = process.read_memory("int", plant_offset + 0x28 + 0x14C * i)
                cob_fire_left = process.read_memory("int", plant_offset + 0x90 + 0x14C * i)
                cob_empty_left = process.read_memory("int", plant_offset + 0x54 + 0x14C * i)
                cob_status = process.read_memory("int", plant_offset + 0x3C + 0x14C * i)
                if cob_status == 37:  # 有炮
                    cd = 0
                elif cob_status == 36:  # 装填
                    cd = 125  # TODO 装填具体剩余时间?
                elif cob_status == 35:  # 空炮
                    cd = 125 + cob_empty_left
                else:  # elif cob_status == 38:  # 发炮
                    if cob_fire_left == 1:
                        cd = 125 + 3000 + 145  # TODO 发炮剩余时间在 1 停留 145?
                    else:
                        cd = 125 + 3000 + cob_fire_left
                cob_list_detailed.append([cd, cob_row + 1, cob_col + 1, i, cob_status])
        cob_list_detailed.sort()  # 根据剩余冷却时间排序

        cob_list = []
        for cob in cob_list_detailed:
            cob_list.append((cob[1], cob[2]))  # 只需要用到行列
        cob_index = 0

        cob_lock.release()

    logger.info(f"Update Cob Cannon list {cob_list}.")


def get_an_available_cob():
    global cob_list_detailed

    cob_lock.acquire()
    plant_offset = process.read_memory("unsigned int", 0x6A9EC0, 0x768, 0xAC)
    for cob in cob_list_detailed:
        # 根据数组下标更新状态
        cob[4] = process.read_memory("int", plant_offset + 0x3C + 0x14C * cob[3])
    cob_lock.release()

    available_cobs_crood = []
    for cob in cob_list_detailed:
        if cob[4] == 37:
            available_cobs_crood.append((cob[1], cob[2]))
    if len(available_cobs_crood) > 0:
        index = random.randint(0, len(available_cobs_crood) - 1)
        return available_cobs_crood[index]
    else:
        return None


# 只考虑落点前场 7~9 列的情况
flying_time = {1: 359, 2: 362, 3: 364, 4: 367, 5: 369, 6: 372, 7: 373}


def get_cob_flying_time(cob_col, fall_col):
    # TODO fall_col
    if cob_col in flying_time:
        return flying_time[cob_col]
    else:
        return 373
