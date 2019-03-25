
[<<< 返回首页](https://pvz.lmintlcx.com/)

# 代码示例

以下脚本文件均可在 [GitHub](https://github.com/lmintlcx/pvzscripts/tree/master/scripts) 上找到.

**部分脚本后期有更新, 可能会出现脚本代码和视频内容不一致的情况.**

**部分脚本操作细节优化来自于冰巫师墨舞, 特此表示感谢!**

## PE二十四炮

![PE二十四炮](/images/build/PE二十四炮.jpg)

```python
# coding=utf-8

"""
作者: lmintlcx
日期: 2019-03-14
阵名: PE二十四炮
出处: https://tieba.baidu.com/p/991306518
节奏: P6: PPDD|PPI|PPSSDD|PPDD|PPI|PPSSDD
视频:
- https://www.bilibili.com/video/av38400974
- https://www.youtube.com/watch?v=88S5vZjfg5I
"""

from pvz import *

# EnableLogger(False)  # 输出调试信息
# SetWindowTopMost(True)  # 窗口置顶

# BackgroundRunning(True)  # 允许后台运行
# ZombieNoFalling(True)  # 僵尸死后不掉钱

# SetSun(8000)  # 阳光 8000
# SetMoney(0)  # 金钱 0
# JumpLevel(1009)  # 完成 2018 面旗帜数

SetZombies(["普僵", "撑杆", "舞王", "冰车", "海豚", "矿工", "跳跳", "蹦极", "扶梯", "篮球", "白眼", "红眼"])

Sleep(200)

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

StartAutoCollectThread()
StartAutoFillIceThread([(4, 9)], 6)


for wave in range(1, 21):
    print("当前操作波次: " + str(wave))

    # 精准之舞 PPDD
    if wave in (1, 4, 7, 11, 14, 17):
        Prejudge(-15, wave)
        Pao((2, 9), (5, 9))
        Delay(107)
        Pao((1, 7.7), (5, 7.7))  # 7.625

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
        if wave in (9, 19):
            Delay(601 + 95 - 108 - 15)  # Until(601 - 15)
            Pao((2, 9), (5, 9))

    # 推迟 PPSSDD
    elif wave == 10:
        Prejudge(-55, wave)
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
        print(f"第 {wave} 波手动收尾.")

```

## PE裸奔十六炮

![PE裸奔十六炮](/images/build/PE裸奔十六炮.jpg)

```python
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

```

## PE半场十二炮

![PE半场十二炮](/images/build/PE半场十二炮.jpg)

```python
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

```

## PE经典四炮

![PE经典四炮](/images/build/PE经典四炮.jpg)

```python
# coding=utf-8

"""
作者: lmintlcx
日期: 2019-03-14
阵名: PE经典四炮
出处: https://tieba.baidu.com/p/664115150
节奏: C7i: PP|I-PP|I-PP|I-N, (6|18|18|11.5)
视频:
- https://www.bilibili.com/video/av40867249
- https://www.youtube.com/watch?v=LXWdCpY7qSc
"""

from pvz import *

# EnableLogger(False)  # 输出调试信息
# SetWindowTopMost(True)  # 窗口置顶

# BackgroundRunning(True)  # 允许后台运行
# ZombieNoFalling(True)  # 僵尸死后不掉钱

# SetSun(8000)  # 阳光 8000
# SetMoney(0)  # 金钱 0
# JumpLevel(1009)  # 完成 2018 面旗帜数

SetZombies(["普僵", "撑杆", "舞王", "冰车", "海豚", "矿工", "跳跳", "蹦极", "扶梯", "篮球", "白眼", "红眼"])

Sleep(200)

SelectCards(["寒冰菇", "复制冰", "核蘑菇", "睡莲", "咖啡豆", "南瓜", "樱桃", "窝瓜", "阳光菇", "小喷"])

UpdatePaoList([(3, 1), (4, 1), (3, 3), (4, 3)])

StartAutoCollectThread()
StartAutoFillIceThread([(3, 5), (1, 4), (6, 4)], 15)


for wave in range(1, 21):
    print("当前操作波次: " + str(wave))

    Prejudge(-200, wave)

    # PP
    if wave in (1, 5, 9, 10, 14, 18):
        Until(601 - 200 - 373)
        Pao((2, 9), (5, 9))
        Until(601 + 20 - 298)  # 20cs 预判冰
        Coffee()
        if wave == 9:  # 第 9 波收尾
            Until(601 + 1800 - 200 - 373)
            Pao((2, 8.3), (5, 8.3))
            print(f"第 {wave} 波手动收尾.")

    # I-PP
    elif wave in (2, 6, 11, 15, 19):
        Until(1800 - 200 - 373)
        Pao((2, 8.3), (5, 8.3))
        if wave == 19:  # 第 19 波收尾
            Until(1800 + 1800 - 200 - 373)
            Pao((2, 8.3), (5, 8.3))
            print(f"第 {wave} 波手动收尾.")
        else:
            Until(1800 + 20 - 298)  # 20cs 预判冰
            Coffee()

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

    elif wave in (20,):
        # 不管珊瑚
        Until(-55)
        Pao((2, 9), (5, 9))
        Until(300)
        Coffee()
        print(f"第 {wave} 波手动收尾.")

```

## DE前置八炮

![DE前置八炮](/images/build/DE前置八炮.jpg)

```python
# coding=utf-8

"""
作者: lmintlcx
日期: 2019-03-14
阵名: DE前置八炮
出处: https://tieba.baidu.com/p/3943536673
节奏: ch5: PP|I-PP|IPP-PP, (601|1437|1437)
视频:
- https://www.bilibili.com/video/av40974728
- https://www.youtube.com/watch?v=0AjJlfJ1dX0
"""

from pvz import *

# EnableLogger(False)  # 输出调试信息
# SetWindowTopMost(True)  # 窗口置顶

# BackgroundRunning(True)  # 允许后台运行
# ZombieNoFalling(True)  # 僵尸死后不掉钱

# SetSun(8000)  # 阳光 8000
# SetMoney(0)  # 金钱 0
# JumpLevel(1009)  # 完成 2018 面旗帜数

SetZombies(["普僵", "撑杆", "舞王", "冰车", "气球", "矿工", "小丑", "跳跳", "蹦极", "扶梯", "篮球", "白眼", "红眼"])

Sleep(200)

SelectCards(["咖啡豆", "寒冰菇", "复制冰", "樱桃", "窝瓜", "坚果", "花盆", "胆小菇", "阳光菇", "小喷菇"])

# UpdatePaoList([(1, 1), (1, 5), (3, 1), (3, 5), (2, 5), (4, 5), (5, 1), (5, 5)])

StartAutoCollectThread()
StartAutoFillIceThread([(2, 1), (4, 1), (3, 7)], 14 - 1)


for wave in range(1, 21):
    print("当前操作波次: " + str(wave))

    Prejudge(-200, wave)

    # PP
    if wave in (1, 4, 7, 10, 13, 16, 19):
        Until(-55) if wave == 10 else Until(-95)
        TryPao((2, 9), (4, 9))
        Until(601 + 10 - 298)
        Coffee()
        if wave in (19,):
            Until(601 + 1437 - 200 - 373)
            TryPao((2, 8.7), (4, 8.7))
            # Until(601 + 1437 - 150)
            Until(4500 - 200 - 373)
            TryPao((2, 8.4), (4, 8.4))

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
        TryPao((2, 8.7), (4, 8.7))
        Until(1437 + 20 - 298)
        Coffee()

    # IPP-PP
    elif wave in (3, 6, 9, 12, 15, 18):
        Until(-150)
        TryPao((2, 8.5), (4, 8.5))
        Until(1437 - 200 - 373)
        TryPao((2, 8.7), (4, 8.7))
        if wave in (9,):
            Until(1437 - 95)
            TryPao((2, 8.7), (4, 8.7))
            # Until(1437 + 601 + 1437 - 200 - 373)
            Until(4500 - 200 - 373)
            TryPao((2, 8.4), (4, 8.4))

    elif wave == 20:
        Until(-60)
        TryPao((2, 9), (4, 9), (2, 9), (4, 9))
        # Delay(100)
        # TryPao((1, 8.8), (4, 8.8))
        Until(601 - 298)
        Coffee()  # 冰杀小偷
        Until(601 + 10)
        Card("复制冰", (4, 1))  # 最后一个存冰
        print(f"第 {wave} 波手动收尾.")

```

## NE舞夜惊魂

![NE舞夜惊魂](/images/build/NE舞夜惊魂.jpg)

```python
# coding=utf-8

"""
作者: lmintlcx
日期: 2019-03-14
阵名: NE舞夜惊魂
出处: https://tieba.baidu.com/p/4354954825
节奏: P6-C: PPC|PPC|PPC|PPC|PPC|PPC
视频:
- https://www.bilibili.com/video/av38406841
- https://www.youtube.com/watch?v=Br-c7O4Z2d0
"""

from pvz import *

# Cannon Fodder
diancai_list = ["小喷菇", "模仿者小喷菇"]
diancai_spot = (4, 9)
diancai_index = 0


@RunningInThread
def DianCai():
    global diancai_index
    # 种垫材
    while ReadMemory("bool", 0x6A9EC0, 0x768, 0x164):  # 等待取消暂停
        Delay(1)
    Card(diancai_list[diancai_index % len(diancai_list)], diancai_spot)
    diancai_index += 1
    # 等待
    Delay(200)
    # 铲垫材
    while ReadMemory("bool", 0x6A9EC0, 0x768, 0x164):  # 等待取消暂停
        Delay(1)
    Shovel(diancai_spot)


# 收尾操作, 多炸三轮
def Ending():
    for _ in range(3):
        Delay(601 - 175 - 95)
        Pao((2, 9))
        Delay(80)
        Pao((4, 9))
        Delay(15 + 175)
        DianCai()


###
###
###

# EnableLogger(False)  # 输出调试信息
# SetWindowTopMost(True)  # 窗口置顶

# BackgroundRunning(True)  # 允许后台运行
# ZombieNoFalling(True)  # 僵尸死后不掉钱

# SetSun(8000)  # 阳光 8000
# SetMoney(0)  # 金钱 0
# JumpLevel(1009)  # 完成 2018 面旗帜数

SetZombies(["普僵", "撑杆", "舞王", "小丑", "气球", "矿工", "跳跳", "蹦极", "扶梯", "篮球", "白眼", "红眼"])

Sleep(200)

SelectCards(["小喷菇", "模仿者小喷菇"])

UpdatePaoList([(1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (1, 6), (2, 6), (3, 5), (3, 7), (4, 5), (4, 7), (5, 6)])

StartAutoCollectThread()
StartStopDancerThread()


for wave in range(1, 21):
    print("当前操作波次: " + str(wave))

    if wave == 10:
        Prejudge(-55, wave)
        Pao((2, 9))
        Until(-15)
        Pao((4, 9))
        Until(175)
        DianCai()

    elif wave == 20:
        Prejudge(-55, wave)
        Pao((2, 9))
        Until(-35)
        Pao((2, 8), (5, 8))  # 炸墓碑冒出的僵尸
        Until(-15)
        Pao((4, 9))
        Until(175)
        DianCai()
        Ending()  # 收尾

    else:
        Prejudge(-95, wave)
        Pao((2, 9))
        Until(-15)  # Delay(80)
        Pao((4, 9))
        Until(175)  # Delay(15 + 175)
        DianCai()
        if wave in (9, 19):
            Ending()  # 收尾

```

## NE十五炮

![NE十五炮](/images/build/NE十五炮.jpg)

```python
# coding=utf-8

"""
作者: 冰巫师墨舞, lmintlcx
日期: 2019-03-14
阵名: NE十五炮
出处: https://tieba.baidu.com/p/1067040250
节奏: C8u: IPP-PP|PADC|PPDD|IPP-PP|NDC|PPDD, (13|6|6|13|6|6)
视频:
- https://www.bilibili.com/video/av41128772
- https://www.youtube.com/watch?v=QltplZCAuoI
"""

from pvz import *


@RunningInThread
def DianCai():
    Card("小喷", (4, 9))
    Card("阳光", (5, 9))
    Delay(120)
    Shovel((4, 9))
    Shovel((5, 9))


# EnableLogger(False)  # 输出调试信息
# SetWindowTopMost(True)  # 窗口置顶

# BackgroundRunning(True)  # 允许后台运行
# ZombieNoFalling(True)  # 僵尸死后不掉钱

# SetSun(8000)  # 阳光 8000
# SetMoney(0)  # 金钱 0
# JumpLevel(1009)  # 完成 2018 面旗帜数

SetZombies(["普僵", "撑杆", "舞王", "小丑", "气球", "矿工", "跳跳", "蹦极", "扶梯", "篮球", "白眼", "红眼"])

Sleep(200)

SelectCards(["复制冰", "原版冰", "核蘑菇", "樱桃", "倭瓜", "墓碑", "南瓜", "三叶草", "阳光菇", "小喷菇"])

UpdatePaoList([
    (1, 1), (2, 1), (3, 1), (4, 1), (5, 1),
    (1, 5), (2, 5), (3, 5), (4, 5), (5, 5),
    (1, 7), (2, 7), (3, 7), (4, 7), (5, 7),
    ])

StartAutoCollectThread()


for wave in range(1, 21):
    print("当前操作波次: " + str(wave))

    # PPD
    if wave in (10,):
        Prejudge(-200, wave)
        Until(-55)
        Pao((2, 9), (4, 9))
        Until(0)
        Pao((2, 9))

    # IPP-PP
    elif wave in (1, 7, 11, 17):
        Prejudge(-200, wave)
        Until(-150)
        Pao((2, 8.5), (4, 8.5))
        Until(5 - 100)
        Card("寒冰菇", (1, 9))
        if wave == 11:
            Until(-150 + 81)
            DianCai()
        Until(1300 - 200 - 373)
        Pao((2, 9), (4, 9))

    # PADC
    elif wave in (2, 8, 12, 18):
        Prejudge(-200, wave)
        Until(-95)
        Pao((2, 9))
        Until(-12)
        Pao((2, 9))
        Until(-95 + 373 - 100)
        Card("樱桃", (5, 9))

    # PPDD
    elif wave in (3, 9, 13, 19):
        Prejudge(-200, wave)
        Until(-95)
        Pao((2, 9), (5, 9))
        Until(-15)
        Pao((1, 9), (4, 9))
        Until(0)
        DianCai()
        Until(601 + 44 - 100 - 320)  # 44cs 预判冰
        Card("模仿者寒冰菇", (1, 9))

        if wave in (9, 19):
            Until(601 - 150)
            Pao((4, 9))
            Delay(450)
            Pao((1, 9))
            Until(601 + 1300 - 200 - 373)
            Delay(300)
            Pao((2, 9), (5, 9))

    # IPP-PP
    elif wave in (4, 14):
        Prejudge(-200, wave)
        Until(-150)
        Pao((2, 8.5), (4, 8.5))
        Until(1300 - 200 - 373)
        Pao((2, 9), (4, 9))

    # NDC
    elif wave in (5, 15):
        Prejudge(-200, wave)
        Until(-12)
        Pao((2, 9))
        Until(-95 + 373 - 100)
        Card("核蘑菇", (3, 9) if wave == 5 else (2, 9))

    # PPDD
    elif wave in (6, 16):
        Prejudge(-200, wave)
        Until(-95)
        Pao((2, 9), (5, 9))
        Until(-12)
        Pao((1, 9), (4, 9))
        Until(0)
        DianCai()

    elif wave == 20:
        Prejudge(-200, wave)
        Until(-55)
        Pao((1, 9), (4, 9))
        Until(-35)
        Pao((2, 9), (5, 9))  # 炸墓碑冒出的僵尸
        Until(601 - 100 - 81)
        Pao((1, 8.3), (4, 8.3))
        Until(601 - 100)
        # 冰杀小偷
        with MouseLock():
            SafeClick()
            ClickSeed("寒冰菇")
            ClickGrid((1, 9))
            ClickGrid((2, 9))
            ClickGrid((3, 9))
            ClickGrid((4, 9))
            ClickGrid((5, 9))
            SafeClick()
        Delay(100)
        Pao((2, 8.2), (5, 8.2))
        print(f"第 {wave} 波手动收尾.")

```

## RE十六炮

![RE十六炮](/images/build/RE十六炮.jpg)

```python
# coding=utf-8

"""
作者: lmintlcx
日期: 2019-03-14
阵名: RE十六炮
出处: https://tieba.baidu.com/p/1410367512
节奏: ch6: PSD/P|IP-PPD|PSD/P|IP-PPD, (6|12|6|12)
视频:
- https://www.bilibili.com/video/av38407808
- https://www.youtube.com/watch?v=g1xNVLRDyKo
"""

from pvz import *

# EnableLogger(False)  # 输出调试信息
# SetWindowTopMost(True)  # 窗口置顶

# BackgroundRunning(True)  # 允许后台运行
# ZombieNoFalling(True)  # 僵尸死后不掉钱

# SetSun(8000)  # 阳光 8000
# SetMoney(0)  # 金钱 0
# JumpLevel(1009)  # 完成 2018 面旗帜数

SetZombies(["普僵", "撑杆", "橄榄", "冰车", "小丑", "气球", "跳跳", "蹦极", "扶梯", "篮球", "白眼", "红眼"])

Sleep(200)

SelectCards(["玉米", "玉米炮", "樱桃", "倭瓜", "坚果", "核蘑菇", "冰蘑菇", "模仿者寒冰菇", "咖啡豆", "花盆"])

UpdatePaoList(
    [
        (1, 3),  # P
        (1, 5),  # S
        (1, 7),  #    P
        (1, 1),  # D
        (2, 3),  # P
        (2, 5),  # P
        (2, 7),  #    P
        (2, 1),  # D
        (3, 3),  # P
        (3, 5),  # S
        (3, 7),  #    P
        (3, 1),  # D
        (4, 6),  # P
        (4, 1),  # P
        (5, 6),  #    P
        (5, 1),  # D
    ]
)

StartAutoFillIceThread([(5, 3), (4, 3)], 11)
StartAutoCollectThread()


for wave in range(1, 21):
    print("当前操作波次: " + str(wave))

    # PPSD
    if wave in (1, 3, 5, 7, 9, 10, 12, 14, 16, 18):
        Prejudge(-10, wave)  # -10+373 < 370
        RoofPao((2, 9), (2, 9), (4, 9))
        Delay(110)  # 110 拦截
        RoofPao((2, 8.8))
        Until(601 + 50 - 298)  # 50cs 预判冰
        Coffee()
        if wave == 9:
            Until(601 - 150)
            RoofPao((2, 9))
            Until(601 + 1200 - 200 - 373)
            RoofPao((5, 9), (5, 9))
            Delay(1100)  # 等会儿
            RoofPao((5, 9))

    # IP-PPD
    elif wave in (2, 4, 6, 8, 11, 13, 15, 17, 19):
        Prejudge(-150, wave)
        RoofPao((2, 9))
        Until(1200 - 200 - 373)  # 1200cs 波长
        RoofPao((2, 9), (4, 9))  # 激活炸
        Delay(220)  # 220 拦截
        RoofPao((2, 7.8))
        if wave == 19:
            Until(1200 - 10)
            RoofPao((2, 9), (2, 9), (4, 9))
            Delay(110)  # 110 拦截
            RoofPao((2, 8.8))
            Until(1200 + 601 - 150)
            RoofPao((5, 9))
            Until(1200 + 601 + 1200 - 200 - 373)
            Delay(50)  # 等会儿
            RoofPao((5, 9))

    elif wave == 20:
        Prejudge(-200, wave)
        Coffee()  # 冰消空降
        Until(-100)
        RoofPao((2, 9), (5, 9))  # 炸冰车
        Until(50)
        RoofPao((4, 2.5), (4, 6.7))  # 炸小偷
        Until(800)
        RoofPao((2, 9), (2, 9), (2, 9), (2, 9))
        Until(1000)
        RoofPao((4, 9), (4, 9), (4, 9), (4, 9))
        print(f"第 {wave} 波手动收尾.")

```

## RE椭盘十四炮

![RE椭盘十四炮](/images/build/RE椭盘十四炮.jpg)

```python
# coding=utf-8

"""
作者: lmintlcx, 冰巫师墨舞
日期: 2019-03-14
阵名: RE椭盘十四炮
出处: https://tieba.baidu.com/p/5029428684
节奏: ch4-35.6s: ICE3+PPDD+P-PP|ICE3+PPDD+P-PP, (17.8|17.8)
视频:
- https://www.bilibili.com/video/av38408382
- https://www.youtube.com/watch?v=KoFX0SIMzWk
"""

from pvz import *

# EnableLogger(False)  # 输出调试信息
# SetWindowTopMost(True)  # 窗口置顶

# BackgroundRunning(True)  # 允许后台运行
# ZombieNoFalling(True)  # 僵尸死后不掉钱

# SetSun(8000)  # 阳光 8000
# SetMoney(0)  # 金钱 0
# JumpLevel(1009)  # 完成 2018 面旗帜数

SetZombies(["普僵", "撑杆", "橄榄", "冰车", "小丑", "气球", "跳跳", "蹦极", "扶梯", "篮球", "白眼", "红眼"])

Sleep(200)

SelectCards(["花盆", "寒冰菇", "模仿者寒冰菇", "毁灭菇", "咖啡豆", "樱桃炸弹", "火爆辣椒", "倭瓜", "寒冰射手", "坚果墙"])

UpdatePaoList(
    [
        (4, 2),  # P
        (4, 4),  # P
        (1, 4),  # D
        (5, 4),  # D
        (5, 6),  # s
        (3, 1),  # P
        (4, 7),  # P
        ###
        (1, 2),  # P
        (2, 4),  # P
        (3, 3),  # D
        (3, 5),  # D
        (2, 6),  # s
        (2, 1),  # P
        (3, 7),  # P
    ]
)

# IPPDDP-PP IPPDDP-PP  14
# PPDDDD    IP-PP      9
# PPSSDD    IAA'aP-PP  9
SkipPao(5)  # 调整炮序


# while GameUI() != 3:
#     Sleep(1)
# while GamePaused():
#     Sleep(1)
Card("花盆", (1, 7))
Card("寒冰菇", (1, 7))
StartAutoCollectThread([1, 2, 3, 4, 5, 6, 17], 15)
StartAutoFillIceThread([(4, 6), (2, 3), (1, 1), (1, 6)], 18 - 1)


for wave in range(1, 21):
    print("当前操作波次: " + str(wave))

    if wave in (1,):
        Prejudge(-200, wave)
        Until(380 - 373)
        RoofPao((2, 8.8), (4, 8.8))
        Until(510 - 373)
        RoofPao((2, 8.8), (4, 8.8))
        Until(601 + 36 - 373)
        RoofPao((2, 8.8), (4, 8.8))
        Until(601 + 36 - 298)
        Card("咖啡豆", (1, 7))  # Coffee()

    elif wave in (2,):
        Prejudge(-200, wave)
        Until(50)
        Shovel((1, 7))  # 铲
        Until(1300 - 200 - 373)  # 727
        RoofPao((4, 8.1))
        Until(1780 - 200 - 373)  # 1207
        RoofPao((2, 9), (4, 9))
        Until(1780 + 10 - 298)  # 1492
        Coffee()

    elif wave in (10,):
        Prejudge(-15, wave)
        RoofPao((2, 9), (4, 9), (2, 9), (4, 9))
        Until(-15 + 110)  # 95
        RoofPao((4, 7.7))  # 空炸小鬼兼小偷
        Until(-15 + 190)  # 175
        RoofPao((1, 5))  # 2-5? 尾炸小鬼兼小偷
        Until(601 + 10 - 298)  # 313
        Coffee()

    elif wave in (11,):
        Prejudge(-200, wave)
        Until(10 + 400 - 100)
        Card("辣椒", (1, 7))
        Card("花盆", (4, 9))
        Card("樱桃", (4, 9))
        Until(10 + 400 + 10)
        Shovel((1, 7))  # 铲
        Shovel((4, 9))  # 铲
        Until(1250 - 200 - 373)  # 1300->1250
        RoofPao((3, 8.15))  # 落点改为 3 路炸掉 2 路冰车
        Until(1780 - 200 - 373)
        RoofPao((2, 9), (4, 9))
        Until(1780 + 10 - 298)
        Coffee()

    elif wave in (3, 12):
        Prejudge(-200, wave)
        Until(10 + 400 - 373)
        RoofPao((2, 9), (4, 9))
        Until(10 + 400 - 373 + 220)
        RoofPao((4, 8.5))  # 空炸
        Until(10 + 400 - 373 + 300)
        RoofPao((2, 4.7))  # 尾炸小鬼跳跳
        Until(1300 - 200 - 373)
        RoofPao((4, 8.1))
        Until(1780 - 200 - 373)
        RoofPao((2, 9), (4, 9))
        Until(1780 + 10 - 298)
        Coffee()

    elif wave in (9, 19):
        Prejudge(-200, wave)
        Until(10 + 400 - 373)
        RoofPao((2, 9), (4, 9))
        Until(10 + 400 - 373 + 220)
        RoofPao((2, 8.5), (4, 8.5))
        Until(1300 - 200 - 373)  # 727
        RoofPao((3, 8.15))  # 落点改为 3 路减少小丑炸核机率
        # 收尾
        Until(1680 - 200 - 298)  # 1182
        Card("花盆", (3, 9))
        Card("核蘑菇", (3, 9))
        Card("咖啡豆", (3, 9))
        Until(1680 - 200 + 230 - 373)
        RoofPao((2, 8.5), (4, 8.5))  # 拦截
        Until(1680 - 200 + 230 + 230 - 373)
        RoofPao((2, 8.5), (4, 8.5))  # 拦截
        Until(1680 - 200 + 230 + 230 + 230 - 373)
        RoofPao((3, 9), (5, 9))  # 留下 1 路
        Delay(50)
        Card("寒冰射手", (1, 6))
        # 清场
        if wave == 9:
            SkipPao(7 - 4 - 1 + 5)  # 调整炮序
            Until(2700)
            Card("花盆", (1, 8))  # 垫一下
            Until(4500 - 200 - 373)  # Until(4500 - 5)  # 出红字时
            Delay(400)  # 等那一门炮
            RoofPao((1, 8))  # 清场
            Until(4500 - 200 + 100)
            Shovel((1, 6))  # 铲掉冰豆
            Until(4500 - 5 + 750 - 599)  # 第 10 波刷新前 599
            Card("花盆", (1, 7))
        else:  # 19
            Until(4500 - 200 - 373)
            RoofPao((1, 8))  # 清场
            Delay(200)
            Shovel((1, 6))  # 铲掉冰豆

    elif wave in (20,):
        Prejudge(50 - 298, wave)
        Coffee()  # 冰消空降
        Until(-150)
        RoofPao((4, 9))  # 炸 3/4 路冰车
        Until(75)
        RoofPao((1, 6), (2, 3), (4, 6))  # 炸小偷
        Until(1250 - 200 - 373)
        RoofPao((1, 9), (2, 9), (4, 9), (5, 9))
        Until(1250 - 200 - 373 + 220)
        RoofPao((1, 9), (2, 9), (4, 9), (5, 9))
        # 收尾
        print(f"第 {wave} 波手动收尾.")
        # Delay(900)
        # while not TryPao((4, 9)):
        #     Delay(10)
        # Delay(100)
        # while not TryPao((3, 9)):
        #     Delay(10)
        # Card("花盆", (1, 7))
        # Card("坚果", (1, 7))
        # Until(5500)
        # Card("倭瓜", (1, 6))
        # Until(5600)
        # Shovel((1, 7))
        # Shovel((1, 7))

    else:  # wave in (4, 5, 6, 7, 8, 13, 14, 15, 16, 17, 18):
        WL = 1950 if wave in (8, 18) else 1780  # 收尾波前一波延长波长
        Prejudge(-200, wave)
        Until(10 + 400 - 373)
        RoofPao((2, 9), (4, 9))
        Until(10 + 400 - 373 + 220)
        RoofPao((2, 8.5), (4, 8.5))
        Until(1300 - 200 - 373)
        RoofPao((4, 8.1))
        Until(WL - 200 - 373)  # WL-573
        RoofPao((2, 9), (4, 9))
        if wave in (8, 18):
            Until(WL - 200 - 373 + 81)  # WL-492
            Card("花盆", (2, 8))  # 垫 2 路梯子
        Until(WL + 10 - 298)  # WL-288
        Coffee()
        if wave in (8, 18):
            Until(WL - 200)  # WL-200
            Shovel((2, 8))  # 炮落地铲

```

## ME十三炮

![ME十三炮](/images/build/ME十三炮.jpg)

```python
# coding=utf-8

"""
作者: lmintlcx
日期: 2019-03-14
阵名: ME十三炮
出处: https://tieba.baidu.com/p/5288033944
节奏: C5u-35s: PPD|PPD|PPD|IP-PPD, (6|6|6|17)
视频:
- https://www.bilibili.com/video/av38407390
- https://www.youtube.com/watch?v=jUjvLI_bUqM
"""

from pvz import *


@RunningInThread
def I():
    Card("花盆", (3, 7))
    Card("寒冰菇", (3, 7))
    Delay(100 + 1)
    Shovel((3, 7))


@RunningInThread
def II():
    Card("花盆", (3, 7))
    Card("复制冰", (3, 7))
    Delay(320 + 100 + 1)
    Shovel((3, 7))


###


# EnableLogger(False)  # 输出调试信息
# SetWindowTopMost(True)  # 窗口置顶

# BackgroundRunning(True)  # 允许后台运行
# ZombieNoFalling(True)  # 僵尸死后不掉钱

# SetSun(8000)  # 阳光 8000
# SetMoney(0)  # 金钱 0
# JumpLevel(1009)  # 完成 2018 面旗帜数

SetZombies(["普僵", "撑杆", "橄榄", "冰车", "小丑", "气球", "跳跳", "蹦极", "扶梯", "篮球", "白眼", "红眼"])

Sleep(200)

SelectCards(["玉米", "玉米炮", "三叶草", "保护伞", "樱桃", "倭瓜", "坚果", "花盆", "寒冰菇", "复制冰"])

UpdatePaoList([(1, 3), (1, 5), (1, 1), (2, 3), (2, 5), (2, 1), (3, 3), (3, 5), (3, 1), (4, 6), (4, 1), (5, 6), (5, 1)])

StartAutoCollectThread()

for wave in range(1, 21):
    print("当前操作波次: " + str(wave))

    if wave in (20,):
        Prejudge(10 - 320, wave)
        II()  # 冰消空降
        Until(100)
        TryPao((5, 8))  # 收尾了就随意选炮吧
        Until(800)
        TryPao((2, 9), (2, 9), (2, 9), (2, 9))
        Until(1000)
        TryPao((4, 9), (4, 9), (4, 9), (4, 9))
        print(f"第 {wave} 波手动收尾.")

    # IP-PPD
    elif wave in (4, 8, 10, 14, 18):
        Prejudge(-200, wave)
        if wave in (4, 10, 18):  # 本波原版冰
            Until(5 - 100)
            I()
        Until(100)
        RoofPao((5, 8))
        Until(1700 - 200 - 373)
        RoofPao((2, 8.5), (4, 8.5))
        Delay(230)  # Until(1700 - 200 - 373 + 230)  # 减速延迟 230 炸小鬼
        RoofPao((2, 7))

    # PPD
    else:  # elif wave in (1, 2, 3, 5, 6, 7, 9, 11, 12, 13, 15, 16, 17, 19):
        Prejudge(10, wave)  # 刷新后
        RoofPao((2, 8.5), (4, 8.5))
        Delay(130)  # Until(10 + 130)  # 原速延迟 130 炸小鬼
        RoofPao((2, 7.7))
        if wave in (7, 13):  # 下一波的复制冰
            Until(601 + 5 - 100 - 320)
            II()
        if wave in (9, 19):  # 收尾
            Until(601)
            RoofPao((2, 8.5), (4, 8.5))
            Delay(130)
            RoofPao((2, 7.5))
            # 自动操作收尾
            Until(601 + 601)
            RoofPao((2, 8.5))
            Delay(300)
            RoofPao((5, 8))
            Delay(500)
            RoofPao((5, 8))

```

## FE花环十六炮

![FE花环十六炮](/images/build/FE花环十六炮.jpg)

```python
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

```

## FE二十二炮

![FE二十二炮](/images/build/FE二十二炮.jpg)

```python
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


## 下面正式开始


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

```
