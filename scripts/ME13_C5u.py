# coding=utf-8

"""
Author: lmintlcx
Date: 2018-12-18
---
Name: ME十三炮
Rhythm: C5u-35s: PPD|PPD|PPD|IP-PPD, (6|6|6|17)
Video:
- https://www.bilibili.com/video/av38407390
- https://youtu.be/jUjvLI_bUqM
"""

from pvz import *


@RunningInThread
def I():
    Card("花盆", (3, 7))
    Card("寒冰菇", (3, 7))
    Delay(100 + 1)
    Shovel((3, 7))


@RunningInThread
def II():
    Card("花盆", (3, 7))
    Card("复制冰", (3, 7))
    Delay(320 + 100 + 1)
    Shovel((3, 7))


Sleep(300)

SelectCards(["玉米", "玉米炮", "三叶草", "保护伞", "樱桃", "倭瓜", "坚果", "花盆", "寒冰菇", "复制冰"])

UpdatePaoList([(1, 3), (1, 5), (1, 1), (2, 3), (2, 5), (2, 1), (3, 3), (3, 5), (3, 1), (4, 6), (4, 1), (5, 6), (5, 1)])

StartAutoCollectThread()

for wave in range(1, 21):

    if wave in (20,):
        Prejudge(0 - 320, wave)
        II()  # 冰消空降
        Until(100)
        TryPao(5, 8)  # 收尾了就随意选炮吧
        Until(700)
        TryPao((2, 9), (2, 9), (2, 9), (2, 9))
        Until(900)
        TryPao((4, 9), (4, 9), (4, 9), (4, 9))

    # IP-PPD
    elif wave in (4, 8, 10, 14, 18):
        Prejudge(-95, wave)
        if wave in (4, 10, 18):  # 本波原版冰
            I()
        Until(100)
        RoofPao(5, 8)
        Until(1700 - 200 - 373)
        RoofPao((2, 8.5), (4, 8.5))
        Delay(230)  # Until(1700 - 200 - 373 + 230)  # 减速延迟 230 炸小鬼
        RoofPao(2, 7)

    # PPD
    else:  # elif wave in (1, 2, 3, 5, 6, 7, 9, 11, 12, 13, 15, 16, 17, 19):
        Prejudge(10, wave)
        RoofPao((2, 8.5), (4, 8.5))
        Delay(130)  # Until(10 + 130)  # 原速延迟 130 炸小鬼
        RoofPao(2, 7.5)
        if wave in (7, 13):  # 下一波的复制冰
            Until(601 + 5 - 100 - 320)
            II()
        if wave in (9, 19):  # 收尾
            Until(601)
            RoofPao((2, 8.5), (4, 8.5))
            Delay(130)
            RoofPao(2, 7.5)
            #
            Until(601 + 601)
            RoofPao(2, 8.5)
            Delay(300)
            RoofPao(5, 8)
            Delay(300)
            RoofPao(5, 8)
