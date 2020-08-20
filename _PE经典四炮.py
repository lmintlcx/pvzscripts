# coding=utf-8
"""
阵名: PE经典四炮
出处: https://tieba.baidu.com/p/664115150
节奏: C7i: PP|I-PP|I-PP|I-N, (6|18|18|11.5)
"""

from pvz import *

SetZombies(["普僵", "撑杆", "舞王", "冰车", "海豚", "矿工", "跳跳", "蹦极", "扶梯", "篮球", "白眼", "红眼"])

SelectCards(["寒冰菇", "复制冰", "核蘑菇", "睡莲", "咖啡豆", "南瓜", "樱桃", "窝瓜", "阳光菇", "小喷"])

UpdatePaoList([(3, 1), (4, 1), (3, 3), (4, 3)])

AutoCollect()  # 自动收集资源
IceSpots([(3, 5), (1, 4), (6, 4), (1, 5), (6, 5)], 15)

for wave in range(1, 21):
    print("当前操作波次: " + str(wave))

    Prejudge(-199, wave)

    # PP
    if wave in (1, 5, 9, 10, 14, 18):
        Until(601 - 200 - 373)
        Pao((2, 9), (5, 9))
        if wave == 10:
            Until(601 - 200 - 100)
            Card("樱桃", (2, 9))
        Until(601 + 20 - 298)  # 20cs 预判冰
        Coffee()
        if wave == 9:  # 第 9 波收尾
            Until(601 + 1800 - 200 - 373)
            Pao((2, 8.3), (5, 8.3))
            print("第 %s 波手动收尾." % wave)  # 倭瓜/垫材

    # I-PP
    elif wave in (2, 6, 11, 15, 19):
        Until(1800 - 200 - 373)
        Pao((2, 8.3), (5, 8.3))
        if wave != 19:
            Until(1800 + 20 - 298)  # 20cs 预判冰
            Coffee()
        if wave == 19:  # 第 19 波收尾
            Until(1800 + 1800 - 200 - 373)
            Pao((2, 8.3), (5, 8.3))
            print("第 %s 波手动收尾." % wave)  # 倭瓜/垫材/樱桃

    # I-PP
    elif wave in (3, 7, 12, 16):
        Until(1800 - 200 - 373)
        Pao((2, 8.3), (5, 8.3))
        Until(1800 + 50 - 298)  # 50cs 预判冰
        Coffee()

    # I-N
    elif wave in (4, 8, 13, 17):
        if wave == 4:
            row, col = (3, 8)
        elif wave == 8:
            row, col = (3, 9)
        elif wave == 13:
            row, col = (4, 8)
        elif wave == 17:
            row, col = (4, 9)
        Until(1150 - 200 - 298)
        Card("睡莲", (row, col))
        Card("核蘑菇", (row, col))
        Card("咖啡豆", (row, col))

    elif wave in (20, ):
        # 不管珊瑚
        Until(-60)
        Pao((2, 9), (5, 9))
        Until(300)
        Coffee()
        print("第 %s 波手动收尾." % wave)  # 樱桃/窝瓜/垫材/炮
