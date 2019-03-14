# coding=utf-8

"""
Tools
"""

import random
import time

from . import logger
from . import process
from . import delay
from . import keyboard
from . import code
from . import utils

# https://github.com/lmintlcx/pvztools


def background_running(on=True):
    """
    允许后台运行.

    @参数 on(bool): 是否开启.
    """
    if utils.game_on():
        if on:
            process.write_memory("short", 0x00EB, 0x0054EBA8)
        else:
            process.write_memory("short", 0x2E74, 0x0054EBA8)


def set_quick_lineup(on=True):
    """
    快捷布阵模式.

    同时开启这些功能: 自动收集, 玉米炮无冷却, 植物无敌, 暂停刷怪, 无视阳光, 卡片无冷却, 紫卡无限制, 浓雾透视.

    @参数 on(bool): 是否开启.
    """
    if utils.game_on():
        if on:
            # Auto Collect
            process.write_memory("byte", 0xEB, 0x0043158F)
            # Cob Cannon No CD
            process.write_memory("byte", 0x80, 0x0046103B)
            # Plant Invincible
            process.write_memory("byte", [0x46, 0x40, 0x00], 0x0052FCF1)
            process.write_memory("byte", [0x90, 0x90, 0x90], 0x0046CFEB)
            process.write_memory("byte", [0x90, 0x90, 0x90], 0x0046D7A6)
            process.write_memory("byte", 0xEB, 0x0052E93B)
            process.write_memory("byte", 0xEB, 0x0041CC2F)
            process.write_memory("byte", 0xEB, 0x005276EA)
            process.write_memory("byte", 0x70, 0x0045EE0A)
            process.write_memory("byte", 0x00, 0x0045EC66)
            # Stop Spawning
            process.write_memory("byte", 0xEB, 0x004265DC)
            # Ignore Sun
            process.write_memory("byte", 0x70, 0x0041BA72)
            process.write_memory("byte", 0x3B, 0x0041BA74)
            process.write_memory("byte", 0x91, 0x0041BAC0)
            process.write_memory("byte", 0x80, 0x00427A92)
            process.write_memory("byte", 0x80, 0x00427DFD)
            process.write_memory("byte", 0xEB, 0x0042487F)
            # Slots No CD
            process.write_memory("byte", 0x70, 0x00487296)
            process.write_memory("byte", 0xEB, 0x00488250)
            # Purple Seed Unlimited
            process.write_memory("byte", [0xB0, 0x01, 0xC3], 0x0041D7D0)
            process.write_memory("byte", 0xEB, 0x0040E477)
            # No Fog
            process.write_memory("unsigned short", 0xD231, 0x0041A68D)
        else:
            # Auto Collect
            process.write_memory("byte", 0x75, 0x0043158F)
            # Cob Cannon No CD
            process.write_memory("byte", 0x85, 0x0046103B)
            # Plant Invincible
            process.write_memory("byte", [0x46, 0x40, 0xFC], 0x0052FCF1)
            process.write_memory("byte", [0x29, 0x50, 0x40], 0x0046CFEB)
            process.write_memory("byte", [0x29, 0x4E, 0x40], 0x0046D7A6)
            process.write_memory("byte", 0x74, 0x0052E93B)
            process.write_memory("byte", 0x74, 0x0041CC2F)
            process.write_memory("byte", 0x75, 0x005276EA)
            process.write_memory("byte", 0x75, 0x0045EE0A)
            process.write_memory("byte", 0xE0, 0x0045EC66)
            # Stop Spawning
            process.write_memory("byte", 0x74, 0x004265DC)
            # Ignore Sun
            process.write_memory("byte", 0x7F, 0x0041BA72)
            process.write_memory("byte", 0x2B, 0x0041BA74)
            process.write_memory("byte", 0x9E, 0x0041BAC0)
            process.write_memory("byte", 0x8F, 0x00427A92)
            process.write_memory("byte", 0x8F, 0x00427DFD)
            process.write_memory("byte", 0x74, 0x0042487F)
            # Slots No CD
            process.write_memory("byte", 0x7E, 0x00487296)
            process.write_memory("byte", 0x75, 0x00488250)
            # Purple Seed Unlimited
            process.write_memory("byte", [0x51, 0x83, 0xF8], 0x0041D7D0)
            process.write_memory("byte", 0x74, 0x0040E477)
            # No Fog
            process.write_memory("unsigned short", 0xF23B, 0x0041A68D)


def set_quick_pass():
    """
    快速过关.

    直接结束关卡, 过关后将阳光数设置为 8000, 已完成 2018 面旗帜数, 玉米炮处于最亮状态.
    """
    if utils.game_on() and utils.game_ui() in (3,):

        time_to_wait = 75 - ((utils.game_clock() + 500) % 75)
        if utils.game_paused():
            if time_to_wait != 0:
                keyboard.restore_game()
                delay.game_delay_for(time_to_wait)
                keyboard.pause_game()
            else:
                pass
        else:
            delay.game_delay_for(time_to_wait)
            keyboard.pause_game()

        time.sleep(0.1)
        code.asm_init()
        code.asm_mov_exx_dword_ptr("ecx", 0x6A9EC0)
        code.asm_mov_exx_dword_ptr_exx_add("ecx", 0x768)
        code.asm_call(0x0040C3E0)
        code.asm_ret()
        code.asm_code_inject_safely()

        # time.sleep(0.1)
        # zombies_count_max = process.read_memory("unsigned int", 0x6A9EC0, 0x768, 0x94)
        # zombies_offset = process.read_memory("unsigned int", 0x6A9EC0, 0x768, 0x90)
        # for i in range(zombies_count_max):
        #     if not process.read_memory("bool", zombies_offset + 0xEC + i * 0x15C):  # not disappear
        #         process.write_memory("int", 3, zombies_offset + 0x28 + i * 0x15C)  # kill

        time.sleep(0.1)
        keyboard.restore_game()
        time.sleep(2.5)  # 等阳光被收集完全
        process.write_memory("int", 8000, 0x6A9EC0, 0x768, 0x5560)
        process.write_memory("int", 1008, 0x6A9EC0, 0x768, 0x160, 0x6C)

        # # [[[0x6A9EC0] +0x768] +0x5538] = min{[[[0x6A9EC0] +0x768] +0x553C] x 10 + 425, 950} + rand(275)
        # process.write_memory("int", 0, 0x6A9EC0, 0x768, 0x553C)  # 53

        # slots_offset = process.read_memory("int", 0x6A9EC0, 0x768, 0x144)
        # seed_types = [40, 41, 42, 43, 44, 45, 46, 47, 8, 48]
        # seed_imitater_types = [-1, -1, -1, -1, -1, -1, -1, -1, -1, 8]
        # for i in range(10):
        #     process.write_memory("int", seed_types[i], slots_offset + 0x5C + i * 0x50)
        #     process.write_memory("int", seed_imitater_types[i], slots_offset + 0x60 + i * 0x50)


def jump_level(level=1008):
    """
    无尽模式跳关.

    @参数 level(int): 轮数.
    """
    if utils.game_on() and utils.game_ui() in (2, 3) and utils.game_mode() in (60, 70, 11, 12, 13, 14, 15):
        process.write_memory("int", level, 0x6A9EC0, 0x768, 0x160, 0x6C)


def set_sun(sun=8000):
    """
    设置阳光.

    @参数 sun(int): 阳光数.
    """
    if utils.game_on() and utils.game_ui() in (2, 3):
        process.write_memory("int", sun, 0x6A9EC0, 0x768, 0x5560)


def set_sun_limit(sun_limit):
    """
    设置阳光上限.

    @参数 sun_limit(int): 阳光上限数.
    """
    if utils.game_on():
        process.write_memory("int", sun_limit, 0x00430A1F)
        process.write_memory("int", sun_limit, 0x00430A2B)


def set_money(money):
    """
    设置金钱. 显示数量为 10 倍.

    @参数 money(int): 金钱数.
    """
    if utils.game_on():
        process.write_memory("int", money, 0x6A9EC0, 0x82C, 0x28)


def set_money_limit(money_limit):
    """
    设置金钱上限. 显示数量为 10 倍.

    @参数 money_limit(int): 金钱上限数.
    """
    if utils.game_on():
        process.write_memory("int", money_limit, 0x00430A74)
        process.write_memory("int", money_limit, 0x00430A7D)


def clear_fog(on=True):
    """
    清除浓雾.

    @参数 on(bool): 是否开启.
    """
    if utils.game_on():
        if on:
            process.write_memory("unsigned short", 0xD231, 0x0041A68D)
        else:
            process.write_memory("unsigned short", 0xF23B, 0x0041A68D)


def zombie_no_falling(on=True):
    """
    僵尸死后不掉钱.

    @参数 on(bool): 是否开启.
    """
    if utils.game_on():
        if on:
            process.write_memory("unsigned char", 0x70, 0x00530275)
            arr = [0x90] * 65
            process.write_memory("unsigned char", arr, 0x0053028A)
        else:
            process.write_memory("unsigned char", 0x75, 0x00530275)
            arr = [
                0x6A,
                0x03,
                0x6A,
                0x03,
                0x56,
                0x8D,
                0x47,
                0xEC,
                0x50,
                0xE8,
                0x78,
                0xC8,
                0xED,
                0xFF,
                0x6A,
                0x03,
                0x6A,
                0x03,
                0x56,
                0x8D,
                0x4F,
                0xE2,
                0x51,
                0x8B,
                0x4B,
                0x04,
                0xE8,
                0x67,
                0xC8,
                0xED,
                0xFF,
                0x8B,
                0x4B,
                0x04,
                0x6A,
                0x03,
                0x6A,
                0x03,
                0x56,
                0x8D,
                0x57,
                0xD8,
                0x52,
                0xE8,
                0x56,
                0xC8,
                0xED,
                0xFF,
                0x8B,
                0x4B,
                0x04,
                0x6A,
                0x03,
                0x6A,
                0x03,
                0x56,
                0x83,
                0xC7,
                0xCE,
                0x57,
                0xE8,
                0x45,
                0xC8,
                0xED,
                0xFF,
            ]
            process.write_memory("unsigned char", arr, 0x0053028A)


music_list = [
    "Grasswalk",
    "Moongrains",
    "Watery Graves",
    "Rigor Mormist",
    "Graze the Roof",
    "Choose Your Seeds",
    "Crazy Dave",
    "Zen Garden",
    "Cerebrawl",
    "Loonboon",
    "Ultimate Battle",
    "Brainiac Maniac",
]


def set_music(music):
    """
    设置背景音乐.

    @参数 music(str/int): 歌曲名或者代号.

    "Grasswalk"          # 1
    "Moongrains"         # 2
    "Watery Graves"      # 3
    "Rigor Mormist"      # 4
    "Graze the Roof"     # 5
    "Choose Your Seeds"  # 6
    "Crazy Dave"         # 7
    "Zen Garden"         # 8
    "Cerebrawl"          # 9
    "Loonboon"           # 10
    "Ultimate Battle"    # 11
    "Brainiac Maniac"    # 12
    """

    if isinstance(music, str) and music in music_list:
        music_id = music_list.index(music) + 1
    elif isinstance(music, int) and music in range(1, 13):
        music_id = music
    else:
        logger.error(f"未知音乐: {music}.")

    if utils.game_on():
        code.asm_init()
        code.asm_mov_exx("edi", music_id)
        code.asm_mov_exx_dword_ptr("eax", 0x6A9EC0)
        code.asm_mov_exx_dword_ptr_exx_add("eax", 0x83C)
        code.asm_call(0x0045B750)
        code.asm_ret()
        code.asm_code_inject_safely()


debug_mode_list = ["OFF", "SPAWNING", "MUSIC", "MEMORY", "COLLISION"]


def set_debug_mode(mode):
    """
    设置调试模式.

    @参数 mode(str/int): 模式名或者代号.

    "OFF"        # 0
    "SPAWNING"   # 1
    "MUSIC"      # 2
    "MEMORY"     # 3
    "COLLISION"  # 4
    """

    if isinstance(mode, str) and mode in debug_mode_list:
        mode_id = debug_mode_list.index(mode)
    elif isinstance(mode, int) and mode in range(5):
        mode_id = mode
    else:
        logger.error(f"未知调试模式: {mode}.")

    if utils.game_on() and utils.game_ui() in (2, 3):
        process.write_memory("int", mode_id, 0x6A9EC0, 0x768, 0x55F8)


def set_random_seed(seed):
    """
    设置随机数种子.
    """
    if utils.game_on() and utils.game_ui() in (2, 3):
        process.write_memory("int", seed, 0x6A9EC0, 0x768, 0x561C)


# generate type from seed
def update_zombies_type():
    """
    从种子生成出怪类型.
    """
    process.write_memory("bool", [False] * 33, 0x6A9EC0, 0x768, 0x54D4)
    code.asm_init()
    code.asm_mov_exx_dword_ptr("esi", 0x6A9EC0)
    code.asm_mov_exx_dword_ptr_exx_add("esi", 0x768)
    code.asm_mov_exx_dword_ptr_exx_add("esi", 0x160)
    code.asm_call(0x00425840)
    code.asm_ret()
    code.asm_code_inject_safely()


# generate list from type
def update_zombies_list():
    """
    从出怪类型生成出怪列表.
    """
    code.asm_init()
    code.asm_mov_exx_dword_ptr("edi", 0x6A9EC0)
    code.asm_mov_exx_dword_ptr_exx_add("edi", 0x768)
    code.asm_call(0x004092E0)
    code.asm_ret()
    code.asm_code_inject_safely()


def update_zombies_preview():
    """
    更新出怪预览.
    """
    process.write_memory("byte", 0x80, 0x0043A153)
    code.asm_init()
    code.asm_mov_exx_dword_ptr("ebx", 0x6A9EC0)
    code.asm_mov_exx_dword_ptr_exx_add("ebx", 0x768)
    code.asm_call(0x0040DF70)
    code.asm_mov_exx_dword_ptr("eax", 0x6A9EC0)
    code.asm_mov_exx_dword_ptr_exx_add("eax", 0x768)
    code.asm_mov_exx_dword_ptr_exx_add("eax", 0x15C)
    code.asm_push_exx("eax")
    code.asm_call(0x0043A140)
    code.asm_ret()
    code.asm_code_inject_safely()
    process.write_memory("byte", 0x85, 0x0043A153)


zombies_string = [
    ["Zombie", "普僵", "普通", "领带"],
    ["Flag Zombie", "旗帜", "摇旗", "旗子"],
    ["Conehead Zombie", "路障"],
    ["Pole Vaulting Zombie", "撑杆", "撑杆跳"],
    ["Buckethead Zombie", "铁桶"],
    ["Newspaper Zombie", "读报", "报纸"],
    ["Screen Door Zombie", "铁门", "铁栅门", "门板"],
    ["Football Zombie", "橄榄", "橄榄球"],
    ["Dancing Zombie", "舞王", "MJ"],
    ["Backup Dancer", "伴舞", "舞伴"],
    ["Ducky Tube Zombie", "鸭子", "救生圈"],
    ["Snorkel Zombie", "潜水"],
    ["Zomboni", "冰车", "制冰车"],
    ["Zombie Bobsled Team", "雪橇", "雪橇队", "雪橇小队"],
    ["Dolphin Rider Zombie", "海豚", "海豚骑士"],
    ["Jack-in-the-Box Zombie", "小丑", "玩偶匣"],
    ["Balloon Zombie", "气球"],
    ["Digger Zombie", "矿工", "挖地"],
    ["Pogo Zombie", "跳跳", "弹跳"],
    ["Zombie Yeti", "雪人"],
    ["Bungee Zombie", "蹦极", "小偷"],
    ["Ladder Zombie", "扶梯", "梯子"],
    ["Catapult Zombie", "投篮", "投篮车", "篮球"],
    ["Gargantuar", "白眼", "伽刚特尔", "巨人"],
    ["Imp", "小鬼", "小恶魔", "IMP"],
    ["Dr. Zomboss", "僵王", "僵博"],
    ["Peashooter Zombie", "豌豆"],
    ["Wall-nut Zombie", "坚果"],
    ["Jalapeno Zombie", "辣椒"],
    ["Gatling Pea Zombie", "机枪", "加特林"],
    ["Squash Zombie", "倭瓜", "窝瓜"],
    ["Tall-nut Zombie", "高坚果"],
    ["GigaGargantuar", "红眼", "暴走伽刚特尔", "红眼巨人"],
]

zombies_string_dict = {}
for i, zombies in enumerate(zombies_string):
    for j, z in enumerate(zombies):
        if j == 0:  # 第一个英文名称
            zombies_string_dict[z] = i
        else:
            zombies_string_dict[z] = i
            zombies_string_dict[z + "僵尸"] = i
# logger.info(f"僵尸名称字符串字典 {zombies_string_dict}.")


def zombie_name_to_index(zombie):
    """
    统一转换为代号表示.
    """
    if isinstance(zombie, str):
        if zombie in zombies_string_dict:
            return zombies_string_dict[zombie]
        else:
            logger.error(f"未知僵尸名称: {zombie}")
    else:  # int
        if zombie in range(33):
            return zombie
        else:
            logger.error(f"未知僵尸类型代号: {zombie}.")


def spawning_debug():
    """
    输出出怪调试信息.
    """

    COUNT = 1000
    WAVES = int(COUNT / 50)

    zombies_list = process.read_memory("int", 0x6A9EC0, 0x768, 0x6B4, array=COUNT)
    logger.info(f"出怪列表 {zombies_list}.")

    for z in range(33):
        zombie_waves = [0] * WAVES
        for i in range(WAVES):
            zombie_waves[i] = zombies_list[50 * i : 50 * i + 50].count(z)
        logger.info(f"僵尸 {zombies_string[z][1]} 的出现波次 {zombie_waves}.")

    zombie_types = list(set(zombies_list))
    zombie_types.sort()
    zombie_types = [z for z in zombie_types if z in range(33)]
    logger.info(f"出怪类型 {[zombies_string[z][1] for z in zombie_types]}.")


def set_internal_spawn(zombies=None):
    """
    内置刷怪, 由游戏自带函数生成出怪列表. 默认使用当前的种子.

    @参数 zombies(list[str/int]): 包含僵尸名称或代号的列表.
    """

    if not (utils.game_on() and utils.game_ui() in (2, 3)):
        return

    if zombies is None:

        update_zombies_type()
        update_zombies_list()
        if utils.game_ui() == 2:
            update_zombies_preview()

    else:

        zombies = [zombie_name_to_index(z) for z in zombies]
        zombies = list(set(zombies))

        zombies_type_offset = process.read_memory("unsigned int", 0x6A9EC0, 0x768) + 0x54D4
        zombies_list_offset = process.read_memory("unsigned int", 0x6A9EC0, 0x768) + 0x6B4

        zombies_type_original = process.read_memory("bool", zombies_type_offset, array=33)

        has_normal_zombie = 0 in zombies or 26 in zombies
        replace_zombie = 0
        if not has_normal_zombie:
            for i in range(33):
                if i in zombies:
                    replace_zombie = i
                    break

        process.write_memory("bool", [True if i in zombies else False for i in range(33)], zombies_type_offset)
        if not has_normal_zombie:
            process.write_memory("bool", False, zombies_type_offset + replace_zombie * 1)
            process.write_memory("bool", True, zombies_type_offset + 26 * 1)

        update_zombies_list()

        if not has_normal_zombie:
            zombies_list = process.read_memory("unsigned int", zombies_list_offset, array=2000)
            for i in range(2000):
                if zombies_list[i] == 26:
                    process.write_memory("unsigned int", replace_zombie, zombies_list_offset + i * 4)

        if utils.game_ui() == 2:
            update_zombies_preview()

        process.write_memory("bool", zombies_type_original, zombies_type_offset)

    # spawning_debug()


def set_customize_spawn(zombies=None, simulate=False, limit_flag=True, limit_yeti=True, limit_bungee=True, limit_giga=False, giga_waves=None):
    """
    自定义刷怪, 由脚本生成并填充出怪列表.

    @参数 zombies(list[str/int]): 包含僵尸名称或代号的列表.

    @参数 simulate(bool): True 模拟自然刷怪(按比例随机填充), False 极限刷怪(均匀填充).

    @参数 limit_flag(bool): 限制旗帜, 旗帜只会在每个旗帜波(大波)出现一只.

    @参数 limit_yeti(bool): 限制雪人, 雪人只会出现一只.

    @参数 limit_bungee(bool): 限制蹦极, 蹦极只会在旗帜波(大波)出现.

    @参数 limit_giga(bool): 限制红眼, 红眼只会在指定的波次出现.

    @参数 giga_waves(list[bool]): 指定红眼出现波数的列表(长度 20).
    """

    if not (utils.game_on() and utils.game_ui() in (2, 3)):
        return

    if zombies is None:
        zombies = ["普僵"]
    zombies = [zombie_name_to_index(z) for z in zombies]
    zombies = list(set(zombies))

    zombies_list = [0] * 2000

    has_flag = 1 in zombies
    has_yeti = 19 in zombies
    has_bungee = 20 in zombies
    has_giga = 32 in zombies

    count = 0
    for i in range(33):
        if i in zombies:
            count += 1

    if count > 0:

        weights = [
            20,
            0,
            37,
            67,
            95,
            37,
            108,
            67,
            37,
            0,
            0,
            67,
            67,
            67,
            52,
            37,
            67,
            37,
            37,
            17,
            0,
            37,
            52,
            52,
            0,
            0,
            120,
            94,
            37,
            67,
            67,
            67,
            36,
        ]
        weights_flag = [
            84,
            10,
            29,
            50,
            71,
            29,
            80,
            50,
            28,
            0,
            0,
            50,
            50,
            49,
            39,
            29,
            50,
            29,
            29,
            10,
            28,
            29,
            39,
            39,
            0,
            0,
            89,
            70,
            28,
            50,
            50,
            50,
            122,
        ]
        dist = []
        dist_flag = []
        for i, w in enumerate(weights):
            dist += [i] * w
        for i, w in enumerate(weights_flag):
            dist_flag += [i] * w

        zombie_type = 0
        for i in range(2000):
            while True:
                if simulate:
                    if ((i // 50) % 10) == 9:  # flag wave
                        zombie_type = random.choice(dist_flag)
                    else:
                        zombie_type = random.choice(dist)
                else:
                    zombie_type += 1
                    zombie_type %= 33
                if not (  #
                    (zombie_type not in zombies)  #
                    or (has_flag and limit_flag and zombie_type == 1)  #
                    or (has_yeti and limit_yeti and zombie_type == 19)  #
                    or (has_bungee and limit_bungee and zombie_type == 20)  #
                    or (has_giga and limit_giga and zombie_type == 32 and not giga_waves[(i // 50) % 20])  #
                ):  #
                    break
            zombies_list[i] = zombie_type

        index_flag = [450, 950, 1450, 1950]
        index_bungee = [451, 452, 453, 454, 951, 952, 953, 954, 1451, 1452, 1453, 1454, 1951, 1952, 1953, 1954]

        if has_flag and limit_flag:
            for i in index_flag:
                zombies_list[i] = 1

        if has_bungee and limit_bungee:
            for i in index_bungee:
                zombies_list[i] = 20

        if has_yeti and limit_yeti:
            i = 0
            while True:
                i = random.randint(0, 999)
                if not ((has_flag and limit_flag and i in index_flag) or (has_bungee and limit_bungee and i in index_bungee)):  #  #  #  #
                    break
            zombies_list[i] = 19

    process.write_memory("unsigned int", zombies_list, 0x6A9EC0, 0x768, 0x6B4)

    if utils.game_ui() == 2:
        update_zombies_preview()

    # spawning_debug()


def set_zombies(zombies=None, mode="极限刷怪"):
    """
    设置出怪.

    旗帜(无需设定)只会在每个大波出现一只, 雪人只会出现一只, 蹦极只会在大波出现.

    @参数 zombies(list[str/int]): 包含僵尸名称或代号的列表, 建议 8~12 种.

    @参数 mode(str): 刷怪模式, 默认使用极限刷怪. 可选值 "自然刷怪" "极限刷怪" "模拟自然刷怪".

    自然刷怪只改变出怪种类, 再由游戏内置的函数生成出怪列表.

    极限刷怪是把所选僵尸种类按顺序均匀地填充到出怪列表.

    模拟自然刷怪则是根据统计规律按一定的比例随机填充出怪列表, 在旗帜波会调整不同僵尸的平均密度/出现概率.

    @示例:

    >>> SetZombies(["撑杆", "舞王", "冰车", "海豚", "气球", "矿工", "跳跳", "扶梯", "白眼", "红眼"])
    """

    # if zombies is None:
    #     zombies = ["普僵"]
    # zombies = [zombie_name_to_index(z) for z in zombies]
    # zombies = list(set(zombies))

    if mode in ("自然", "自然出怪", "自然刷怪"):
        set_internal_spawn(zombies)
    elif mode in ("极限", "极限出怪", "极限刷怪"):
        set_customize_spawn(zombies + ["旗帜"], False, True, True, True, False, None)
    elif mode in ("模拟自然", "模拟自然出怪", "模拟自然刷怪"):
        set_customize_spawn(zombies + ["旗帜"], True, True, True, True, False, None)
    else:
        logger.error(f"未知刷怪模式: {mode}.")
