# coding=utf-8

"""
Author: lmintlcx
Date: 2018-12-18
---
Name: PE经典十二炮
Rhythm: P6
Video:
- https://www.bilibili.com/video/av38400383
- https://youtu.be/Ey1g_HmnKGw
"""

from pvz import *

Sleep(300)

SelectCards(["樱桃"])

UpdatePaoList([(3, 1), (4, 1), (3, 3), (4, 3), (1, 5), (2, 5), (3, 5), (4, 5), (5, 5), (6, 5), (3, 7), (4, 7)])

StartAutoCollectThread()

for wave in range(1, 21):
    if wave == 10:
        Prejudge(-33, wave)
        Pao((2, 9), (5, 9))
        Delay(373 - 100)
        Card("樱桃", 2, 9)
    elif wave == 20:
        Prejudge(-150 - 30, wave)
        Pao(4, 7, 30)
        Until(-60)
        Pao((2, 9), (5, 9))
        ## 关底自动收尾
        Delay(601)
        Pao((2, 9), (5, 9))
        Delay(601)
        Pao((2, 9), (5, 9))
    else:
        Prejudge(-95, wave)
        Pao((2, 9), (5, 9))
        ## 手动收尾
        # if wave in (9, 19):
        #     SkipPao(4)
        ## 自动收尾
        if wave in (9, 19):
            Delay(601)
            Pao((2, 9), (5, 9))
            Delay(601)
            Pao((2, 9), (5, 9))
