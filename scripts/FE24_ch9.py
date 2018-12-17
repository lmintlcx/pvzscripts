# coding=utf-8

"""
Author: lmintlcx
Date: 2018-12-18
---
Name: FE二十四炮
Rhythm: ch9-56s: PSD/PDC|IPP-PPDD|PSD/PDC|IPP-PPDD|PSD/PDC|AD/PDC|PDD/PDC, (6|13|6|13|6|6|6)
Video:
- https://www.bilibili.com/video/av38409007
- https://youtu.be/kNBwhHvhark
"""

from pvz import *


# Ice-shroom
def I():
    Card("寒冰菇", (2, 9))


# Imitater Ice-shroom
def II():
    Card("模仿者寒冰菇", (2, 9))


# Cherry Bomb
def A():
    Card("樱桃炸弹", (2, 9))


# Cannon Fodder
# 下标 6/7 8/9
# 垫材 花盆/胆小菇 阳光菇/小喷菇
# 根据小喷是否可用来决定用哪一组垫材
@RunningInThread
def DianCai():
    if ReadMemory("bool", 0x6A9EC0, 0x768, 0x144, 0x70 + 9 * 0x50):
        Card("阳光菇", (5, 9))
        Card("小喷菇", (6, 9))
    else:
        Card("花盆", (5, 9))
        Card("胆小菇", (6, 9))
    Delay(30)
    Shovel((5, 9))
    Shovel((6, 9))


## 定义逐波操作


# PSD/PDC
def wave1():
    Prejudge(-135, 1)
    Pao((1, 9), (5, 9))
    Until(-95)
    Pao(2, 9)
    Until(-135 + 110)
    Pao(5, 8)
    Until(-95 + 110)
    Pao(1, 8.7)


# IPP-PPDD
def wave2():
    Prejudge(-180, 2)
    DianCai()
    Until(-135)
    Pao(2, 8.5)
    Until(-95)
    I()  # 原版冰
    Until(180 - 30)  # 提前 30cs 点炮
    Pao(5, 7.2, 30)  # 推迟 30cs 发射
    Until(650)
    DianCai()
    Until(1300 - 200 - 373)
    Pao((2, 9), (5, 9))
    Delay(220)
    Pao((1, 8.5), (5, 8.5))


# PSD/PDC
def wave3():
    Prejudge(-135, 3)
    Pao((1, 9), (5, 9))
    Until(-95)
    Pao(2, 9)
    Until(-135 + 110)
    Pao(5, 8)
    Until(-95 + 110)
    Pao(1, 8.7)
    Until(601 - 100 - 320 + 5)
    II()  # 复制冰


# IPP-PPDD
def wave4():
    Prejudge(-180, 4)
    DianCai()
    Until(-135)
    Pao(2, 8.5)
    Until(180 - 30)  # 提前 30cs 点炮
    Pao(5, 7.2, 30)  # 推迟 30cs 发射
    Until(650)
    DianCai()
    Until(1300 - 200 - 373)
    Pao((2, 9), (5, 9))
    Delay(220)
    Pao((1, 8.5), (5, 8.5))


# PSD/PDC
def wave5():
    Prejudge(-200, 5)
    wave1()


# AD/PDC
def wave6():
    Prejudge(-145, 6)  # -145
    Pao(5, 9)
    Until(-145 + 81)  # -64
    DianCai()
    Until(-145 + 110)  # -35
    Pao(5, 8)
    Until(-15 + 108)  # 93
    Pao(1, 7.8)
    Until(-15 + 373 - 100)  # 258
    A()  # 樱桃


# PDD/PDC
# 复用炮时机微调
def wave7():
    Prejudge(-145, 7)  # -145
    Pao(5, 9)
    Until(-55)  # -55
    Pao(2, 9)
    Until(-145 + 81)  # -64
    DianCai()
    Until(-145 + 110)  # -35
    Pao(5, 8)
    Until(-55 + 110)  # 55
    Pao(1, 8.7)
    Until(-55 + 110 + 110)  # 165
    Pao(1, 8.7)


# PSD/PDC
def wave8():
    Prejudge(-145, 8)
    Pao((1, 9), (5, 9))
    Until(-95)
    Pao(2, 9)
    Until(-145 + 81)
    DianCai()
    Until(-145 + 110)
    Pao(5, 8)
    Until(-95 + 110)
    Pao(1, 8.7)


# IPP-PPDD PPPP
def wave9():
    Prejudge(-180, 9)
    DianCai()
    Until(-135)
    Pao(2, 8.5)
    Until(-95)
    I()  # 原版冰
    Until(180 - 30)  # 提前 30cs 点炮
    Pao(5, 7.2, 30)  # 推迟 30cs 发射
    Until(650)
    DianCai()
    Until(1300 - 200 - 373)
    Pao((2, 9), (5, 9))
    Delay(220)
    Pao((1, 8.5), (5, 8.5))
    # 收尾
    Delay(220)
    Pao((1, 8.5), (5, 8.5))
    Delay(650)
    Pao((2, 9), (5, 9))  # 清场
    Delay(800)
    Pao((2, 9), (5, 9))  # 哦还有伴舞


# PSD/PDC
# 推迟消延迟
def wave10():
    Prejudge(-55, 10)  # -55
    Pao((1, 9), (2, 9), (5, 9))
    Until(-55 + 110)  # 55
    Pao((1, 8.7), (5, 8))
    Until(601 - 100 - 320 + 5)  # 186
    II()  # 复制冰


# IPP-PPDD
def wave11():
    Prejudge(-200, 11)
    wave4()


# PSD/PDC
def wave12():
    Prejudge(-200, 12)
    wave1()


# IPP-PPDD
def wave13():
    Prejudge(-200, 13)
    wave2()


# PSD/PDC
def wave14():
    Prejudge(-200, 14)
    wave5()


# AD/PDC
def wave15():
    Prejudge(-200, 15)
    wave6()


# PDD/PDC
def wave16():
    Prejudge(-200, 16)
    wave7()


# PSD/PDC
def wave17():
    Prejudge(-145, 17)
    Pao((1, 9), (5, 9))
    Until(-95)
    Pao(2, 9)
    Until(-145 + 81)
    DianCai()
    Until(-145 + 110)
    Pao(5, 8)
    Until(-95 + 110)
    Pao(1, 8.7)
    Until(601 + 5 - 100 - 320)
    II()  # 复制冰


# IPP-PPDD
def wave18():
    Prejudge(-180, 18)
    DianCai()
    Until(-135)
    Pao(2, 8.5)
    Until(180 - 30)  # 提前 30cs 点炮
    Pao(5, 7.2, 30)  # 推迟 30cs 发射
    Until(650)
    DianCai()
    Until(1300 - 200 - 373)
    Pao((2, 9), (5, 9))
    Delay(220)
    Pao((1, 8.5), (5, 8.5))


# PSD/PDC PPPP
def wave19():
    Prejudge(-135, 19)
    Pao((1, 9), (5, 9))
    Until(-95)
    Pao(2, 9)
    Until(-135 + 110)
    Pao(5, 8)
    Until(-95 + 110)
    Pao(1, 8.7)
    # 收尾
    Until(601 - 150)
    Pao(5, 9)
    Until(601 - 150 + 81)
    DianCai()
    Until(601 - 150 + 110)
    Pao(2, 9)
    Pao(5, 8.5)
    Until(601 - 150 + 110 + 300)
    Pao(5, 9)  # 清场
    Delay(400)
    Pao(2, 9)  # 残留伴舞


# PP-PPPPPPPP
def wave20():
    Prejudge(-180, 20)
    Pao(4, 7, 30)  # 炮炸珊瑚
    Until(-60)  # 等到刷新前 60cs
    Pao((1, 9), (2, 9), (5, 9), (6, 9))
    Delay(108)
    Pao((1, 9), (2, 9), (5, 9), (6, 9))


### 下面正式开始

Sleep(300)

# # 三种方式等价
# SelectCards([14, 14 + 48, 17, 2, 3, 30, 33, 13, 9, 8])
# SelectCards([(2, 7), (2, 7, True), (3, 2), (1, 3), (1, 4), (4, 7), (5, 2), (2, 6), (2, 2), (2, 1)])
SelectCards(["寒冰菇", "模仿冰", "倭瓜", "樱桃", "坚果", "南瓜", "花盆", "胆小", "阳光", "小喷"])


# UpdatePaoList(
#     [
#         (1, 1),
#         (1, 3),
#         (1, 5),
#         (1, 7),
#         (2, 1),
#         (2, 3),
#         (2, 5),
#         (2, 7),
#         (3, 1),
#         (3, 3),
#         (3, 5),
#         (3, 7),
#         (4, 1),
#         (4, 3),
#         (4, 5),
#         (4, 7),
#         (5, 1),
#         (5, 3),
#         (5, 5),
#         (5, 7),
#         (6, 1),
#         (6, 3),
#         (6, 5),
#         (6, 7),
#     ]
# )
# UpdatePaoList([(r, c) for r in range(1, 7) for c in range(1, 8, 2)])

StartAutoCollectThread()

wave1()
wave2()
wave3()
wave4()
wave5()
wave6()
wave7()
wave8()
wave9()
wave10()
wave11()
wave12()
wave13()
wave14()
wave15()
wave16()
wave17()
wave18()
wave19()
wave20()
