# coding=utf-8

"""
Utils
"""

from . import logger
from . import process
from . import seeds


# 游戏基址, 事先缓存
# 获取常用数据时使用该基址以减少读内存次数
# TODO 逐渐应用到其他地方
pvz_base = None
main_object = None
zombies_offset = None
plants_offset = None
bullets_offset = None
items_offset = None
lawn_mowers_offset = None
grid_items_offset = None
mouse_offset = None
slots_offset = None


def update_game_base():
    """
    更新游戏基址.
    """

    global pvz_base
    global main_object
    global zombies_offset
    global plants_offset
    global bullets_offset
    global items_offset
    global lawn_mowers_offset
    global grid_items_offset
    global mouse_offset
    global slots_offset

    if game_on() and game_ui() in (2, 3, 4):
        pvz_base = process.read_memory("unsigned int", 0x6A9EC0)
        main_object = process.read_memory("unsigned int", pvz_base + 0x768)
        zombies_offset = process.read_memory("unsigned int", main_object + 0x90)
        plants_offset = process.read_memory("unsigned int", main_object + 0xAC)
        bullets_offset = process.read_memory("unsigned int", main_object + 0xC8)
        items_offset = process.read_memory("unsigned int", main_object + 0xE4)
        lawn_mowers_offset = process.read_memory("unsigned int", main_object + 0x100)
        grid_items_offset = process.read_memory("unsigned int", main_object + 0x11C)
        mouse_offset = process.read_memory("unsigned int", main_object + 0x138)
        slots_offset = process.read_memory("unsigned int", main_object + 0x144)

    logger.info(f"更新游戏内存基址.")


def game_on():
    """
    @返回值 (bool): 游戏是否开启, 没开则会尝试重新查找一次.
    """
    if process.is_valid():
        return True
    else:
        return process.find_pvz_1051()


def game_ui():
    """
    @返回值 (int): 游戏界面.

    1: 主界面, 2: 选卡, 3: 正常游戏/战斗, 4: 僵尸进屋, 7: 模式选择.
    """
    return process.read_memory("int", 0x6A9EC0, 0x7FC)


def game_mode():
    """
    @返回值 (int): 游戏模式, 13 为生存无尽.
    """
    return process.read_memory("int", 0x6A9EC0, 0x7F8)


## 以下常用数据获取使用已缓存的游戏基址


def game_scene():
    """
    @返回值 (int): 游戏场景/场地/地图.

    0: 白天, 1: 黑夜, 2: 泳池, 3: 浓雾, 4: 屋顶, 5: 月夜, 6: 蘑菇园, 7: 禅境花园, 8: 水族馆, 9: 智慧树.
    """
    # return process.read_memory("int", 0x6A9EC0, 0x768, 0x554C)
    return process.read_memory_int(main_object + 0x554C)


def game_paused():
    """
    @返回值 (bool): 当前游戏是否暂停.
    """
    # return process.read_memory("bool", 0x6A9EC0, 0x768, 0x164)
    return process.read_memory_bool(main_object + 0x164)


def mouse_in_game():
    """
    @返回值 (bool): 鼠标是否在游戏窗口内部.
    """
    # return process.read_memory("bool", 0x6A9EC0, 0x768, 0x138, 0x18)  # 0x6A9EC0, 0x768, 0x59
    return process.read_memory_bool(mouse_offset + 0x18)


def mouse_have_something():
    """
    @返回值 (bool): 鼠标是否选中卡炮或铲子.
    """
    # return process.read_memory("int", 0x6A9EC0, 0x768, 0x138, 0x30) in (1, 6, 8)
    return process.read_memory_int(mouse_offset + 0x30) in (1, 6, 8)


def game_clock():
    """
    @返回值 (int): 内部时钟, 游戏暂停和选卡时会暂停计时.
    """
    # return process.read_memory("int", 0x6A9EC0, 0x768, 0x5568)  # TODO 时钟选取
    return process.read_memory_int(main_object + 0x5568)


def wave_init_countdown():
    """
    @返回值 (int): 刷新倒计时初始值.
    """
    # return process.read_memory("int", 0x6A9EC0, 0x768, 0x55A0)
    return process.read_memory_int(main_object + 0x55A0)


def wave_countdown():
    """
    @返回值 (int): 下一波刷新倒计时, 触发刷新时重置为 200, 减少至 1 后刷出下一波.
    """
    # return process.read_memory("int", 0x6A9EC0, 0x768, 0x559C)
    return process.read_memory_int(main_object + 0x559C)


def huge_wave_countdown():
    """
    @返回值 (int): 大波刷新倒计时, 对于旗帜波, 刷新倒计时减少至 4 后停滞, 由该值代替减少.
    """
    # return process.read_memory("int", 0x6A9EC0, 0x768, 0x55A4)
    return process.read_memory_int(main_object + 0x55A4)


def current_wave():
    """
    @返回值 (int): 已刷新波数.
    """
    # return process.read_memory("int", 0x6A9EC0, 0x768, 0x557C)
    return process.read_memory_int(main_object + 0x557C)


def dancer_clock():
    """
    @返回值 (int): 一个内部时钟, 可用于判断舞王/伴舞的舞蹈/前进.
    """
    # return process.read_memory("int", 0x6A9EC0, 0x838)
    return process.read_memory_int(pvz_base + 0x838)


## 以上常用数据获取使用已缓存的游戏基址

zombie_names = {
    0: "Zombie",
    1: "Flag Zombie",
    2: "Conehead Zombie",
    3: "Pole Vaulting Zombie",
    4: "Buckethead Zombie",
    5: "Newspaper Zombie",
    6: "Screen Door Zombie",
    7: "Football Zombie",
    8: "Dancing Zombie",
    9: "Backup Dancer",
    10: "Ducky Tube Zombie",
    11: "Snorkel Zombie",
    12: "Zomboni",
    13: "Zombie Bobsled Team",
    14: "Dolphin Rider Zombie",
    15: "Jack-in-the-Box Zombie",
    16: "Balloon Zombie",
    17: "Digger Zombie",
    18: "Pogo Zombie",
    19: "Zombie Yeti",
    20: "Bungee Zombie",
    21: "Ladder Zombie",
    22: "Catapult Zombie",
    23: "Gargantuar",
    24: "Imp",
    25: "Dr. Zomboss",
    26: "Peashooter Zombie",
    27: "Wall-nut Zombie",
    28: "Jalapeno Zombie",
    29: "Gatling Pea Zombie",
    30: "Squash Zombie",
    31: "Tall-nut Zombie",
    32: "GigaGargantuar",
}


def get_zombie_spawning_types():
    """
    @返回值 (list[int]): 包含当前出怪类型的列表. 僵尸类型代号请查阅附录

    只能在选卡或者战斗界面使用.
    """
    zombie_types = []

    if game_ui() in (2, 3):
        zombies = process.read_memory("int", 0x6A9EC0, 0x768, 0x6B4, array=1000)
        zombie_types = list(set(zombies))
        zombie_types.sort()

    logger.info(f"获取出怪类型 {[zombie_names[z] for z in zombie_types]}.")
    return zombie_types


def get_zombie_spawning_appear_waves(zombie_type=32):
    """
    @参数 zombie_type(int): 僵尸类型代号, 默认为红眼. 详情请查阅附录.

    @返回值 (list[bool]): 包含指定僵尸在 20 波中是否出现的列表.

    只能在选卡或者战斗界面使用.
    """
    zombie_waves = [False] * 20

    if game_ui() in (2, 3):
        zombies = process.read_memory("int", 0x6A9EC0, 0x768, 0x6B4, array=1000)
        for i in range(20):
            zombie_count = zombies[50 * i : 50 * i + 50].count(zombie_type)
            zombie_waves[i] = zombie_count > 0

    logger.info(f"获取 {zombie_names[zombie_type]} 僵尸的出现波次 {zombie_waves}.")
    return zombie_waves


def get_seeds_index(seed: str):
    """
    @参数 seed(str): 卡片名称.

    @返回值 (list[int]): 某种卡片(包括模仿者)在卡槽的数组下标列表.
    """
    seed = seeds.get_seed_by_name(seed)
    seed %= 48

    seed_indexes = []
    slots_count = process.read_memory("int", 0x6A9EC0, 0x768, 0x144, 0x24)
    slots_offset = process.read_memory("unsigned int", 0x6A9EC0, 0x768, 0x144)
    for i in range(slots_count):
        seed_type = process.read_memory("int", slots_offset + 0x5C + i * 0x50)
        seed_imitater_type = process.read_memory("int", slots_offset + 0x60 + i * 0x50)
        if seed_type == seed or (seed_type == 48 and seed_imitater_type == seed):
            seed_indexes.append(i)
    logger.info(f"获取卡片 {seed} 卡槽数组下标 {seed_indexes}.")
    return seed_indexes


def get_plants_croods():
    """
    获取场上植物坐标.
    """
    croods = []
    plants_count_max = process.read_memory("unsigned int", 0x6A9EC0, 0x768, 0xB0)
    plants_offset = process.read_memory("unsigned int", 0x6A9EC0, 0x768, 0xAC)
    for i in range(plants_count_max):
        plant_disappeared = process.read_memory("bool", plants_offset + 0x141 + 0x14C * i)
        plant_crushed = process.read_memory("bool", plants_offset + 0x142 + 0x14C * i)
        if not plant_disappeared and not plant_crushed:
            plant_type = process.read_memory("int", plants_offset + 0x24 + 0x14C * i)
            plant_row = process.read_memory("int", plants_offset + 0x1C + 0x14C * i)
            plant_col = process.read_memory("int", plants_offset + 0x28 + 0x14C * i)
            croods.append((plant_type, plant_row + 1, plant_col + 1))
    logger.debug(f"获取植物坐标列表 {croods}.")
    return croods


def get_block_type(*crood):
    """
    获取格子类型. 1.lawn 2.bare 3.pool
    """
    if isinstance(crood[0], tuple):
        row, col = crood[0]
    else:
        row, col = crood
    row, col = row - 1, col - 1
    # return process.read_memory("int", 0x6a9ec0, 0x768, 0x168 + row * 0x04 + col * 0x18)
    return process.read_memory("int", main_object + 0x168 + row * 0x04 + col * 0x18)
