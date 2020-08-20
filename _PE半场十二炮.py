# coding=utf-8
"""
阵名: PE半场十二炮
出处: https://tieba.baidu.com/p/1801759994
节奏: ch4: I+BC/d-PDD/P|I+BC/d-PDD/P, (18|18)
"""

from pvz import *

WriteMemory("int", 0x00679300, 0x0040FCED)  # 取消点炮限制


# 种垫铲垫
@RunningInThread
def DianCai():
    Card("小喷", (1, 9))
    Card("阳光", (2, 9))
    Delay(100)
    Shovel((1, 9))
    Shovel((2, 9))


# 烧小偷
@RunningInThread
def 口吐金蛇():
    # 等第 10 波刷新
    while ReadMemory("int", 0x6A9EC0, 0x768, 0x557C) < 10:
        Sleep(1)
    Delay(400)
    Card("睡莲", (4, 9))
    Card("辣椒", (4, 9))
    Delay(100 + 1)
    Shovel((4, 9))
    # 等第 20 波刷新
    while ReadMemory("int", 0x6A9EC0, 0x768, 0x557C) < 20:
        Sleep(1)
    Delay(400)
    Card("睡莲", (4, 9))
    Card("辣椒", (4, 9))
    Delay(100 + 1)
    Shovel((4, 9))



@RunningInThread
def NutsFixer(spots, seed):
    """
    坚果类植物修复. 在单独的子线程运行.
    @参数 spots(list): 位置, 包括若干个 (行, 列) 元组.
    @参数 seed(str): 卡片名称, 可选值 ["坚果", "高坚果", "南瓜头"].
    @示例:
    >>> NutsFixer([(3, 8), (4, 8)], "高坚果")
    >>> NutsFixer([(4, 5),(4, 6),(4, 7),(4, 8)], "南瓜头")
    """

    # 1.草地 2.裸地 3.泳池
    # 16.睡莲 33.花盆
    # 3.坚果 23.高坚果 30.南瓜头

    from pvz.core import debug
    from pvz.core import info
    from pvz.core import warning
    from pvz.core import error
    from pvz.core import read_memory
    from pvz.core import thread_sleep_for
    from pvz.extra import get_seed_by_name
    from pvz.extra import get_index_by_name
    from pvz.extra import get_block_type
    from pvz.extra import get_plants_croods
    from pvz.extra import use_seed
    from pvz.extra import game_scene
    from pvz.extra import game_delay_for

    while read_memory("int", 0x6A9EC0, 0x7FC) != 3:
        thread_sleep_for(1)

    info("启动坚果类植物修复线程.")

    seed_type = get_seed_by_name(seed)  # 根据名称得到卡片代号
    if seed_type not in (3, 23, 30, 3 + 48, 23 + 48, 30 + 48):
        error("自动修复只支持 坚果/高坚果/南瓜头.")
    seed_index = get_index_by_name(seed)  # 获取卡片的位置, 数组下标需要 -1
    if seed_index is None:
        error("卡槽没有 %s 卡片, 退出坚果类植物修复线程." % seed)

    seed_cost = read_memory("int", 0x69F2C0 + seed_type * 0x24)  # 卡片价格
    seed_recharge = read_memory("int", 0x69F2C4 + seed_type * 0x24)  # 卡片冷却
    # HP_MAX = 4000 if seed_type in (3, 30) else 8000
    if seed_type == 3:  # Wall-nut
        HP_MAX = read_memory("int", 0x45E1A7)
    elif seed_type == 23:  # Tall-nut
        HP_MAX = read_memory("int", 0x45E215)
    else:  # 30 Pumpkin
        HP_MAX = read_memory("int", 0x45E445)
    LINIT = int(HP_MAX * 0.1) if len(spots) < 2 else int(HP_MAX * 0.3)  # TODO

    # 补种函数
    def fix(spot):
        slots_offset = read_memory("unsigned int", 0x6A9EC0, 0x768, 0x144)
        seed_usable = read_memory("bool", slots_offset + 0x70 + (seed_index - 1) * 0x50)  # 该卡片是否可用
        sun = read_memory("int", 0x6A9EC0, 0x768, 0x5560)  # 当前阳光
        if seed_usable and sun >= seed_cost:
            while read_memory("bool", 0x6A9EC0, 0x768, 0x164):  # 处于暂停
                thread_sleep_for(1)
        else:
            return False
        success = False
        if get_block_type(spot) == 3 and (16, spot[0], spot[1]) not in get_plants_croods():
            seed_lilypad_index = get_index_by_name("睡莲")
            if seed_lilypad_index is None:
                warning("卡片 睡莲 不在卡槽中.")
            else:
                seed_lilypad_usable = read_memory("bool", slots_offset + 0x70 + (seed_lilypad_index - 1) * 0x50)
                if seed_lilypad_usable:
                    use_seed("睡莲", spot)
                    use_seed(seed, spot)
                    success = True
        elif game_scene in (4, 5) and (33, spot[0], spot[1]) not in get_plants_croods():
            seed_flowerpot_index = get_index_by_name("花盆")
            if seed_flowerpot_index is None:
                warning("卡片 花盆 不在卡槽中.")
            else:
                seed_flowerpot_usable = read_memory("bool", slots_offset + 0x70 + (seed_flowerpot_index - 1) * 0x50)
                if seed_flowerpot_usable:
                    use_seed("花盆", spot)
                    use_seed(seed, spot)
                    success = True
        else:
            use_seed(seed, spot)
            success = True
        thread_sleep_for(1)
        return success

    while read_memory("int", 0x6A9EC0, 0x7FC) == 3 and read_memory("int", 0x6A9EC0, 0x768, 0x557C) < 20:
    # while read_memory("int", 0x6A9EC0, 0x7FC) == 3:

        croods_which_has_plant = []
        plants = get_plants_croods()
        for plant_type, plant_row, plant_col in plants:
            # 需要修复的植物是 南瓜 时, 只有南瓜才算占位
            # 需要修复的植物是 坚果/高坚果 时, 不是 睡莲/花盆/南瓜 就算占位
            if (seed_type in (30, 30 + 48) and plant_type in (30, 30 + 48)) or (seed_type not in (30, 30 + 48)
                                                                                and plant_type not in (16, 30, 33)):
                croods_which_has_plant.append((plant_row, plant_col))
                if plant_type == 47:  # 玉米炮占两格
                    croods_which_has_plant.append((plant_row, plant_col + 1))
        spot_which_has_plant = [i for i in spots if i in croods_which_has_plant]

        for spot in spots:
            # 位置有植物但不是坚果/高坚果/南瓜
            if spot in spot_which_has_plant and (seed_type, spot[0], spot[1]) not in plants:
                thread_sleep_for(1)
                continue
            # 位置有植物而且是坚果/高坚果/南瓜
            elif spot in spot_which_has_plant and (seed_type, spot[0], spot[1]) in plants:
                plants_count_max = read_memory("unsigned int", 0x6A9EC0, 0x768, 0xB0)
                plants_offset = read_memory("unsigned int", 0x6A9EC0, 0x768, 0xAC)
                plants_index = None
                for i in range(plants_count_max):
                    plants_disappeared = read_memory("bool", plants_offset + 0x141 + 0x14C * i)
                    plants_crushed = read_memory("bool", plants_offset + 0x142 + 0x14C * i)
                    plants_type = read_memory("int", plants_offset + 0x24 + 0x14C * i)
                    plants_row = read_memory("int", plants_offset + 0x1C + 0x14C * i)
                    plants_col = read_memory("int", plants_offset + 0x28 + 0x14C * i)
                    if (not plants_disappeared and not plants_crushed and plants_type == seed_type and plants_row == spot[0] - 1
                            and plants_col == spot[1] - 1):  # 特定位置
                        plants_index = i
                debug("位置 %s 的植物 %s 下标为 %d." % (str(spot), seed, plants_index))
                plant_hp = read_memory("int", plants_offset + 0x40 + 0x14C * plants_index)
                debug("位置 %s 的植物 %s 血量为 %d." % (str(spot), seed, plant_hp))
                if plant_hp < LINIT:
                    if fix(spot):  # 种植
                        game_delay_for(seed_recharge + 1)
                    break
            # 位置没有植物
            elif spot not in spot_which_has_plant:
                if fix(spot):  # 种植
                    game_delay_for(seed_recharge + 1)
                break

        game_delay_for(10)

    info("停止坚果类植物修复线程.")



###

SetZombies(["普僵", "撑杆", "舞王", "冰车", "海豚", "矿工", "跳跳", "蹦极", "扶梯", "篮球", "白眼", "红眼"])

SelectCards(["白冰", "冰菇", "咖啡", "荷叶", "南瓜", "樱桃", "辣椒", "倭瓜", "阳光", "小喷"])

UpdatePaoList([
    (1, 3), (2, 3), (3, 3), \
    (1, 5), (2, 5), (3, 5), \
    (1, 7), (2, 7), (3, 7), \
    (1, 1), (2, 1), (3, 1), \
    ])


while ReadMemory("int", 0x6A9EC0, 0x7FC) != 3:  # 还没进入战斗界面
    Sleep(1)
while ReadMemory("bool", 0x6A9EC0, 0x768, 0x164):  # 处于暂停状态
    Sleep(1)
Card("寒冰菇", (5, 5))  # 临时存冰
Card("睡莲", (3, 9))  # 临时存冰位
Card("南瓜头", (3, 9))  # 其实不需要


AutoCollect()  # 自动收集资源
IceSpots([(4, 5), (4, 6), (4, 7), (4, 8), (3, 9)], 17 - 1)
NutsFixer([(4, 5), (4, 6), (4, 7), (4, 8)], "南瓜头")
口吐金蛇()


for wave in range(1, 21):
    print("当前操作波次: " + str(wave))
    Prejudge(-190, wave)

    if wave in (1, 10):
        Until(-95)
        Pao((1, 9))
        Until(-15)
        Pao((2, 9), (5, 9))
        Until(-15 + 110)
        Pao((5, 7.7))
        Until(-15 + 110 + 373 - 100)  # 368
        Card("樱桃", (1, 9))

    elif wave == 20:
        Until(-150)
        Pao((4, 7))
        Until(-60)  # 等到刷新前 60cs
        Pao((2, 9), (5, 9), (2, 9), (5, 9))
        Until(-60 + 110)
        Pao((1, 8.8), (2, 8.8))  # 炮不够 ==
        Until(-60 + 110 + 373 - 100)
        Card("樱桃", (5, 9))
        print("第 %s 波手动收尾." % wave)
        # Pao((5, 8))
        Until(5500 + 100)
        Shovel((3, 9), (3, 9))  # 跳白字后铲掉

    else:
        Until(-133)
        Pao((1, 8.0))  # 拦截上波红眼, 分离部分快速僵尸
        Until(360 - 373)
        Pao((2, 8.15))  # 无冰分离
        Until(360 - 298)  # 360cs 反应冰
        Coffee() if wave not in (2,) else Card("咖啡豆", (5, 5))
        Until(360 + 500 - 373)
        # WZ_PNT = (5, 2.7) if wave in (3, 12) else (5, 3)  # 尾炸落点
        WZ_PNT = (5, 3)
        Pao(WZ_PNT) if wave not in (2, 11) else None  # 下半场尾炸
        Until(1800 - 200 - 373)
        Pao((2, 9), (5, 8.1))  # 激活炸
        Delay(10)
        DianCai()  # 垫撑杆
        Until(1800 - 200 - 373 + 220)
        Pao((1, 8.2))  # 秒白眼, 触发红眼投掷

        if wave in (9, 19):  # 收尾波次
            Until(1800 - 133)
            Pao((1, 8.0))
            Until(1800 + 360 - 373)
            Pao((2, 9))
            Until(1800 + 360 + 500 - 373)
            Pao((5, 2.5))
            Until(1800 + 1800 - 200 - 373)
            Pao((5, 6))
            Delay(110)
            Pao((5, 6))
            Delay(110)
            Pao((5, 3))
            Until(4500 - 200 - 373)
            Pao((5, 5))
            Skip(2) if wave == 9 else None  # 中场调整炮序
