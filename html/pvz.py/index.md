
# 脚本框架

## 项目简介

**`pip install pvz==3.3.3`**

蟒蛇大战僵尸(Python vs. Zombies)是一个以 Python 语言写成的用于植物大战僵尸键控(脚本操控)的框架, 本项目可以免去配置构建半自动化脚本所需基础框架的繁重工作, 用户无需了解其中的实现细节和复杂逻辑, 只要使用暴露出来的接口函数即可, 从而可以将精力集中在轨道主流程处理上, 有效快速地完成脚本编写和视频制作.

本项目只能在 Windows 7 SP1 以及更高版本上面使用, 目前支持的 Python 版本 >= 3.5, 只支持植物大战僵尸原版 1.0.0.1051 版本(英文原版和汉化二版), 如有问题报告或者功能需求可通过 [GitHub](https://github.com/lmintlcx/pvzscripts) / [邮件](mailto:lmintlcx@gmail.com) / [QQ群](https://jq.qq.com/?_wv=1027&k=5Q6zrTD) 联系作者.

## 编程语言

本项目依赖于 Python3, \>\>\> [点击下载](https://www.python.org/downloads/) <<<.

根据自己的操作系统位数选择合适的版本, 32 位选择"x86", 64 位选择"x86-64""AMD64".

如果不清楚自己的操作系统位数就选择 32 位的安装包.

![Python 版本选择](/images/python/版本选择.png)

勾选 "添加到环境变量" "安装包管理器" 以及 "为所有用户安装".

![Python 添加到环境变量](/images/python/安装_环境变量.jpg)

![Python 安装包管理器](/images/python/安装_包管理器.jpg)

![Python 为所有用户安装](/images/python/安装_所有用户.jpg)

打开命令提示符运行`python --version`检查是否安装成功.

![Python 检查安装是否成功](/images/python/检查py安装是否成功.png)

Windows 版本的 Python 可执行程序使用 Visual C++ 编译, 需要 vc 运行库的支持, \>\>\> [点击下载](https://support.microsoft.com/zh-cn/help/2977003/the-latest-supported-visual-c-downloads/) <<<.

脚本运行方法: (假设文件名为 `xxx.py`)

- 用专业的文本编辑器/集成开发环境点击菜单调试运行. (推荐)

- 如果启用了文件关联, 直接双击脚本文件即可运行.

- 打开"命令提示符", 切换到脚本所在目录, 运行`python xxx.py`.

可以直接在脚本所在目录按住"Shift"并右键选择"在此处打开命令窗口".

对于便携版/多版本共存/其他解释器的用户, 使用绝对路径来运行指定的 Python 解释器.

**正常情况下在命令界面按 `Ctrl + C` 即可结束脚本运行, 如果无法终止则去任务管理器里找到对应的 Python.exe 进程杀掉.**

推荐几个在线教程网站:

- [Python 菜鸟教程](http://www.runoob.com/python3/python3-tutorial.html)
- [Python 廖雪峰](https://www.liaoxuefeng.com/wiki/0014316089557264a6b348958f449949df42a6d3a2e542c000)
- [Python 入门指南](http://www.pythondoc.com/pythontutorial3/)
- [Python Cookbook](https://python3-cookbook.readthedocs.io/zh_CN/latest/)

需要学习了解的内容主要包括:

- 文件编码(utf-8)
- 注释格式(单行/多行)
- 代码块的缩进层级与空行
- 调试输出(print函数)
- 导入模块(import语句)
- 变量及其作用域(global语句)
- 数据类型(数字/字符串/列表/元组)
- 运算符(算术/比较/赋值/逻辑/成员)
- 流程控制(if语句/for语句/range函数)
- 函数的定义与调用(默认/关键字/可变参数)

## 脚本框架

在命令提示符下运行 `pip install pvz` 来安装本框架.

运行 `pip list` 来检查已安装的包, 若显示有 pvz 则安装成功.

![Python 检查安装是否成功](/images/python/检查pvz安装是否成功.png)

脚本框架可能会有后续更新, 可通过运行 `pip install --upgrade pvz` 进行升级.

## 文本编辑

编写代码最好是用专业的文本编辑器.

[Notepad++](https://notepad-plus-plus.org/download/) 免费小巧

[Sublime Text 3](https://www.sublimetext.com/3) 轻量快速, 收费软件

[Visual Studio Code](https://code.visualstudio.com/Download) 功能丰富, 墙裂推荐

[Vim](https://www.vim.org/download.php) 编辑器之神, 过于专业不推荐

[Emacs](http://www.gnu.org/software/emacs/download.html) 神之编辑器, 过于专业不推荐

[PyCharm](http://www.jetbrains.com/pycharm/download/) 成熟好用, Python 专用, 社区版免费

[Visual Studio 2017](https://visualstudio.microsoft.com/zh-hans/downloads/) 宇宙最强 IDE, 过于庞大不推荐

由于某些原因 **不建议用记事本!!!**

这里墙裂推荐 \>\>\> [Visual Studio Code](https://code.visualstudio.com/Download) <<<, 安装后在 "拓展" 页面搜索 "Chinese" 中文语言包.

## 最佳实践

声明文字编码为 UTF-8, 尤其是在内容包括汉字的时候.

注意这里只是声明, 文本编辑器保存文件的时候也需要采用该编码.

```python
# coding=utf-8
```

导入本项目的基础函数. (三种方式任选其一即可)

```python
# 方式 1
# 调用时需要加上 pvz. 前缀
import pvz
# pvz.Pao((2, 9), (5, 9))
# pvz.Card("小喷", (3, 9))

# 方式 2
# 推荐, 本教程示例均用此种方式
from pvz import *
# Pao((2, 9), (5, 9))
# Card("小喷", (3, 9))

# 方式 3
# 只导入需要的内容, 可给函数取别名
from pvz import Countdown
from pvz import Sleep
from pvz import Pao as 发炮
from pvz import Card as 用卡
# 发炮((2, 9), (5, 9))
# 用卡("小喷", (3, 9))
```

按需求把一些用卡用炮操作封装成函数: (可选, 非必须, 可以在逐波具体操作中直接调用 `Card` 和 `Pao`.)

```python
# 在某行某列释放樱桃
def A(row, col):
    Card("樱桃", (row, col))

# 在水路某行某列释放核蘑菇
def N(row, col):
    Card("睡莲", (row, col))
    Card("核蘑菇", (row, col))
    Card("咖啡豆", (row, col))

# 在某行某列释放原版冰
def I(row, col):
    Card("原版冰", (row, col))

# 在某行某列释放复制冰
def II(row, col):
    Card("复制冰", (row, col))

# 存冰函数在子线程里运行
# 开场后立即运行
# 存冰位 3-1 3-2 3-3 3-4
# 优先存复制冰, 优先存在永久位
# 每 50.1s 存两个冰, 共 10 个
@RunningInThread
def StoreIce():
    ice_spots = [(3, 1), (3, 2), (3, 3), (3, 4)]
    Countdown(599)
    for i in range(5):
        MouseLock().acquire()
        SafeClick()
        ClickSeed("复制冰")
        for spot in ice_spots:
            ClickGrid(spot)
        SafeClick()
        ClickSeed("原版冰")
        for spot in ice_spots:
            ClickGrid(spot)
        SafeClick()
        MouseLock().release()
        if i != (5 - 1):
            Delay(5000 + 1)

# 点冰
def UseIce():
    ice_spots = [(3, 1), (3, 2), (3, 3), (3, 4)]
    MouseLock().acquire()
    SafeClick()
    ClickSeed("咖啡豆")
    for spot in reversed(ice_spots):
        ClickGrid(spot)
    SafeClick()
    MouseLock().release()

# 种垫材后铲除
# 在子线程里运行
@RunningInThread
def DianCai():
    Card("阳光菇", (5, 9))
    Card("小喷菇", (6, 9))
    Delay(30)
    Shovel((5, 9))
    Shovel((6, 9))

# 吹 10 次风扇
# 在子线程里运行
@RunningInThread
def BloverThread():
    for _ in range(10):
        Card("三叶草", (1, 1))
        Delay(2700)

# 吃墓碑
def EatGrave():
    with MouseLock()：
        SafeClick()
        ClickSeed("墓碑吞噬者")
        for r in range(1, 6):  # 1~5 路
            for c in range(5, 10):  # 5~9 列
                ClickGrid(r, c)
        SafeClick()

# 非旗帜波双边 PSD
def PPSSDD():
    Until(-95)
    Pao((2, 9), (5, 9), (2, 9), (5, 9))
    Delay(110)
    Pao((1, 8.8), (5, 8.8))

# 炮数足够的情况下最后一波收尾
# 点炮后延迟 30cs 炸珊瑚
def wave20():
    Prejudge(150 - 30, 20)
    Pao((4, 7), 30)
    Until(-60)
    Pao((1, 9), (2, 9), (5, 9), (6, 9))
    Delay(108)
    Pao((1, 9), (2, 9), (5, 9), (6, 9))
```

启用一些常用的修改器功能, 比如 后台运行/修改阳光/僵尸不掉钱/清除浓雾/修改出怪 等等.

```python
EnableLogger(False)  # 输出调试信息
SetWindowTopMost(True)  # 窗口置顶

BackgroundRunning(True)  # 允许后台运行
ZombieNoFalling(True)  # 僵尸死后不掉钱
ClearFog(True)  # 清除浓雾

SetSun(8000)  # 阳光 8000
SetMoney(0)  # 金钱 0
JumpLevel(int(2018/2))  # 完成 2018 面旗帜数

SetZombies(["普僵", "撑杆", "舞王", "冰车", "海豚", "矿工", "跳跳", "蹦极", "扶梯", "篮球", "白眼", "红眼"])
```

等待 2 秒钟(启动脚本后给开录像预留时间), 选卡并点击"Let's Rock!".

```python
Sleep(200)

SelectCards(["复制冰", "寒冰菇", "咖啡豆", "樱桃", "坚果", "倭瓜", "花盆", "胆小", "阳光", "小喷"])
```

启动 自动收集/自动存冰 等线程.

```python
# 收集钻石和阳光, 间隔 0.15s
StartAutoCollectThread([3, 4, 5, 6], 15)

# 往 6-1 5-1 2-1 1-1 累计存 8 个寒冰菇
StartAutoFillIceThread([(6, 1), (5, 1), (2, 1), (1, 1)], 8)
```

正式编写具体操作.

如果有相当多的波次操作完全相同, 可以用一个循环变量 `wave` 遍历 1~20, 对应每次选卡共 20 波僵尸的处理, 把相同操作的波次写在同一个分支里.

```python
for wave in range(1, 21):
    if wave == 10:
        # 第 10 波操作
        pass
    elif wave == 20:
        # 第 20 波操作
        pass
    elif wave in (1, 3, 5, 7, 9, 12, 14, 16, 18):
        # 第 1/3/5/7/9/12/14/16/18 波操作
        pass
    else:
        # 剩余波次操作
        pass
```

不同波次操作几乎都不相同的情况下, 可以逐波写出来. 以下两种推荐写法:

第一种: 直接将每一波的操作逐波写出, 参考示例 FE花环十六炮.

```python
# 第 1 波
Prejudge(-100, 1)
pass

# 第 2 波
Prejudge(-100, 2)
pass

# 第 3 波
Prejudge(-100, 3)
pass

# ...
# ...
# ...

# 第 20 波
Prejudge(-150, 20)
pass
```

第二种: 给每一波的操作定义一个函数, 相同操作的波次可以合并, 参考示例 FE双冰二十二炮.

注意, 这种写法函数定义内部不能包含 `Prejudge` 只能用 `Until`. 需要在每一波函数实际调用之前调用 `Prejudge`.

```python
# 第 1 波
def wave1():
    pass

# 第 2 波
def wave2():
    pass

# 第 3 波, 操作同第 1 波
def wave3():
    wave1()

# ...
# ...
# ...

# 第 20 波
def wave20():
    pass

Prejudge(-200, 1)
wave1()
Prejudge(-200, 2)
wave2()
Prejudge(-200, 3)
wave3()
# ...
Prejudge(-200, 20)
wave20()
```

对于每一波的处理分为几个部分: 设定预判时间, 执行主要操作, 延时到本波刷新以后(使用`Prejudge`函数时可省略, 以及注意不要超过下一波的预判时间).

常用预判时间 95cs, 早于 149cs 可能炸不全巨人. 第 10 波部分僵尸出生点偏右, 为避免刷怪延迟因此推迟到 55cs, 再晚可能伴舞会出土, 同时可加上樱核补运算量. 第 20 波预判 150cs 可炮炸珊瑚.

第 9/19 波执行完主要操作后可能还需要额外用炮收尾, 所以要在对应波次的地方跳过一定数量的炮数, 使第 10/20 波自动选择的炮位相应地延后. 当然也可以算好时间写好脚本操作自动收尾.

第 20 波视情况炮炸珊瑚/冰消珊瑚/冰杀小偷/炮炸小偷, 然后手动/脚本收尾.

以泳池场地第 3 波预判 100cs 延迟 85cs 的双边 PD 为例, 以下几种写法均可:

```python
# 1
Countdown(100)
Pao((2, 9))
Pao((5, 9))
Sleep(85)
Pao((2, 9))
Pao((5, 9))
Sleep(15 + 1)

# 2
Countdown(100, 3 % 10 == 0)
Pao((2, 9), (5, 9))
Delay(85)
Pao((2, 9), (5, 9))
Delay(15)

# 3
Prejudge(-100, 3)
Pao((2, 9), (5, 9))
Delay(85)
Pao((2, 9), (5, 9))

# 4
Prejudge(-200, 3)
Until(-100)
Pao([(2, 9), (5, 9)])
Until(-100 + 85)
Pao([(2, 9), (5, 9)])

# 5
# 推荐
Prejudge(-200, 3)
Until(-100)
Pao((2, 9), (5, 9))
Delay(85)
Pao((2, 9), (5, 9))

# 6
# 推荐
def wave3():
    Until(-100)
    Pao((2, 9), (5, 9))
    Until(-100 + 85)
    Pao((2, 9), (5, 9))
Prejudge(-200, 3)
wave3()
```

## 常见问题

### `Countdown` 和 `Prejudge` 的区别

`Countdown` 阻塞到刷新倒计时数值达到指定值, 需要用户保证设定波次的上一波操作运行到上一波刷新之后再进行本波预判. 只能在设定波次刷新前调用. 该函数仅保留兼容传统写法, 已不推荐使用.

`Prejudge` 参数为相对于本波刷新时间点的相对时间, 用于预判则为负值. 每波在且仅在最开始调用一次, 可自动判断设定波次的上一波有没有刷出. 该函数既可在设定波次刷新前调用也可在刷新后调用.

### `Sleep` 和 `Delay` 的区别

`Sleep` 借助于操作系统实现延时, 由于 Windows 不是实时操作系统所以实际睡眠时间会有波动.

`Delay` 靠读取游戏内部时钟来实现延时, 相比线程睡眠更加精确, 也不用担心游戏中途突然暂停的影响.

### 操作和波次的对应

节奏简式表达的是针对每一波的操作, 理想情况下是把本波的所有操作都写在本波.

然而某些操作离其生效时间较长, 这个时候应该把操作写在上一波. 比如 预判冰点咖啡豆, 预判复制冰 等等.

另外某些操作执行的时候已经到了下一波刷新的时候了, 则写在下一波. 比如 垫撑杆 等等.

### 操作时机计算

`Until` 的参数为 "与本波刷新时间点的差值", 该函数需要配合 `Prejudge` 使用.

刷新前 95: -95.

刷新后 180: 180.

刷新后 360 生效炮发射时机: 360 - 373.

白天点下一波预判冰的咖啡豆时机, (假设为加速波)波长 601, 使冰在下一波刷新后 20 生效, 点下咖啡豆到冰生效 298, 计算可得: 601 + 20 - 298.

夜间种植下一波预判复制冰时机, (假设为减速波)波长 1350, 使冰在下一波刷新后 5 生效, 冰种植到生效 100, 模仿者变身耗时 320, 计算可得: 1350 + 5 - 100 - 320.

减速波激活炸时机, 假设波长为 1200, 从加速运算量生效到下一波刷出 200, 玉米炮飞行时间 373, 计算可得: 1200 - 200 - 373.

白天减速波核蘑菇激活点咖啡时机, 假设波长为 1150, 从加速运算量生效到下一波刷出 200, 核蘑菇被唤醒到生效 100, 咖啡豆种下到完成唤醒 198, 计算可得: 1150 - 200 - 100 - 198.

### 延时函数顺序

多个 `Until` 连用以及与 `Sleep` `Delay` 混用时, 需要注意把对应的操作按时间顺序(参数大小)排列.

在下面的例子中, 本意是在冰波激活炸之后尾炸小鬼再点下一波的预判冰, 由于尾炸延时较长, 执行尾炸发炮操作时已经超过了本应点预判冰的时机, 脚本逻辑出错.

只要把每个时机的具体数字算出来就能发现问题所在了, 将时机(和对应的操作)按照大小顺序排序即可解决.

```python
# 错误示范
# 727 < 1077 < 1022  (✗)
Until(1300 - 200 - 373)  # 727
Pao((2, 8.8), (5, 8.8))  # 冰波激活炸
Delay(350)               # 1077
Pao((1, 2.4), (5, 2.4))  # 减速尾炸
Until(1300 + 20 - 298)   # 1022
Coffee()                 # 20cs 预判冰

# 正确示范
# 727 < 1022 < 1077  (✓)
Until(1300 - 200 - 373)        # 727
Pao((2, 8.8), (5, 8.8))        # 冰波激活炸
Until(1300 + 20 - 298)         # 1022
Coffee()                       # 20cs 预判冰
Until(1300 - 200 - 373 + 350)  # 1077
Pao((1, 2.4), (5, 2.4))        # 减速尾炸
```

### 自动存冰与点冰函数

`Coffee` 需要与 `StartAutoFillIceThread` 配合使用. 为了减少资源占用该函数存冰并不及时, 需要更精确的控制存冰时间可参考 `StoreIce` 和 `UseIce` 示例自己实现存冰和点冰函数.

### 多线程操作

`RunningInThread` 的异步功能是靠开新线程实现的, 建议只在精度要求不高(电脑配置很好)的情况下使用. 注意这并不是一个普通的函数, 而是一个装饰器. 定义一个函数然后用这个装饰器装饰, 该函数在调用的时候会运行在单独的线程当中.

建议把一些与主线程操作关系不大的操作放在子线程里, 比如 自动存冰, 补南瓜, 铲种垫材 等等.

### 玉米炮不能秒射自己

炮落点位于自身附近快速点击无法发射的解决方法:

- 开场不使用脚本自动找炮, 而是用 `UpdatePaoList()` 函数手动调整玉米炮列表顺序.

- 发射单门炮且操作前 30cs 内无其他操作时可提前并设置额外的延时发射参数(主线程后续计算累积延时时要加上此延时).

`Pao((4, 7))` -> `Pao((4, 7), 30)`

- 同时发射两门炮时可临时调整两个落点的顺序.

`Pao((1, 8), (5, 8))` -> `Pao((5, 8), (1, 8))`

### 鼠标锁

众所周知, 鼠标只有一个.

脚本为了方便使用了多线程技术, 为了避免(脚本不同操作之间以及键控与手控之间的)冲突, 在进行不可中断的操作的时候, 需要通过内置唯一鼠标锁获取操作权, 操作完毕后再释放.

本框架封装的高级函数 (`Card` `Shovel` `Pao` `TryPao` `RoofPao` `StartAutoCollectThread` `StartAutoFillIceThread` `Coffee`) 均有使用鼠标锁, 使用的时候无需担心冲突.

但是在使用基础点击函数 (`LeftClick` `RightClick` `ButtonClick` `SafeClick` `ClickSeed` `ClickShovel` `ClickGrid`) 构建自定义操作的时候, 为了脚本的可靠性建议加锁.

### 脚本调试省时

**在调试脚本的时候可以把选卡函数注释掉, 手工选卡进入游戏场景然后退回主界面, 找到存档位置设置存档只读. 这样每次调试的时候是直接从选完卡后开始, 省去重新选卡和切换画面的时间.**

**同样可以在积累了一定工作量(比如上半场前九波完成)之后存个档, 注释掉前面已完成的代码(跳过一定炮数并从第10波开始)再继续之后步骤的编写调试. 等到全部完成后再从选卡阶段录制完整的表演视频.**

**具体操作参考视频 [《脚本大战僵尸》键控教程](https://www.bilibili.com/video/av39561553/).**

举个栗子:

手动选卡, 开场即退出, 设置存档只读, 编写调试前 9 波.

```python
# 这里注释掉了选卡函数
# 从第 1 波开始操作

# SelectCards(cards)
for wave in range(1, 21):
    pass
```

第 10 波刷新前取消存档只读, 退回游戏主菜单, 再次设置存档只读, 跳过一定炮数, 编写调试第 10~19(20) 波.

```python
# 这里注释掉了选卡函数
# 按顺序跳过了一定炮数
# 从第 10 波开始操作

# SelectCards(cards)
SkipPao(x)
for wave in range(10, 21):
    pass
```

待脚本编写完成后用未选完卡的存档重新开始.

```python
# 这里启用了选卡函数
# 从头开始运行完整的操作

SelectCards(cards)
for wave in range(1, 21):
    pass
```
