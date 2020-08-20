# coding=utf-8
"""
阵名: PE经典十二炮
出处: https://tieba.baidu.com/f?kz=675626485
节奏: P6: PP|PP|PP|PP|PP|PP
"""

from pvz import *

WriteMemory("int", 0x00679300, 0x0040FCED)  # 取消点炮限制

SelectCards(["樱桃", "小喷"])

AutoCollect()  # 自动收集资源

for wave in range(1, 21):
    print("当前操作波次: " + str(wave))
    Prejudge(-199, wave)

    # 关底炮炸珊瑚
    if wave in (20, ):
        Until(-150)
        Pao((4, 7))

    # 每波预判炸
    Until(-95)
    if wave in (10, 20):
        Until(-30)
    Pao((2, 9), (5, 9))

    # 旗帜波加樱桃消延迟
    if wave in (10, ):
        Until(-30 + 373 - 100)
        Card("樱桃", (2, 9))

    # 收尾额外多炸两轮
    if wave in (9, 19, 20):
        for _ in range(2):
            Delay(601)
            Pao((2, 9), (5, 9))
