# coding=utf-8

"""
Author: lmintlcx
Date: 2018-11-24
---
Name: PE真二炮 (2字十六炮)
Rhythm: ch5-35.4s: PPddCC|IPPCC-PPDD|IPPCC-PPDD, (6|14.7|14.7)
Video:
- https://www.bilibili.com/video/av35369870
- https://youtu.be/dS2iNkAOoHQ
"""

from pvz import *


# 种垫材
def DianCai():
    Card("胆小菇", (1, 9))
    Card("阳光菇", (2, 9))
    # Card("花盆", (5, 9))
    Card("小喷菇", (6, 9))


# 铲垫材
def ChanDianCai():
    Shovel((1, 9))
    Shovel((2, 9))
    # Shovel((5, 9))
    Shovel((6, 9))


@RunningInThread
def StartTallNutKeeperThread(spots):
    """
    泳池水路 7/8 列临时高坚果阻挡海豚.
    残血或被偷后自动补, 两行均有时中场种伞保护, 关底大波刷出后停止运行.
    @参数 spots(list[(int, int)]): 坐标.
    示例:
    >>> StartTallNutKeeperThread([(3, 7)])
    >>> StartTallNutKeeperThread([(3, 8), (4, 8)])
    """

    slots_offset = ReadMemory("unsigned int", 0x6A9EC0, 0x768, 0x144)
    slots_count = ReadMemory("unsigned int", 0x6A9EC0, 0x768, 0x144, 0x24)

    # 睡莲/高坚果/保护伞的下标
    lilypad_seed = None
    tallnut_seed = None
    umbrella_seed = None
    for i in range(slots_count):
        seed_type = ReadMemory("int", slots_offset + 0x5C + i * 0x50)
        if seed_type == 16:
            lilypad_seed = i
        if seed_type == 23:
            tallnut_seed = i
        if seed_type == 37:
            umbrella_seed = i

    # 游戏界面
    def GameUI():
        return ReadMemory("int", 0x6A9EC0, 0x7FC)

    # 是否暂停
    def GamePaused():
        return ReadMemory("bool", 0x6A9EC0, 0x768, 0x164)

    # (非旗帜波)刷新倒计时
    def WaveCountdown():
        return ReadMemory("int", 0x6A9EC0, 0x768, 0x559C)

    # 当前刷新波数
    def CurrentWave():
        return ReadMemory("int", 0x6A9EC0, 0x768, 0x557C)

    # 获取指定位置的高坚果下标, 没有返回 None
    def GetTheTallnutIndex(r, c):
        plant_count_max = ReadMemory("int", 0x6A9EC0, 0x768, 0xB0)
        plant_offset = ReadMemory("unsigned int", 0x6A9EC0, 0x768, 0xAC)
        for i in range(plant_count_max):
            plant_disappeared = ReadMemory("bool", plant_offset + 0x141 + 0x14C * i)
            plant_crushed = ReadMemory("bool", plant_offset + 0x142 + 0x14C * i)
            plant_type = ReadMemory("int", plant_offset + 0x24 + 0x14C * i)
            plant_row = ReadMemory("int", plant_offset + 0x1C + 0x14C * i)
            plant_col = ReadMemory("int", plant_offset + 0x28 + 0x14C * i)
            if (
                not plant_disappeared
                and not plant_crushed
                and plant_type == 23
                and plant_row == (r - 1)
                and plant_col == (c - 1)
            ):
                return i

    # 更新高坚果
    def UpdateTallnut(r, c):
        slots_offset = ReadMemory("unsigned int", 0x6A9EC0, 0x768, 0x144)
        seed_usable = ReadMemory("bool", slots_offset + 0x70 + tallnut_seed * 0x50) # 该卡片是否可用
        seed_cost = ReadMemory("int", 0x69F2C0 + 23 * 0x24) # 卡片价格
        sun = ReadMemory("int", 0x6A9EC0, 0x768, 0x5560) # 当前阳光
        if seed_usable and sun >= seed_cost:
            while GamePaused():
                Delay(1)
            Card("高坚果", r, c)

    # 开场种
    for spot in spots:
        while GamePaused():
            Delay(1)
        Card("睡莲", spot)
        Card("高坚果", spot)
        if spot != spots[-1]: # 不是最后一个
            Delay(3000 + 1)
    Delay(1)

    # 保护伞状态, 种植于第一个高坚果前一列
    umbrella_planted = False
    umbrella_shoveled = False
    umbrella_row, umbrella_col = spots[0][0], spots[0][1] + 1

    # 主循环, 第 20 波刷新前持续运行
    while GameUI() == 3 and CurrentWave() < 20:

        # 两列均有高坚果时, 第 10 波刷新前种伞, 第 11 波铲掉
        if len(spots) == 2 and umbrella_seed is not None:
            if not umbrella_planted and 9 <= CurrentWave() <= 10 and WaveCountdown() <= 600:
                while GamePaused():
                    Delay(1)
                print("Planting Umbrella Leaf to protect 2 Tall-nuts.")
                Card("睡莲", umbrella_row, umbrella_col) 
                Card("伞叶", umbrella_row, umbrella_col) 
                umbrella_planted = True
            if not umbrella_shoveled and CurrentWave() >= 11:
                while GamePaused():
                    Delay(1)
                print("Shovel Umbrella Leaf.")
                Shovel(umbrella_row, umbrella_col)
                Shovel(umbrella_row, umbrella_col)
                umbrella_shoveled = True

        # 遍历指定要种植高坚果的格点
        for spot in spots:
            row, col = spot
            index = GetTheTallnutIndex(row, col) # 获取该格点的高坚果下标
            if index is None:
                # 没有则补种高坚果
                UpdateTallnut(row, col)
                Delay(3000 + 1)
            else:
                plant_offset = ReadMemory("unsigned int", 0x6A9EC0, 0x768, 0xAC)
                plant_hp = ReadMemory("int", plant_offset + 0x40 + 0x14C * index)
                if plant_hp < 2000:
                    # 血量低于一定值则修复高坚果
                    UpdateTallnut(row, col)
                    Delay(3000 + 1)

        Sleep(100) # 每 1s 检测一次

###
###
###

Sleep(300)

SelectCards(["复制冰", "寒冰菇", "咖啡豆", "睡莲", "高坚果", "樱桃", "花盆", "胆小", "阳光", "小喷"])

# UpdatePaoList([(1, 2), (1, 4), (1, 6), (2, 1), (2, 5), (2, 7), (3, 4), (3, 6), (4, 3), (4, 5), (5, 2), (5, 4), (6, 1), (6, 3), (6, 5), (6, 7)])

StartAutoCollectThread()
StartAutoFillIceThread([(5, 1), (4, 1), (2, 3), (2, 4)], 13)
StartTallNutKeeperThread([(3, 8)])


for wave in range(1, 21):

    # 精准之舞
    if wave in (1,):
        Prejudge(-15, wave)
        Pao((2, 9), (5, 9))
        Delay(107)
        Pao((1, 7.625), (5, 7.625))

    # PPDDCC
    elif wave in (2,):
        Prejudge(-135, wave)
        Pao((2, 9), (5, 9))
        Until(-135 + 110)
        Pao((1, 7.7), (5, 7.7))
        Until(600 + 10 - 298)  # 10cs 预判冰
        Coffee()
        Until(600 - 175)  # 190
        DianCai()
        Until(600 - 175 + 10)
        ChanDianCai()

    # PPADDCC
    elif wave in (10,):
        Prejudge(-135, wave)
        Pao((2, 9), (5, 9))
        Until(-135 + 110)
        Pao((1, 9), (5, 7.6))
        Until(-135 + 373 - 100)
        Card("樱桃", 2, 9)  # A
        Until(600 + 10 - 298)  # 10cs 预判冰
        Coffee()
        Until(600 - 175)  # 190
        DianCai()
        Until(600 - 175 + 10)
        ChanDianCai()

    # IPPCC-PPDD
    elif wave in (3, 6, 9, 11, 14, 17):
        Prejudge(180, wave)  # 刷新后 180
        Pao((1, 7.2), (5, 7.2))
        Until(630)
        DianCai()
        Until(1470 - 200 - 373 - 43)
        ChanDianCai()
        Until(1470 - 200 - 373)
        Pao((2, 9), (5, 9))
        Until(1470 - 200 - 373 + 220)
        Pao((1, 7.5), (5, 7.5))
        Until(1470 + 15 - 298)  # 15cs 预判冰
        Coffee()
        if wave == 9:
            Until(1470 + 180)
            Pao((5, 7.2), (1, 7.2))  # 调整炮序
            Until(1470 + 630)
            DianCai()
            Until(1470 + 1470 - 200 - 373 - 43)
            ChanDianCai()
            Until(1470 + 1470 - 200 - 373)
            Pao((2, 9), (5, 9))
            Delay(220)
            Pao((1, 7.8), (5, 7.8))
            SkipPao(4)  # 预留收尾

    # IPPCC-PPDD
    elif wave in (4, 7, 12, 15, 18):
        Prejudge(180, wave)
        Pao((5, 7.2), (1, 7.2))  # 调整炮序
        Until(630)
        DianCai()
        Until(1470 - 200 - 373 - 43)
        ChanDianCai()
        Until(1470 - 200 - 373)
        Pao((2, 9), (5, 9))
        Delay(220)
        Pao((1, 8.5), (5, 8.5))

    # PPddCC
    elif wave in (5, 8, 13, 16, 19):
        Prejudge(-135, wave)
        Pao((1, 8.8), (5, 8.8))
        Until(-135 + 250)  # 原速尾炸参考时机
        # 调整炮序
        if wave in (13, 16, 19):
            Pao((5, 4.5), (1, 4.5))
        else:
            Pao((1, 4.5), (5, 4.5))
        Until(600 + 10 - 298)  # 10cs 预判冰
        Coffee()
        Until(600 - 175)
        DianCai()
        Until(600 - 175 + 10)
        ChanDianCai()
        if wave == 19:
            Until(600 + 180)
            Pao((1, 7.2), (5, 7.2))
            Until(600 + 630)
            DianCai()
            Until(600 + 1470 - 200 - 373 - 43)
            ChanDianCai()
            Until(600 + 1470 - 200 - 373)
            Pao((2, 9), (5, 9))
            Delay(220)
            Pao((1, 7.8), (5, 7.8))
            SkipPao(4)  # 预留收尾

    elif wave in (20,):
        Prejudge(-150, wave)
        Pao(4, 7)
        Until(-60)  # 等到刷新前 60cs
        Pao((1, 9), (2, 9), (5, 9), (6, 9))
        Delay(108)
        Pao((1, 9), (2, 9), (5, 9), (6, 9))
