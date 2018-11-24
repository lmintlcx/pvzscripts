# coding=utf-8

"""
Author: lmintlcx
Date: 2018-11-24
---
Name: PE超前置十六炮
Rhythm: ch6: PPDD|IPP-PP|PPDD|IPP-PP, (6|12|6|12)
Video:
- https://www.bilibili.com/video/av34825956
- https://youtu.be/8e7phSRx7uk
"""

from pvz import *

Sleep(300)

SelectCards(["复制冰", "寒冰菇", "咖啡豆", "窝瓜", "坚果", "樱桃", "花盆", "胆小", "阳光", "小喷"])

# UpdatePaoList([(1, 5), (1, 7), (2, 5), (2, 7), (3, 1), (3, 3), (3, 5), (3, 7), (4, 1), (4, 3), (4, 5), (4, 7), (5, 5), (5, 7), (6, 5), (6, 7)])
# UpdatePaoList([(r, c) for r in range(1, 7) for c in range(1, 8, 2) if not (r in (1, 2, 5, 6) and c in (1, 3))])

StartAutoCollectThread()
StartAutoFillIceThread([(6, 1), (5, 1), (2, 1), (1, 1)], 10)

for wave in range(1, 21):
    if wave in (1, 3, 5, 7, 9, 10, 12, 14, 16, 18):
        Prejudge(-95, wave)
        Pao((2, 9), (5, 9))
        Delay(80)
        Pao((2, 9), (5, 9))
        Delay(600 + 95 - 80 - 298 + 50)  # Until(600 + 50 - 298)
        Coffee()  # 点咖啡豆
        if wave == 9:
            # 第 9 波留 4 门炮手动收尾
            SkipPao(4)
    elif wave in (2, 4, 6, 8, 11, 13, 15, 17, 19):
        Prejudge(-95, wave)
        Pao((2, 8.5), (5, 8.5))
        Delay(1200 + 95 - 373 - 200)  # Until(1200 - 200 - 373)
        Pao((2, 9), (5, 9))
        if wave == 19:
            Until(1200 - 95)
            Pao((2, 9), (5, 9))
            Delay(80)
            Pao((2, 9), (5, 9))
            # 第 19 波留 3 门炮手动收尾
            SkipPao(3)
    elif wave == 20:
        Prejudge(-180, wave)
        Pao(4, 7, 30)  # 点炮后延迟 30cs 炸珊瑚
        Until(-55)  # 等到刷新前 55cs
        Pao((1, 9), (2, 9), (5, 9), (6, 9))
        Delay(108)
        Pao((1, 9), (2, 9), (5, 9), (6, 9))
