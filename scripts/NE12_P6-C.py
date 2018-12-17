# coding=utf-8

"""
Author: lmintlcx
Date: 2018-12-18
---
Name: NE舞夜惊魂
Rhythm: P6-C: PPC|PPC|PPC|PPC|PPC|PPC
Video:
- https://www.bilibili.com/video/av38406841
- https://youtu.be/ldJiGuXWiDQ
"""

"""
https://tieba.baidu.com/p/4354954825
https://tieba.baidu.com/p/3937751350
https://tieba.baidu.com/p/2648042818
"""

from pvz import *


# Cannon Fodder
diancai_list = ["小喷菇", "模仿者小喷菇"]
diancai_spot = (4, 9)
diancai_index = 0


@RunningInThread
def DianCai():
    global diancai_index
    # 种垫材
    while ReadMemory("bool", 0x6A9EC0, 0x768, 0x164):  # 等待取消暂停
        Delay(1)
    Card(diancai_list[diancai_index % len(diancai_list)], diancai_spot)
    diancai_index += 1
    # 等待
    Delay(200)
    # 铲垫材
    while ReadMemory("bool", 0x6A9EC0, 0x768, 0x164):  # 等待取消暂停
        Delay(1)
    Shovel(diancai_spot)


# 收尾操作, 多炸三轮
def Ending():
    for _ in range(3):
        Delay(601 - 175 - 95)
        Pao(2, 9)
        Delay(80)
        Pao(4, 9)
        Delay(15 + 175)
        DianCai()


###
###
###

Sleep(300)

SelectCards(["小喷菇", "模仿者小喷菇"])

UpdatePaoList([(1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (1, 6), (2, 6), (3, 5), (3, 7), (4, 5), (4, 7), (5, 6)])

StartAutoCollectThread()
StartStopDancerThread()


for wave in range(1, 21):
    if wave == 10:
        Prejudge(-55, wave)
        Pao(2, 9)
        Until(-15)
        Pao(4, 9)
        Until(175)
        DianCai()
    elif wave == 20:
        Prejudge(-55, wave)
        Pao(2, 9)
        Until(-35)
        Pao((2, 8), (5, 8))  # 炸墓碑冒出的僵尸
        Until(-15)
        Pao(4, 9)
        Until(175)
        DianCai()
        Ending()  # 收尾
    else:
        Prejudge(-95, wave)
        Pao(2, 9)
        Until(-15)  # Delay(80)
        Pao(4, 9)
        Until(175)  # Delay(15 + 175)
        DianCai()
        if wave in (9, 19, 20):
            Ending()  # 收尾
