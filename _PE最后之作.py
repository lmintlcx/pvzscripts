# coding=utf-8
"""
阵名: PE最后之作
出处: https://tieba.baidu.com/p/5102612180
节奏: ch5u-35.62s: PPDD|I-PPdd|IPP-PPDDCC, (6|13|16.62)
"""

from pvz import *

WriteMemory("int", 0x00679300, 0x0040FCED)  # 取消点炮限制

# @RunningInThread
# def DianCai():
#     diancai_list = ["保护伞", "胆小", "阳光", "小喷"]
#     diancai_spot = [(1, 8), (2, 8), (5, 8), (6, 8)]
#     import random
#     random.shuffle(diancai_list)
#     for i in range(4):
#         Card(diancai_list[i], diancai_spot[i])
#     Delay(10)
#     for i in range(4):
#         Shovel(diancai_spot[i])


@RunningInThread
def DianCai():
    Card("保护伞", (1, 8))
    Card("胆小", (2, 8))
    Card("阳光", (5, 8))
    Card("小喷", (6, 8))
    Delay(10)
    Shovel((1, 8))
    Shovel((2, 8))
    Shovel((5, 8))
    Shovel((6, 8))


@RunningInThread
def TallNutKeeper(spots):
    """
    泳池水路 7/8 列临时高坚果阻挡海豚.
    残血或被偷后自动补, 两行均有时中场种伞保护, 关底大波刷出后停止运行.
    @参数 spots(list[(int, int)]): 坐标.
    示例:
    >>> TallNutKeeper([(3, 7)])
    >>> TallNutKeeper([(3, 8), (4, 8)])
    """

    slots_offset = ReadMemory("unsigned int", 0x6A9EC0, 0x768, 0x144)
    slots_count = ReadMemory("unsigned int", 0x6A9EC0, 0x768, 0x144, 0x24)

    # 睡莲/高坚果/保护伞的卡槽数组下标
    lilypad_seed = None
    tallnut_seed = None
    umbrella_seed = None
    for i in range(slots_count):
        seed_type = ReadMemory("int", slots_offset + 0x5C + i * 0x50)
        if seed_type == 16:
            lilypad_seed = i
        elif seed_type == 23:
            tallnut_seed = i
        elif seed_type == 37:
            umbrella_seed = i

    # 返回值 (bool): 当前游戏是否暂停
    def GamePaused():
        return ReadMemory("bool", 0x6A9EC0, 0x768, 0x164)

    # 返回值 (int): 游戏界面
    def GameUI():
        return ReadMemory("int", 0x6A9EC0, 0x7FC)

    # 返回值 (int): 已刷新波数
    def CurrentWave():
        return ReadMemory("int", 0x6A9EC0, 0x768, 0x557C)

    # 返回值 (int): 下一波刷新倒计时
    def WaveCountdown():
        return ReadMemory("int", 0x6A9EC0, 0x768, 0x559C)

    # 获取指定位置的高坚果下标, 没有返回 None
    def GetTheTallnutIndex(r, c):
        plants_count_max = ReadMemory("int", 0x6A9EC0, 0x768, 0xB0)
        plants_offset = ReadMemory("unsigned int", 0x6A9EC0, 0x768, 0xAC)
        for i in range(plants_count_max):
            plant_disappeared = ReadMemory("bool", plants_offset + 0x141 + 0x14C * i)
            plant_crushed = ReadMemory("bool", plants_offset + 0x142 + 0x14C * i)
            plant_type = ReadMemory("int", plants_offset + 0x24 + 0x14C * i)
            plant_row = ReadMemory("int", plants_offset + 0x1C + 0x14C * i)
            plant_col = ReadMemory("int", plants_offset + 0x28 + 0x14C * i)
            if (not plant_disappeared and not plant_crushed \
            and plant_type == 23 and plant_row == (r - 1) and plant_col == (c - 1)):
                return i

    # 更新高坚果
    def UpdateTallnut(r, c):
        slots_offset = ReadMemory("unsigned int", 0x6A9EC0, 0x768, 0x144)
        seed_usable = ReadMemory("bool", slots_offset + 0x70 + tallnut_seed * 0x50)  # 该卡片是否可用
        seed_cost = ReadMemory("int", 0x69F2C0 + 23 * 0x24)  # 卡片价格
        sun = ReadMemory("int", 0x6A9EC0, 0x768, 0x5560)  # 当前阳光
        if seed_usable and sun >= seed_cost:
            while GamePaused():
                Delay(1)
            Card("高坚果", (r, c))

    # 开场种
    Delay(800)  # TODO 让给存冰位先
    for spot in spots:
        while GamePaused():
            Delay(1)
        Card("睡莲", spot)
        Card("高坚果", spot)
        if spot != spots[-1]:  # 不是最后一个
            Delay(3000 + 1)
    Delay(1)

    # 保护伞状态, 种植于第一个高坚果前一列
    umbrella_planted = False  # 已经种植
    umbrella_shoveled = False  # 已经铲除
    umbrella_row, umbrella_col = spots[0][0], spots[0][1] + 1

    # 主循环, 第 20 波刷新前持续运行
    while GameUI() == 3 and CurrentWave() < 20:

        # 两列均有高坚果时, 第 10 波刷新前种伞, 第 11 波铲掉
        if len(spots) == 2 and umbrella_seed is not None:
            if not umbrella_planted and 9 <= CurrentWave() <= 10 and WaveCountdown() <= 600:
                while GamePaused():
                    Delay(1)
                # print("Planting Umbrella Leaf to protect 2 Tall-nuts.")
                Card("睡莲", (umbrella_row, umbrella_col))
                Card("伞叶", (umbrella_row, umbrella_col))
                umbrella_planted = True
            elif not umbrella_shoveled and CurrentWave() >= 11:
                while GamePaused():
                    Delay(1)
                # print("Shovel Umbrella Leaf.")
                Shovel((umbrella_row, umbrella_col))
                Shovel((umbrella_row, umbrella_col))
                umbrella_shoveled = True

        # 遍历指定要种植高坚果的格点
        for spot in spots:
            row, col = spot
            index = GetTheTallnutIndex(row, col)  # 获取该格点的高坚果下标
            if index is None:
                # 没有则补种高坚果
                UpdateTallnut(row, col)
                Delay(3000 + 1)
            else:
                plants_offset = ReadMemory("unsigned int", 0x6A9EC0, 0x768, 0xAC)
                plant_hp = ReadMemory("int", plants_offset + 0x40 + 0x14C * index)
                if plant_hp < 2000:
                    # 血量低于一定值则修复高坚果
                    UpdateTallnut(row, col)
                    Delay(3000 + 1)

        Sleep(100)  # 每 1s 检测一次


###
###
###

SetZombies(["普僵", "撑杆", "舞王", "冰车", "海豚", "矿工", "跳跳", "蹦极", "扶梯", "篮球", "白眼", "红眼"])

SelectCards(["咖啡豆", "寒冰菇", "复制冰", "睡莲", "高坚果", "樱桃", "保护伞", "胆小", "阳光", "小喷"])

# UpdatePaoList([
#     (1, 1), (2, 1), (5, 1), (6, 1), \
#     (1, 3), (2, 3), (5, 3), (6, 3), \
#     (1, 6), (2, 6), (3, 6), (4, 6), (5, 6), (6, 6), \
#     ])

while ReadMemory("int", 0x6A9EC0, 0x7FC) != 3:  # 还没进入战斗界面
    Sleep(1)
while ReadMemory("bool", 0x6A9EC0, 0x768, 0x164):  # 处于暂停状态
    Sleep(1)
Card("睡莲", (3, 3))  # 临时存冰位

AutoCollect()  # 自动收集资源
IceSpots([(1, 5), (6, 5), (3, 3)], 13)
TallNutKeeper([(3, 8), (4, 8)])

for wave in range(1, 21):
    print("当前操作波次: " + str(wave))

    if wave in (1, ):
        Prejudge(-95, wave)
        Pao((2, 9), (5, 9))
        Delay(110)
        Pao((1, 7.7), (5, 7.7))

    elif wave in (2, 10):
        Prejudge(-15, wave)
        Pao((2, 9), (5, 9))
        Until(-15 + 107)
        Pao((1, 7.625), (5, 7.625))
        if wave == 10:
            Until(-15 + 373 - 100)
            Card("樱桃", (2, 9))  # A
        Until(601 + 20 - 298)  # 20cs 预判冰
        Coffee()

    elif wave in (3, 6, 9, 11, 14, 17):  # I-PPdd
        Prejudge(1300 - 200 - 373, wave)
        Pao((2, 8.8), (5, 8.8))
        Until(1300 + 20 - 298)  # 20cs 预判冰
        Coffee()
        Until(1300 - 200 - 373 + 350)  # 减速尾炸
        Pao((1, 2.4), (5, 2.4))
        if wave == 9:
            Until(1300 + 180)
            Pao((1, 7.2), (5, 7.2))  # 可省略
            Until(1300 + 1662 - 200 - 373)
            Pao((2, 8.8), (5, 8.8))
            Delay(81)
            DianCai()
            Delay(220 - 81)
            Pao((1, 7.8), (5, 7.8))
            Skip(4)

    elif wave in (4, 7, 12, 15, 18):  # IPP-PPDDC
        Prejudge(180, wave)
        Pao((1, 7.2), (5, 7.2))
        Until(1662 - 200 - 373)
        Pao((2, 8.8), (5, 8.8))
        Delay(81)
        DianCai()
        Delay(220 - 81)
        Pao((1, 7.4), (5, 7.4))  # 左移

    elif wave in (5, 8, 13, 16, 19):  # PPDD
        Prejudge(-15, wave)
        Pao((2, 9), (5, 9))
        Until(-15 + 107)
        Pao((1, 7.625), (5, 7.625))
        Until(601 + 20 - 298)  # 20cs 预判冰
        Coffee()
        if wave == 19:
            Until(601 + 1300 - 200 - 373)
            Delay(100)  # 尾炸炮时机微调
            Pao((2, 8.8), (5, 8.8))
            Delay(220)
            Pao((1, 7.8), (5, 7.8))
            Skip(3)

    elif wave in (20, ):
        Prejudge(-150, wave)
        Pao((4, 7))
        Until(-60)
        Pao((1, 9), (2, 9), (5, 9), (6, 9))
        Delay(108)
        Pao((1, 9), (2, 9), (5, 9), (6, 9))
