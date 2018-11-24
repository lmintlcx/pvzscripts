# coding=utf-8

"""
Author: lmintlcx
Date: 2018-11-24
---
Name: PE经典十炮
Rhythm: P6: PP|PP|PP|PP|PP|N
Video:
- https://www.bilibili.com/video/av34824833
- https://youtu.be/_vqyPvBYAIE
"""

from pvz import *

# 临时伞
def TempUmbrella():
    Card("睡莲", 3, 8)
    Card("保护伞", 3, 8)


# 释放樱桃
def A(row, col):
    Card("樱桃", row, col)


# 释放核蘑菇
def N(row, col):
    Card("睡莲", row, col)
    Card("核蘑菇", row, col)
    Card("咖啡豆", row, col)


# 偷菜线程
@RunningInThread
def TempSunFlower():
    Card("向日葵", 1, 1)
    Delay(750 + 1)
    Card("向日葵", 2, 1)
    Delay(750 + 1)
    Card("向日葵", 5, 1)
    Delay(750 + 1)
    Card("向日葵", 6, 1)


# 清理偷菜痕迹
def ClearTempPlants():
    Shovel(1, 1)
    Shovel(2, 1)
    Shovel(5, 1)
    Shovel(6, 1)
    Shovel(3, 8)
    Shovel(3, 8)


#

Sleep(300)

SelectCards(["寒冰菇", "核蘑菇", "睡莲", "咖啡豆", "樱桃", "倭瓜", "保护伞", "高坚果", "向日葵", "小喷菇"])

UpdatePaoList([(3, 1), (4, 1), (3, 3), (4, 3), (1, 5), (2, 5), (3, 5), (4, 5), (5, 5), (6, 5)])

StartAutoCollectThread()
TempSunFlower()
TempUmbrella()

for wave in range(1, 21):
    if wave == 10:
        Prejudge(-33, wave)
        Pao((2, 9), (5, 9))
        Delay(373 - 100)
        A(2, 9)
    elif wave == 20:
        Prejudge(-150, wave)
        Pao(4, 7)
        Delay(90)
        Pao((2, 9), (5, 9))
        # 关底收尾
        Delay(600)
        Pao((2, 9), (5, 9))
        Delay(600)
        Pao((2, 9), (5, 9))
        Delay(600)
        ClearTempPlants()
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
        ## 铲掉重新种 ^_^
        if wave == 11:
            ClearTempPlants()
            Delay(300)
            TempSunFlower()
            TempUmbrella()
        ## 9/19 自动收尾
        if wave == 9:
            Delay(600)
            Pao((2, 9), (5, 9))
            Delay(600)
            Pao((2, 9), (5, 9))
        elif wave == 19:
            Delay(600)
            Pao((2, 9), (5, 9))
            Delay(600 + 600)
            Pao((2, 9), (5, 9))


# for wave in range(1, 21):
#     if wave == 10:
#         Prejudge(-33, wave)
#         Pao((2, 9), (5, 9))
#         Delay(373 - 100)
#         A(2, 9)
#     elif wave == 20:
#         Prejudge(-150, wave)
#         Pao(4, 7)
#         Delay(90)
#         Pao((2, 9), (5, 9))
#     elif wave in (6, 15):
#         Prejudge(-95, wave)
#         Delay(373 - 198 - 100)
#         if wave == 6:
#             N(3, 9)
#         else:
#             N(4, 9)
#     else:
#         Prejudge(-95, wave)
#         Pao((2, 9), (5, 9))
#         ## 手动收尾
#         if wave in (9, 19):
#             SkipPao(4)
