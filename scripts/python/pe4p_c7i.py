# -*- coding: utf-8 -*-

"""
Author: lmintlcx
Date: 2018-10-31
---
Name: PE四炮
Rhythm: C7i: PP|I-PP|I-PP|I-N, (6.5|18|18|11.5)
Video:
- https://www.bilibili.com/video/av34990799
- https://youtu.be/0rEfTS3mUyM
"""

from pvz import *

SelectCards(["复制冰", "寒冰菇", "核蘑菇", "睡莲", "咖啡豆", "南瓜", "樱桃", "窝瓜", "阳光菇", "小喷"])

# UpdatePaoList([(3, 1), (3, 3), (4, 1), (4, 3)])

StartAutoCollectThread()
StartAutoFillIceThread([(3, 5), (4, 5), (2, 5), (5, 5)])

for wave in range(1, 21):
    if wave in (1, 5, 9, 14, 18):
        Prejudge(650 - 200 - 373, wave)
        Pao((2, 9), (5, 9))
        if wave == 9:
            Until(650 + 1800 - 200 - 373)
            Pao((2, 8.4), (5, 8.4))
        else:
            Until(650 + 20 - 298)  # 20cs 预判冰
            Coffee()
    elif wave in (2, 6, 11, 15, 19):
        Prejudge(0, wave)
        Until(1800 - 200 - 373)
        Pao((2, 8.4), (5, 8.4))
        if wave == 19:
            Until(1800 + 1800 - 200 - 373)
            Pao((2, 8.4), (5, 8.4))
        else:
            Until(1800 + 20 - 298)  # 20cs 预判冰
            Coffee()
    elif wave in (3, 7, 12, 16):
        Prejudge(0, wave)
        Until(1800 - 200 - 373)
        Pao((2, 8.4), (5, 8.4))
        Until(1800 + 100 - 298)  # 100cs 预判冰
        Coffee()
    elif wave in (4, 8, 13, 17):
        Prejudge(0, wave)
        if wave == 4:
            row, col = 3, 8
        elif wave == 8:
            row, col = 3, 9
        elif wave == 13:
            row, col = 4, 8
        elif wave == 17:
            row, col = 4, 9
        Until(1150 - 200 - 298)
        Card(4, row, col)  # 睡莲
        Card(3, row, col)  # 核蘑菇
        Card(5, row, col)  # 咖啡豆
    elif wave in (10,):
        Prejudge(650 - 200 - 373, wave)
        Pao((2, 9), (5, 9))
        Until(650 + 20 - 298)  # 20cs 预判冰
        Coffee()
    elif wave in (20,):
        # 不管珊瑚
        Prejudge(-55, wave)
        Pao((2, 9), (5, 9))
