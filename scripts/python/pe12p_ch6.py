# -*- coding: utf-8 -*-

"""
Author: lmintlcx
Date: 2018-10-30
---
Name: PE后花园十二炮
Rhythm: ch6: PPCC|IPP-PP|PPCC|IPP-PP, (6|12|6|12)
Video:
- https://www.bilibili.com/video/av34923817
- https://youtu.be/v6EKVQJnrCw
"""

from pvz import *


# def DianCai():
#     diancai_list = [7, 8, 9, 10]
#     diancai_spot = [(1, 9), (2, 9), (5, 9), (6, 9)]
#     import random
#     random.shuffle(diancai_list)
#     for i in range(4):
#         Card(diancai_list[i], diancai_spot[i][0], diancai_spot[i][1])


# def ChanDianCai():
#     diancai_spot = [(1, 9), (2, 9), (5, 9), (6, 9)]
#     for i in range(4):
#         Shovel(diancai_spot[i][0], diancai_spot[i][1])


def DianCai():
    Card(7, 1, 9)
    Card(8, 2, 9)
    Card(9, 5, 9)
    Card(10, 6, 9)


def ChanDianCai():
    Shovel(1, 9)
    Shovel(2, 9)
    Shovel(5, 9)
    Shovel(6, 9)


# SelectCards(["咖啡豆", "寒冰菇", "复制冰", "南瓜", "窝瓜", "樱桃", "花盆", "胆小", "阳光", "小喷"])
SelectCards(["咖啡豆", "寒冰菇", "复制冰", "南瓜", "窝瓜", "樱桃", "三线", "西瓜", "双发", "冰豆"])


# UpdatePaoList([(1, 5), (1, 7), (2, 5), (2, 7), (3, 5), (3, 7), (4, 5), (4, 7), (5, 5), (5, 7), (6, 5), (6, 7)])
# UpdatePaoList([(r, c) for r in (1, 2, 3, 4, 5, 6) for c in (5, 7)])


StartAutoCollectThread()
StartAutoFillIceThread([(3, 9), (4, 9)])


for wave in range(1, 21):
    if wave in (1, 3, 5, 7, 9, 10, 12, 14, 16, 18):
        Prejudge(-95, wave)
        if wave == 10:
            Until(-55)
        Pao((2, 9), (5, 9))
        if wave == 10:
            Delay(373 - 100)
            Card(6, 2, 9)  # A
        Until(600 + 50 - 298)
        Coffee()
        if wave == 9:
            Until(600 - 95)
            Pao((2, 8.5), (5, 8.5))
            Delay(82)
            DianCai()
            Delay(100)
            ChanDianCai()
            Until(600 + 1200 - 200 - 373)
            Pao((2, 9), (5, 9))
            Delay(373 + 200 - 95)
            Pao((2, 9), (5, 9))
    elif wave in (2, 4, 6, 8, 11, 13, 15, 17, 19):
        Prejudge(-95, wave)
        Pao((2, 8.5), (5, 8.5))
        Delay(82)
        DianCai()
        Delay(100)
        ChanDianCai()
        Until(1200 - 200 - 373)
        Pao((2, 9), (5, 9))
        if wave == 19:
            Until(1200 - 95)
            Pao((2, 9), (5, 9))
            Until(1200 + 600 - 95)
            Pao((2, 8.5), (5, 8.5))
            # 自古一路...夭寿啦一路出巨人啦
            Card(5, 2, 9)  # a
            Card(6, 5, 9)  # A
            SkipPao(2)  # 留下 1 路拖
    elif wave == 20:
        Prejudge(-180, wave)
        Pao(4, 7, 30)  # 点炮后延迟 30cs 炸珊瑚
        Until(-55)  # 等到刷新前 55cs
        Pao((2, 9), (5, 9), (2, 9), (5, 9))
        Delay(90)
        Pao((2, 9), (5, 9), (2, 9), (5, 9))
        Until(600 + 0 - 298)
        Coffee()  # 冰杀小偷
