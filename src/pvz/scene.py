# coding=utf-8

"""
Scene
"""

from . import logger
from . import process
from . import seeds
from . import mouse


# 卡槽格数, 选卡和用卡函数需要
slots_count = 10

# 场景地图, 点击场上格子相关函数需要
# 0. day
# 1. night
# 2. pool
# 3. fog
# 4. roof
# 5. moon
# 6. mushroom garden
# 7. zen garden
# 8. aquarium garden
# 9. tree of wisdom
game_scene = 2


def update_game_scene():
    # 更新卡槽格数和场景地图
    global slots_count, game_scene
    slots_count = process.read_memory("int", 0x6A9EC0, 0x768, 0x144, 0x24)
    game_scene = process.read_memory("int", 0x6A9EC0, 0x768, 0x554C)
    logger.info(f"Update slots count {slots_count}.")
    logger.info(f"Update game scene {game_scene}.")


def click_seed(seed):
    """
    点击卡槽中的卡片.

    @参数 seed(int/str): 卡槽第几格或者卡片名称.

    @示例:

    >>> click_seed(5)  # 点击第 5 格卡槽

    >>> click_seed("樱桃")  # 点击卡槽中的樱桃卡片
    """

    if isinstance(seed, str):
        slot_index = seeds.get_index_by_name(seed)
        if slot_index is None:
            raise Exception(f"No seed {seed} in slots, operation failed.")
    else:  # int
        slot_index = seed
        if slot_index not in range(1, 11):
            raise Exception(f"Index {slot_index} out of range, operation failed.")

    if slots_count == 10:
        x = 63 + 51 * slot_index
    elif slots_count == 9:
        x = 63 + 52 * slot_index
    elif slots_count == 8:
        x = 61 + 54 * slot_index
    elif slots_count == 7:
        x = 61 + 59 * slot_index
    else:
        x = 61 + 59 * slot_index
    y = 12
    mouse.left_click(x, y)


def click_shovel():
    """
    点击铲子.
    """
    if slots_count == 10:
        x = 640
    elif slots_count == 9:
        x = 600
    elif slots_count == 8:
        x = 570
    elif slots_count == 7:
        x = 550
    else:
        x = 490
    y = 36
    mouse.left_click(x, y)


# 坐标转换
def rc2xy(*crood):
    """
    row, col -> x, y
    """

    if isinstance(crood[0], tuple):
        row, col = crood[0]
    else:
        row, col = crood

    x = 80 * col
    if game_scene in (2, 3):
        y = 55 + 85 * row
    elif game_scene in (4, 5):
        if col >= 6:
            y = 45 + 85 * row
        else:
            y = 45 + 85 * row + 20 * (6 - col)
    else:
        y = 40 + 100 * row

    return int(x), int(y)  # 取整


def click_grid(*crood):
    """
    点击场上格点.

    @参数 crood(float/tuple): 坐标, 两个分别表示 行/列 的数字或者一个 (行, 列) 元组, 数字可为小数.

    @示例:

    >>> click_grid(2, 9)  # click_grid((2, 9))  # 点击 2 行 9 列
    """
    x, y = rc2xy(*crood)
    mouse.left_click(x, y)
