# coding=utf-8

"""
作者: lmintlcx
日期: 2019-03-14
阵名: PE半场十二炮
出处: https://tieba.baidu.com/p/1801759994
节奏: ch4: I+BC/d-PDD/P|I+BC/d-PDD/P, (18|18)
视频:
- https://www.bilibili.com/video/av40880422
- https://www.youtube.com/watch?v=MvKZKGRMwoU
"""

from pvz import *

# 种垫铲垫
@RunningInThread
def DianCai():
    Card("小喷", (1, 9))
    Card("阳光", (2, 9))
    Delay(100)
    Shovel((1, 9))
    Shovel((2, 9))


# 烧小偷
@RunningInThread
def 口吐金蛇():
    # 等第 10 波刷新
    while CurrentWave() < 10:
        Sleep(1)
    Delay(400)
    Card("睡莲", (4, 9))
    Card("辣椒", (4, 9))
    Delay(100 + 1)
    Shovel((4, 9))
    # 等第 20 波刷新
    while CurrentWave() < 20:
        Sleep(1)
    Delay(400)
    Card("睡莲", (4, 9))
    Card("辣椒", (4, 9))
    Delay(100 + 1)
    Shovel((4, 9))


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

SelectCards(["白冰", "冰菇", "咖啡", "荷叶", "南瓜", "樱桃", "辣椒", "倭瓜", "阳光", "小喷"])

UpdatePaoList([
    (1, 3), (2, 3), (3, 3),
    (1, 5), (2, 5), (3, 5),
    (1, 7), (2, 7), (3, 7),
    (1, 1), (2, 1), (3, 1),
    ])


while GameUI() != 3:
    Sleep(1)
while GamePaused():
    Sleep(1)
Card("寒冰菇", (5, 5))  # 临时存冰
Card("睡莲", (3, 9))  # 临时存冰位
Card("南瓜头", (3, 9))  # 其实不需要


StartAutoCollectThread()
StartAutoFillIceThread([(4, 5), (4, 6), (4, 7), (4, 8), (3, 9)], 17 - 1)
StartNutsFixerThread([(4, 5), (4, 6), (4, 7), (4, 8)], "南瓜头")
口吐金蛇()  # 这什么鬼函数名


for wave in range(1, 21):
    print("当前操作波次: " + str(wave))

    Prejudge(-200, wave)

    if wave in (1, 10):
        Until(-95)
        Pao((1, 9))
        Until(-15)
        Pao((2, 9), (5, 9))
        Until(-15 + 110)
        Pao((5, 7.7))
        Until(-15 + 110 + 373 - 100)  # 368
        Card("樱桃", (1, 9))

    elif wave == 20:
        Until(-150 - 30)
        Pao((4, 7), 30)
        Until(-60)  # 等到刷新前 60cs
        Pao((2, 9), (5, 9), (2, 9), (5, 9))
        Until(-60 + 110)
        Pao((1, 8.8), (2, 8.8))  # 炮不够 ==
        Until(-60 + 110 + 373 - 100)
        Card("樱桃", (5, 9))
        while not TryPao((5, 8)):
            Sleep(1)
        print(f"第 {wave} 波手动收尾.")
        Until(5500 + 100)
        Shovel((3, 9), (3, 9))  # 跳白字后铲掉

    else:
        Until(-133)
        Pao((1, 8.0))  # 拦截上波红眼, 分离部分快速僵尸
        Until(360 - 373)
        Pao((2, 8.15))  # "无冰分离."  ----发出日智的声音
        Until(360 - 298)  # 360cs 反应冰
        Coffee() if wave not in (2,) else Card("咖啡豆", (5, 5))
        Until(360 + 500 - 373)
        # WZ_PNT = (5, 2.7) if wave in (3, 12) else (5, 3)  # 尾炸落点
        WZ_PNT = (5, 3)
        Pao(WZ_PNT) if wave not in (2, 11) else None  # 下半场尾炸
        Until(1800 - 200 - 373)
        Pao((2, 9), (5, 8.1))  # 激活炸
        Delay(10)
        DianCai()  # 垫撑杆
        Until(1800 - 200 - 373 + 220)
        Pao((1, 8.2))  # 秒白眼, 触发红眼投掷

        if wave in (9, 19):  # 收尾波次
            Until(1800 - 133)
            Pao((1, 8.0))
            Until(1800 + 360 - 373)
            Pao((2, 9))
            Until(1800 + 360 + 500 - 373)
            Pao((5, 2.5))
            Until(1800 + 1800 - 200 - 373)
            Pao((5, 6))
            Delay(110)
            Pao((5, 6))
            Delay(110)
            Pao((5, 3))
            Until(4500 - 200 - 373)
            Pao((5, 5))
            SkipPao(2) if wave == 9 else None  # 中场调整
