# -*- coding: utf-8 -*-

from pvz import *

# 种垫材
def DianCai():
    Card(9, 5, 9)
    Card(10, 6, 9)


# 铲垫材
def ChanDianCai():
    Shovel(5, 9)
    Shovel(6, 9)


SelectCards(["咖啡豆", "寒冰菇", "复制冰", "樱桃", "窝瓜", "南瓜", "花盆", "胆小", "阳光", "小喷"])

# UpdatePaoList(
#     [
#         (1, 1),
#         (2, 1),
#         (3, 1),
#         (4, 1),
#         (5, 1),
#         (6, 1),
#         (1, 3),
#         (2, 3),
#         (3, 3),
#         (4, 3),
#         (5, 3),
#         (6, 3),
#         (1, 5),
#         (2, 5),
#         (3, 5),
#         (4, 5),
#         (5, 5),
#         (6, 5),
#         (1, 7),
#         (2, 7),
#         (5, 7),
#         (6, 7),
#     ]
# )

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
# StartAutoFillIceThread([(4, 9), (3, 9)], 10)  # 需要拖时间

for wave in range(1, 21):
    if wave in (1, 3, 5, 7, 9, 12, 14, 16, 18):
        Prejudge(-135, wave)
        Pao((1, 9), (5, 9))
        Until(-95)
        Pao(2, 9)
        Until(-135 + 110)
        Pao(5, 7.8)
        Until(-95 + 110)
        Pao(1, 8.8)
        Until(600 + 50 - 298)  # 50cs 预判冰
        Coffee()
        if wave == 9:
            Until(600 - 135)
            DianCai()
            Delay(20)
            ChanDianCai()
            # Until(-95)
            # Pao(2, 8.5)
            Until(600 + 180 - 30)
            Pao(5, 7.2, 30)
            Until(600 + 1200 - 373 - 200)
            Pao(5, 9)
            Delay(220)
            Pao(5, 8.4)
            Until(600 + 1200 - 135)
            Pao((2, 9), (5, 9))
    elif wave in (2, 4, 6, 8, 11, 13, 15, 17, 19):
        # -135 种垫材
        # -135+180 = 45 跳跃完成
        # 50 冰生效
        Prejudge(-135, wave)
        DianCai()
        Delay(20)
        ChanDianCai()
        Until(-95)  # 刷新前 95cs
        Pao(2, 8.5)  # 上半场热过渡
        Until(180 - 30)  # 刷新后 180cs
        Pao(5, 7.2, 30)  # 下半场热过渡, 点炮延迟发射
        Until(1200 - 373 - 200)  # 1200cs 波长
        Pao((2, 9), (5, 9))  # 激活炸
        Delay(220)
        Pao((1, 8.4), (5, 8.4))  # 拦截并再次触发投掷
        if wave == 19:
            Until(1200 - 135)
            Pao((1, 9), (5, 9))
            Until(1200 + 600)
            Pao((2, 9), (5, 9))
    elif wave == 10:
        #  预判推迟到 55cs
        Prejudge(-55, wave)
        Pao((1, 9), (5, 9))
        Until(-55)
        Pao(2, 9)
        Until(-55 + 110)
        Pao(5, 7.8)
        Until(-55 + 110)
        Pao(1, 8.8)
        Until(600 + 50 - 298)
        Coffee()
    elif wave == 20:
        Prejudge(-180, wave)
        Pao(4, 7, 30)  # 点炮后延迟 30cs 炸珊瑚
        Pao(4, 8)
        Until(-55)  # 等到刷新前 55cs
        Pao((2, 9), (5, 9), (2, 9), (5, 9))
        Delay(90)
        Pao((2, 9), (5, 9), (2, 9), (5, 9))
