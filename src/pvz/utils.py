# coding=utf-8

"""
Utils
"""

from . import logger
from . import process


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


mode_names = {
    0: "Adventure",
    1: "Survival: Day",
    2: "Survival: Night",
    3: "Survival: Pool",
    4: "Survival: Fog",
    5: "Survival: Roof",
    6: "Survival: Day (Hard)",
    7: "Survival: Night (Hard)",
    8: "Survival: Pool (Hard)",
    9: "Survival: Fog (Hard)",
    10: "Survival: Roof (Hard)",
    11: "Survival: Day (Endless)",
    12: "Survival: Night (Endless)",
    13: "Survival: Endless",
    14: "Survival: Fog (Endless)",
    15: "Survival: Roof (Endless)",
    16: "ZomBotany",
    17: "Wall-nut Bowling",
    18: "Slot Machine",
    19: "It's Raining Seeds",
    20: "Beghouled",
    21: "Invisi-ghoul",
    22: "Seeing Stars",
    23: "Zombiquarium",
    24: "Beghouled Twist",
    25: "Big Trouble Little Zombie",
    26: "Portal Combat",
    27: "Column Like You See'Em",
    28: "Bobseld Bonanza",
    29: "Zombie Nimble Zombie Quick",
    30: "Whack a Zombie",
    31: "Last Stand",
    32: "ZomBotany 2",
    33: "Wall-nut Bowling 2",
    34: "Pogo Party",
    35: "Dr. Zomboss's Revenge",
    36: "Art Challenge Wall-nut",
    37: "Sunny Day",
    38: "Unsodded",
    39: "Big Time",
    40: "Art Challenge Sunflower",
    41: "Air Raid",
    42: "Ice Level",
    43: "Zen Garden",
    44: "High Gravity",
    45: "Grave Danger",
    46: "Can You Dig It?",
    47: "Dark Stormy Night",
    48: "Bungee Blitz",
    49: "Squirrel",
    50: "Tree of Wisdom",
    51: "Vasebreaker",
    52: "To the Left",
    53: "Third Vase",
    54: "Chain Reaction",
    55: "M is for Metal",
    56: "Scary Potter",
    57: "Hokey Pokey",
    58: "Another Chain Reaction",
    59: "Ace of Vase",
    60: "Vasebreaker Endless",
    61: "I, Zombie",
    62: "I, Zombie Too",
    63: "Can You Dig It?",
    64: "Totally Nuts",
    65: "Dead Zeppelin",
    66: "Me Smash!",
    67: "ZomBoogie",
    68: "Three Hit Wonder",
    69: "All your brainz r belong to us",
    70: "I, Zombie Endless",
    71: "Upsell",
    72: "Intro",
}


def game_mode():
    """
    @返回值 (int): 游戏模式, 13 为生存无尽.
    """
    return process.read_memory("int", 0x6A9EC0, 0x7F8)


def game_scene():
    """
    @返回值 (int): 游戏场景.

    0: 白天, 1: 黑夜, 2: 泳池, 3: 浓雾, 4: 屋顶, 5: 月夜, 6: 蘑菇园, 7: 禅境花园, 8: 水族馆, 9: 智慧树.
    """
    return process.read_memory("int", 0x6A9EC0, 0x768, 0x554C)


def game_paused():
    """
    @返回值 (bool): 当前游戏是否暂停.
    """
    return process.read_memory("bool", 0x6A9EC0, 0x768, 0x164)


def mouse_in_game():
    """
    @返回值 (bool): 鼠标是否在游戏窗口内部.
    """
    return process.read_memory("bool", 0x6A9EC0, 0x768, 0x59)
    # return read_memory("bool", 0x6A9EC0, 0x768, 0x138, 0x18)


def mouse_have_something():
    """
    @返回值 (bool): 鼠标是否选中卡炮或铲子.
    """
    return process.read_memory("int", 0x6A9EC0, 0x768, 0x138, 0x30) in (1, 6, 8)


def game_clock():
    """
    @返回值 (int): 游戏内部时钟, 暂停和选卡时停止计时.
    """
    # TODO 时钟选取
    return process.read_memory("int", 0x6A9EC0, 0x768, 0x5568)


def wave_countdown():
    """
    @返回值 (int): 下一波刷新倒计时, 触发刷新时重置为 200, 减少至 0 刷出下一波.
    """
    return process.read_memory("int", 0x6A9EC0, 0x768, 0x559C)


def huge_wave_countdown():
    """
    @返回值 (int): 大波刷新倒计时, 对于旗帜波, 刷新倒计时减少至 4 后停滞, 由该值代替减少.
    """
    return process.read_memory("int", 0x6A9EC0, 0x768, 0x55A4)


def current_wave():
    """
    @返回值 (int): 已刷新波数.
    """
    return process.read_memory("int", 0x6A9EC0, 0x768, 0x557C)


def dance_clock():
    """
    @返回值 (int): 一个内部时钟, 可用于判断舞王/伴舞的舞蹈/前进.
    """
    return process.read_memory("int", 0x6A9EC0, 0x838)


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
    @返回值 (list[int]): 包含当前出怪类型的列表.

    只能在选卡或者战斗界面使用.
    """
    zombie_types = []

    if game_ui() in (2, 3):
        zombies = process.read_memory("int", 0x6A9EC0, 0x768, 0x6B4, array=1000)
        zombie_types = list(set(zombies))
        zombie_types.sort()

    logger.info(f"Get zombie types {[zombie_names[z] for z in zombie_types]}.")
    return zombie_types


def get_zombie_spawning_appear_waves(z=32):
    """
    @返回值 (list[bool]): 包含指定僵尸在 20 波中是否出现的列表, 默认参数为红眼.

    只能在选卡或者战斗界面使用.
    """
    zombie_waves = [False] * 20

    if game_ui() in (2, 3):
        zombies = process.read_memory("int", 0x6A9EC0, 0x768, 0x6B4, array=1000)
        for i in range(20):
            zombie_count = zombies[50 * i : 50 * i + 50].count(z)
            zombie_waves[i] = zombie_count > 0

    logger.info(f"Get zombie {zombie_names[z]} appear waves {zombie_waves}.")
    return zombie_waves

