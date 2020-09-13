# coding=utf-8
"""
阵名: RE椭盘十四炮
出处: https://tieba.baidu.com/p/5029428684
节奏: ch4: ICE3+PPDD+B-PP|ICE3+PPDD+B-PP, (1780|1780)
"""

from pvz import *


# 冰三修正函数
@RunningInThread
def ICE3(t):
    clock = ReadMemory("int", 0x6A9EC0, 0x768, 0x5568)  # 基准时间
    while (ReadMemory("int", 0x6A9EC0, 0x768, 0x5568) - clock) < (t - 50):
        Sleep(0.1)
    ice_index = 0
    plants_count_max = ReadMemory("unsigned int", 0x6A9EC0, 0x768, 0xB0)
    plants_offset = ReadMemory("unsigned int", 0x6A9EC0, 0x768, 0xAC)
    for i in range(plants_count_max):
        plant_dead = ReadMemory("bool", plants_offset + 0x141 + 0x14C * i)
        plant_crushed = ReadMemory("bool", plants_offset + 0x142 + 0x14C * i)
        plant_type = ReadMemory("int", plants_offset + 0x24 + 0x14C * i)
        plant_countdown = ReadMemory("int", plants_offset + 0x50 + 0x14C * i)
        if not plant_dead and not plant_crushed and plant_type == 14 and 45 < plant_countdown < 55:
            ice_index = i
            break
    while (ReadMemory("int", 0x6A9EC0, 0x768, 0x5568) - clock) < (t - 10):
        Sleep(0.1)
    WriteMemory("int", 11, plants_offset + 0x50 + 0x14C * ice_index)


WriteMemory("int", 0x00679300, 0x0040FCED)  # 取消点炮限制

SetZombies(["普僵", "撑杆", "橄榄", "冰车", "小丑", "气球", "跳跳", "蹦极", "扶梯", "篮球", "白眼", "红眼"])

SelectCards(["花盆", "寒冰菇", "模仿者寒冰菇", "毁灭菇", "咖啡豆", "樱桃炸弹", "火爆辣椒", "倭瓜", "寒冰射手", "坚果墙"])

UpdatePaoList([
    (4, 2),  # P
    (4, 4),  # P
    (1, 4),  # D
    (5, 4),  # D
    (5, 6),  # B
    (3, 1),  # P
    (4, 7),  # P
    ###
    (1, 2),  # P
    (2, 4),  # P
    (3, 3),  # D
    (3, 5),  # D
    (2, 6),  # B
    (2, 1),  # P
    (3, 7),  # P
])
# IPPDDP-PP IPPDDP-PP  14
# PPDDDD    IP-PP      9
# PPSSDD    IAA'aP-PP  9
Skip(5)  # 调整炮序
# while ReadMemory("int", 0x6A9EC0, 0x7FC) != 3:
#     Sleep(1)
# while ReadMemory("bool", 0x6A9EC0, 0x768, 0x164):
#     Sleep(1)
Card("花盆", (1, 7))
Card("寒冰菇", (1, 7))

AutoCollect([1, 2, 3, 4, 5, 6, 17], 15)
IceSpots([(4, 6), (2, 3), (1, 1), (1, 6)], 18 - 1)

for wave in range(1, 21):
    print("当前操作波次: " + str(wave))

    if wave in (1, ):
        Prejudge(-190, wave)
        Until(377 - 373)
        RoofPao((2, 8.8), (4, 8.8))
        Until(506 - 373)
        RoofPao((2, 8.8), (4, 8.8))
        Until(601 + 34 - 373)
        RoofPao((2, 8.8), (4, 8.8))
        Until(601 + 34 - 298)
        Card("咖啡豆", (1, 7))  # Coffee()
        ICE3(298)

    elif wave in (2, ):
        Prejudge(-190, wave)
        Until(50)
        Shovel((1, 7))  # 铲
        Until(1300 - 200 - 373)  # 727
        RoofPao((4, 8.2))
        Until(1780 - 200 - 373)  # 1207
        RoofPao((2, 9), (4, 9))
        Until(1780 + 10 - 298)  # 1492
        Coffee()
        ICE3(298)

    elif wave in (10, ):
        Prejudge(-15, wave)
        RoofPao((2, 9), (4, 9), (2, 9), (4, 9))
        Until(-15 + 110)  # 95
        RoofPao((4, 7.7))  # 空炸小鬼兼小偷
        Until(-15 + 190)  # 175
        RoofPao((1, 5))  # 2-5? 尾炸小鬼兼小偷
        Until(601 + 10 - 298)  # 313
        Coffee()
        ICE3(298)

    elif wave in (11, ):
        Prejudge(-190, wave)
        Until(10 + 400 - 100)
        Card("辣椒", (1, 7))
        Card("花盆", (4, 9))
        Card("樱桃", (4, 9))
        Until(10 + 400 + 10)
        Shovel((1, 7))  # 铲
        Shovel((4, 9))  # 铲
        Until(1250 - 200 - 373)  # 1300->1250
        RoofPao((3, 8.21))  # 落点改为 3 路炸掉 2 路冰车
        Until(1780 - 200 - 373)
        RoofPao((2, 9), (4, 9))
        Until(1780 + 10 - 298)
        Coffee()
        ICE3(298)

    elif wave in (3, 12):
        Prejudge(-190, wave)
        Until(10 + 400 - 373)
        RoofPao((2, 9), (4, 9))
        Until(10 + 400 - 373 + 220)
        RoofPao((4, 8.5))  # 空炸
        Until(10 + 400 - 373 + 300)
        RoofPao((2, 4.7))  # 尾炸小鬼跳跳
        Until(1300 - 200 - 373)
        RoofPao((4, 8.2))
        Until(1780 - 200 - 373)
        RoofPao((2, 9), (4, 9))
        Until(1780 + 10 - 298)
        Coffee()
        ICE3(298)

    elif wave in (9, 19):
        Prejudge(-190, wave)
        Until(10 + 400 - 373)
        RoofPao((2, 9), (4, 9))
        Until(10 + 400 - 373 + 220)
        RoofPao((2, 8.5), (4, 8.5))
        Until(1300 - 200 - 373)
        RoofPao((3, 8.22))  # 落点改为 3 路减少小丑炸核机率
        # 收尾
        Until(1705 - 200 - 298)
        Card("花盆", (3, 9))
        Card("核蘑菇", (3, 9))
        Card("咖啡豆", (3, 9))
        Until(1705 - 200 + 230 - 373)
        RoofPao((2, 8.5), (4, 8.5))  # 拦截
        Until(1705 - 200 + 230 + 230 - 373)
        RoofPao((2, 8.5), (4, 8.5))  # 拦截
        Until(1705 - 200 + 230 + 230 + 230 - 373)
        RoofPao((3, 9), (5, 9))  # 留下 1 路
        Delay(50)
        Card("寒冰射手", (1, 6))
        # 清场
        if wave == 9:
            Skip(7 - 4 - 1 + 5)  # 调整炮序
            Until(2700)
            Card("花盆", (1, 8))  # 垫一下
            Until(4500 - 200 - 373)  # Until(4500 - 5)  # 出红字时
            Delay(400)  # 等那一门炮
            RoofPao((1, 8))  # 清场
            Until(4500 - 200 + 100)
            Shovel((1, 6))  # 铲掉冰豆
            Until(4500 - 5 + 750 - 599)  # 第 10 波刷新前 599
            Card("花盆", (1, 7))
        else:  # 19
            Until(4500 - 200 - 373)
            RoofPao((1, 8))  # 清场
            Delay(200)
            Shovel((1, 6))  # 铲掉冰豆

    elif wave in (20, ):
        Prejudge(50 - 298, wave)
        Coffee()  # 冰消空降
        Until(75)
        RoofPao((2, 3), (4, 8), (2, 8))  # 炸冰车小偷
        Until(1250 - 200 - 373)
        RoofPao((1, 9), (2, 9), (4, 9), (5, 9))
        Until(1250 - 200 - 373 + 220)
        RoofPao((1, 9), (2, 9), (4, 9), (5, 9))
        # 收尾
        print("第 %d 波手动收尾." % wave)
        # Delay(1000)
        # Pao((3, 9), (4, 9))
        # Card("花盆", (1, 7))
        # Card("坚果", (1, 7))
        # Until(5500 - 182)
        # Card("倭瓜", (1, 6))
        # Until(5500 + 100)
        # Shovel((1, 7))
        # Shovel((1, 7))

    else:  # wave in (4, 5, 6, 7, 8, 13, 14, 15, 16, 17, 18):
        # 收尾波前一波延长波长
        WL = 1925 if wave in (8, 18) else 1780
        Prejudge(-190, wave)
        Until(10 + 400 - 373)
        RoofPao((2, 9), (4, 9))
        Until(10 + 400 - 373 + 220)
        RoofPao((2, 8.5), (4, 8.5))
        Until(1300 - 200 - 373)
        RoofPao((4, 8.2))
        Until(WL - 200 - 373)  # WL-573
        RoofPao((2, 9), (4, 9))
        if wave in (8, 18):
            Until(WL - 200 - 373 + 83)  # WL-490
            Card("花盆", (2, 8))  # 垫 2 路梯子
        Until(WL + 10 - 298)  # WL-288
        Coffee()
        ICE3(298)
        if wave in (8, 18):
            Until(WL - 200)  # WL-200
            Shovel((2, 8))  # 炮落地铲
