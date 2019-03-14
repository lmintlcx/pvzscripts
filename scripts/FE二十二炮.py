# coding=utf-8

"""
作者: 冰巫师墨舞, lmintlcx
日期: 2019-03-14
阵名: FE二十二炮
出处: None
节奏: ch9-57s: IPP-PPDD|PSD/PDC|IPP-PPDD|PSD/PDC|N+AD/DC|PD/PDC|PSD/PDC, (13.5|6|13.5|6|6|6|6)
视频:
- https://www.bilibili.com/video/av46250639
- https://www.youtube.com/watch?v=RB3VUOx61x8
"""

from pvz import *


# Cannon Fodder
# 下标 6/7 8/9
# 垫材 花盆/胆小菇 阳光菇/小喷菇
# 根据小喷是否可用来决定用哪一组垫材
@RunningInThread
def DianCai():
    if ReadMemory("bool", 0x6A9EC0, 0x768, 0x144, 0x70 + 9 * 0x50):
        Card("阳光菇", (5, 9))
        Card("小喷菇", (6, 9))
    else:
        Card("花盆", (5, 9))
        Card("胆小菇", (6, 9))
    Delay(30)
    Shovel((5, 9), (6, 9))


## 定义逐波操作


# IPP-PPDD
def wave1():
    Until(5 - 100)  # 本波 5cs 预判冰
    Card("寒冰菇", (2, 9))
    Until(-15)
    Pao((1, 8.8))  # 上半场热过渡, 炸 1 路收跳跳
    Until(444 - 373)
    Pao((5, 7.4))  # 下半场热过渡, 右极限大概 7.43
    Until(1350 - 200 - 373)
    Pao((2, 9), (5, 8.7))  # 激活炮, 下半场落点左移收跳跳
    Delay(220)
    Pao((1, 8.6), (5, 8.6))  # 连续拦截之一, 落点左移


# PSD/PDC
def wave2():
    Until(-133)  # 133 预判对应上波过 220 继续拦截
    Pao((1, 9), (5, 9))  # 连续拦截之二
    Until(-95)
    Pao((2, 9))  # 上半场 S
    Until(-133 + 110)
    Pao((5, 7.8))  # 下半场 D
    Until(-95 + 110)
    Pao((1, 8.8))  # 上半场 D
    Until(601 + 5 - 100 - 320)  # 下一波 5cs 预判冰
    Card("模仿者寒冰菇", (2, 9))


# IPP-PPDD
# 相比 wave1() 多了垫材操作
def wave3():
    Until(-180)
    DianCai()  # 垫上一波撑杆
    Until(-15)
    Pao((1, 8.8))
    Until(444 - 373)
    Pao((5, 7.4))
    Until(5 + 600)  # 全部解冻
    DianCai()  # 垫红眼
    Until(1350 - 200 - 373)
    Pao((2, 9), (5, 8.7))
    Delay(220)
    Pao((1, 8.6), (5, 8.6))


# PSD/PDC
# 炸法同 wave2()
def wave4():
    Until(-133)
    Pao((1, 9), (5, 9))
    Until(-95)
    Pao((2, 9))
    Until(-133 + 110 - 30)
    Pao((5, 7.8), 30)  # 避免射不到自己
    Until(-95 + 110)
    Pao((1, 8.8))


# N+AD/DC
# 连续加速波下半场对应垫材 24 炮打法, 因此激活炮要尽早生效
# 最早为 218 可全炸巨人, 相当于 155 预判炮
# 这里 N 相当于激活炮, 上半场 A 相当于 S
def wave5():
    Until(-145 + 81)  # 下半场使撑杆不啃炮的最早放垫材时间
    DianCai()  # 垫上一波撑杆
    Until(-145 + 110)
    Pao((5, 7.8))  # 下半场 D
    Until(-95 + 110)
    Pao((1, 8.8))  # 上半场 D
    Until(-145 + 373 - 100)  # 等效 145 预判炮
    Card("睡莲", (3, 9))
    Card("毁灭菇", (3, 9))
    Until(-95 + 373 - 100)  # 等效 95 预判炮
    Card("樱桃炸弹", (2, 9))


# PD/PDC
# 下半场对应垫材 24 炮打法, 上半场精准之舞
def wave6():
    Until(-145)
    Pao((5, 9))  # 下半场 P
    Delay(81)
    DianCai()  # 垫上一波撑杆
    Until(-145 + 110)
    Pao((5, 7.8))  # 下半场 D
    Until(-15)
    Pao((2, 9))  # 上半场 P
    Delay(107 - 30)  # 避免射不到自己
    Pao((1, 7.8), 30)  # 上半场 D


# PSD/PDC
def wave7():
    Until(-145)
    Pao((5, 9))  # 下半场 P
    Until(-95)
    Pao((2, 9), (2, 9))  # 上半场 PS
    Until(-145 + 81)
    DianCai()  # 垫上一波撑杆
    Until(-145 + 110)
    Pao((5, 7.8))  # 下半场 D
    Until(-95 + 110)
    Pao((1, 8.8))  # 上半场 D


# IPP-PPDD
def wave8():
    Until(-180)
    DianCai()
    Until(5 - 100)
    Card("寒冰菇", (2, 9))
    Until(-15)
    Pao((1, 8.8))
    Until(444 - 373)
    Pao((5, 7.4))
    Until(1350 + 15 - 100 - 320 - 373 - 1)  # 571
    Pao((2, 8.2))
    Until(5 + 600)  # 全部解冻
    DianCai()
    Until(1350 - 200 - 373)  # 777
    Pao((2, 9), (5, 8.7))
    Until(1350 + 15 - 100 - 320)  # 945
    Card("模仿者寒冰菇", (2, 9))
    Until(1350 - 200 - 373 + 220)  # 997
    Pao((1, 8.8), (5, 8.6))  # 上半场炸撑杆


# 收尾
def wave9():
    Until(-133)
    Pao((1, 9), (5, 9))
    Until(-15)
    Pao((1, 9), (5, 9))
    Until(1300 - 200 - 373)  # 1350->1300
    Pao((2, 9), (5, 9))
    Delay(220)
    Pao((1, 9), (5, 9))
    Delay(220)
    Pao((1, 9), (5, 9))
    Delay(600)  # 等冰菇 CD
    Pao((2, 9), (5, 9))
    Delay(700)  # 清伴舞
    Pao((2, 9), (5, 9))


# PSD/PDC
# 上半场 PSD, 下半场 15 预判收撑杆省垫材
def wave10():
    Until(-57)  # -57
    Pao((1, 9))
    Until(-15)  # -15
    Pao((5, 9))
    Until(-57 + 104)  # 420-373=47
    Pao((2, 9))
    Until(-15 + 110)  # 95
    Pao((5, 7.8))
    Until(-57 + 104 + 110)  # 157
    Pao((1, 8.8))


# IPP-PPDD
def wave11():
    # 相比 wave1() 多了垫红眼操作
    Until(5 - 100)
    Card("寒冰菇", (2, 9))
    Until(-15)
    Pao((1, 8.8))
    Until(444 - 373)
    Pao((5, 7.4))
    Until(5 + 600)  # 全部解冻
    DianCai()
    Until(1350 - 200 - 373)
    Pao((2, 9), (5, 8.7))
    Delay(220)
    Pao((1, 8.6), (5, 8.6))


# PSD/PDC
def wave12():
    wave2()


# IPP-PPDD
def wave13():
    wave3()


# PSD/PDC
def wave14():
    wave4()


# N+AD/DC
# 操作同 wave5(),  弹坑改为 4-9
def wave15():
    Until(-145 + 81)
    DianCai()
    Until(-145 + 110)
    Pao((5, 7.8))
    Until(-95 + 110)
    Pao((1, 8.8))
    Until(-145 + 373 - 100)
    Card("睡莲", (4, 9))
    Card("毁灭菇", (4, 9))
    Until(-95 + 373 - 100)
    Card("樱桃炸弹", (2, 9))


# PD/PDC
def wave16():
    wave6()


# PSD/PDC
def wave17():
    wave7()


# IPP-PPDD
def wave18():
    wave8()


# 收尾
def wave19():
    wave9()


# PP-PPPPPPPP
def wave20():
    Until(-150)
    Pao((4, 7))  # 炮炸珊瑚
    Until(-60)  # 等到刷新前 60cs
    Pao((2, 9), (5, 9))
    Delay(108)
    Pao((1, 8.8), (5, 8.8))
    Delay(108)
    Pao((1, 8.6), (5, 8.6))
    Delay(108)
    Pao((2, 8.4), (5, 8.4))  # 炸小偷


### 下面正式开始


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

SelectCards(["寒冰菇", "模仿冰", "毁灭菇", "睡莲", "樱桃", "坚果", "花盆", "胆小", "阳光", "小喷"])

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
        # (3, 7),
        # (4, 7),
        (5, 7),
        (6, 7),
    ]
)

# 自动收集
StartAutoCollectThread()

Prejudge(-200, 1)  # Prejudge(-599, 1)
wave1()
Prejudge(-200, 2)
wave2()
Prejudge(-200, 3)
wave3()
Prejudge(-200, 4)
wave4()
Prejudge(-200, 5)
wave5()
Prejudge(-200, 6)
wave6()
Prejudge(-200, 7)
wave7()
Prejudge(-200, 8)
wave8()
Prejudge(-200, 9)
wave9()
Prejudge(-200, 10)  # Prejudge(-750, 1)
wave10()
Prejudge(-200, 11)
wave11()
Prejudge(-200, 12)
wave12()
Prejudge(-200, 13)
wave13()
Prejudge(-200, 14)
wave14()
Prejudge(-200, 15)
wave15()
Prejudge(-200, 16)
wave16()
Prejudge(-200, 17)
wave17()
Prejudge(-200, 18)
wave18()
Prejudge(-200, 19)
wave19()
Prejudge(-200, 20)  # Prejudge(-750, 1)
wave20()
print(f"最后一大波手动收尾.")
