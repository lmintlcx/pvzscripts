# coding=utf-8

"""
Author: lmintlcx
Date: 2018-12-18
---
Name: PE新二十二炮
Rhythm: ch6: PSD/PDC|IPP-PPDD|PSD/PDC|IPP-PPDD, (6|12|6|12)
Video:
- https://www.bilibili.com/video/av38402840
- https://youtu.be/5e52yWxsMZU
"""

from pvz import *


@RunningInThread
def DianCai():
    Card("阳光菇", (5, 9))
    Card("小喷菇", (6, 9))
    Delay(30)
    Shovel((5, 9))
    Shovel((6, 9))


Sleep(300)

SelectCards(["玉米", "玉米炮", "咖啡豆", "复制冰", "寒冰菇", "樱桃", "窝瓜", "南瓜", "阳光", "小喷"])

UpdatePaoList(
    [
        (1, 1),
        (2, 1),
        (3, 1),
        (4, 1),
        (5, 1),
        (6, 1),
        (1, 3),
        (2, 3),
        (3, 3),
        (4, 3),
        (5, 3),
        (6, 3),
        (1, 5),
        (2, 5),
        (3, 5),
        (4, 5),
        (5, 5),
        (6, 5),
        (1, 7),
        (2, 7),
        (5, 7),
        (6, 7),
    ]
)

# UpdatePaoList(
#     [
#         (r, c)
#         for r in range(1, 7)
#         for c in range(1, 8, 2)
#         if not (r in (3, 4) and c == 7)
#     ]
# )


StartAutoCollectThread()
StartAutoFillIceThread([(4, 9), (3, 9), (2, 9)], 10)
# StartAutoFillIceThread([(4, 9), (3, 9)], 10)  # 只用两个存冰位中场需要拖时间

for wave in range(1, 21):
    # if wave == 19:
    #     SetFixPao((2, 7))
    if wave in (1, 3, 5, 7, 9, 12, 14, 16, 18):
        Prejudge(-135, wave)
        Pao((1, 9), (5, 9))
        Until(-95)
        Pao(2, 9)
        Until(-135 + 110)
        Pao(5, 7.8)
        Until(-95 + 110)
        Pao(1, 8.8)
        Until(601 + 50 - 298)  # 50cs 预判冰
        Coffee()
        if wave == 9:
            Until(601 - 135)
            DianCai()
            Until(-95)
            Pao(2, 8.5)  # 上半场清空 ==
            Until(601 + 180 - 30)
            Pao(5, 7.2, 30)
            Until(601 + 1200 - 373 - 200)
            Pao(5, 9)
            Delay(220)
            Pao(5, 8.4)
            Until(601 + 1200 - 135)
            Delay(270)  # 等会儿
            Pao((2, 9), (5, 9))  # 清场
    elif wave == 10:
        # 预判推迟到 55cs
        Prejudge(-55, wave)
        Pao((1, 9), (5, 9))
        # Until(-55)
        Pao(2, 9)
        Until(-55 + 110)
        Pao(5, 7.8)
        Until(-55 + 110)
        Pao(1, 8.8)
        Until(601 + 50 - 298)  # 50cs 预判冰
        Coffee()
    elif wave in (2, 4, 6, 8, 11, 13, 15, 17, 19):
        # -135 种垫材
        # -135+180 = 45 跳跃完成
        # 50 冰生效
        Prejudge(-135, wave)
        DianCai()
        Until(-95)  # 刷新前 95cs
        Pao(2, 8.5)  # 上半场热过渡
        Until(180 - 30)  # 刷新后 180cs, 提前 30cs 点炮
        Pao(5, 7.2, 30)  # 下半场热过渡, 点炮延迟发射
        Until(1200 - 373 - 200)  # 1200cs 波长
        Pao((2, 9), (5, 9))  # 激活炸
        Delay(220)
        Pao((1, 8.4), (5, 8.4))  # 拦截并再次触发投掷, 落点左移
        if wave == 19:
            Until(1200 - 135)
            Pao((1, 9), (5, 9))
            Until(1200 + 601)
            Pao((2, 9), (5, 9))  # 清场
    elif wave == 20:
        Prejudge(-180, wave)
        Pao(4, 7, 30)  # 点炮后延迟 30cs 炸珊瑚
        Pao(4, 8)
        Until(-60)  # 等到刷新前 60cs
        Pao((1, 9), (2, 9), (5, 9), (6, 9))
        Delay(108)
        Pao((1, 9), (2, 9), (5, 9), (6, 9))
