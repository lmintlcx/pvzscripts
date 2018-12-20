# coding=utf-8

"""
Author: lmintlcx
Date: 2018-12-18
---
Name: RE椭盘十四炮
Rhythm: ch4-35.6s: ICE3+PPDD+P-PP|ICE3+PPDD+P-PP, (17.8|17.8)
Video:
- https://www.bilibili.com/video/av38408382
- https://youtu.be/KoFX0SIMzWk
"""

from pvz import *

Sleep(300)

SelectCards(["花盆", "寒冰菇", "模仿者寒冰菇", "毁灭菇", "咖啡豆", "樱桃炸弹", "火爆辣椒", "倭瓜", "寒冰射手", "坚果墙"])

UpdatePaoList(
    [
        (4, 2),  # P
        (4, 4),  # P
        (1, 4),  # D
        (5, 4),  # D
        (5, 6),  # s
        (3, 1),  # P
        (4, 7),  # P
        ###
        (1, 2),  # P
        (2, 4),  # P
        (3, 3),  # D
        (3, 5),  # D
        (2, 6),  # s
        (2, 1),  # P
        (3, 7),  # P
    ]
)

# IPPDDP-PP IPPDDP-PP  14
# PPDDDD    IP-PP      9
# PPSSDD    IAA'aP-PP  9
SkipPao(5)  # 调整炮序


# while GameUI() != 3:
#     Sleep(1)
# while GamePaused():
#     Sleep(1)
Card("花盆", (1, 7))
Card("寒冰菇", (1, 7))
StartAutoCollectThread([1, 2, 3, 4, 5, 6, 17], 15)
StartAutoFillIceThread([(4, 6), (2, 3), (1, 1), (1, 6)], 18 - 1)


for wave in range(1, 21):
    # print("当前波次: " + str(wave))

    if wave in (1,):
        Prejudge(-200, wave)
        Until(380 - 373)
        RoofPao((2, 8.8), (4, 8.8))
        Until(510 - 373)
        RoofPao((2, 8.8), (4, 8.8))
        Until(601 + 36 - 373)
        RoofPao((2, 8.8), (4, 8.8))
        Until(601 + 36 - 298)
        Card("咖啡豆", (1, 7))  # Coffee()

    elif wave in (2,):
        Prejudge(-200, wave)
        Until(50)
        Shovel((1, 7))  # 铲
        Until(1300 - 200 - 373)  # 727
        RoofPao(4, 8.1)
        Until(1780 - 200 - 373)  # 1207
        RoofPao((2, 9), (4, 9))
        Until(1780 + 10 - 298)  # 1492
        Coffee()

    elif wave in (10,):
        Prejudge(-15, wave)
        RoofPao((2, 9), (4, 9), (2, 9), (4, 9))
        Until(-15 + 110)  # 95
        RoofPao((4, 7.7))  # 空炸小鬼兼小偷
        Until(-15 + 190)  # 175
        RoofPao((1, 5))  # 2-5? 尾炸小鬼兼小偷
        Until(601 + 10 - 298)  # 313
        Coffee()

    elif wave in (11,):
        Prejudge(-200, wave)
        Until(10 + 400 - 100)
        Card("辣椒", (1, 7))
        Card("花盆", (4, 9))
        Card("樱桃", (4, 9))
        Until(10 + 400 + 10)
        Shovel((1, 7))  # 铲
        Shovel((4, 9))  # 铲
        Until(1250 - 200 - 373)  # 1300->1250
        RoofPao(3, 8.15)  # 落点改为 3 路炸掉 2 路冰车
        Until(1780 - 200 - 373)
        RoofPao((2, 9), (4, 9))
        Until(1780 + 10 - 298)
        Coffee()

    elif wave in (3, 12):
        Prejudge(-200, wave)
        Until(10 + 400 - 373)
        RoofPao((2, 9), (4, 9))
        Until(10 + 400 - 373 + 220)
        RoofPao(4, 8.5)  # 空炸
        Until(10 + 400 - 373 + 300)
        RoofPao(2, 4.7)  # 尾炸小鬼跳跳
        Until(1300 - 200 - 373)
        RoofPao(4, 8.1)
        Until(1780 - 200 - 373)
        RoofPao((2, 9), (4, 9))
        Until(1780 + 10 - 298)
        Coffee()

    elif wave in (9, 19):
        Prejudge(-200, wave)
        Until(10 + 400 - 373)
        RoofPao((2, 9), (4, 9))
        Until(10 + 400 - 373 + 220)
        RoofPao((2, 8.5), (4, 8.5))
        Until(1300 - 200 - 373)  # 727
        RoofPao(3, 8.15)  # 落点改为 3 路减少小丑炸核机率
        # 收尾
        Until(1680 - 200 - 298)  # 1182
        Card("花盆", (3, 9))
        Card("核蘑菇", (3, 9))
        Card("咖啡豆", (3, 9))
        Until(1680 - 200 + 230 - 373)
        RoofPao((2, 8.5), (4, 8.5))  # 拦截
        Until(1680 - 200 + 230 + 230 - 373)
        RoofPao((2, 8.5), (4, 8.5))  # 拦截
        Until(1680 - 200 + 230 + 230 + 230 - 373)
        RoofPao((3, 9), (5, 9))  # 留下 1 路
        Delay(50)
        Card("寒冰射手", (1, 6))
        # 清场
        if wave == 9:
            SkipPao(7 - 4 - 1 + 5)  # 调整炮序
            Until(2700)
            Card("花盆", (1, 8))  # 垫一下
            Until(4500 - 200 - 373)  # Until(4500 - 5)  # 出红字时
            Delay(400)  # 等那一门炮
            RoofPao(1, 8)  # 清场
            Until(4500 - 200 + 100)
            Shovel((1, 6))  # 铲掉冰豆
            Until(4500 - 5 + 750 - 599)  # 第 10 波刷新前 599
            Card("花盆", (1, 7))
        else:  # 19
            Until(4500 - 200 - 373)
            RoofPao(1, 8)  # 清场
            Delay(200)
            Shovel((1, 6))  # 铲掉冰豆

    elif wave in (20,):
        Prejudge(50 - 298, wave)
        Coffee()  # 冰消空降
        Until(-95)
        RoofPao((4, 9))  # 炸 3/4 路冰车
        Until(75)
        RoofPao((1, 6), (2, 3), (4, 6))  # 炸小偷
        Until(1250 - 200 - 373)
        RoofPao((1, 9), (2, 9), (4, 9), (5, 9))
        Until(1250 - 200 - 373 + 220)
        RoofPao((1, 9), (2, 9), (4, 9), (5, 9))
        # # 收尾
        # Delay(800)
        # while not TryPao(4, 9):
        #     Delay(10)
        # Delay(10)
        # while not TryPao(3, 9):
        #     Delay(10)
        # Card("花盆", (1, 7))
        # Card("坚果", (1, 7))
        # Until(5500)
        # Card("倭瓜", (1, 6))
        # Until(5600)
        # Shovel((1, 7))
        # Shovel((1, 7))

    else:  # wave in (4, 5, 6, 7, 8, 13, 14, 15, 16, 17, 18):
        WL = 1950 if wave in (8, 18) else 1780  # 收尾波前一波延长波长
        Prejudge(-200, wave)
        Until(10 + 400 - 373)
        RoofPao((2, 9), (4, 9))
        Until(10 + 400 - 373 + 220)
        RoofPao((2, 8.5), (4, 8.5))
        Until(1300 - 200 - 373)
        RoofPao(4, 8.1)
        Until(WL - 200 - 373)  # WL-573
        RoofPao((2, 9), (4, 9))
        if wave in (8, 18):
            Until(WL - 200 - 373 + 81)  # WL-492
            Card("花盆", (2, 8))  # 垫 2 路梯子
        Until(WL + 10 - 298)  # WL-288
        Coffee()
        if wave in (8, 18):
            Until(WL - 200)  # WL-200
            Shovel((2, 8))  # 炮落地铲
