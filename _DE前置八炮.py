# coding=utf-8
"""
阵名: DE前置八炮
出处: https://tieba.baidu.com/p/3943536673
节奏: ch5: PP|I-PP|IPP-PP, (601|1437|1437)
"""

from pvz import *

SetZombies(["普僵", "撑杆", "舞王", "冰车", "气球", "矿工", "小丑", "跳跳", "蹦极", "扶梯", "篮球", "白眼", "红眼"])

SelectCards(["咖啡豆", "寒冰菇", "复制冰", "樱桃", "窝瓜", "坚果", "花盆", "胆小菇", "阳光菇", "小喷菇"])

UpdatePaoList([(1, 1), (1, 5), (3, 1), (3, 5), (2, 5), (4, 5), (5, 1), (5, 5)])

AutoCollect()  # 自动收集资源
IceSpots([(2, 1), (4, 1), (3, 7)], 14 - 1)

for wave in range(1, 21):
    print("当前操作波次: " + str(wave))
    Prejudge(-195, wave)

    # PP
    if wave in (1, 4, 7, 10, 13, 16, 19):
        Until(-40)
        Pao((2, 9), (4, 9))
        Until(601 + 10 - 298)
        Coffee()
        if wave in (19, ):
            Until(601 + 1437 - 200 - 373)
            Pao((2, 8.7), (4, 8.7))
            # Until(601 + 1437 - 150)
            Until(4500 - 200 - 373)
            Pao((2, 8.4), (4, 8.4))

    # I-PP
    elif wave in (2, 5, 8, 11, 14, 17):
        if wave == 2:
            Until(10 + 400)
            Card("倭瓜", (3, 9))  # 压冰车护存冰
        if wave == 11:
            Until(10 + 400 - 100)
            Card("樱桃", (3, 8))  # 炸冰车小偷护存冰
        if wave == 2:
            Until(750)
            Card("小喷菇", (3, 8))  # 垫撑杆
            Delay(100)
            Shovel((3, 8))
        Until(1437 - 200 - 373)
        Pao((2, 8.7), (4, 8.7))
        Until(1437 + 20 - 298)
        Coffee()

    # IPP-PP
    elif wave in (3, 6, 9, 12, 15, 18):
        Until(-150)
        Pao((2, 8.5), (4, 8.5))
        Until(1437 - 200 - 373)
        Pao((2, 8.7), (4, 8.7))
        if wave in (9, ):
            Until(1437 - 40)
            Pao((2, 8.7), (4, 8.7))
            # Until(1437 + 601 + 1437 - 200 - 373)
            Until(4500 - 200 - 373)
            Pao((2, 8.4), (4, 8.4))

    elif wave == 20:
        Until(-60)
        Pao((1, 9), (2, 9), (4, 9), (5, 9))
        Delay(108)
        Pao((1, 8.8), (4, 8.8))
        Until(300)
        Coffee()  # 冰杀小偷
        Until(999)
        Card("复制冰", (4, 1))  # 最后一个存冰
        print("第 %s 波手动收尾." % wave)
