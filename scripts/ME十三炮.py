# coding=utf-8

"""
作者: lmintlcx
日期: 2019-03-14
阵名: ME十三炮
出处: https://tieba.baidu.com/p/5288033944
节奏: C5u-35s: PPD|PPD|PPD|IP-PPD, (6|6|6|17)
视频:
- https://www.bilibili.com/video/av38407390
- https://www.youtube.com/watch?v=jUjvLI_bUqM
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


###


# EnableLogger(False)  # 输出调试信息
# SetWindowTopMost(True)  # 窗口置顶

# BackgroundRunning(True)  # 允许后台运行
# ZombieNoFalling(True)  # 僵尸死后不掉钱

# SetSun(8000)  # 阳光 8000
# SetMoney(0)  # 金钱 0
# JumpLevel(1009)  # 完成 2018 面旗帜数

SetZombies(["普僵", "撑杆", "橄榄", "冰车", "小丑", "气球", "跳跳", "蹦极", "扶梯", "篮球", "白眼", "红眼"])

Sleep(200)

SelectCards(["玉米", "玉米炮", "三叶草", "保护伞", "樱桃", "倭瓜", "坚果", "花盆", "寒冰菇", "复制冰"])

UpdatePaoList([(1, 3), (1, 5), (1, 1), (2, 3), (2, 5), (2, 1), (3, 3), (3, 5), (3, 1), (4, 6), (4, 1), (5, 6), (5, 1)])

StartAutoCollectThread()

for wave in range(1, 21):
    print("当前操作波次: " + str(wave))

    if wave in (20,):
        Prejudge(10 - 320, wave)
        II()  # 冰消空降
        Until(100)
        TryPao((5, 8))  # 收尾了就随意选炮吧
        Until(800)
        TryPao((2, 9), (2, 9), (2, 9), (2, 9))
        Until(1000)
        TryPao((4, 9), (4, 9), (4, 9), (4, 9))
        print(f"第 {wave} 波手动收尾.")

    # IP-PPD
    elif wave in (4, 8, 10, 14, 18):
        Prejudge(-200, wave)
        if wave in (4, 10, 18):  # 本波原版冰
            Until(5 - 100)
            I()
        Until(100)
        RoofPao((5, 8))
        Until(1700 - 200 - 373)
        RoofPao((2, 8.5), (4, 8.5))
        Delay(230)  # Until(1700 - 200 - 373 + 230)  # 减速延迟 230 炸小鬼
        RoofPao((2, 7))

    # PPD
    else:  # elif wave in (1, 2, 3, 5, 6, 7, 9, 11, 12, 13, 15, 16, 17, 19):
        Prejudge(10, wave)  # 刷新后
        RoofPao((2, 8.5), (4, 8.5))
        Delay(130)  # Until(10 + 130)  # 原速延迟 130 炸小鬼
        RoofPao((2, 7.7))
        if wave in (7, 13):  # 下一波的复制冰
            Until(601 + 5 - 100 - 320)
            II()
        if wave in (9, 19):  # 收尾
            Until(601)
            RoofPao((2, 8.5), (4, 8.5))
            Delay(130)
            RoofPao((2, 7.5))
            # 自动操作收尾
            Until(601 + 601)
            RoofPao((2, 8.5))
            Delay(300)
            RoofPao((5, 8))
            Delay(500)
            RoofPao((5, 8))
