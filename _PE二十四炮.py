# coding=utf-8
"""
阵名: PE二十四炮
出处: https://tieba.baidu.com/p/991306518
节奏: P6: PPDD|PPI|PPSSDD|PPDD|PPI|PPSSDD
"""

from pvz import *

WriteMemory("int", 0x00679300, 0x0040FCED)  # 取消点炮限制

SetZombies(["普僵", "撑杆", "舞王", "冰车", "海豚", "矿工", "跳跳", "蹦极", "扶梯", "篮球", "白眼", "红眼"])

SelectCards(["复制冰", "寒冰菇", "咖啡豆", "南瓜", "坚果", "窝瓜", "花盆", "胆小", "阳光", "小喷"])

# UpdatePaoList(
#     [
#         (1, 1), (1, 3), (1, 5), (1, 7),
#         (2, 1), (2, 3), (2, 5), (2, 7),
#         (3, 1), (3, 3), (3, 5), (3, 7),
#         (4, 1), (4, 3), (4, 5), (4, 7),
#         (5, 1), (5, 3), (5, 5), (5, 7),
#         (6, 1), (6, 3), (6, 5), (6, 7),
#     ]
# )
# UpdatePaoList([(r, c) for r in range(1, 7) for c in range(1, 8, 2)])

AutoCollect()  # 自动收集资源
IceSpots([(4, 9)], 6)

for wave in range(1, 21):
    print("当前操作波次: " + str(wave))

    # 精准之舞 PPDD
    if wave in (1, 4, 7, 11, 14, 17):
        Prejudge(-14, wave)
        Pao((2, 9), (5, 9))
        Delay(107)
        Pao((1, 7.7), (5, 7.7))

    # 冰之旋舞 PPI
    elif wave in (2, 5, 8, 12, 15, 18):
        Prejudge(-95, wave)
        Pao((2, 9), (5, 9))
        Delay(373 - 100 - 198)  # 冰同步于炮生效
        Coffee()

    # 六神乱舞 PPSSDD
    elif wave in (3, 6, 9, 13, 16, 19):
        Prejudge(-95, wave)
        Pao((2, 9), (5, 9), (2, 9), (5, 9))
        Delay(108)
        Pao((1, 8.8), (5, 8.8))
        if wave in (9, 19):  # 收尾
            Until(601 - 15)
            Pao((2, 9), (5, 9))

    # 大波推迟 PPSSDD
    elif wave == 10:
        Prejudge(-56, wave)
        Pao((2, 9), (5, 9), (2, 9), (5, 9))
        Delay(108)
        Pao((1, 8.8), (5, 8.8))

    elif wave == 20:
        Prejudge(-150, wave)
        Pao((4, 6), (4, 8))  # 炮炸珊瑚
        Delay(90)  # Until(-60)
        Pao((1, 9), (2, 9), (5, 9), (6, 9))
        Delay(108)
        Pao((1, 9), (2, 9), (5, 9), (6, 9))
        print("第 %s 波手动收尾." % wave)
