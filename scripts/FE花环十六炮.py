# coding=utf-8

"""
作者: lmintlcx
日期: 2019-03-14
阵名: FE花环十六炮
出处: https://tieba.baidu.com/p/4394965593
节奏: C8u-50s: I-PPDD|I-PPDD|PPA'dd|PPDD|NAd|PPDD, (13|13|6|6|6|6)
视频:
- https://www.bilibili.com/video/av38409700
- https://www.youtube.com/watch?v=La31spQ_bzU
"""

from pvz import *


# EnableLogger(False)  # 输出调试信息
# SetWindowTopMost(True)  # 窗口置顶

# BackgroundRunning(True)  # 允许后台运行
# ZombieNoFalling(True)  # 僵尸死后不掉钱
# ClearFog(True)  # 开雾

# SetSun(8000)  # 阳光 8000
# SetMoney(0)  # 金钱 0
# JumpLevel(1009)  # 完成 2018 面旗帜数

SetZombies(["普僵", "撑杆", "舞王", "冰车", "海豚", "矿工", "跳跳", "蹦极", "扶梯", "篮球", "白眼", "红眼"])

Sleep(200)

SelectCards(["玉米投手", "玉米加农炮", "睡莲", "毁灭菇", "寒冰菇", "模仿者寒冰菇", "樱桃炸弹", "火爆辣椒", "坚果", "倭瓜"])

UpdatePaoList(
    [
        (3, 1),
        (3, 4),
        (3, 7),  # 计划铲种
        (6, 4),
        (6, 6),
        (6, 2),
        (1, 6),
        (1, 2),
        (1, 4),
        (4, 1),
        (4, 4),
        (4, 7),  # 计划铲种
        (5, 6),
        (5, 2),
        (2, 6),
        (2, 2),
    ]
)

# 自动收集
StartAutoCollectThread()

## 逐波操作

# 1 PPDD
Prejudge(-95, 1)
Pao((2, 9), (5, 9))
Delay(110)
Pao((1, 7.8), (5, 7.8))

# 2 PPDD
Prejudge(-95, 2)
Pao((2, 9), (5, 9))
Delay(110)
Pao((1, 7.8), (5, 7.8))

# 3 PPDD
Prejudge(-15, 3)
Pao((2, 9), (5, 9))
Delay(107)
Pao((1, 7.7), (5, 7.7))

# 4 I-PPDD
Prejudge(-95, 4)
Until(5 - 100)
Card("寒冰菇", (1, 1))  # 5cs
Until(1300 - 200 - 373)
Pao((2, 9), (5, 9))
Until(1300 + 58 - 100 - 320)  # 938
Card("模仿者寒冰菇", (1, 1))  # 58cs
Until(1300 - 200 - 373 + 220)  # 947
Pao((1, 7.8), (5, 7.8))

# 5 I-PPDD
Prejudge(-95, 5)
SetFixPao((3, 7))  # 铲种炮
Until(1300 - 200 - 373)
Pao((2, 9), (5, 9))
Until(1300 - 200 - 373 + 220)
Pao((1, 8.5), (5, 8.5))

# 6 PPA'dd
Prejudge(-133, 6)
Pao((2, 9), (5, 9))
Until(-133 + 250)  # 115
Pao((1, 2.4), (5, 2.4))  # 尾炸
Until(-133 + 373 - 100)  # 138
Card("火爆辣椒", (1, 1))

# 7 PPDD
Prejudge(-95, 7)
Pao((2, 9), (5, 9))
Delay(110)
Pao((1, 7.8), (5, 7.8))

# 8 NAd
Prejudge(-200, 8)
Until(-95 + 240 - 30)  # 145-30
Pao((5, 4), 30)  # 尾炸
Until(-95 + 373 - 100)  # 178
Card("睡莲", (3, 9))
Card("毁灭菇", (3, 9))
Until(-95 + 110 + 373 - 100)  # 288
Card("樱桃炸弹", (1, 8))

# 9 PPDD
Prejudge(-90, 9)  # 晚点
Pao((2, 9), (5, 9))
Delay(110)
Pao((5, 7.8), (1, 7.8))  # 调整
Until(601 + 5 - 100)
Card("寒冰菇", (1, 1))
# 收尾
Delay(600)  # 等会儿
Pao((2, 7.1), (5, 7.1))  # 只留本波巨人
Until(601 + 1300 + 58 - 100 - 320)
Card("模仿者寒冰菇", (1, 1))  # 58cs
Delay(600)  # 等会儿
Pao((2, 8.5), (5, 8.5))
Delay(220)
Pao((1, 8), (5, 8))
Delay(800)  # 等樱桃冷却
Pao((2, 8), (5, 8))

# 10 PPAdd
Prejudge(-55, 10)
Pao((2, 9), (5, 9))
Until(-55 + 240)  # 185
Pao((2, 4), (5, 4))  # 尾炸小偷
Until(-55 + 373 - 100)  # 218
Card("樱桃炸弹", (2, 9))

# 11 PPDD
Prejudge(-95, 11)
Pao((2, 9), (5, 9))
Delay(110)
Pao((1, 7.8), (5, 7.8))

# 12 PPDD
Prejudge(-15, 12)
Pao((2, 9), (5, 9))
Delay(107)
Pao((1, 7.7), (5, 7.7))

# 13 I-PPDD
Prejudge(-95, 13)
Until(5 - 100)  # -95
Card("寒冰菇", (1, 1))  # 5cs
Until(1300 - 200 - 373)
Pao((2, 9), (5, 9))
Until(1300 + 58 - 100 - 320)  # 938
Card("模仿者寒冰菇", (1, 1))  # 58cs
Until(1300 - 200 - 373 + 220)  # 947
Pao((1, 7.8), (5, 7.8))

# 14 I-PPDD
Prejudge(-95, 14)
SetFixPao((4, 7))  # 铲种炮
Until(1300 - 200 - 373)
Pao((2, 9), (5, 9))
Until(1300 - 200 - 373 + 220)
Pao((1, 8.5), (5, 8.5))

# 15 PPA'dd
Prejudge(-133, 15)
Pao((2, 9), (5, 9))
Until(-133 + 250)  # 115
Pao((1, 2.4), (5, 2.4))  # 尾炸
Until(-133 + 373 - 100)  # 138
Card("火爆辣椒", (1, 1))

# 16 PPDD
Prejudge(-95, 16)
Pao((2, 9), (5, 9))
Delay(110)
Pao((1, 7.8), (5, 7.8))

# 17 NAd
Prejudge(-200, 17)
Until(-95 + 240 - 30)  # 145-30
Pao((5, 4), 30)  # 尾炸
Until(-95 + 373 - 100)  # 178
Card("睡莲", (4, 9))
Card("毁灭菇", (4, 9))
Until(-95 + 110 + 373 - 100)  # 288
Card("樱桃炸弹", (1, 8))

# 18 PPDD
Prejudge(-15, 18)
Pao((2, 9), (5, 9))
Delay(107)
Pao((5, 7.7), (1, 7.7))  # 调整

# 19 I-PPDD
Prejudge(-95, 19)
Until(5 - 100)
Card("寒冰菇", (1, 1))  # 5cs
Until(1300 - 200 - 373)
Pao((2, 9), (5, 9))
# Until(1300 + 58 - 100 - 320)  # 940  # 58cs
Until(1300 - 200 - 373 + 220)  # 947
Pao((1, 7.8), (5, 7.8))
Delay(250)
Pao((1, 1), (5, 1))  # 尾炸矿工
Delay(250)  # 等会儿再冰
Card("模仿者寒冰菇", (1, 1))
# 收尾
Until(1300 + 1300 - 200 - 373)  # 2027
Pao((2, 9), (5, 9))
Delay(220)
Pao((1, 8.5), (5, 8.5))
Delay(1300)  # 等寒冰菇冷却
Pao((2, 8), (5, 8))

# 20
Prejudge(-95, 20)
Pao((2, 8), (5, 8))  # 炸矿工冰车
Until(50)
Card("寒冰菇", (1, 1))  # 冰消珊瑚
Until(75)
Pao((2, 4), (5, 4))  # 炮炸小偷
Until(750)
Pao((2, 9), (5, 9))  # 轰 !!!
Delay(50)
Pao((2, 9), (5, 9))  # 轰 !!!
Delay(50)
Pao((2, 9), (5, 9))  # 轰 !!!
Delay(50)
Pao((2, 9), (5, 9))  # 轰 !!!
print(f"最后一大波手动收尾.")
