# coding=utf-8

"""
作者: 冰巫师墨舞, lmintlcx
日期: 2019-03-14
阵名: NE十五炮
出处: https://tieba.baidu.com/p/1067040250
节奏: C8u: IPP-PP|PADC|PPDD|IPP-PP|NDC|PPDD, (13|6|6|13|6|6)
视频:
- https://www.bilibili.com/video/av41128772
- https://www.youtube.com/watch?v=QltplZCAuoI
"""

from pvz import *


@RunningInThread
def DianCai():
    Card("小喷", (4, 9))
    Card("阳光", (5, 9))
    Delay(120)
    Shovel((4, 9))
    Shovel((5, 9))


# EnableLogger(False)  # 输出调试信息
# SetWindowTopMost(True)  # 窗口置顶

# BackgroundRunning(True)  # 允许后台运行
# ZombieNoFalling(True)  # 僵尸死后不掉钱

# SetSun(8000)  # 阳光 8000
# SetMoney(0)  # 金钱 0
# JumpLevel(1009)  # 完成 2018 面旗帜数

SetZombies(["普僵", "撑杆", "舞王", "小丑", "气球", "矿工", "跳跳", "蹦极", "扶梯", "篮球", "白眼", "红眼"])

Sleep(200)

SelectCards(["复制冰", "原版冰", "核蘑菇", "樱桃", "倭瓜", "墓碑", "南瓜", "三叶草", "阳光菇", "小喷菇"])

# UpdatePaoList([
#     (1, 1), (2, 1), (3, 1), (4, 1), (5, 1),
#     (1, 5), (2, 5), (3, 5), (4, 5), (5, 5),
#     (1, 7), (2, 7), (3, 7), (4, 7), (5, 7),
#     ])

StartAutoCollectThread()


for wave in range(1, 21):
    print("当前操作波次: " + str(wave))

    # PPD
    if wave in (10,):
        Prejudge(-200, wave)
        Until(-55)
        Pao((2, 9), (4, 9))
        Until(0)
        Pao((2, 9))

    # IPP-PP
    elif wave in (1, 7, 11, 17):
        Prejudge(-200, wave)
        Until(-150)
        Pao((2, 8.5), (4, 8.5))
        Until(5 - 100)
        Card("寒冰菇", (1, 9))
        if wave == 11:
            Until(-150 + 81)
            DianCai()
        Until(1300 - 200 - 373)
        Pao((2, 9), (4, 9))

    # PADC
    elif wave in (2, 8, 12, 18):
        Prejudge(-200, wave)
        Until(-95)
        Pao((2, 9))
        Until(-12)
        Pao((2, 9))
        Until(-95 + 373 - 100)
        Card("樱桃", (5, 9))

    # PPDD
    elif wave in (3, 9, 13, 19):
        Prejudge(-200, wave)
        Until(-95)
        Pao((2, 9), (5, 9))
        Until(-15)
        Pao((1, 9), (4, 9))
        Until(0)
        DianCai()
        Until(601 + 44 - 100 - 320)  # 44cs 预判冰
        Card("模仿者寒冰菇", (1, 9))

        if wave in (9, 19):
            Until(601 - 150)
            Pao((4, 9))
            Delay(450)
            Pao((1, 9))
            Until(601 + 1300 - 200 - 373)
            Delay(300)
            Pao((2, 9), (5, 9))

    # IPP-PP
    elif wave in (4, 14):
        Prejudge(-200, wave)
        Until(-150)
        Pao((2, 8.5), (4, 8.5))
        Until(1300 - 200 - 373)
        Pao((2, 9), (4, 9))

    # NDC
    elif wave in (5, 15):
        Prejudge(-200, wave)
        Until(-12)
        Pao((2, 9))
        Until(-95 + 373 - 100)
        Card("核蘑菇", (3, 9) if wave == 5 else (2, 9))

    # PPDD
    elif wave in (6, 16):
        Prejudge(-200, wave)
        Until(-95)
        Pao((2, 9), (5, 9))
        Until(-12)
        Pao((1, 9), (4, 9))
        Until(0)
        DianCai()

    elif wave == 20:
        Prejudge(-200, wave)
        Until(-55)
        Pao((1, 9), (4, 9))
        Until(-35)
        Pao((2, 9), (5, 9))  # 炸墓碑冒出的僵尸
        Until(601 - 100 - 81)
        Pao((1, 8.3), (4, 8.3))
        Until(601 - 100)
        # 冰杀小偷
        with MouseLock():
            SafeClick()
            ClickSeed("寒冰菇")
            ClickGrid((1, 9))
            ClickGrid((2, 9))
            ClickGrid((3, 9))
            ClickGrid((4, 9))
            ClickGrid((5, 9))
            SafeClick()
        Delay(100)
        Pao((2, 8.2), (5, 8.2))
        print(f"第 {wave} 波手动收尾.")
