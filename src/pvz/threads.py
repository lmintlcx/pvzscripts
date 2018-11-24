# coding=utf-8

"""
Threads
"""

import functools
import threading
import time

from . import logger
from . import process
from . import utils
from . import delay
from . import mouse
from . import seeds
from . import scene
from . import operate


### 子线程装饰器

# TODO 守护线程?
def running_in_thread(func):
    """
    将此装饰器应用到需要在子线程运行的函数上.
    """

    @functools.wraps(func)  # 复制原函数元信息
    def wrapper(*args, **kwargs):
        thread = threading.Thread(target=func, args=args, kwargs=kwargs)
        thread.start()

    return wrapper


### Auto Collect Thread


# 1.silver_coin 2.gold_coin 3.diamond 4.sun 5.small_sun 6.big_sun 17.sprout
# TODO  接受列表参数包括汉字
@running_in_thread
def auto_collect(collect_items=[1, 2, 3, 4, 5, 6, 17], interval_cs=12):
    """
    自动收集场上资源. 在单独的子线程运行.

    为了避免操作冲突, 鼠标光标放到游戏窗口内部时会暂停收集.

    @参数 collect_items(list): 需要收集的资源类型.

    1.银币 2.金币 3.钻石 4.阳光 5.小阳光 6.大阳光 17.幼苗

    @参数 interval_cs(float): 间隔, 单位 cs, 默认 12.

    @示例:

    >>> auto_collect()

    >>> auto_collect([3, 4, 5, 6], 20)  # 只收集钻石和阳光, 间隔 0.2s
    """
    interval = interval_cs / 100

    while utils.game_ui() != 3:
        time.sleep(0.1)

    logger.info("Start automatic collection.")

    while utils.game_ui() == 3:
        item_count = process.read_memory("int", 0x6A9EC0, 0x768, 0xF4)
        item_count_max = process.read_memory("int", 0x6A9EC0, 0x768, 0xE8)
        item_offset = process.read_memory("int", 0x6A9EC0, 0x768, 0xE4)

        if item_count == 0:
            time.sleep(interval)
            continue

        uncollected_item_count = 0
        for i in range(item_count_max):
            disappeared = process.read_memory("bool", item_offset + 0x38 + 0xD8 * i)
            collected = process.read_memory("bool", item_offset + 0x50 + 0xD8 * i)
            item_type = process.read_memory("int", item_offset + 0x58 + 0xD8 * i)
            if not disappeared and not collected and item_type in collect_items:
                uncollected_item_count += 1
        if uncollected_item_count == 0:
            time.sleep(interval * 3)  # 等久一点
            continue

        for i in range(item_count_max):
            if utils.game_ui() != 3:
                break
            # while game_paused() or (mouse_in_game() and mouse_have_something()):
            while utils.game_paused() or utils.mouse_in_game():
                time.sleep(interval)

            disappeared = process.read_memory("bool", item_offset + 0x38 + 0xD8 * i)
            collected = process.read_memory("bool", item_offset + 0x50 + 0xD8 * i)
            item_type = process.read_memory("int", item_offset + 0x58 + 0xD8 * i)
            if not disappeared and not collected and item_type in collect_items:
                # write_memory("bool", True, item_offset + 0x50 + 0xd8 * i)
                # time.sleep(interval)

                item_x = process.read_memory("float", item_offset + 0x24 + 0xD8 * i)
                item_y = process.read_memory("float", item_offset + 0x28 + 0xD8 * i)
                if item_x >= 0.0 and item_y >= 70.0:
                    operate.mouse_lock.acquire()
                    mouse.safe_click()
                    x, y = int(item_x + 30), int(item_y + 30)
                    mouse.left_click(x, y)
                    mouse.safe_click()
                    operate.mouse_lock.release()

                    logger.info(f"Collect item {item_type} at {(x, y)}.")
                    time.sleep(interval)

    logger.info("Stop automatic collection.")


### Auto Fill Ice Thread


# 存冰位
ice_spots = []


# 获取所有寒冰菇卡片的下标.
def get_ice_seed_list():
    ice_seeds = []
    slots_count = process.read_memory("int", 0x6A9EC0, 0x768, 0x144, 0x24)
    slots_offset = process.read_memory("unsigned int", 0x6A9EC0, 0x768, 0x144)
    for i in range(slots_count):
        seed_type = process.read_memory("int", slots_offset + 0x5C + i * 0x50)
        seed_imitater_type = process.read_memory("int", slots_offset + 0x60 + i * 0x50)
        if seed_type == 14 or (seed_type == 48 and seed_imitater_type == 14):
            ice_seeds.append(i)
    logger.info(f"Get ice seed index {[i + 1 for i in ice_seeds]}.")
    return ice_seeds

# # 获取所有场上寒冰菇的坐标.
# def get_ice_spots_list():
#     croods = []
#     plant_count_max = process.read_memory("unsigned int", 0x6A9EC0, 0x768, 0xB0)
#     plant_offset = process.read_memory("unsigned int", 0x6A9EC0, 0x768, 0xAC)
#     for i in range(plant_count_max):
#         plant_disappeared = process.read_memory("bool", plant_offset + 0x141 + 0x14C * i)
#         plant_crushed = process.read_memory("bool", plant_offset + 0x142 + 0x14C * i)
#         plant_type = process.read_memory("int", plant_offset + 0x24 + 0x14C * i)
#         plant_imitater_type = process.read_memory("int", plant_offset + 0x138 + 0x14C * i)
#         if (
#             not plant_disappeared
#             and not plant_crushed
#             and (plant_type == 14 or (plant_type == 48 and plant_imitater_type == 14))
#         ):
#             plant_row = process.read_memory("int", plant_offset + 0x1C + 0x14C * i)
#             plant_col = process.read_memory("int", plant_offset + 0x28 + 0x14C * i)
#             crood = (plant_row + 1, plant_col + 1)
#             croods.append(crood)
#     logger.info(f"Get ice spots list {croods}.")
#     return croods


# 获取已设定存冰位不可存冰的坐标列表.
def get_ice_spots_list():
    croods = []  # 有植物
    plant_count_max = process.read_memory("unsigned int", 0x6A9EC0, 0x768, 0xB0)
    plant_offset = process.read_memory("unsigned int", 0x6A9EC0, 0x768, 0xAC)
    for i in range(plant_count_max):
        plant_disappeared = process.read_memory("bool", plant_offset + 0x141 + 0x14C * i)
        plant_crushed = process.read_memory("bool", plant_offset + 0x142 + 0x14C * i)
        plant_type = process.read_memory("int", plant_offset + 0x24 + 0x14C * i)
        if not plant_disappeared and not plant_crushed and plant_type not in (16, 30, 33):  # 睡莲/南瓜/花盆
            plant_row = process.read_memory("int", plant_offset + 0x1C + 0x14C * i)
            plant_col = process.read_memory("int", plant_offset + 0x28 + 0x14C * i)
            crood = (plant_row + 1, plant_col + 1)
            croods.append(crood)
            if plant_type == 47:  # 玉米炮占两格
                crood = (plant_row + 1, plant_col + 1 + 1)
                croods.append(crood)
    croods_in_ice_spot_which_has_plant = [i for i in ice_spots if i in croods]
    logger.info(f"Get ice spots list {croods_in_ice_spot_which_has_plant}.")
    return croods_in_ice_spot_which_has_plant


@running_in_thread
def auto_fill_ice(spots=None, total=0xFFFFFFFF):
    """
    自动存冰. 在单独的子线程运行.

    @参数 spots(list): 存冰点, 包括若干个 (行, 列) 元组. 永久位在前, 临时位在后. 默认为场上现有存冰的位置.

    @参数 total(int): 总个数, 默认无限.

    @示例:

    >>> auto_fill_ice()

    >>> auto_fill_ice([(6, 1), (5, 1), (2, 1), (1, 1)], 10)
    """

    while utils.game_ui() != 3:
        time.sleep(0.01)

    logger.info("Start automatic fill ice.")

    if spots is None:
        spots = get_ice_spots_list()
    global ice_spots
    ice_spots = spots

    slots_offset = process.read_memory("unsigned int", 0x6A9EC0, 0x768, 0x144)

    ice_seeds_index = get_ice_seed_list()  # 保存所有寒冰菇卡片的序号

    filled = 0  # 已存数量
    while utils.game_ui() == 3 and filled < total:

        while utils.game_paused():
            time.sleep(0.01)  # 等待暂停取消

        current_ice_spots = get_ice_spots_list()
        if utils.game_ui() != 3 and current_ice_spots == []:
            break
        if set(current_ice_spots) >= set(spots):  # 存冰位植物满了
            # time.sleep(0.1)  # TODO 0.01
            # continue
            ice_seeds_cd_left = []
            for i in ice_seeds_index:
                seed_usable = process.read_memory("bool", slots_offset + 0x70 + i * 0x50)
                seed_cd_past = process.read_memory("int", slots_offset + 0x4C + i * 0x50)
                seed_cd_total = process.read_memory("int", slots_offset + 0x50 + i * 0x50)
                ice_seeds_cd_left.append(0 if seed_usable else (seed_cd_total - seed_cd_past))
            if min(ice_seeds_cd_left) > 0:  # 冰卡都在冷却时等待最小的卡片CD
                logger.info(f"All ice cooldown, delay for {min(ice_seeds_cd_left) + 1}.")
                delay.game_delay_for(min(ice_seeds_cd_left) + 1)
                continue
            else:  # 冰卡可用时等待用咖啡豆 TODO
                time.sleep(0.1)
                continue

        # 遍历指定的存冰位
        for spot in spots:
            if utils.game_ui() != 3:
                break

            # 如果该位置无冰则尝试存冰
            if spot not in current_ice_spots:
                # 遍历寒冰菇卡片, 通常为 原版冰 x 1 + 复制冰 x 1
                for i in ice_seeds_index:
                    seed_usable = process.read_memory("bool", slots_offset + 0x70 + i * 0x50)
                    seed_ice_cost = process.read_memory("int", 0x69F2C0 + 14 * 0x24)
                    sun = process.read_memory("int", 0x6A9EC0, 0x768, 0x5560)
                    if seed_usable and sun >= seed_ice_cost:  # TODO 无视阳光
                        while utils.game_paused():
                            time.sleep(0.01)  # 等待暂停取消
                        operate.mouse_lock.acquire()
                        mouse.safe_click()
                        scene.click_seed(i + 1)
                        scene.click_grid(spot)
                        mouse.safe_click()
                        operate.mouse_lock.release()
                        filled += 1
                        logger.info(f"Fill ice spot {spot} with seed {i+1}.")
                        delay.game_delay_for(1)  # 等待内存数据更新
                        break
                    else:
                        time.sleep(0.01)
                break  # 不管有没有成功都重新遍历存冰位以保证顺序(先永久位后临时位)
            else:
                pass

    logger.info("Stop automatic fill ice.")


def activate_ice():
    """
    点冰. 使用咖啡豆激活存冰.

    优先点临时位. 该函数需要配合自动存冰线程 auto_fill_ice() 使用.
    """
    operate.mouse_lock.acquire()
    mouse.safe_click()
    scene.click_seed(seeds.seeds_in_slot[35])  # 咖啡豆
    for spot in reversed(ice_spots):  # 优先点临时位
        scene.click_grid(spot)
    mouse.safe_click()
    operate.mouse_lock.release()
