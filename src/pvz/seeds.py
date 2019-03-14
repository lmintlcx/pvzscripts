# coding=utf-8

"""
Seeds
"""

import time
import functools
import gc

from . import logger
from . import process
from . import utils
from . import delay
from . import mouse
from . import cobs
from . import scene


seeds_string = [
    ["Peashooter", "豌豆射手", "豌豆", "单发"],
    ["Sunflower", "向日葵", "小向", "太阳花", "花"],
    ["Cherry Bomb", "樱桃炸弹", "樱桃", "炸弹", "爆炸", "草莓", "樱"],
    ["Wall-nut", "坚果墙", "坚果", "墙果", "建国", "柠檬圆"],
    ["Potato Mine", "土豆雷", "土豆", "地雷", "土豆地雷"],
    ["Snow Pea", "寒冰射手", "冰豆", "冰豌豆", "雪花豌豆", "雪花"],
    ["Chomper", "大嘴花", "大嘴", "食人花", "咀嚼者", "食"],
    ["Repeater", "双发射手", "双发", "双发豌豆"],
    ["Puff-shroom", "小喷菇", "小喷", "喷汽蘑菇", "烟雾蘑菇", "免费蘑菇", "炮灰菇", "小蘑菇", "免费货", "免费"],
    ["Sun-shroom", "阳光菇", "阳光", "阳光蘑菇"],
    ["Fume-shroom", "大喷菇", "大喷", "烟雾喷菇", "大蘑菇", "喷子", "喷"],
    ["Grave Buster", "墓碑吞噬者", "墓碑破坏者", "墓碑", "墓碑苔藓", "苔藓", "咬咬碑"],
    ["Hypno-shroom", "魅惑菇", "魅惑", "迷惑菇", "催眠蘑菇", "催眠", "花蘑菇", "毒蘑菇"],
    ["Scaredy-shroom", "胆小菇", "胆小", "胆怯蘑菇", "胆小鬼蘑菇", "杠子蘑菇"],
    ["Ice-shroom", "寒冰菇", "冰菇", "冷冻蘑菇", "冰蘑菇", "面瘫", "蓝冰", "原版冰", "冰"],
    ["Doom-shroom", "毁灭菇", "核蘑菇", "核弹", "核武", "毁灭", "末日蘑菇", "末日菇", "末日", "黑核", "原版核", "核"],
    ["Lily Pad", "睡莲", "荷叶", "莲叶", "莲"],
    ["Squash", "窝瓜", "倭瓜", "窝瓜大叔", "倭瓜大叔", "镇压者"],
    ["Threepeater", "三线射手", "三线", "三头豌豆", "三头", "三管", "三联装豌豆", "管"],
    ["Tangle Kelp", "缠绕海草", "海草", "缠绕海藻", "海藻", "缠绕海带", "毛线"],
    ["Jalapeno", "火爆辣椒", "辣椒", "墨西哥胡椒", "墨西哥辣椒", "辣", "椒"],
    ["Spikeweed", "地刺", "刺", "尖刺", "尖刺杂草", "棘草"],
    ["Torchwood", "火炬树桩", "火树", "火炬", "树桩", "火炬木", "火"],
    ["Tall-nut", "高坚果", "搞基果", "高建国", "巨大墙果", "巨大", "高墙果", "大土豆"],
    ["Sea-shroom", "海蘑菇", "水兵菇"],
    ["Plantern", "路灯花", "灯笼", "路灯", "灯笼草", "灯笼花", "吐槽灯", "灯"],
    ["Cactus", "仙人掌", "小仙", "掌"],
    ["Blover", "三叶草", "三叶", "风扇", "吹风", "愤青"],
    ["Split Pea", "裂荚射手", "裂荚", "双头", "分裂豌豆", "双头豌豆"],
    ["Starfruit", "杨桃", "星星", "星星果", "五角星", "1437", "大帝", "桃"],
    ["Pumpkin", "南瓜头", "南瓜", "南瓜罩", "南瓜壳", "套"],
    ["Magnet-shroom", "磁力菇", "磁铁", "磁力蘑菇", "磁"],
    ["Cabbage-pult", "卷心菜投手", "包菜", "卷心菜", "卷心菜投抛者"],
    ["Flower Pot", "花盆", "盆"],
    ["Kernel-pult", "玉米投手", "玉米", "黄油投手", "玉米投抛者"],
    ["Coffee Bean", "咖啡豆", "咖啡", "兴奋剂", "春药"],
    ["Garlic", "大蒜", "蒜"],
    ["Umbrella Leaf", "叶子保护伞", "莴苣", "白菜", "保护伞", "伞叶", "叶子", "伞", "叶"],
    ["Marigold", "金盏花", "金盏草", "金盏菊", "吐钱花"],
    ["Melon-pult", "西瓜投手", "西瓜", "绿皮瓜", "瓜", "西瓜投抛者"],
    ["Gatling Pea", "机枪射手", "机枪", "加特林豌豆", "加特林", "格林豌豆", "枪"],
    ["Twin Sunflower", "双子向日葵", "双子", "双向", "双花"],
    ["Gloom-shroom", "忧郁蘑菇", "忧郁", "忧郁菇", "章鱼", "曾哥", "曾哥蘑菇", "曾"],
    ["Cattail", "香蒲", "猫尾草", "猫尾", "猫尾香蒲", "小猫", "猫"],
    ["Winter Melon", "冰瓜", "'冰'瓜", '"冰"瓜', "冰西瓜", "冰冻西瓜"],
    ["Gold Magnet", "吸金磁", "吸金", "吸金草", "金磁铁"],
    ["Spikerock", "地刺王", "钢刺", "钢地刺", "尖刺岩石", "尖刺石", "石荆棘"],
    ["Cob Cannon", "玉米加农炮", "玉米炮", "加农炮", "春哥", "春哥炮", "炮", "春", "神"],
]

# # 确保没有重复项, 发布时注释掉 TODO
seeds_string_all = []
for items in seeds_string:
    seeds_string_all += items
assert len(seeds_string_all) == len(set(seeds_string_all))

# 模仿者卡片前缀
seeds_imitater_string = ["Imitater", "imitater", "模仿者", "模仿", "复制", "白", "小白", "变身茄子"]

# 整理成字典方便快速查找
# key: 卡片名称
# value: 卡片代号 0~47 (模仿者 +48)
seeds_string_dict = {}
for i, items in enumerate(seeds_string):
    for item in items:
        # 绿卡 紫卡
        seeds_string_dict[item] = i
        # 白卡
        for j, im in enumerate(seeds_imitater_string):
            seeds_string_dict[im + item] = i + 48
            seeds_string_dict[im + " " + item] = i + 48
# logger.info(f"卡片名称字符串字典 {seeds_string_dict}.")  # it's huge!!!


# 每张卡片在卡槽里的位置, 用于根据卡片代号找卡槽位置
seeds_in_slot = [None] * (48 * 2)

# 卡槽中每张卡片的代号, 用于根据卡槽位置找卡片代号
slot_seeds = [None] * 10


def update_seeds_list():
    """
    更新卡片相关数据. 该函数须在点击"Let's Rock!"后调用.
    """
    global seeds_in_slot, slot_seeds
    seeds_in_slot = [None] * (48 * 2)
    slot_seeds = [None] * 10

    slots_count = process.read_memory("int", 0x6A9EC0, 0x768, 0x144, 0x24)
    slots_offset = process.read_memory("unsigned int", 0x6A9EC0, 0x768, 0x144)
    for i in range(slots_count):
        seed_type = process.read_memory("int", slots_offset + 0x5C + i * 0x50)
        seed_imitater_type = process.read_memory("int", slots_offset + 0x60 + i * 0x50)
        if seed_type == 48:
            seed = seed_imitater_type + 48
        else:
            seed = seed_type
        seeds_in_slot[seed] = i + 1
        slot_seeds[i] = seed

    # logger.info(f"更新卡槽位置 {seeds_in_slot}.")  # 每张卡片在卡槽里的位置
    logger.info(f"更新卡片代号 {slot_seeds}.")  # 卡槽中每张卡片的代号


# 卡片名字 name
# 卡片代号 seed
# 卡槽位置 index


def get_seed_by_name(name: str) -> int:
    """
    根据卡片名字得到卡片代号. (模仿者 +48)
    """
    if name not in seeds_string_dict:
        logger.error(f"未知卡片名称: {name}.")
    return seeds_string_dict[name]


def get_index_by_seed(seed: int) -> int:
    """
    根据卡片代号得到卡槽位置. 不在返回 None.
    """
    if seed not in range(48 * 2):
        logger.error(f"卡片代号 {seed} 超出有效范围.")
    return seeds_in_slot[seed]


def get_index_by_name(name: str) -> int:
    """
    根据卡片名字得到卡槽位置. 不在返回 None.
    """
    if name not in seeds_string_dict:
        logger.error(f"未知卡片名称: {name}.")
    return seeds_in_slot[seeds_string_dict[name]]


def get_seed_by_index(index: int) -> int:
    """
    根据卡槽位置得到卡片代号.
    """
    if index not in range(1, 11):
        logger.error(f"卡槽位置 {index} 超出有效范围.")
    return slot_seeds[index - 1]


# (50, 160) 为左上角卡片中心坐标, (215, 160) 为模仿者选卡界面左上角卡片中心坐标, 单张卡片宽度约 50px 高度约 70px.
# 对于模仿者卡片, 需要把鼠标移动到目标位置 (490, 550) 才能成功点击, 单击完毕后移回原位, 延迟 0.2s 等待界面出现再选卡.
# 每次选完卡均等待 0.15s.

SEED_0_0_X = 50
SEED_0_0_Y = 160
IMITATER_SEED_0_0_X = 215
IMITATER_SEED_0_0_Y = 160
SEED_WIDTH = 50
SEED_HEIGHT = 70
IMITATER_X = 490
IMITATER_Y = 550


# 模拟手动选卡
simulate_manual_control = False


def select_seed_by_crood(row, col, imitater=False):
    """
    选择单张卡片.

    @参数 row(int): 行

    @参数 col(int): 列

    @参数 imitater(bool): 是否为模仿者
    """

    if imitater:
        if row not in (1, 2, 3, 4, 5):
            logger.critical(f"卡片行数 {row} 超出有效范围.")
        if col not in (1, 2, 3, 4, 5, 6, 7, 8):
            logger.critical(f"卡片列数 {col} 超出有效范围.")
    else:
        if row not in (1, 2, 3, 4, 5, 6):
            logger.critical(f"卡片行数 {row} 超出有效范围.")
        if col not in (1, 2, 3, 4, 5, 6, 7, 8):
            logger.critical(f"卡片列数 {col} 超出有效范围.")

    if simulate_manual_control:
        if imitater:
            mouse.move_to_click(IMITATER_X, IMITATER_Y)
            time.sleep(0.2)
            x = IMITATER_SEED_0_0_X + (col - 1) * (SEED_WIDTH + 1)
            y = IMITATER_SEED_0_0_Y + (row - 1) * (SEED_HEIGHT + 2)
        else:
            x = SEED_0_0_X + (col - 1) * (SEED_WIDTH + 3)
            y = SEED_0_0_Y + (row - 1) * (SEED_HEIGHT + 0)
        mouse.move_to_click(x, y)
        time.sleep(0.05)

    else:
        if imitater:
            mouse.special_button_click(IMITATER_X, IMITATER_Y)
            time.sleep(0.2)
            x = IMITATER_SEED_0_0_X + (col - 1) * (SEED_WIDTH + 1)
            y = IMITATER_SEED_0_0_Y + (row - 1) * (SEED_HEIGHT + 2)
        else:
            x = SEED_0_0_X + (col - 1) * (SEED_WIDTH + 3)
            y = SEED_0_0_Y + (row - 1) * (SEED_HEIGHT + 0)
        mouse.left_click(x, y)
        time.sleep(0.15)

    if imitater:
        im_str = seeds_imitater_string[0] + " "
    else:
        im_str = ""
    seed_str = seeds_string[(row - 1) * 8 + (col - 1)][0]
    logger.info(f"选择单张卡片 {im_str}{seed_str}.")


@functools.singledispatch
def seed_to_crood(seed):
    """
    卡片转换为 (行, 列, 模仿者) 的标准形式.
    
    根据参数类型选择不同的实现.

    @参数 seed(int/tuple/str): 卡片

    @示例:

    >>> seed_to_crood(14 + 48)
    (2, 7, True)

    >>> seed_to_crood((2, 7, True))
    (2, 7, True)

    >>> seed_to_crood("复制冰")
    (2, 7, True)
    """
    logger.error(f"卡片参数不支持 {type(seed)} 类型.")


@seed_to_crood.register(int)
def _(seed):
    if seed == 1437:
        row = 4
        col = 6
        imitater = False
    else:
        imitater = seed >= 48
        index = seed % 48
        row, col = divmod(index, 8)
    return row + 1, col + 1, imitater


@seed_to_crood.register(tuple)
def _(seed):
    if len(seed) == 2:
        row, col = seed
        imitater = False
    elif len(seed) == 3:
        row, col, im = seed
        imitater = im not in (False, 0)
    return row, col, imitater


@seed_to_crood.register(str)
def _(seed):
    if not seed in seeds_string_dict:
        logger.error(f"未知卡片名称: {seed}.")
    seed_index = seeds_string_dict[seed]  # 卡片代号(+48)
    imitater = seed_index >= 48
    index = seed_index % 48
    row, col = divmod(index, 8)
    return row + 1, col + 1, imitater


def select_all_seeds(seeds_selected=None):
    """
    选择所有卡片.
    """

    default_seeds = [40, 41, 42, 43, 44, 45, 46, 47, 8, 8 + 48]
    slots_count = process.read_memory("int", 0x6A9EC0, 0x768, 0x144, 0x24)

    # 默认八张紫卡和两张免费卡
    if seeds_selected is None:
        seeds_selected = default_seeds[0:slots_count]

    # 参数个数小于卡槽数则用默认卡片填充
    while len(seeds_selected) < slots_count:
        for seed in default_seeds:
            if seed_to_crood(seed) not in [seed_to_crood(s) for s in seeds_selected]:
                seeds_selected += [seed]
                break

    if len(seeds_selected) != slots_count:
        logger.critical(f"已选卡片数 {len(seeds_selected)} 不等于卡槽格数 {slots_count}.")

    # 卡片列表转换为标准形式
    seeds_selected = [seed_to_crood(seed) for seed in seeds_selected]
    logger.info(f"所选卡片转换为标准形式 {seeds_selected}.")

    retry_count = 0

    # TODO : check if exact match
    while process.read_memory("int", 0x6A9EC0, 0x774, 0xD24) < slots_count:

        if retry_count > 3:
            logger.critical(f"选卡重试多次失败, 哪里出错了.")
        retry_count += 1

        logger.info(f"选卡过程未完成, 正在重试.")

        # clear all seeds in slots
        for _ in range(10):
            if simulate_manual_control:
                mouse.move_to_click(108, 42)
            else:
                mouse.left_click(108, 42)
                time.sleep(0.1)
        time.sleep(0.2)

        # select all seeds
        for seed in seeds_selected:
            row, col, imitater = seed
            select_seed_by_crood(row, col, imitater)
        time.sleep(0.5)


def lets_rock():
    # if still in seeds select ui
    while process.read_memory("bool", 0x6A9EC0, 0x768, 0x15C, 0x2C):
        if simulate_manual_control:
            mouse.move_to_click(234, 567)
        else:
            mouse.left_down(234, 567)
            time.sleep(0.01)
            mouse.left_up(234, 567)
        time.sleep(0.3)

        # if there is dialog
        time.sleep(0.1)
        while process.read_memory("int", 0x6A9EC0, 0x320, 0x94) != 0:
            if simulate_manual_control:
                mouse.move_to_click(320, 400)
            else:
                mouse.left_click(320, 400)
            time.sleep(0.3)

    if simulate_manual_control:
        mouse.move_to_click(400, 640, False)


def select_seeds_and_lets_rock(seeds_selected=None):
    """
    选卡并开始游戏.

    选择所有卡片, 点击开始游戏, 更新加农炮列表, 更新卡片列表, 更新场景数据, 等待开场红字消失.

    @参数 seeds_selected(list): 卡片列表, 参数为空默认选择八张紫卡和两张免费卡. 参数个数小于卡槽数则用默认卡片填充.
    
    列表长度不大于卡槽格数. 单张卡片 seed 可用 int/tuple/str 表示, 不同表示方法可混用.

    seed(int): 卡片序号, 0 为豌豆射手, 47 为玉米加农炮, 对于模仿者这个数字再加上 48.

    seed(tuple): 卡片位置, 用 (行, 列, 是否模仿者) 表示, 第三项可省略, 默认非模仿者.

    seed(str): 卡片名称, 参考 seeds.py/seeds_string, 包含了一些常用名字.

    @示例:

    >>> SelectCards()

    >>> SelectCards([14, 14 + 48, 17, 2, 3, 30, 33, 13, 9, 8])

    >>> SelectCards([(2, 7), (2, 7, True), (3, 2), (1, 3, False), (1, 4, False), (4, 7), (5, 2), (2, 6), (2, 2), (2, 1),])

    >>> SelectCards(["寒冰菇", "复制冰", "窝瓜", "樱桃", "坚果", "南瓜", "花盆", "胆小", "阳光", "小喷"])

    >>> SelectCards(["小喷菇", "模仿者小喷菇"])
    """
    gc.collect()

    # process.set_pvz_foreground()
    delay.wait_for_game_stop()

    utils.update_game_base()

    select_all_seeds(seeds_selected)
    lets_rock()

    scene.update_game_scene()
    update_seeds_list()
    cobs.update_cob_cannon_list()

    delay.wait_for_game_start()
