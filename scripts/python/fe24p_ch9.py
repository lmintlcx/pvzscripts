# -*- coding: utf-8 -*-

"""
Author: lmintlcx
Date: 2018-10-29
---
Name: FE二十四炮
Rhythm: ch9-56s: PSD/PDC|IPP-PPDD|PSD/PDC|IPP-PPDD|PSD/PDC|AD/PDC|PSD/PDC, (6|13|6|13|6|6|6)
Video:
- https://www.bilibili.com/video/av34828474
- https://youtu.be/p-4ZbBtxBrI
"""

from pvz import *

# Ice-shroom
def Ice(row, col):
    Card(1, row, col)


# Imitater Ice-shroom
def ImitaterIce(row, col):
    Card(2, row, col)


# Cherry Bomb
def A(row, col):
    Card(4, row, col)


# # Doom-shroom
# def N(row, col):
#     Card(4, row, col)
#     Card(3, row, col)

# Cannon Fodder 1
def DianCai1():
    Card(9, 5, 9)
    Card(10, 6, 9)


# Cannon Fodder 2
def DianCai2():
    Card(7, 5, 9)
    Card(8, 6, 9)


# Delete Cannon Fodder
def ChanDianCai():
    Shovel(5, 9)
    Shovel(6, 9)


## 逐波操作


def wave1():
    Prejudge(-135, 1)
    Pao((1, 9), (5, 9))
    Until(-95)
    Pao(2, 9)
    Until(-135 + 110)
    Pao(5, 8)
    Until(-95 + 110)
    Pao(1, 8.7)


def wave2():
    Prejudge(-180, 2)
    DianCai1()
    Until(-150)
    ChanDianCai()
    Until(-135)
    Pao(2, 8.5)
    Until(-95)
    Ice(2, 9)
    Until(180 - 30)
    Pao(5, 7.2, 30)
    Until(1300 - 200 - 373)
    Pao((2, 9), (5, 9))
    Until(1300 - 200 - 373 + 220)
    Pao((1, 8.5), (5, 8.5))


def wave3():
    Prejudge(-135, 3)
    Pao((1, 9), (5, 9))
    Until(-95)
    Pao(2, 9)
    Until(-135 + 110)
    Pao(5, 8)
    Until(-95 + 110)
    Pao(1, 8.7)
    Until(600 - 100 - 320 + 5)
    ImitaterIce(2, 9)


def wave4():
    Prejudge(-180, 4)
    DianCai1()
    Until(-150)
    ChanDianCai()
    Until(-135)
    Pao(2, 8.5)
    Until(180 - 30)
    Pao(5, 7.2, 30)
    Until(1300 - 200 - 373)
    Pao((2, 9), (5, 9))
    Until(1300 - 200 - 373 + 220)
    Pao((1, 8.5), (5, 8.5))


def wave5():
    Prejudge(-200, 5)
    wave1()


# │AD/BDC│
def wave6():
    Prejudge(-145, 6)  # -145
    Pao(5, 9)
    Until(-145 + 81)  # -64
    DianCai1()
    Until(-145 + 110)  # -39
    Pao(5, 8)
    Until(-145 + 81 + 30)  # -34
    ChanDianCai()
    Until(-15 + 108)  # 93
    Pao(1, 7.9)
    Until(-15 + 373 - 98)  # 260
    A(2, 9)


# │PSD/BDC│
def wave7():
    Prejudge(-145, 7)  # -145
    Pao(5, 9)
    Until(-55)  # -55
    Pao(2, 9)
    Until(-145 + 81)  # -64
    DianCai2()
    Until(-145 + 110)  # -35
    Pao(5, 8)
    Until(-145 + 81 + 30)  # -34
    ChanDianCai()
    Until(-55 + 110)  # 55
    Pao(1, 8.7)
    Until(-55 + 110 + 110)  # 165
    Pao(1, 8.7)


def wave8():
    Prejudge(-145, 8)
    Pao((1, 9), (5, 9))
    Until(-95)
    Pao(2, 9)
    Until(-145 + 81)
    DianCai1()
    Until(-145 + 110)
    Pao(5, 8)
    Until(-145 + 81 + 30)
    ChanDianCai()
    Until(-95 + 110)
    Pao(1, 8.7)


def wave9():
    Prejudge(-180, 9)
    DianCai2()
    Until(-150)
    ChanDianCai()
    Until(-135)
    Pao(2, 8.5)
    Until(-95)
    Ice(2, 9)
    Until(180 - 30)
    Pao(5, 7.2, 30)
    Until(1300 - 200 - 373)
    Pao((2, 9), (5, 9))
    Until(1300 - 200 - 373 + 220)
    Pao((1, 8.5), (5, 8.5))
    Until(1300 - 200 - 373 + 220 + 220)
    Pao((1, 8.5), (5, 8.5))
    Until(1300 - 200 - 373 + 220 + 220 + 750)
    Pao((2, 9), (5, 9))


def wave10():
    Prejudge(-55, 10)
    Pao((1, 9), (5, 9))
    Until(-55 + 100)  # 45
    Pao(2, 9)
    Until(-55 + 110)  # 55
    Pao(5, 8)
    Until(-55 + 100 + 110)  # 155
    Pao(1, 8.7)
    Until(600 - 100 - 320 + 5)  # 185
    ImitaterIce(2, 9)

def wave11():
    Prejudge(-200, 11)
    wave4()


def wave12():
    Prejudge(-200, 12)
    wave1()


def wave13():
    Prejudge(-200, 13)
    wave2()


def wave14():
    Prejudge(-200, 14)
    wave5()


def wave15():
    Prejudge(-200, 15)
    wave6()


def wave16():
    Prejudge(-200, 16)
    wave7()


def wave17():
    Prejudge(-145, 17)
    Pao((1, 9), (5, 9))
    Until(-95)
    Pao(2, 9)
    Until(-145 + 81)
    DianCai1()
    Until(-145 + 110)
    Pao(5, 8)
    Until(-145 + 81 + 30)
    ChanDianCai()
    Until(-95 + 110)
    Pao(1, 8.7)
    Until(600 - 100 - 320 + 5)
    ImitaterIce(2, 9)


def wave18():
    Prejudge(-180, 18)
    DianCai2()
    Until(-150)
    ChanDianCai()
    Until(-135)
    Pao(2, 8.5)
    Until(180 - 30)
    Pao(5, 7.2, 30)
    Until(1300 - 200 - 373)
    Pao((2, 9), (5, 9))
    Until(1300 - 200 - 373 + 220)
    Pao((1, 8.5), (5, 8.5))


def wave19():
    Prejudge(-135, 19)
    Pao((1, 9), (5, 9))
    Until(-95)
    Pao(2, 9)
    Until(-135 + 110)
    Pao(5, 8)
    Until(-95 + 110)
    Pao(1, 8.7)
    #
    Until(600 - 150)
    Pao(5, 9)
    Until(600 - 150 + 81)
    DianCai1()
    Until(600 - 150 + 81 + 20)
    ChanDianCai()
    Until(600 - 150 + 110)
    Pao(2, 9)
    Pao(5, 8.5)
    Until(600 - 150 + 110 + 300)
    Pao(5, 9)


def wave20():
    Prejudge(-180, 20)
    Pao(4, 7, 30)  # 炮炸珊瑚
    Until(-60)
    Pao((2, 9), (5, 9))
    Until(-60 + 50)
    Pao((2, 9), (5, 9))
    Until(-60 + 100)
    Pao((2, 9), (5, 9))
    Until(-60 + 150)
    Pao((2, 9), (5, 9))


###

SelectCards(
    [
        (2, 7, 0),
        (2, 7, 1),
        (3, 2, 0),
        (1, 3, 0),
        (1, 4, 0),
        (4, 7, 0),
        (5, 2, 0),
        (2, 6, 0),
        (2, 2, 0),
        (2, 1, 0),
    ]
)

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
