# coding=utf-8

"""
作者: lmintlcx
日期: 2019-03-14
阵名: PE裸奔十六炮
出处: https://tieba.baidu.com/p/1289540813
节奏: ch6: PPDC|IPd-PPD|PPDC|IPd-PPD, (6|12|6|12)
视频:
- https://www.bilibili.com/video/av40496902
- https://www.youtube.com/watch?v=6WUQcO9xaYo
"""

from pvz import *


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
        Delay(750 + 1)
    # 等第 20 波刷新
    while CurrentWave() < 20:
        Sleep(100)
    # 等白字出现
    while ReadMemory("int", 0x6A9EC0, 0x768, 0x140, 0x8C) != 12:
        Sleep(100)
    # 结尾铲
    for spot in sunflower_spots:
        Shovel(spot)


###

# EnableLogger(False)  # 输出调试信息
# SetWindowTopMost(True)  # 窗口置顶

# BackgroundRunning(True)  # 允许后台运行
# ZombieNoFalling(True)  # 僵尸死后不掉钱

# SetSun(8000)  # 阳光 8000
# SetMoney(0)  # 金钱 0
# JumpLevel(1009)  # 完成 2018 面旗帜数

SetZombies(["普僵", "撑杆", "舞王", "冰车", "海豚", "矿工", "跳跳", "蹦极", "扶梯", "篮球", "白眼", "红眼"])

Sleep(200)

SelectCards(["咖啡豆", "寒冰菇", "复制冰", "樱桃", "窝瓜", "南瓜头", "向日葵", "胆小菇", "阳光菇", "小喷菇"])

# UpdatePaoList([
#     (3, 1), (3, 3), (3, 5), (3, 7),
#     (4, 1), (4, 3), (4, 5), (4, 7),
#     (5, 1), (5, 3), (5, 5), (5, 7),
#     (6, 1), (6, 3), (6, 5), (6, 7),
# ])


StartAutoCollectThread()
StartAutoFillIceThread([(3, 9), (4, 9), (1, 4), (2, 4)], 10)
Sunflower()  # 偷菜线程


for wave in range(1, 21):
    print("当前操作波次: " + str(wave))

    Prejudge(-200, wave)  # 每波均用 200 预判

    # PPD|I-
    if wave in (1, 3, 5, 7, 9, 10, 12, 14, 16, 18):
        if wave == 10:
            Until(-55)
            Pao((2, 9), (5, 9))
            Until(-55 + 110)
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
            Until(601 + 444 - 373 - 30)
            Pao((5, 7.4), 30)
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
        DianCai()
        Until(-100)
        if wave == 11:
            Pao((1, 4))  # 炸小鬼和小偷
        else:
            Pao((1, 2.4))
        Until(444 - 373 - 30)  # 提前 30cs 点炮
        Pao((5, 7.4), 30)  # 推迟 30cs 发射
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
        Until(-150 - 30)
        Pao((4, 7), 30)  # 点炮后延迟 30cs 炸珊瑚
        Until(-60)  # 等到刷新前 60cs
        Pao((1, 9), (2, 9), (5, 9), (6, 9))
        Delay(108)
        Pao((1, 9), (2, 9), (5, 9), (6, 9))
        Delay(180)
        Pao((1, 4))  # 尾炸小偷
        print(f"第 {wave} 波手动收尾.")
