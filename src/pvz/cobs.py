# coding=utf-8

"""
Cobs
"""

import threading

from . import logger
from . import process


# (row, col) x n
cob_list = []

# index of current cob in list
cob_index = 0

# 修改以上两个变量时加锁
cob_lock = threading.Lock()


# TODO 排序
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

    global cob_list, cob_index

    if cobs is not None:
        cob_lock.acquire()
        cob_list = cobs
        cob_index = 0
        cob_lock.release()

    else:
        cob_lock.acquire()
        cob_list = []
        plant_count_max = process.read_memory("unsigned int", 0x6A9EC0, 0x768, 0xB0)
        plant_offset = process.read_memory("unsigned int", 0x6A9EC0, 0x768, 0xAC)
        for i in range(plant_count_max):
            plant_disappeared = process.read_memory("bool", plant_offset + 0x141 + 0x14C * i)
            plant_crushed = process.read_memory("bool", plant_offset + 0x142 + 0x14C * i)
            plant_type = process.read_memory("int", plant_offset + 0x24 + 0x14C * i)
            if not plant_disappeared and not plant_crushed and plant_type == 47:
                plant_row = process.read_memory("int", plant_offset + 0x1C + 0x14C * i)
                plant_col = process.read_memory("int", plant_offset + 0x28 + 0x14C * i)
                cob = (plant_row + 1, plant_col + 1)
                cob_list.append(cob)
        cob_list.sort()
        cob_index = 0
        cob_lock.release()

    logger.info(f"Update Cob Cannon list {cob_list}.")
