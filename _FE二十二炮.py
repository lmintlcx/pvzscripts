# coding=utf-8
"""
阵名: FE二十二炮
出处: None
节奏: ch9-57s: IPP-PPDD|PSD/PDC|IPP-PPDD|PSD/PDC|N+AD/DC|PD/PDC|PSD/PDC, (13.5|6|13.5|6|6|6|6)
"""

from pvz import *

WriteMemory("int", 0x00679300, 0x0040FCED)  # 取消点炮限制
WriteMemory("unsigned short", 0xd231, 0x0041a68d)  # 浓雾透视


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


SetZombies(["普僵", "撑杆", "舞王", "冰车", "海豚", "矿工", "跳跳", "蹦极", "扶梯", "篮球", "白眼", "红眼"])

SelectCards(["寒冰菇", "模仿冰", "毁灭菇", "睡莲", "樱桃", "坚果", "花盆", "胆小", "阳光", "小喷"])

UpdatePaoList([
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
])

AutoCollect()  # 自动收集资源

# IPP-PPDD
Prejudge(5 - 100, 1)  # 本波 5cs 预判冰
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
Prejudge(-133, 2)  # 133 预判对应上波过 220 继续拦截
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
# 相比 wave1 多了垫材操作
Prejudge(-180, 3)
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
# 炸法同 wave2
Prejudge(-133, 4)
Pao((1, 9), (5, 9))
Until(-95)
Pao((2, 9))
Until(-133 + 110)
Pao((5, 7.8))
Until(-95 + 110)
Pao((1, 8.8))

# N+AD/DC
# 连续加速波下半场对应垫材 24 炮打法, 因此激活炮要尽早生效
# 最早为 226 可全炸巨人, 相当于 147 预判炮
# 这里 N 相当于激活炮, 上半场 A 相当于 S
Prejudge(-145 + 83, 5)  # 下半场使撑杆不啃炮的最早放垫材时间
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
Prejudge(-145, 6)
Pao((5, 9))  # 下半场 P
Delay(83)
DianCai()  # 垫上一波撑杆
Until(-145 + 110)
Pao((5, 7.8))  # 下半场 D
Until(-14)
Pao((2, 9))  # 上半场 P
Delay(107)
Pao((1, 7.8))  # 上半场 D

# PSD/PDC
Prejudge(-145, 7)
Pao((5, 9))  # 下半场 P
Until(-95)
Pao((2, 9), (2, 9))  # 上半场 PS
Until(-145 + 83)
DianCai()  # 垫上一波撑杆
Until(-145 + 110)
Pao((5, 7.8))  # 下半场 D
Until(-95 + 110)
Pao((1, 8.8))  # 上半场 D

# IPP-PPDD
Prejudge(-180, 8)
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

# 收尾波
Prejudge(-133, 9)
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
# 上半场 PSD, 下半场收撑杆省垫材
Prejudge(-83, 10)  # -83
Pao((1, 9))
Until(-14)  # -14
Pao((5, 9))
Until(-83 + 104)  # 394-373=21
Pao((2, 9))
Until(-14 + 110)  # 96
Pao((5, 7.8))
Until(-83 + 104 + 110)  # 131
Pao((1, 8.8))

# IPP-PPDD
Prejudge(5 - 100, 11)
# 相比 wave1 多了垫红眼操作
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
Prejudge(-133, 12)  # 133 预判对应上波过 220 继续拦截
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
# 相比 wave11 多了垫材操作
Prejudge(-180, 13)
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
# 炸法同 wave12
Prejudge(-133, 14)
Pao((1, 9), (5, 9))
Until(-95)
Pao((2, 9))
Until(-133 + 110)
Pao((5, 7.8))
Until(-95 + 110)
Pao((1, 8.8))

# N+AD/DC
# 操作同 wave5,  弹坑改为 4-9
Prejudge(-145 + 83, 15)
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
# 下半场对应垫材 24 炮打法, 上半场精准之舞
Prejudge(-145, 16)
Pao((5, 9))  # 下半场 P
Delay(83)
DianCai()  # 垫上一波撑杆
Until(-145 + 110)
Pao((5, 7.8))  # 下半场 D
Until(-14)
Pao((2, 9))  # 上半场 P
Delay(107)
Pao((1, 7.8))  # 上半场 D

# PSD/PDC
Prejudge(-145, 17)
Pao((5, 9))  # 下半场 P
Until(-95)
Pao((2, 9), (2, 9))  # 上半场 PS
Until(-145 + 83)
DianCai()  # 垫上一波撑杆
Until(-145 + 110)
Pao((5, 7.8))  # 下半场 D
Until(-95 + 110)
Pao((1, 8.8))  # 上半场 D

# IPP-PPDD
Prejudge(-180, 18)
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

# 收尾波
Prejudge(-133, 19)
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

# PP-PPPPPPPP
Prejudge(-150, 20)
Pao((4, 7))  # 炮炸珊瑚
Until(-60)  # 等到刷新前 60cs
Pao((2, 9), (5, 9))
Delay(108)
Pao((1, 8.8), (5, 8.8))
Delay(108)
Pao((1, 8.6), (5, 8.6))
Delay(108)
Pao((2, 8.4), (5, 8.4))  # 炸小偷
print("最后一大波手动收尾.")
