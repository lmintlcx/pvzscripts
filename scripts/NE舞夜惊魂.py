# coding=utf-8

"""
作者: lmintlcx
日期: 2019-03-14
阵名: NE舞夜惊魂
出处: https://tieba.baidu.com/p/4354954825
节奏: P6-C: PPC|PPC|PPC|PPC|PPC|PPC
视频:
- https://www.bilibili.com/video/av38406841
- https://www.youtube.com/watch?v=Br-c7O4Z2d0
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
        Pao((2, 9))
        Delay(80)
        Pao((4, 9))
        Delay(15 + 175)
        DianCai()


###
###
###

# EnableLogger(False)  # 输出调试信息
# SetWindowTopMost(True)  # 窗口置顶

# BackgroundRunning(True)  # 允许后台运行
# ZombieNoFalling(True)  # 僵尸死后不掉钱

# SetSun(8000)  # 阳光 8000
# SetMoney(0)  # 金钱 0
# JumpLevel(1009)  # 完成 2018 面旗帜数

SetZombies(["普僵", "撑杆", "舞王", "小丑", "气球", "矿工", "跳跳", "蹦极", "扶梯", "篮球", "白眼", "红眼"])

Sleep(200)

SelectCards(["小喷菇", "模仿者小喷菇"])

UpdatePaoList([(1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (1, 6), (2, 6), (3, 5), (3, 7), (4, 5), (4, 7), (5, 6)])

StartAutoCollectThread()
StartStopDancerThread()


for wave in range(1, 21):
    print("当前操作波次: " + str(wave))

    if wave == 10:
        Prejudge(-55, wave)
        Pao((2, 9))
        Until(-15)
        Pao((4, 9))
        Until(175)
        DianCai()

    elif wave == 20:
        Prejudge(-55, wave)
        Pao((2, 9))
        Until(-35)
        Pao((2, 8), (5, 8))  # 炸墓碑冒出的僵尸
        Until(-15)
        Pao((4, 9))
        Until(175)
        DianCai()
        Ending()  # 收尾

    else:
        Prejudge(-95, wave)
        Pao((2, 9))
        Until(-15)  # Delay(80)
        Pao((4, 9))
        Until(175)  # Delay(15 + 175)
        DianCai()
        if wave in (9, 19):
            Ending()  # 收尾
