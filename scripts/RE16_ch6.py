# coding=utf-8

"""
Author: lmintlcx
Date: 2018-12-18
---
Name: RE十六炮
Rhythm: ch6: PSD/P|IP-PPD|PSD/P|IP-PPD, (6|12|6|12)
Video:
- https://www.bilibili.com/video/av38407808
- https://youtu.be/g1xNVLRDyKo
"""

from pvz import *

Sleep(300)

SelectCards(["玉米", "玉米炮", "樱桃", "倭瓜", "坚果", "核蘑菇", "冰蘑菇", "模仿者寒冰菇", "咖啡豆", "花盆"])

UpdatePaoList(
    [
        (1, 3),
        (1, 5),
        (1, 7),
        (1, 1),
        (2, 3),
        (2, 5),
        (2, 7),
        (2, 1),
        (3, 3),
        (3, 5),
        (3, 7),
        (3, 1),
        (4, 6),
        (4, 1),
        (5, 6),
        (5, 1),
    ]
)

StartAutoFillIceThread([(5, 3), (4, 3)], 11)
StartAutoCollectThread()


for wave in range(1, 21):

    # PPSD
    if wave in (1, 3, 5, 7, 9, 10, 12, 14, 16, 18):
        Prejudge(-10, wave)  # -10+373 < 370
        RoofPao((2, 9), (2, 9), (4, 9))
        Delay(110)  # 110 拦截
        RoofPao(2, 8.8)
        Until(601 + 50 - 298)  # 50cs 预判冰
        Coffee()
        if wave == 9:
            Until(601 - 95)
            RoofPao(2, 9)
            Until(601 + 1200 - 200 - 373)
            RoofPao((5, 9), (5, 9))
            Delay(1100)  # 等会儿
            RoofPao(5, 9)

    # IP-PPD
    elif wave in (2, 4, 6, 8, 11, 13, 15, 17, 19):
        Prejudge(-95, wave)
        RoofPao(2, 9)
        Until(1200 - 200 - 373)  # 1200cs 波长
        RoofPao((2, 9), (4, 9))  # 激活炸
        Delay(220)  # 220 拦截
        RoofPao(2, 7.8)
        if wave == 19:
            Until(1200 - 10)
            RoofPao((2, 9), (2, 9), (4, 9))
            Delay(110)  # 110 拦截
            RoofPao(2, 8.8)
            Until(1200 + 601 - 95)
            RoofPao(5, 9)
            Until(1200 + 601 + 1200 - 200 - 373)
            Delay(50)  # 等会儿
            RoofPao(5, 9)

    elif wave == 20:
        Prejudge(-200, wave)
        Coffee()  # 冰消空降
        Until(-100)
        RoofPao((2, 9), (5, 9))  # 炸冰车
        Until(50)
        RoofPao((4, 2.5), (4, 6.7))  # 炸小偷
        Until(800)
        RoofPao((2, 9), (2, 9), (2, 9), (2, 9))
        Until(1000)
        RoofPao((4, 9), (4, 9), (4, 9), (4, 9))
