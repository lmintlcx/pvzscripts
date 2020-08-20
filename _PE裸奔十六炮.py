# coding=utf-8
"""
阵名: PE裸奔十六炮
出处: https://tieba.baidu.com/p/1289540813
节奏: ch6: PPDC|IPd-PPD|PPDC|IPd-PPD, (6|12|6|12)
"""

from pvz import *

WriteMemory("int", 0x00679300, 0x0040FCED)  # 取消点炮限制


# 种垫铲垫
@RunningInThread
def DianCai():
    Card("小喷菇", (5, 9))
    Card("阳光菇", (6, 9))
    Delay(100)
    Shovel((5, 9))
    Shovel((6, 9))


# 偷菜
@RunningInThread
def Sunflower():
    sunflower_spots = [(1, 2), (1, 5), (1, 6), (2, 2), (2, 5), (2, 6)]
    # 开局种
    for spot in sunflower_spots:
        Card("向日葵", spot)
        Delay(751 + 1)
    # 等第 20 波刷新
    while ReadMemory("int", 0x6A9EC0, 0x768, 0x557C) < 20:
        Sleep(100)
    # 等白字出现
    while ReadMemory("int", 0x6A9EC0, 0x768, 0x140, 0x8C) != 12:
        Sleep(100)
    # 结尾铲
    for spot in sunflower_spots:
        Shovel(spot)


###

SetZombies(["普僵", "撑杆", "舞王", "冰车", "海豚", "矿工", "跳跳", "蹦极", "扶梯", "篮球", "白眼", "红眼"])

SelectCards(["咖啡豆", "寒冰菇", "复制冰", "樱桃", "窝瓜", "南瓜头", "向日葵", "胆小菇", "阳光菇", "小喷菇"])

# UpdatePaoList([
#     (3, 1), (3, 3), (3, 5), (3, 7),
#     (4, 1), (4, 3), (4, 5), (4, 7),
#     (5, 1), (5, 3), (5, 5), (5, 7),
#     (6, 1), (6, 3), (6, 5), (6, 7),
# ])

AutoCollect()  # 自动收集资源
IceSpots([(3, 9), (4, 9), (1, 4), (2, 4)], 10)
Sunflower()  # 偷菜线程

for wave in range(1, 21):
    print("当前操作波次: " + str(wave))

    Prejudge(-198, wave)  # 每波均用 198 预判

    # PPD|I-
    if wave in (1, 3, 5, 7, 9, 10, 12, 14, 16, 18):
        if wave == 10:
            Until(-56)
            Pao((2, 9), (5, 9))
            Until(-56 + 110)
            Pao((5, 8))
            Until(601 - 200 - 100)  # 301
            Card("樱桃", (2, 9))  # 消延迟 炸小偷
        else:
            Until(-133)
            Pao((2, 9), (5, 9))
            Until(-133 + 110)
            Pao((5, 8))
        Until(601 + 50 - 298)  # 353
        Coffee()  # 50cs 预判冰

        if wave == 9:  # 第 9 波收尾
            Until(601 - 135)
            DianCai()
            Until(601 - 100)
            Pao((1, 2.4))
            Until(601 + 444 - 373)
            Pao((5, 7.4))
            Until(601 + 1200 - 200 - 373)
            Pao((2, 9), (5, 9))
            Delay(220)
            Pao((5, 8.5))
            Until(601 + 1200 - 133)
            Pao((1, 2.4), (5, 9))
            Until(601 + 1200 - 133 + 110)
            Pao((2, 9))
            Until(601 + 1200 + 601 - 100)
            Delay(600)
            Pao((2, 8), (5, 9))
            Card("小喷菇", (1, 7))
            Card("阳光菇", (2, 7))
            Delay(400)
            Shovel((1, 7), (2, 7))

    # C|Pd-PPD
    elif wave in (2, 4, 6, 8, 11, 13, 15, 17, 19):
        Until(-135)
        DianCai()  # -135 放垫, 撑杆跳跃用时 180, 落地后 5 冰生效
        Until(-100)
        if wave == 11:
            Pao((1, 4))  # 炸小鬼和小偷
        else:
            Pao((1, 2.4))
        Until(444 - 373)
        Pao((5, 7.4))
        Until(1200 - 200 - 373)
        Pao((2, 9), (5, 9))
        Delay(220)
        Pao((5, 8.5))

        if wave == 19:  # 第 19 波收尾
            Until(1200 - 133)
            Pao((2, 9), (5, 9))
            Delay(350)
            Pao((1, 2.4))
            Delay(300)
            Pao((5, 9))
            Delay(400)
            Pao((2, 9))
            Delay(500)
            Pao((5, 9))
            Delay(400)
            Pao((2, 8))
            Card("小喷菇", (1, 7))
            Card("阳光菇", (2, 7))
            Delay(400)
            Shovel((1, 7), (2, 7))

    elif wave == 20:
        Until(-150)
        Pao((4, 7))
        Until(-60)  # 等到刷新前 60cs
        Pao((1, 9), (2, 9), (5, 9), (6, 9))
        Delay(108)
        Pao((1, 9), (2, 9), (5, 9), (6, 9))
        Delay(180)
        Pao((1, 4))  # 尾炸小偷
        print("第 %s 波手动收尾." % wave)
