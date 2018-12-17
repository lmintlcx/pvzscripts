# coding=utf-8

"""
Author: lmintlcx
Date: 2018-12-18
---
Name: PE垫材二十四炮
Rhythm: P6: PDC|PDC|PDC|PDC|PDC|PDC
Video:
- https://www.bilibili.com/video/av38401606
- https://youtu.be/GTei1zO7B3w
"""

from pvz import *


# Cannon Fodder
diancai_list = ["小喷菇", "模仿者小喷菇", "阳光菇", "胆小菇", "花盆", "向日葵", "大蒜", "大喷菇"]
diancai_spot = [(1, 9), (2, 9), (5, 9), (6, 9)]
diancai_index = 0


@RunningInThread
def DianCai():
    global diancai_index
    # 种垫材
    for i in range(4):
        Card(diancai_list[diancai_index % len(diancai_list)], diancai_spot[i])
        diancai_index += 1
    # 等待
    Delay(373 - 208 - 81)
    # 铲垫材
    for spot in diancai_spot:
        Shovel(spot)


###
###
###

Sleep(300)

SelectCards(["樱桃", "南瓜"] + diancai_list)

UpdatePaoList(
    [
        (1, 7),
        (1, 5),
        (1, 3),
        (1, 1),
        (2, 7),
        (2, 5),
        (2, 3),
        (2, 1),
        (3, 7),
        (3, 5),
        (3, 3),
        (3, 1),
        (4, 7),
        (4, 5),
        (4, 3),
        (4, 1),
        (5, 7),
        (5, 5),
        (5, 3),
        (5, 1),
        (6, 7),
        (6, 5),
        (6, 3),
        (6, 1),
    ]
)
# UpdatePaoList([(r, c) for r in range(1, 7) for c in range(7, 0, -2)])


StartAutoCollectThread()


for wave in range(1, 21):

    if wave == 1:
        Prejudge(-150, wave)
        Pao((2, 9), (5, 9))
        Until(-150 + 108)
        Pao((1, 8), (5, 8))

    elif wave == 10:  # PSA/PD
        Prejudge(-55, wave)
        Pao((2, 9), (5, 9))
        Until(-55 + 100)  # 100 < 105, P+S 秒白眼
        Pao(2, 9)  # S 炸 3-9 小偷
        Until(-55 + 108)
        Pao(5, 8)  # D 炸 4-9 小偷
        Until(-55 + 100 + 108 + 373 - 100)
        Card("樱桃", 1, 9)  # A 1-9 拦截

    elif wave == 20:
        Prejudge(-150, wave)
        Pao((4, 6), (4, 8))  # 炮炸珊瑚
        Delay(90)
        Pao((1, 9), (2, 9), (5, 9), (6, 9))
        Delay(108)
        Pao((1, 9), (2, 9), (5, 9), (6, 9))

    else:  # (2, 3, 4, 5, 6, 7, 8, 9, 11, 12, 13, 14, 15, 16, 17, 18, 19)
        Prejudge(-150, wave)
        Pao((2, 9), (5, 9))
        Until(-150 + 81)
        DianCai()
        Until(-150 + 108)
        Pao((1, 8), (5, 8))

        if wave in (9, 19):  # 9/19 波收尾
            Until(601 - 150)
            Pao((2, 9), (5, 9))
            Until(601 - 150 + 81)
            DianCai()
            Until(601 - 150 + 108)
            Pao((1, 8), (5, 8))
            Until(601 + 601 - 150)
            Pao((2, 9), (5, 9))
            Until(601 + 601 - 150 + 81)
            DianCai()
            if wave == 9:  # P 用前场炮, D 用后场炮
                SkipPao(2)
