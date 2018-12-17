# coding=utf-8

"""
Author: lmintlcx
Date: 2018-12-18
---
Name: DE十四炮
Rhythm: ch6: PPdC|IP-PPD|PPdC|IP-PPD, (6|12|6|12)
Video:
- https://www.bilibili.com/video/av38405871
- https://youtu.be/5_3ezGon-Sk
"""

from pvz import *


@RunningInThread
def DianCai():
    Card("胆小菇", (1, 9))
    Card("阳光菇", (2, 9))
    Card("小喷菇", (3, 9))
    Delay(30)
    Shovel((1, 9))
    Shovel((2, 9))
    Shovel((3, 9))


Sleep(300)

SelectCards(["咖啡豆", "寒冰菇", "复制冰", "樱桃", "窝瓜", "南瓜头", "花盆", "胆小菇", "阳光菇", "小喷菇"])

UpdatePaoList(
    [(1, 1), (2, 1), (1, 5), (2, 5), (3, 5), (1, 7), (2, 7), (3, 7), (4, 2), (5, 2), (4, 4), (5, 4), (4, 6), (5, 6)]
)


StartAutoCollectThread()
StartAutoFillIceThread([(4, 1), (5, 1)], 10)


for wave in range(1, 21):

    if wave in (1, 3, 5, 7, 9, 12, 14, 16, 18):
        Prejudge(-135, wave)
        Pao((2, 9), (4, 9))
        Delay(250)  # 原速尾炸参考延时
        Pao(4, 2.4)
        Until(601 + 50 - 298)  # 50cs 预判冰
        Coffee()
        if wave == 9:
            Until(601 - 135)
            Pao(2, 8.5)
            Delay(81)
            DianCai()
            Until(601 + 1200 - 373 - 200)
            Pao((2, 9), (4, 9))
            Delay(220)
            Pao(4, 8.4)
            SkipPao(4)

    elif wave == 10:
        # 预判推迟到 55cs
        Prejudge(-55, wave)
        Pao((2, 9), (4, 9))
        Until(-55 + 250)
        Pao(4, 2.4)  # 尾炸小鬼小偷
        Until(-55 + 373 - 100)
        Card("樱桃", (2, 9))
        Until(601 + 50 - 298)  # 50cs 预判冰
        Coffee()

    elif wave in (2, 4, 6, 8, 11, 13, 15, 17, 19):
        Prejudge(-135, wave)
        Pao(2, 8.5)
        Delay(81)
        DianCai()
        Until(1200 - 373 - 200)  # 1200cs 波长
        Pao((2, 9), (4, 9))  # 激活炸
        Delay(220)
        Pao(4, 8.4)  # 拦截并再次触发投掷, 落点左移
        if wave == 19:
            Until(1200 - 135)
            Pao((2, 9), (4, 9))
            Delay(250)  # 原速尾炸参考延时
            Pao(4, 2.4)
            Until(1200 + 601 - 135)
            Pao(2, 8.5)
            SkipPao(3)

    elif wave == 20:
        Prejudge(-60, wave)
        Pao((1, 9), (2, 9), (4, 9), (5, 9))
        Delay(108)
        Pao((1, 9), (2, 9), (4, 9), (5, 9))
        Sleep(100)  # 炸小偷
        Pao(2, 1.5)
        Pao(2, 5.7)
        Pao(4, 2.4)
