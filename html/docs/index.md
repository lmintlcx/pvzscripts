
# 接口文档

**以下公开接口函数均采用大驼峰法命名, 对应的内部实现均为下划线法命名并以下划线开头.**

## 调试日志

### `EnableLogger()`

启用日志.

输出调试信息开销较大, 会影响操作精度, 建议调试完成后关闭.

@参数 on(bool): 是否启用, 默认启用.

## 查找游戏读取内存

### `FindPvZ()`

查找原版植物大战僵尸游戏进程.

@返回值 (bool): 查找成功返回 True, 没找到或是版本不符则返回 False.

### `ReadMemory(data_type, *address, array=1)`

读取内存数据.

@参数 data_type(str): 数据类型, 取自 C/C++ 语言关键字, 可选值 ["char", "bool", "unsigned char", "short", "unsigned short", "int", "unsigned int", "long", "unsigned long", "long long", "unsigned long long", "float", "double"]

@参数 address(int): 地址, 可为多级偏移.

@参数 array(int): 数量. 默认一个, 大于一个时需要显式指定关键字参数.

@返回值 (int/float/bool/tuple): 默认情况下返回单个数值, 获取多个数据则返回一个长度为指定数量的元组.

@示例:

```python
ReadMemory("int", 0x6a9ec0, 0x768, 0x5560)
8000
```

```python
ReadMemory("byte", 0x0041d7d0, array=3)
(81, 131, 248)
```

<!--

### `WriteMemory(data_type, values, *address)`

写入内存数据.

@参数 data_type(str): 数据类型, 取自 C/C++ 语言关键字, 可选值 ["char", "bool", "unsigned char", "short", "unsigned short", "int", "unsigned int", "long", "unsigned long", "long long", "unsigned long long", "float", "double"]

@参数 values(int/float/bool/list/tuple): 需要写入的数据, 多个数据采用列表或者元组形式.

@参数 address(int): 地址, 可为多级偏移.

@示例:

```python
WriteMemory("int", 8000, 0x6a9ec0, 0x768, 0x5560)
```

```python
WriteMemory("unsigned char", [0xb0, 0x01, 0xc3], 0x0041d7d0)
```

-->

### `SetWindowTopMost(on=True)`

置顶显示游戏窗口.

@参数 on(bool): 是否开启.

## 模拟鼠标点击

### `LeftClick(x, y)`

鼠标左键单击.

@参数 x(int): 横坐标, 单位像素. 建议范围 [0, 799].

@参数 y(int): 纵坐标, 单位像素. 建议范围 [0, 599].

@示例:

```python
LeftClick(108, 42)  # 左键单击卡槽第一张卡片的位置
```

### `RightClick(x, y)`

鼠标右键单击.

@参数 x(int): 横坐标, 单位像素. 建议范围 [0, 799].

@参数 y(int): 纵坐标, 单位像素. 建议范围 [0, 599].

@示例:

```python
RightClick(399, 299)  # 右键单击场地中间位置
```

### `ButtonClick(x, y)`

适用于模仿者按钮和菜单按钮的特殊点击.

@参数 x(int): 横坐标, 单位像素. 建议范围 [0, 799].

@参数 y(int): 纵坐标, 单位像素. 建议范围 [0, 599].

@示例:

```python
ButtonClick(490, 550)  # 选卡界面点击模仿者卡片
```

```python
ButtonClick(740, 10)  # 点击菜单按钮
```

## 模拟键盘敲击

### `PressEsc()`

敲击 退出 键.

### `PressSpace()`

敲击 空格 键.

### `PressEnter()`

敲击 回车 键.

### `PressKeys(keys)`

敲击一系列按键.

@参数 keys(str): 按键字符串, 由 '0' - '9' 'A' - 'Z' 组成.

@示例:

```python
PressKeys("FUTURE")  # 智慧树指令, 使僵尸带上眼镜
```

### `PauseGame()`

暂停游戏.

### `RestoreGame()`

恢复游戏.

## 延时机制

### `Sleep(time_cs)`

线程睡眠. 实际睡眠时间依赖于操作系统线程切换时间片精度.

@参数 time_cs(float): 时间, 单位 cs, 精度 0.1.

### `Delay(time_cs)`

游戏内部时钟延时. 相对于线程睡眠更精确.

只能在战斗界面 `[[0x6A9EC0]+0x7FC] == 3` 使用. 游戏暂停时计时同样暂停.

@参数 time_cs(int): 时间, 单位 cs, 精度 1.

### `Countdown(time_cs, hugewave=False)`

等待直至刷新倒计时数值达到指定值.

调用时需要保证上一波已经刷出. 该函数仅保留兼容旧式写法, 已不推荐使用.

@参数 time_cs(int): 倒计时数值, 单位 cs, 精度 1. 建议范围 [200, 1].

第一波最早 599, 旗帜波最早 750.

@参数 hugewave(bool): 是否为旗帜波, 默认不是. 可用 (波数 % 10 == 0) 判断.

@示例:

```python
Countdown(100)  # 非旗帜波 100cs 预判
```

```python
Countdown(55, True)  # 旗帜波 55cs 预判
```

```python
Countdown(95, wave % 10 == 0)  # 第 wave 波 95cs 预判
```

### `Prejudge(time_relative_cs, wave)`

读内存获取刷新状况, 等待直至与设定波次刷新时间点的差值达到指定值.

该函数须在每波操作开始时执行一次. 通常用于预判(在设定波次刷新前调用), 也可以在设定波次刷新之后调用.

@参数 time_relative_cs(int): 与刷新时间点的相对时间, 单位 cs, 精度 1. 建议范围 [-200, 400].

第一波最早 -599, 旗帜波最早 -750. 为了方便可统一给每波设置 -200 (此时不会检查参数合理性).

@参数 wave(int): 波数. 用于判断刷新状况以及本波是否为旗帜波.

@示例:

```python
Prejudge(-95, wave)  # 95cs 预判
```

```python
Prejudge(-150, 20)  # 第 20 波炮炸珊瑚时机
```

```python
Prejudge(900 - 200 - 373, wave)  # 900cs 波长反应炸时机
```

### `Until(time_relative_cs)`

等待直至当前时间戳与本波刷新时间点的差值达到指定值.

该函数需要配合 Prejudge() 使用. 多个 Until() 连用时注意调用顺序必须符合时间先后顺序.

@参数 time_relative_cs(int): 相对时间, 单位 cs, 精度 1. 建议范围 [-200, 2300].

@示例:

```python
Until(-95)  # 刷新前 95cs
```

```python
Until(180)  # 刷新后 180cs
```

```python
Until(-150)  # 炮炸珊瑚可用时机
```

```python
Until(444 - 373)  # 444cs 生效炮发射时机
```

```python
Until(601 + 20 - 298)  # 加速波下一波 20cs 预判冰点咖啡豆时机
```

```python
Until(601 + 5 - 100 - 320)  # 加速波下一波 5cs 预判冰复制冰种植时机
```

```python
Until(1200 - 200 - 373)  # 1200cs 波长激活炸时机
```

```python
Until(4500 - 5)  # 收尾波拖满时红字出现时机
```

```python
Until(5500)  # 最后一大波白字出现时机
```

## 选卡/更新炮列表

### `SelectCards(seeds_selected=None)`

选卡并开始游戏.

选择所有卡片, 点击开始游戏, 更新加农炮列表, 更新卡片列表, 更新场景数据, 等待开场红字消失.

@参数 seeds_selected(list): 卡片列表, 参数为空默认选择八张紫卡和两张免费卡. 参数个数小于卡槽数则用默认卡片填充.

列表长度不大于卡槽格数. 单张卡片 seed 可用 int/tuple/str 表示, 不同表示方法可混用.

seed(int): 卡片序号, 0 为豌豆射手, 47 为玉米加农炮, 对于模仿者这个数字再加上 48.

seed(tuple): 卡片位置, 用 (行, 列, 是否模仿者) 表示, 第三项可省略, 默认非模仿者.

seed(str): 卡片常用名称参考附录.

@示例:

```python
SelectCards()
```

```python
SelectCards([14, 14 + 48, 17, 2, 3, 30, 33, 13, 9, 8])
```

```python
SelectCards([(2, 7), (2, 7, True), (3, 2), (1, 3, False), (1, 4, False), (4, 7), (5, 2), (2, 6), (2, 2), (2, 1),])
```

```python
SelectCards(["寒冰菇", "复制冰", "窝瓜", "樱桃", "坚果", "南瓜", "花盆", "胆小", "阳光", "小喷"])
```

```python
SelectCards(["小喷菇", "模仿者小喷菇"])
```

### `UpdatePaoList(cobs=None)`

更新玉米加农炮列表.

选卡时自动调用, 空参数则自动找炮. 若需要自定义炮组请在选卡函数后面使用.

如果出现炮落点位于自身附近快速点击无法发射的现象可通过调整炮序解决.

@参数 cobs(list): 加农炮列表, 包括若干个 (行, 列) 元组, 以后轮坐标为准.

@示例:

```python
UpdatePaoList()
```

```python
UpdatePaoList([(3, 1), (4, 1), (3, 3), (4, 3), (1, 5), (2, 5), (3, 5), (4, 5), (5, 5), (6, 5)])
```

```python
UpdatePaoList(
    [
        (r, c)
        for r in (1, 2, 3, 4, 5, 6)
        for c in (1, 3, 5, 7)
        if not (r in (3, 4) and c == 7)
    ]
)
```

```python
UpdatePaoList([
                    (1, 5), (1, 7),
    (2, 1),         (2, 5), (2, 7),
    (3, 1), (3, 3), (3, 5), (3, 7),
    (4, 1), (4, 3), (4, 5), (4, 7),
    (5, 1),         (5, 5), (5, 7),
                    (6, 5), (6, 7),
    ])
```

## 场地相关点击函数

### `MouseLock()`

获取鼠标锁, 进行完整的(不可分割的)鼠标操作前加锁, 操作完毕后释放.

@返回值 (object): 唯一内置鼠标锁.

@示例:

```python
MouseLock().acquire()  # 获取鼠标操作权
SafeClick()            # 安全右键避免冲突
pass                   # 干点什么
MouseLock().release()  # 释放鼠标操作权
```

```python
with MouseLock():  # 获取鼠标操作权, 代码块结束后自动释放
    SafeClick()    # 安全右键避免冲突
    pass           # 干点什么
```

### `SafeClick()`

安全右键.

即右键单击左上角, 用于取消之前的(可能未完成的)操作以避免冲突.

### `ClickSeed(seed)`

点击卡槽中的卡片.

@参数 seed(int/str): 卡槽第几格或者卡片名称.

@示例:

```python
ClickSeed(5)  # 点击第 5 格卡槽
```

```python
ClickSeed("樱桃")  # 点击卡槽中的樱桃卡片
```

### `ClickShovel()`

点击铲子.

### `ClickGrid(*crood)`

点击场上格点.

@参数 crood(float/tuple): 坐标, 两个分别表示 行/列 的数字或者一个 (行, 列) 元组, 数字可为小数.

@示例:

```python
ClickGrid((2, 9))  # 点击 2 行 9 列
```

```python
ClickGrid(2, 9)  # 不推荐
```

## 用卡用炮铲子操作

### `Card(seed, *crood)`

用卡操作.

@参数 seed(int/str): 卡槽第几格或者卡片名称.

@参数 crood(int/tuple): 坐标, 两个分别表示 行/列 的数字或者一个 (行, 列) 元组, 数字均为整数.

@示例:

```python
Card(1, (2, 3))  # 将卡槽中的第 1 张卡片种在 2 行 3 列
```

```python
Card("樱桃", (5, 9))  # 将樱桃种在 5 行 9 列
```

```python
Card(1, 2, 3)  # 不推荐
```

```python
Card("樱桃", 5, 9)  # 不推荐
```

### `Shovel(*croods)`

用铲子操作.

@参数 croods(float/tuple): 坐标, 两个分别表示 行/列 的数字或者一至多个 (行, 列) 元组, 数字可为小数.

@示例:

```python
Shovel((3, 4))  # 铲掉 3 行 4 列的普通植物
```

```python
Shovel((5 + 0.1, 6))  # 铲掉 5 行 6 列的南瓜头
```

```python
Shovel((1, 9), (2, 9), (5, 9), (6, 9))  # 铲掉所有 9 列垫材
```

```python
Shovel(1, 2)  # 不推荐
```

### `Pao(*croods)`

用炮操作.

@参数 croods(float/tuple/list): 落点, 一至多个格式为 (行, 列) 的元组, 或者一个包含了这些元组的列表.

为了避免炮落点位于自身附近点击失效可设置额外的延时参数(发射单门炮时)或者调换连续两炮的顺序(发射多门炮时).

@示例:

```python
Pao((2, 9))
```

```python
Pao((2, 9), (5, 9), (2, 9), (5, 9))
```

```python
Pao((5, 7), 30)  # 点炮身延迟 30cs 再发射
```

```python
Pao((5, 4), (1, 4))  # 调整炮序
```

```python
Pao(2, 9)  # 不推荐
```

```python
Pao(5, 7, 30)  # 不推荐
```

```python
Pao([(2, 9), (5, 9), (2, 9), (5, 9)])  # 不推荐
```

### `SkipPao(num)`

按炮列表顺序跳过即将发射的一定数量的玉米炮, 通常用于 wave9/19 手动收尾.

@参数 num(int): 数量.

### `TryPao(*croods)`

自动找炮发射.

此函数有一定开销, 不可连续使用(间隔至少 1cs). 参数格式同 `Pao()`.

@返回值 (bool): 成功返回 True, 无炮可用或者中途无炮导致发射不完全则返回 False.

### `RoofPao(*croods)`

屋顶修正飞行时间发炮.

此函数开销较大(开新线程)不适合精确键控. 只适用于前场 (约 7~9 列). 参数格式大体与 `Pao()` 相同 (缺少额外的点炮延时参数).

### `SetFixPao(*crood)`

设置要更换的玉米炮, 下一次该门炮发射后会自动替换并在可用时更新炮列表相关数据.

@参数 crood(int/tuple): 坐标, 两个分别表示 行/列 的数字或者一个 (行, 列) 元组.

## 子线程操作

### `RunningInThread`

将此装饰器应用到需要在子线程运行的函数上.

定义一个函数, 应用该装饰器, 则函数在调用的时候会运行在单独的线程中.

@示例:

```python
@RunningInThread
def func():
    pass
```

### `StartAutoCollectThread(collect_items=None, interval_cs=12)`

自动收集场上资源, 在单独的子线程运行.

为了避免操作冲突, 当鼠标选中 卡片/铲子/玉米炮 时会暂停收集. 建议把鼠标光标移出窗口外以避免卡顿.

@参数 collect_items(list\[str/int\]): 包含需要收集的资源类型的列表, 默认所有.

可选值物品名称 ["银币", "金币", "钻石", "阳光", "小阳光", "大阳光", "幼苗"] 或者代号 [1, 2, 3, 4, 5, 6, 17].

@参数 interval_cs(float/int): 点击间隔, 单位 cs, 默认 12.

@示例:

```python
StartAutoCollectThread()  # 自动收集所有资源
```

```python
StartAutoCollectThread(["钻石", "阳光", "小阳光", "大阳光"], 20)  # 只收集钻石和各种阳光, 间隔 0.2s
```

### `StartAutoFillIceThread(spots=None, total=0x7FFFFFFF)`

自动存冰. 在单独的子线程运行.

@参数 spots(list): 存冰点, 包括若干个 (行, 列) 元组. 永久位在前, 临时位在后. 默认为场上现有存冰的位置.

@参数 total(int): 总个数, 默认无限.

@示例:

```python
StartAutoFillIceThread()
```

```python
StartAutoFillIceThread([(6, 1), (5, 1), (2, 1), (1, 1)], 10)
```

### `Coffee()`

点冰. 使用咖啡豆激活存冰, 优先点临时位.

该函数需要配合自动存冰线程 StartAutoFillIceThread() 使用.

### `StartStopDancerThread()`

女仆秘籍. 通过暂停控制舞王/伴舞的跳舞/行走.

### `StartNutsFixerThread(spots, seed)`

坚果类植物修复. 在单独的子线程运行.

@参数 spots(list): 位置, 包括若干个 (行, 列) 元组.

@参数 seed(str): 卡片名称, 可选值 ["坚果", "高坚果", "南瓜头"].

@示例:

```python
StartNutsFixerThread([(3, 8), (4, 8)], "高坚果")
```

```python
StartNutsFixerThread([(4, 5),(4, 6),(4, 7),(4, 8)], "南瓜头")
```

## 信息获取

### `GameOn()`

@返回值 (bool): 游戏是否开启, 没开则会尝试重新查找一次.

### `GameUI()`

@返回值 (int): 游戏界面.

1: 主界面, 2: 选卡, 3: 正常游戏/战斗, 4: 僵尸进屋, 7: 模式选择.

### `GameMode()`

@返回值 (int): 游戏模式, 13 为生存无尽. 详情查阅附录.

### `GameScene()`

@返回值 (int): 游戏场景/场地/地图.

0: 白天, 1: 黑夜, 2: 泳池, 3: 浓雾, 4: 屋顶, 5: 月夜, 6: 蘑菇园, 7: 禅境花园, 8: 水族馆, 9: 智慧树.

### `GamePaused()`

@返回值 (bool): 当前游戏是否暂停.

### `GameClock()`

@返回值 (int): 内部时钟, 游戏暂停和选卡时会暂停计时.

### `WaveCountdown()`

@返回值 (int): 下一波刷新倒计时, 触发刷新时重置为 200, 减少至 1 后刷出下一波.

### `HugeWaveCountdown()`

@返回值 (int): 大波刷新倒计时, 对于旗帜波, 刷新倒计时减少至 4 后停滞, 由该值代替减少.

### `CurrentWave()`

@返回值 (int): 已刷新波数.

### `GetZombieTypes()`

@返回值 (list\[int\]): 包含当前出怪类型的列表. 僵尸类型代号请查阅附录.

只能在选卡或者战斗界面使用.

### `GetZombieWaves(z=32)`

@参数 zombie_type(int): 僵尸类型代号, 默认为红眼. 详情请查阅附录.

@返回值 (list\[bool\]): 包含指定僵尸在 20 波中是否出现的列表.

只能在选卡或者战斗界面使用.

## 挂机辅助

### `GotoMainUI()`

切换到主界面. 需要先开启后台运行.

### `GotoEndless()`

切换到无尽模式选卡界面. 需要先开启后台运行.

### `Save()`

备份存档. 退回主界面再调用.

### `Load()`

还原存档. 退回主界面再调用.

## 功能修改

### `BackgroundRunning(on=True)`

允许后台运行.

@参数 on(bool): 是否开启.

### `QuickLineup(on=True)`

快捷布阵模式.

同时开启这些功能: 自动收集, 玉米炮无冷却, 植物无敌, 暂停刷怪, 无视阳光, 卡片无冷却, 紫卡无限制, 浓雾透视.

@参数 on(bool): 是否开启.

### `QuickPass()`

快速过关.

直接结束关卡, 过关后将阳光数设置为 8000, 已完成 2018 面旗帜数, 玉米炮处于最亮状态.

### `JumpLevel(level=1008)`

无尽模式跳关.

@参数 level(int): 轮数.

### `SetSun(sun=8000)`

设置阳光.

@参数 sun(int): 阳光数.

### `SetMoney(money)`

设置金钱. 显示数量为 10 倍.

@参数 money(int): 金钱数.

### `ClearFog(on=True)`

清除浓雾.

@参数 on(bool): 是否开启.

### `ZombieNoFalling(on=True)`

僵尸死后不掉钱.

@参数 on(bool): 是否开启.

### `SetMusic(music)`

设置背景音乐.

@参数 music(str/int): 歌曲名或者代号.

```python
"Grasswalk"          # 1
"Moongrains"         # 2
"Watery Graves"      # 3
"Rigor Mormist"      # 4
"Graze the Roof"     # 5
"Choose Your Seeds"  # 6
"Crazy Dave"         # 7
"Zen Garden"         # 8
"Cerebrawl"          # 9
"Loonboon"           # 10
"Ultimate Battle"    # 11
"Brainiac Maniac"    # 12
```

### `SetDebug(mode)`

设置调试模式.

@参数 mode(str/int): 模式名或者代号.

```python
"OFF"        # 0
"SPAWNING"   # 1
"MUSIC"      # 2
"MEMORY"     # 3
"COLLISION"  # 4
```

### `SetZombies(zombies=None, mode="极限刷怪")`

设置出怪.

旗帜(无需设定)只会在每个大波出现一只, 雪人只会出现一只, 蹦极只会在大波出现.

@参数 zombies(list\[str/int\]): 包含僵尸名称或代号的列表, 建议 8~12 种.

@参数 mode(str): 刷怪模式, 默认使用极限刷怪. 可选值 "自然刷怪" "极限刷怪" "模拟自然刷怪".

自然刷怪只改变出怪种类, 再由游戏内置的函数生成出怪列表.

极限刷怪是把所选僵尸种类按顺序均匀地填充到出怪列表.

模拟自然刷怪则是根据统计规律按一定的比例随机填充出怪列表, 在旗帜波会调整不同僵尸的平均密度.

@示例:

```python
SetZombies(["撑杆", "舞王", "冰车", "海豚", "气球", "矿工", "跳跳", "扶梯", "白眼", "红眼"])
```

## 附录

### 卡片名称代号

部分函数(`SelectCards` `ClickSeed` `Card`)支持用卡片(种子包)名称字符串作为参数, 卡片常用名称以及模仿者前缀如下.

```python
[
    ["Peashooter", "豌豆射手", "单发"],              # 0
    ["Sunflower", "向日葵", "小向"],                 # 1
    ["Cherry Bomb", "樱桃炸弹", "樱桃"],             # 2
    ["Wall-nut", "坚果墙", "坚果"],                  # 3
    ["Potato Mine", "土豆雷", "地雷"],               # 4
    ["Snow Pea", "寒冰射手", "冰豆"],                # 5
    ["Chomper", "大嘴花", "食人花"],                 # 6
    ["Repeater", "双发射手", "双发"],                # 7
    ["Puff-shroom", "小喷菇", "小喷"],               # 8
    ["Sun-shroom", "阳光菇", "阳光"],                # 9
    ["Fume-shroom", "大喷菇", "大喷"],               # 10
    ["Grave Buster", "墓碑吞噬者", "墓碑"],          # 11
    ["Hypno-shroom", "魅惑菇", "魅惑"],              # 12
    ["Scaredy-shroom", "胆小菇", "胆小"],            # 13
    ["Ice-shroom", "寒冰菇", "冰蘑菇", "冰"],        # 14
    ["Doom-shroom", "毁灭菇", "核蘑菇", "核"],       # 15
    ["Lily Pad", "睡莲", "荷叶"],                    # 16
    ["Squash", "窝瓜", "倭瓜"],                      # 17
    ["Threepeater", "三线射手", "三线"],             # 18
    ["Tangle Kelp", "缠绕海草", "海草"],             # 19
    ["Jalapeno", "火爆辣椒", "辣椒"],                # 20
    ["Spikeweed", "地刺"],                           # 21
    ["Torchwood", "火炬树桩", "火树"],               # 22
    ["Tall-nut", "高坚果", "搞基果"],                # 23
    ["Sea-shroom", "海蘑菇"],                        # 24
    ["Plantern", "路灯花", "灯笼"],                  # 25
    ["Cactus", "仙人掌"],                            # 26
    ["Blover", "三叶草", "三叶"],                    # 27
    ["Split Pea", "裂荚射手", "裂荚"],               # 28
    ["Starfruit", "杨桃", "五角星", "大帝"],         # 29
    ["Pumpkin", "南瓜头", "南瓜"],                   # 30
    ["Magnet-shroom", "磁力菇", "磁铁"],             # 31
    ["Cabbage-pult", "卷心菜投手", "包菜"],          # 32
    ["Flower Pot", "花盆"],                          # 33
    ["Kernel-pult", "玉米投手", "玉米"],             # 34
    ["Coffee Bean", "咖啡豆", "咖啡"],               # 35
    ["Garlic", "大蒜"],                              # 36
    ["Umbrella Leaf", "叶子保护伞", "莴苣"],         # 37
    ["Marigold", "金盏花"],                          # 38
    ["Melon-pult", "西瓜投手", "西瓜"],              # 39
    ["Gatling Pea", "机枪射手", "机枪", "加特林"],   # 40
    ["Twin Sunflower", "双子向日葵", "双子"],        # 41
    ["Gloom-shroom", "忧郁蘑菇", "忧郁菇", "曾哥"],  # 42
    ["Cattail", "香蒲", "猫尾草", "小猫"],           # 43
    ["Winter Melon", "冰瓜", "冰西瓜"],              # 44
    ["Gold Magnet", "吸金磁", "吸金"],               # 45
    ["Spikerock", "地刺王", "钢刺"],                 # 46
    ["Cob Cannon", "玉米加农炮", "玉米炮", "春哥"],  # 47
]

["Imitater", "模仿者", "复制",]  # 48
```

### 游戏模式代号

```python
{
    0: "Adventure",
    1: "Survival: Day",
    2: "Survival: Night",
    3: "Survival: Pool",
    4: "Survival: Fog",
    5: "Survival: Roof",
    6: "Survival: Day (Hard)",
    7: "Survival: Night (Hard)",
    8: "Survival: Pool (Hard)",
    9: "Survival: Fog (Hard)",
    10: "Survival: Roof (Hard)",
    11: "Survival: Day (Endless)",
    12: "Survival: Night (Endless)",
    13: "Survival: Endless",
    14: "Survival: Fog (Endless)",
    15: "Survival: Roof (Endless)",
    16: "ZomBotany",
    17: "Wall-nut Bowling",
    18: "Slot Machine",
    19: "It's Raining Seeds",
    20: "Beghouled",
    21: "Invisi-ghoul",
    22: "Seeing Stars",
    23: "Zombiquarium",
    24: "Beghouled Twist",
    25: "Big Trouble Little Zombie",
    26: "Portal Combat",
    27: "Column Like You See'Em",
    28: "Bobseld Bonanza",
    29: "Zombie Nimble Zombie Quick",
    30: "Whack a Zombie",
    31: "Last Stand",
    32: "ZomBotany 2",
    33: "Wall-nut Bowling 2",
    34: "Pogo Party",
    35: "Dr. Zomboss's Revenge",
    36: "Art Challenge Wall-nut",
    37: "Sunny Day",
    38: "Unsodded",
    39: "Big Time",
    40: "Art Challenge Sunflower",
    41: "Air Raid",
    42: "Ice Level",
    43: "Zen Garden",
    44: "High Gravity",
    45: "Grave Danger",
    46: "Can You Dig It?",
    47: "Dark Stormy Night",
    48: "Bungee Blitz",
    49: "Squirrel",
    50: "Tree of Wisdom",
    51: "Vasebreaker",
    52: "To the Left",
    53: "Third Vase",
    54: "Chain Reaction",
    55: "M is for Metal",
    56: "Scary Potter",
    57: "Hokey Pokey",
    58: "Another Chain Reaction",
    59: "Ace of Vase",
    60: "Vasebreaker Endless",
    61: "I, Zombie",
    62: "I, Zombie Too",
    63: "Can You Dig It?",
    64: "Totally Nuts",
    65: "Dead Zeppelin",
    66: "Me Smash!",
    67: "ZomBoogie",
    68: "Three Hit Wonder",
    69: "All your brainz r belong to us",
    70: "I, Zombie Endless",
    71: "Upsell",
    72: "Intro",
}
```

### 僵尸类型代号

```python
[
    ["Zombie", "普僵"],                   # 0
    ["Flag Zombie", "旗帜"],              # 1
    ["Conehead Zombie", "路障"],          # 2
    ["Pole Vaulting Zombie", "撑杆"],     # 3
    ["Buckethead Zombie", "铁桶"],        # 4
    ["Newspaper Zombie", "读报"],         # 5
    ["Screen Door Zombie", "铁门"],       # 6
    ["Football Zombie", "橄榄"],          # 7
    ["Dancing Zombie", "舞王"],           # 8
    ["Backup Dancer", "伴舞"],            # 9
    ["Ducky Tube Zombie", "鸭子"],        # 10
    ["Snorkel Zombie", "潜水"],           # 11
    ["Zomboni", "冰车"],                  # 12
    ["Zombie Bobsled Team", "雪橇"],      # 13
    ["Dolphin Rider Zombie", "海豚"],     # 14
    ["Jack-in-the-Box Zombie", "小丑"],   # 15
    ["Balloon Zombie", "气球"],           # 16
    ["Digger Zombie", "矿工"],            # 17
    ["Pogo Zombie", "跳跳"],              # 18
    ["Zombie Yeti", "雪人"],              # 19
    ["Bungee Zombie", "蹦极"],            # 20
    ["Ladder Zombie", "扶梯"],            # 21
    ["Catapult Zombie", "投篮"],          # 22
    ["Gargantuar", "白眼"],               # 23
    ["Imp", "小鬼"],                      # 24
    ["Dr. Zomboss", "僵博"],              # 25
    ["Peashooter Zombie", "豌豆"],        # 26
    ["Wall-nut Zombie", "坚果"],          # 27
    ["Jalapeno Zombie", "辣椒"],          # 28
    ["Gatling Pea Zombie", "机枪"],       # 29
    ["Squash Zombie", "倭瓜"],            # 30
    ["Tall-nut Zombie", "高坚果"],        # 31
    ["GigaGargantuar", "红眼"],           # 32
]
```
