# -*- coding: utf-8 -*-

from pvz import *

SelectCards(["复制冰", "寒冰菇", "咖啡豆", "窝瓜", "南瓜", "樱桃", "花盆", "胆小", "阳光", "小喷"])

# UpdatePaoList([(1, 1), (1, 3), (1, 5), (1, 7), (2, 1), (2, 3), (2, 5), (2, 7), (3, 1), (3, 3), (3, 5), (3, 7), (4, 1), (4, 3), (4, 5), (4, 7), (5, 1), (5, 3), (5, 5), (5, 7), (6, 1), (6, 3), (6, 5), (6, 7)])

# UpdatePaoList([(r, c) for r in range(1, 7) for c in range(1, 8, 2)])

StartAutoCollectThread()
StartAutoFillIceThread([(4, 9)])

for wave in range(1, 21):
    if wave in (1, 4, 7, 11, 14, 17):
        # 精准之舞
        Prejudge(-15, wave)
        Pao((2, 9), (5, 9))
        Delay(107)
        Pao((1, 7.8), (5, 7.8))
    elif wave in (2, 5, 8, 12, 15, 18):
        # 冰之旋舞
        Prejudge(-95, wave)
        Pao((2, 9), (5, 9))
        Delay(373 - 298 - 5)  # 冰稍早生效
        Coffee()
    elif wave in (3, 6, 9, 13, 16, 19):
        # 六神乱舞
        Prejudge(-95, wave)
        Pao((2, 9), (5, 9), (2, 9), (5, 9))
        Delay(110)
        Pao((1, 8.8), (5, 8.8))
        if wave in (9, 19):
            Delay(600 + 95 - 110)  # Until(600 - 15)
            Pao((2, 9), (5, 9))
    elif wave == 10:
        Prejudge(-55, wave)
        Pao((2, 9), (5, 9), (2, 9), (5, 9))
        Delay(110)
        Pao((1, 8.8), (5, 8.8))
    elif wave == 20:
        Prejudge(-150, wave)
        Pao((4, 6), (4, 8))  # 炮炸珊瑚
        Delay(95)
        Pao((2, 9), (5, 9))
        Delay(30)
        Pao((2, 9), (5, 9))
        Delay(30)
        Pao((2, 9), (5, 9))
        Delay(30)
        Pao((2, 9), (5, 9))
