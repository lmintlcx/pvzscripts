# coding=utf-8

"""
Author: lmintlcx
Date: 2018-12-18
---
Name: PE超前置十六炮
Rhythm: ch6: PPDD|IPP-PP|PPDD|IPP-PP, (6|12|6|12)
Video:
- https://www.bilibili.com/video/av38402042
- https://youtu.be/7RIwOCl7xNI
"""

from pvz import *

Sleep(300)

SelectCards(["复制冰", "寒冰菇", "咖啡豆", "窝瓜", "坚果", "樱桃", "花盆", "胆小", "阳光", "小喷"])

# UpdatePaoList([(3, 1), (4, 1), (3, 3), (4, 3), (1, 5), (2, 5), (3, 5), (4, 5), (5, 5), (6, 5), (1, 7), (2, 7), (3, 7), (4, 7), (5, 7), (6, 7)])
# UpdatePaoList([(r, c) for r in range(1, 7) for c in range(1, 8, 2) if not (r in (1, 2, 5, 6) and c in (1, 3))])

StartAutoCollectThread()
StartAutoFillIceThread([(6, 1), (5, 1), (2, 1), (1, 1)], 10)

for wave in range(1, 21):
    if wave in (1, 3, 5, 7, 9, 10, 12, 14, 16, 18):
        Prejudge(-95, wave)
        TryPao((2, 9), (5, 9))
        Delay(80)
        TryPao((2, 9), (5, 9))
        Delay(601 + 95 - 80 - 298 + 50)  # Until(601 + 50 - 298)
        Coffee()  # 点咖啡豆
        # # 第 9 波留 4 门炮手动收尾
        # if wave == 9:
        #     SkipPao(4)
    elif wave in (2, 4, 6, 8, 11, 13, 15, 17, 19):
        Prejudge(-95, wave)
        TryPao((2, 8.5), (5, 8.5))
        Delay(1200 + 95 - 373 - 200)  # Until(1200 - 200 - 373)
        TryPao((2, 9), (5, 9))
        if wave == 19:
            Until(1200 - 95)
            TryPao((2, 9), (5, 9))
            Delay(80)
            TryPao((2, 9), (5, 9))
            # # 第 19 波留 3 门炮手动收尾
            # SkipPao(3)
    elif wave == 20:
        Prejudge(-180, wave)
        TryPao(4, 7, 30)  # 点炮后延迟 30cs 炸珊瑚
        Until(-60)  # 等到刷新前 60cs
        TryPao((1, 9), (2, 9), (5, 9), (6, 9))
        Delay(108)
        TryPao((1, 9), (2, 9), (5, 9), (6, 9))
