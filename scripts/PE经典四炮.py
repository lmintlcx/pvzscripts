# coding=utf-8

"""
作者: lmintlcx
日期: 2019-03-14
阵名: PE经典四炮
出处: https://tieba.baidu.com/p/664115150
节奏: C7i: PP|I-PP|I-PP|I-N, (6|18|18|11.5)
视频:
- https://www.bilibili.com/video/av40867249
- https://www.youtube.com/watch?v=LXWdCpY7qSc
"""

from pvz import *

# EnableLogger(False)  # 输出调试信息
# SetWindowTopMost(True)  # 窗口置顶

# BackgroundRunning(True)  # 允许后台运行
# ZombieNoFalling(True)  # 僵尸死后不掉钱

# SetSun(8000)  # 阳光 8000
# SetMoney(0)  # 金钱 0
# JumpLevel(1009)  # 完成 2018 面旗帜数

SetZombies(["普僵", "撑杆", "舞王", "冰车", "海豚", "矿工", "跳跳", "蹦极", "扶梯", "篮球", "白眼", "红眼"])

Sleep(200)

SelectCards(["寒冰菇", "复制冰", "核蘑菇", "睡莲", "咖啡豆", "南瓜", "樱桃", "窝瓜", "阳光菇", "小喷"])

UpdatePaoList([(3, 1), (4, 1), (3, 3), (4, 3)])

StartAutoCollectThread()
StartAutoFillIceThread([(3, 5), (1, 4), (6, 4)], 15)


for wave in range(1, 21):
    print("当前操作波次: " + str(wave))

    Prejudge(-200, wave)

    # PP
    if wave in (1, 5, 9, 10, 14, 18):
        Until(601 - 200 - 373)
        Pao((2, 9), (5, 9))
        Until(601 + 20 - 298)  # 20cs 预判冰
        Coffee()
        if wave == 9:  # 第 9 波收尾
            Until(601 + 1800 - 200 - 373)
            Pao((2, 8.3), (5, 8.3))
            print(f"第 {wave} 波手动收尾.")

    # I-PP
    elif wave in (2, 6, 11, 15, 19):
        Until(1800 - 200 - 373)
        Pao((2, 8.3), (5, 8.3))
        if wave == 19:  # 第 19 波收尾
            Until(1800 + 1800 - 200 - 373)
            Pao((2, 8.3), (5, 8.3))
            print(f"第 {wave} 波手动收尾.")
        else:
            Until(1800 + 20 - 298)  # 20cs 预判冰
            Coffee()

    # I-PP
    elif wave in (3, 7, 12, 16):
        Until(1800 - 200 - 373)
        Pao((2, 8.3), (5, 8.3))
        Until(1800 + 50 - 298)  # 50cs 预判冰
        Coffee()

    # I-N
    elif wave in (4, 8, 13, 17):
        if wave == 4:
            row, col = (3, 8)
        elif wave == 8:
            row, col = (3, 9)
        elif wave == 13:
            row, col = (4, 8)
        elif wave == 17:
            row, col = (4, 9)
        Until(1150 - 200 - 298)
        Card("睡莲", (row, col))
        Card("核蘑菇", (row, col))
        Card("咖啡豆", (row, col))

    elif wave in (20,):
        # 不管珊瑚
        Until(-55)
        Pao((2, 9), (5, 9))
        Until(300)
        Coffee()
        print(f"第 {wave} 波手动收尾.")
