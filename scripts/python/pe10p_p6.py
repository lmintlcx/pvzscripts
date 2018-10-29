# -*- coding: utf-8 -*-

"""
Author: lmintlcx
Date: 2018-10-29
---
Name: PE经典十炮
Rhythm: P6: PP|PP|PP|PP|PP|N
Video:
- https://www.bilibili.com/video/av34824833
- https://youtu.be/_vqyPvBYAIE
"""

from pvz import *

# 释放樱桃
def A(row, col):
    Card(5, row, col)  # 樱桃


# 释放核蘑菇
def N(row, col):
    Card(3, row, col)  # 睡莲
    Card(2, row, col)  # 核蘑菇
    Card(4, row, col)  # 咖啡豆


SelectCards(["寒冰菇", "核蘑菇", "睡莲", "咖啡豆", "樱桃", "倭瓜", "三叶草", "高坚果", "阳光菇", "小喷菇"])

# UpdatePaoList([(1, 5), (2, 5), (3, 1), (3, 3), (3, 5), (4, 1), (4, 3), (4, 5), (5, 5), (6, 5)])

StartAutoCollectThread()

for wave in range(1, 21):
    if wave == 10:
        Prejudge(-55, wave)
        Pao((2, 9), (5, 9))
        Delay(373 - 100)
        A(2, 9)
    elif wave == 20:
        Prejudge(-150, wave)
        Pao(4, 7)
        Delay(95)
        Pao((2, 9), (5, 9))
    elif wave in (6, 15):
        Prejudge(-95, wave)
        Delay(373 - 198 - 100)
        if wave == 6:
            N(3, 9)
        else:
            N(4, 9)
    else:
        Prejudge(-95, wave)
        Pao((2, 9), (5, 9))
        ## 手动收尾
        if wave in (9, 19):
            SkipPao(4)
