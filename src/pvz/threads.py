# coding=utf-8

"""
Threads
"""

import functools
import threading
import time
import random

from . import logger
from . import process
from . import utils
from . import delay
from . import mouse
from . import keyboard
from . import cobs
from . import seeds
from . import scene
from . import operate


### 子线程装饰器


def running_in_thread(func):
    """
    将此装饰器应用到需要在子线程运行的函数上.

    定义一个函数, 应用该装饰器, 则函数在调用的时候会运行在单独的线程中.

    @示例:

    >>> @RunningInThread
    >>> def func():
    >>>     pass
    """

    @functools.wraps(func)  # 复制原函数元信息
    def wrapper(*args, **kwargs):
        thread = threading.Thread(target=func, args=args, kwargs=kwargs)
        # thread.setDaemon(True)  # TODO 守护线程
        thread.start()

    return wrapper


### Auto Collect Thread

collect_items_dict = {
    "银币": 1,
    "金币": 2,
    "钻石": 3,
    "阳光": 4,
    "小阳光": 5,
    "大阳光": 6,
    "太阳": 4,
    "小太阳": 5,
    "大太阳": 6,
    "幼苗": 17,
    "花苗": 17,
    "盆栽": 17,
    "花盆": 17,
    "礼盒": 17,
    "礼品盒": 17,
    1: 1,
    2: 2,
    3: 3,
    4: 4,
    5: 5,
    6: 6,
    17: 17,
}

item_type_names = {1: "银币", 2: "金币", 3: "钻石", 4: "阳光", 5: "小阳光", 6: "大阳光", 17: "幼苗"}


@running_in_thread
def auto_collect(collect_items=None, interval_cs=12):
    """
    自动收集场上资源, 在单独的子线程运行.

    为了避免操作冲突, 当鼠标选中 卡片/铲子/玉米炮 时会暂停收集. 建议把鼠标光标移出窗口外以避免卡顿.

    @参数 collect_items(list[str/int]): 包含需要收集的资源类型的列表, 默认所有.

    可选值物品名称 ["银币", "金币", "钻石", "阳光", "小阳光", "大阳光", "幼苗"] 或者代号 [1, 2, 3, 4, 5, 6, 17].

    @参数 interval_cs(float/int): 点击间隔, 单位 cs, 默认 12.

    @示例:

    >>> StartAutoCollectThread()  # 自动收集所有资源

    >>> StartAutoCollectThread(["钻石", "阳光", "小阳光", "大阳光"], 20)  # 只收集钻石和各种阳光, 间隔 0.2s
    """

    if collect_items is None:
        collect_items = ["银币", "金币", "钻石", "阳光", "小阳光", "大阳光", "幼苗"]
    collect_items_list = [collect_items_dict[item] for item in collect_items]
    interval = interval_cs / 100

    while utils.game_ui() != 3:
        time.sleep(0.1)

    logger.info("启动自动收集线程.")

    while utils.game_ui() == 3:
        items_count = process.read_memory("int", 0x6A9EC0, 0x768, 0xF4)
        items_count_max = process.read_memory("int", 0x6A9EC0, 0x768, 0xE8)
        items_offset = process.read_memory("int", 0x6A9EC0, 0x768, 0xE4)

        if items_count == 0:
            time.sleep(interval)
            continue

        uncollected_item_count = 0
        for i in range(items_count_max):
            disappeared = process.read_memory("bool", items_offset + 0x38 + 0xD8 * i)
            collected = process.read_memory("bool", items_offset + 0x50 + 0xD8 * i)
            item_type = process.read_memory("int", items_offset + 0x58 + 0xD8 * i)
            if not disappeared and not collected and item_type in collect_items_list:
                uncollected_item_count += 1
        if uncollected_item_count == 0:
            time.sleep(interval * 5)  # 等久一点
            continue

        for i in range(items_count_max):
            if utils.game_ui() != 3:
                break

            # while utils.game_paused():  # 一直收集
            # while utils.game_paused() or utils.mouse_in_game():  # 鼠标移出时收集
            while utils.game_paused() or (utils.mouse_in_game() and utils.mouse_have_something()):  # 没选中卡炮铲时收集
                time.sleep(interval)

            disappeared = process.read_memory("bool", items_offset + 0x38 + 0xD8 * i)
            collected = process.read_memory("bool", items_offset + 0x50 + 0xD8 * i)
            item_type = process.read_memory("int", items_offset + 0x58 + 0xD8 * i)
            if not disappeared and not collected and item_type in collect_items_list:

                item_x = process.read_memory("float", items_offset + 0x24 + 0xD8 * i)
                item_y = process.read_memory("float", items_offset + 0x28 + 0xD8 * i)
                if item_x >= 0.0 and item_y >= 70.0:
                    # process.write_memory("bool", True, items_offset + 0x50 + 0xd8 * i)
                    x, y = int(item_x + 30), int(item_y + 30)
                    scene.mouse_lock.acquire()
                    scene.safe_click()
                    mouse.left_click(x, y)
                    scene.safe_click()
                    scene.mouse_lock.release()

                    logger.debug(f"收集位于 {(x, y)} 的物品 {item_type_names[item_type]}.")
                    # time.sleep(interval)  # TODO 时间波动
                    time.sleep(random.randint(int(interval_cs * 0.5), int(interval_cs * 1.5)) / 100)

    logger.info("停止自动收集线程.")


### Auto Fill Ice Thread

# 存冰位
ice_spots = []


@running_in_thread
def auto_fill_ice(spots=None, total=0x7FFFFFFF):
    """
    自动存冰. 在单独的子线程运行.

    @参数 spots(list): 存冰点, 包括若干个 (行, 列) 元组. 永久位在前, 临时位在后. 默认为场上现有存冰的位置.

    @参数 total(int): 总个数, 默认无限.

    @示例:

    >>> StartAutoFillIceThread()

    >>> StartAutoFillIceThread([(6, 1), (5, 1), (2, 1), (1, 1)], 10)
    """

    while utils.game_ui() != 3:
        time.sleep(0.01)

    logger.info("启动自动存冰线程.")

    # 默认为场上现有存冰的位置
    if spots is None:
        spots = []
        plants = utils.get_plants_croods()
        for plant_type, plant_row, plant_col in plants:
            if plant_type == seeds.get_seed_by_name("寒冰菇"):
                spots.append((plant_row, plant_col))
        if spots == []:
            logger.error(f"场上没有冰蘑菇, 退出自动存冰.")
    global ice_spots
    ice_spots = spots

    slots_offset = process.read_memory("unsigned int", 0x6A9EC0, 0x768, 0x144)

    ice_seeds_index = utils.get_seeds_index("寒冰菇")  # 获取所有寒冰菇卡片的下标
    if ice_seeds_index == []:
        logger.error(f"卡槽没有冰蘑菇, 退出自动存冰.")

    filled = 0  # 已存数量
    while utils.game_ui() == 3 and filled < total:

        while utils.game_paused():
            time.sleep(0.01)  # 等待暂停取消

        croods_which_has_plant = []
        plants = utils.get_plants_croods()
        for plant_type, plant_row, plant_col in plants:
            if plant_type not in (16, 30, 33):  # 睡莲/南瓜/花盆
                croods_which_has_plant.append((plant_row, plant_col))
                if plant_type == 47:  # 玉米炮占两格
                    croods_which_has_plant.append((plant_row, plant_col + 1))
        ice_spot_which_has_plant = [i for i in ice_spots if i in croods_which_has_plant]

        if utils.game_ui() != 3 and ice_spot_which_has_plant == []:
            break

        if set(ice_spot_which_has_plant) >= set(spots):  # 存冰位植物满了
            ice_seeds_cd_left = []
            for i in ice_seeds_index:
                seed_usable = process.read_memory("bool", slots_offset + 0x70 + i * 0x50)
                seed_cd_past = process.read_memory("int", slots_offset + 0x4C + i * 0x50)
                seed_cd_total = process.read_memory("int", slots_offset + 0x50 + i * 0x50)
                ice_seeds_cd_left.append(0 if seed_usable else (seed_cd_total - seed_cd_past))
            if min(ice_seeds_cd_left) > 0:  # 冰卡都在冷却时等待最小的卡片 CD
                logger.info(f"寒冰菇卡片冷却中, 等待 {min(ice_seeds_cd_left) + 1}.")
                delay.game_delay_for(min(ice_seeds_cd_left) + 1)
                continue
            else:  # TODO 冰卡可用时等待用咖啡豆
                time.sleep(0.03)  # 延时减小遍历植物的 CPU 消耗. 0.01~10%  0.05~4%  0.10~1%
                continue

        # 遍历指定的存冰位
        for spot in spots:
            if utils.game_ui() != 3:
                break

            # 如果该位置无植物则尝试存冰
            seed_ice_cost = process.read_memory("int", 0x69F2C0 + 14 * 0x24)
            sun = process.read_memory("int", utils.main_object + 0x5560)
            block_type = utils.get_block_type(spot)
            # 1.草地 2.裸地 3.泳池 16.睡莲 33.花盆
            if (
                spot not in ice_spot_which_has_plant
                and sun >= seed_ice_cost
                and (
                    (block_type == 1 and scene.game_scene not in (4, 5))
                    or (block_type == 1 and scene.game_scene in (4, 5) and (33, spot[0], spot[1]) in plants)
                    or (block_type == 3 and (16, spot[0], spot[1]) in plants)
                )
            ):
                # 遍历寒冰菇卡片, 通常为 原版冰 x 1 + 复制冰 x 1
                for i in ice_seeds_index:
                    seed_usable = process.read_memory("bool", slots_offset + 0x70 + i * 0x50)
                    if seed_usable:
                        while utils.game_paused():
                            time.sleep(0.01)  # 等待暂停取消
                        scene.mouse_lock.acquire()
                        scene.safe_click()
                        scene.click_seed(i + 1)
                        scene.click_grid(spot)
                        scene.safe_click()
                        scene.mouse_lock.release()
                        filled += 1
                        logger.info(f"往 {spot} 存冰 (第 {i+1} 张卡).")
                        delay.game_delay_for(1)  # 等待内存数据更新
                        break
                    else:
                        time.sleep(0.01)
                break  # 不管有没有成功都重新遍历存冰位以保证顺序(先永久位后临时位)
            else:
                pass

    logger.info("停止自动存冰线程.")


def activate_ice():
    """
    点冰. 使用咖啡豆激活存冰, 优先点临时位.

    该函数需要配合自动存冰线程 StartAutoFillIceThread() 使用.
    """
    coffee_index = seeds.get_index_by_seed(35)  # 咖啡豆位置
    if coffee_index is None:
        logger.error(f"卡槽没有咖啡豆, 点冰失败.")

    scene.mouse_lock.acquire()
    scene.safe_click()
    scene.click_seed(coffee_index)
    for spot in reversed(ice_spots):  # 优先点临时位
        row, col = spot
        row -= 0.3  # 咖啡豆 理想种植坐标偏上约 30px
        scene.click_grid((row, col))
    scene.safe_click()
    scene.mouse_lock.release()


@running_in_thread
def immobilize_dancer():
    """
    女仆秘籍. 通过暂停控制舞王/伴舞的跳舞/行走.
    """

    while utils.game_ui() != 3:
        time.sleep(0.01)
    # keyboard.pause_game()

    logger.info("启动女仆秘籍线程.")

    while utils.game_ui() == 3:
        while (((utils.dancer_clock() + 10) % (23 * 20)) // 20) > 11:
            time.sleep(0.01)
        keyboard.pause_game()
        time.sleep(0.5)
        while (((utils.dancer_clock()) % (23 * 20)) // 20) <= 11:
            time.sleep(0.01)
        keyboard.restore_game()

    logger.info("停止女仆秘籍线程.")


@running_in_thread
def replace_cob_cannon(*crood):
    """
    替换玉米加农炮. 完成后自动更新炮列表相关数据.

    @参数 crood(int/tuple): 坐标, 两个分别表示 行/列 的数字或者一个 (行, 列) 元组.
    """
    clock = utils.game_clock()  # 初始参考时钟

    if isinstance(crood[0], tuple):
        row, col = crood[0]
    else:
        row, col = crood

    # 炮列表为空或者指定炮不在列表里
    if len(cobs.cob_list) == 0 or (row, col) not in cobs.cob_list:
        logger.warning(f"指定的玉米炮不存在, 铲种失败.")

    # 没带玉米炮卡片
    if seeds.get_index_by_name("Kernel-pult") is None or seeds.get_index_by_name("Cob Cannon") is None:
        logger.warning(f"卡槽没有玉米和加农炮, 铲种失败.")

    while (utils.game_clock() - clock) < (205 + 1):  # 等待子弹分离
        delay.delay_a_little_time()
    operate.use_shovel((row, col))  # 铲掉
    operate.use_seed("Kernel-pult", (row, col))  # 第一株玉米

    cobs.cob_lock.acquire()
    current_cob = cobs.cob_list[cobs.cob_index]
    cobs.cob_list.remove((row, col))
    cobs.cob_index = cobs.cob_list.index(current_cob)
    for c in cobs.cob_list_detailed:
        if c[1] == row and c[2] == col:
            cobs.cob_list_detailed.remove(c)
            break
    cobs.cob_lock.release()

    while (utils.game_clock() - clock) < (205 + 750 + 2):  # 玉米投手冷却时间
        delay.delay_a_little_time()
    operate.use_seed("Kernel-pult", (row, col + 1))  # 第二株玉米
    operate.use_seed("Cob Cannon", (row, col))  # 升级加农炮

    delay.thread_sleep_for(10)  # 等内存数据更新, 获取新种玉米炮的下标
    new_cob_index = None
    plants_count_max = process.read_memory("int", 0x6A9EC0, 0x768, 0xB0)
    plants_offset = process.read_memory("unsigned int", 0x6A9EC0, 0x768, 0xAC)
    for i in range(plants_count_max):
        plant_disappeared = process.read_memory("bool", plants_offset + 0x141 + 0x14C * i)
        plant_crushed = process.read_memory("bool", plants_offset + 0x142 + 0x14C * i)
        plant_type = process.read_memory("int", plants_offset + 0x24 + 0x14C * i)
        plant_row = process.read_memory("int", plants_offset + 0x1C + 0x14C * i)
        plant_col = process.read_memory("int", plants_offset + 0x28 + 0x14C * i)
        if not plant_disappeared and not plant_crushed and plant_type == 47 and plant_row == (row - 1) and plant_col == (col - 1):
            new_cob_index = i
            break

    while (utils.game_clock() - clock) < (205 + 750 + 625 + 3):  # 等到可用
        delay.delay_a_little_time()
    cobs.cob_lock.acquire()
    cobs.cob_list.insert(cobs.cob_index, (row, col))
    cobs.cob_list_detailed.insert(cobs.cob_index, [0, row, col, new_cob_index, 37])
    cobs.cob_lock.release()

    logger.info(f"玉米炮 {crood} 铲种成功, 新的炮列表 {cobs.cob_list}.")


@running_in_thread
def nuts_fixer(spots, seed):
    """
    坚果类植物修复. 在单独的子线程运行.

    @参数 spots(list): 位置, 包括若干个 (行, 列) 元组.

    @参数 seed(str): 卡片名称, 可选值 ["坚果", "高坚果", "南瓜头"].

    @示例:

    >>> StartNutsFixerThread([(3, 8), (4, 8)], "高坚果")

    >>> StartNutsFixerThread([(4, 5),(4, 6),(4, 7),(4, 8)], "南瓜头")
    """

    # 1.草地 2.裸地 3.泳池
    # 16.睡莲 33.花盆
    # 3.坚果 23.高坚果 30.南瓜头

    while utils.game_ui() != 3:
        time.sleep(0.01)

    logger.info("启动坚果类植物修复线程.")

    seed_type = seeds.get_seed_by_name(seed)  # 根据名称得到卡片代号
    if seed_type not in (3, 23, 30, 3 + 48, 23 + 48, 30 + 48):
        logger.error(f"自动修复只支持 坚果/高坚果/南瓜头.")
    seed_index = seeds.get_index_by_name(seed)  # 获取卡片的位置, 数组下标需要 -1
    if seed_index is None:
        logger.error(f"卡槽没有 {seed} 卡片, 退出坚果类植物修复线程.")

    seed_cost = process.read_memory("int", 0x69F2C0 + seed_type * 0x24)  # 卡片价格
    seed_recharge = process.read_memory("int", 0x69F2C4 + seed_type * 0x24)  # 卡片冷却
    # HP_MAX = 4000 if seed_type in (3, 30) else 8000
    if seed_type == 3:  # Wall-nut
        HP_MAX = process.read_memory("int", 0x45E1A7)
    elif seed_type == 23:  # Tall-nut
        HP_MAX = process.read_memory("int", 0x45E215)
    else:  # 30 Pumpkin
        HP_MAX = process.read_memory("int", 0x45E445)
    LINIT = int(HP_MAX * 0.1) if len(spots) < 2 else int(HP_MAX * 0.3)  # TODO

    # 补种函数
    def fix(spot):
        slots_offset = process.read_memory("unsigned int", 0x6A9EC0, 0x768, 0x144)
        seed_usable = process.read_memory("bool", slots_offset + 0x70 + (seed_index - 1) * 0x50)  # 该卡片是否可用
        sun = process.read_memory("int", 0x6A9EC0, 0x768, 0x5560)  # 当前阳光
        if seed_usable and sun >= seed_cost:
            while utils.game_paused():
                delay.thread_sleep_for(1)
        else:
            return False
        success = False
        if utils.get_block_type(spot) == 3 and (16, spot[0], spot[1]) not in utils.get_plants_croods():
            seed_lilypad_index = seeds.get_index_by_name("睡莲")
            if seed_lilypad_index is None:
                logger.warning(f"卡片 睡莲 不在卡槽中.")
            else:
                seed_lilypad_usable = process.read_memory("bool", slots_offset + 0x70 + (seed_lilypad_index - 1) * 0x50)
                if seed_lilypad_usable:
                    operate.use_seed("睡莲", spot)
                    operate.use_seed(seed, spot)
                    success = True
        elif scene.game_scene in (4, 5) and (33, spot[0], spot[1]) not in utils.get_plants_croods():
            seed_flowerpot_index = seeds.get_index_by_name("花盆")
            if seed_flowerpot_index is None:
                logger.warning(f"卡片 花盆 不在卡槽中.")
            else:
                seed_flowerpot_usable = process.read_memory("bool", slots_offset + 0x70 + (seed_flowerpot_index - 1) * 0x50)
                if seed_flowerpot_usable:
                    operate.use_seed("花盆", spot)
                    operate.use_seed(seed, spot)
                    success = True
        else:
            operate.use_seed(seed, spot)
            success = True
        delay.thread_sleep_for(1)
        return success

    # while utils.game_ui() == 3 and utils.current_wave() < 20:
    while utils.game_ui() == 3:

        croods_which_has_plant = []
        plants = utils.get_plants_croods()
        for plant_type, plant_row, plant_col in plants:
            # 需要修复的植物是 南瓜 时, 只有南瓜才算占位
            # 需要修复的植物是 坚果/高坚果 时, 不是 睡莲/花盆/南瓜 就算占位
            if (seed_type in (30, 30 + 48) and plant_type in (30, 30 + 48)) or (
                seed_type not in (30, 30 + 48) and plant_type not in (16, 30, 33)
            ):
                croods_which_has_plant.append((plant_row, plant_col))
                if plant_type == 47:  # 玉米炮占两格
                    croods_which_has_plant.append((plant_row, plant_col + 1))
        spot_which_has_plant = [i for i in spots if i in croods_which_has_plant]

        for spot in spots:
            # 位置有植物但不是坚果/高坚果/南瓜
            if spot in spot_which_has_plant and (seed_type, spot[0], spot[1]) not in plants:
                delay.thread_sleep_for(1)
                continue
            # 位置有植物而且是坚果/高坚果/南瓜
            elif spot in spot_which_has_plant and (seed_type, spot[0], spot[1]) in plants:
                plants_count_max = process.read_memory("unsigned int", 0x6A9EC0, 0x768, 0xB0)
                plants_offset = process.read_memory("unsigned int", 0x6A9EC0, 0x768, 0xAC)
                plants_index = None
                for i in range(plants_count_max):
                    plants_disappeared = process.read_memory("bool", plants_offset + 0x141 + 0x14C * i)
                    plants_crushed = process.read_memory("bool", plants_offset + 0x142 + 0x14C * i)
                    plants_type = process.read_memory("int", plants_offset + 0x24 + 0x14C * i)
                    plants_row = process.read_memory("int", plants_offset + 0x1C + 0x14C * i)
                    plants_col = process.read_memory("int", plants_offset + 0x28 + 0x14C * i)
                    if (
                        not plants_disappeared
                        and not plants_crushed
                        and plants_type == seed_type
                        and plants_row == spot[0] - 1
                        and plants_col == spot[1] - 1
                    ):  # 特定位置
                        plants_index = i
                logger.debug(f"位置 {spot} 的植物 {seed} 下标为 {plants_index}.")
                plant_hp = process.read_memory("int", plants_offset + 0x40 + 0x14C * plants_index)
                logger.debug(f"位置 {spot} 的植物 {seed} 血量为 {plant_hp}.")
                if plant_hp < LINIT:
                    if fix(spot):  # 种植
                        delay.game_delay_for(seed_recharge + 1)
                    break
            # 位置没有植物
            elif spot not in spot_which_has_plant:
                if fix(spot):  # 种植
                    delay.game_delay_for(seed_recharge + 1)
                break

        delay.thread_sleep_for(10)

    logger.info("停止坚果类植物修复线程.")
