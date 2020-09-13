# coding=utf-8

from .core import *

### 读取常用信息


def game_on():
    """
    @返回值 (bool): 游戏是否开启, 没开则会尝试重新查找一次.
    """
    if is_valid():
        return True
    else:
        return find_pvz()


def game_ui():
    """
    @返回值 (int): 游戏界面.

    1: 主界面, 2: 选卡, 3: 正常游戏/战斗, 4: 僵尸进屋, 7: 模式选择.
    """
    return read_memory("int", 0x6A9EC0, 0x7FC)


def game_mode():
    """
    @返回值 (int): 游戏模式, 13 为生存无尽.
    """
    return read_memory("int", 0x6A9EC0, 0x7F8)


def game_scene():
    """
    @返回值 (int): 游戏场景/场地/地图.

    0: 白天, 1: 黑夜, 2: 泳池, 3: 浓雾, 4: 屋顶, 5: 月夜, 6: 蘑菇园, 7: 禅境花园, 8: 水族馆, 9: 智慧树.
    """
    return read_memory("int", 0x6A9EC0, 0x768, 0x554C)


def game_paused():
    """
    @返回值 (bool): 当前游戏是否暂停.
    """
    return read_memory("bool", 0x6A9EC0, 0x768, 0x164)


def mouse_in_game():
    """
    @返回值 (bool): 鼠标是否在游戏窗口内部.
    """
    return read_memory("bool", 0x6A9EC0, 0x768, 0x138, 0x18)  # 0x6A9EC0, 0x768, 0x59


def mouse_have_something():
    """
    @返回值 (bool): 鼠标是否选中卡炮或铲子.
    """
    return read_memory("int", 0x6A9EC0, 0x768, 0x138, 0x30) in (1, 6, 8)


def game_clock():
    """
    @返回值 (int): 内部时钟, 游戏暂停和选卡时会暂停计时.
    """
    return read_memory("int", 0x6A9EC0, 0x768, 0x5568)


def wave_init_countdown():
    """
    @返回值 (int): 刷新倒计时初始值.
    """
    return read_memory("int", 0x6A9EC0, 0x768, 0x55A0)


def wave_countdown():
    """
    @返回值 (int): 下一波刷新倒计时, 触发刷新时重置为 200, 减少至 1 后刷出下一波.
    """
    return read_memory("int", 0x6A9EC0, 0x768, 0x559C)


def huge_wave_countdown():
    """
    @返回值 (int): 大波刷新倒计时, 对于旗帜波, 刷新倒计时减少至 4 后停滞, 由该值代替减少.
    """
    return read_memory("int", 0x6A9EC0, 0x768, 0x55A4)


def current_wave():
    """
    @返回值 (int): 已刷新波数.
    """
    return read_memory("int", 0x6A9EC0, 0x768, 0x557C)


### 修改出怪


# 从出怪种子生成出怪类型
def update_zombies_type():
    write_memory("bool", [False] * 33, 0x6A9EC0, 0x768, 0x54D4)
    asm_init()
    asm_mov_exx_dword_ptr("esi", 0x6A9EC0)
    asm_mov_exx_dword_ptr_exx_add("esi", 0x768)
    asm_mov_exx_dword_ptr_exx_add("esi", 0x160)
    asm_call(0x00425840) if pvz_ver() == "1.0.0.1051" else asm_call(0x004258A0)
    asm_ret()
    asm_code_inject_safely()


# 从出怪类型生成出怪列表
def update_zombies_list():
    asm_init()
    asm_mov_exx_dword_ptr("edi", 0x6A9EC0)
    asm_mov_exx_dword_ptr_exx_add("edi", 0x768)
    asm_call(0x004092E0) if pvz_ver() == "1.0.0.1051" else asm_call(0x004092F0)
    asm_ret()
    asm_code_inject_safely()


# 更新选卡界面出怪预览
def update_zombies_preview():
    write_memory("byte", 0x80, 0x0043A153) if pvz_ver() == "1.0.0.1051" else write_memory("byte", 0x80, 0x0043A1C3)
    asm_init()
    asm_mov_exx_dword_ptr("ebx", 0x6A9EC0)
    asm_mov_exx_dword_ptr_exx_add("ebx", 0x768)
    asm_call(0x0040DF70) if pvz_ver() == "1.0.0.1051" else asm_call(0x0040DF80)
    asm_mov_exx_dword_ptr("eax", 0x6A9EC0)
    asm_mov_exx_dword_ptr_exx_add("eax", 0x768)
    asm_mov_exx_dword_ptr_exx_add("eax", 0x15C)
    asm_push_exx("eax")
    asm_call(0x0043A140) if pvz_ver() == "1.0.0.1051" else asm_call(0x0043A1B0)
    asm_ret()
    asm_code_inject_safely()
    write_memory("byte", 0x85, 0x0043A153) if pvz_ver() == "1.0.0.1051" else write_memory("byte", 0x85, 0x0043A1C3)


# 僵尸名称统一转换为代号表示
def zombie_name_to_index(zombie):
    if isinstance(zombie, str):
        if zombie in zombies_string_dict:
            return zombies_string_dict[zombie]
        else:
            error("未知僵尸名称: %s." % zombie)
    else:  # int
        if zombie in range(33):
            return zombie
        else:
            error("未知僵尸类型代号: %s." % zombie)


def set_internal_spawn(zombies=None):
    """
    内置刷怪, 由游戏自带函数生成出怪列表. 普僵不管有没有选都是必出.

    @参数 zombies(list[str/int]): 包含僵尸名称或代号的列表.
    """

    if not (game_on() and game_ui() in (2, 3)):
        return

    if zombies is None:
        zombies = []
    zombies += [0]  # 普僵必出
    zombies = [zombie_name_to_index(z) for z in zombies]
    zombies = list(set(zombies))

    zombies_type_offset = read_memory("unsigned int", 0x6A9EC0, 0x768) + 0x54D4
    write_memory("bool", [True if i in zombies else False for i in range(33)], zombies_type_offset)
    update_zombies_list()

    if game_ui() == 2:
        update_zombies_preview()


def set_customize_spawn(zombies=None):
    """
    自定义刷怪, 由脚本生成并填充出怪列表.

    @参数 zombies(list[str/int]): 包含僵尸名称或代号的列表.
    """

    if not (game_on() and game_ui() in (2, 3)):
        return

    if zombies is None:
        zombies = [0]  # 默认普僵
    zombies = [zombie_name_to_index(z) for z in zombies]
    zombies = list(set(zombies))

    zombies_list = [0] * 1000

    has_flag = 1 in zombies
    has_yeti = 19 in zombies
    has_bungee = 20 in zombies
    limit_flag = True
    limit_yeti = True
    limit_bungee = True

    count = 0
    for i in range(33):
        if i in zombies:
            count += 1

    if count > 0:

        zombie_type = 0
        for i in range(1000):
            while True:
                zombie_type += 1
                zombie_type %= 33
                if not (  #
                    (zombie_type not in zombies)  #
                        or (has_flag and limit_flag and zombie_type == 1)  #
                        or (has_yeti and limit_yeti and zombie_type == 19)  #
                        or (has_bungee and limit_bungee and zombie_type == 20)  #
                ):  #
                    break
            zombies_list[i] = zombie_type

        index_flag = [450, 950]
        index_bungee = [451, 452, 453, 454, 951, 952, 953, 954]

        if has_flag and limit_flag:
            for i in index_flag:
                zombies_list[i] = 1

        if has_bungee and limit_bungee:
            for i in index_bungee:
                zombies_list[i] = 20

        if has_yeti and limit_yeti:
            i = 0
            while True:
                i = random.randint(0, 999)
                if not ((i in index_flag) or (i in index_bungee)):
                    break
            zombies_list[i] = 19

    write_memory("unsigned int", zombies_list, 0x6A9EC0, 0x768, 0x6B4)

    if game_ui() == 2:
        update_zombies_preview()


def set_zombies(zombies=None, mode="极限刷怪"):
    """
    设置出怪.

    旗帜只会在每个大波出现一只, 雪人只会出现一只, 蹦极只会在大波出现.

    @参数 zombies(list[str/int]): 包含僵尸名称或代号的列表, 建议 8~12 种.

    @参数 mode(str): 刷怪模式, 默认使用极限刷怪. 可选值 "自然刷怪" "极限刷怪".

    自然刷怪只改变出怪种类, 再由游戏内置的函数生成出怪列表.

    极限刷怪是把所选僵尸种类按顺序均匀地填充到出怪列表.

    @示例:

    >>> SetZombies(["撑杆", "舞王", "冰车", "海豚", "气球", "矿工", "跳跳", "扶梯", "白眼", "红眼"])
    """

    if mode in ("自然", "内置", "内置生成", "自然出怪", "自然刷怪"):
        set_internal_spawn(zombies + ["普僵"])
    elif mode in ("极限", "填充", "均匀填充", "极限出怪", "极限刷怪"):
        set_customize_spawn(zombies + ["旗帜"])
    else:
        error("未知刷怪模式: %s." % mode)


### 选卡

# (50, 160) 为左上角卡片中心坐标
# (215, 160) 为模仿者选卡界面左上角卡片中心坐标
# 单张卡片宽度约 50px 高度约 70px
# 模仿者卡片位置 (490, 550), 成功点击后等待界面出现再选卡
# 每次选完卡均等待一定时间

SEED_0_0_X = 50
SEED_0_0_Y = 160
IMITATER_SEED_0_0_X = 215
IMITATER_SEED_0_0_Y = 160
SEED_WIDTH = 50
SEED_HEIGHT = 70
IMITATER_X = 490
IMITATER_Y = 550
IMITATER_SHOW_UP = 0
SEED_DELAY_TIME = 5


def select_seed_by_crood(row, col, imitater=False):
    """
    选择单张卡片.

    @参数 row(int): 行

    @参数 col(int): 列

    @参数 imitater(bool): 是否为模仿者
    """

    if imitater:
        if row not in (1, 2, 3, 4, 5):
            critical("卡片行数 %d 超出有效范围." % row)
        if col not in (1, 2, 3, 4, 5, 6, 7, 8):
            critical("卡片列数 %d 超出有效范围." % col)
    else:
        if row not in (1, 2, 3, 4, 5, 6):
            critical("卡片行数 %d 超出有效范围." % row)
        if col not in (1, 2, 3, 4, 5, 6, 7, 8):
            critical("卡片列数 %d 超出有效范围." % col)

    if imitater:
        special_button_click(IMITATER_X, IMITATER_Y)
        thread_sleep_for(IMITATER_SHOW_UP)
        x = IMITATER_SEED_0_0_X + (col - 1) * (SEED_WIDTH + 1)
        y = IMITATER_SEED_0_0_Y + (row - 1) * (SEED_HEIGHT + 2)
    else:
        x = SEED_0_0_X + (col - 1) * (SEED_WIDTH + 3)
        y = SEED_0_0_Y + (row - 1) * (SEED_HEIGHT + 0)

    # 不小心点进了图鉴或者商店
    window_type = read_memory("int", 0x6A9EC0, 0x320, 0x88, 0xC)
    if window_type == 1:
        left_click(720, 580)
        thread_sleep_for(5)
    elif window_type == 4:
        left_click(430, 550)
        thread_sleep_for(5)

    special_button_click(x, y)
    thread_sleep_for(SEED_DELAY_TIME)

    if imitater:
        im_str = seeds_imitater_string[0] + " "
    else:
        im_str = ""
    seed_str = seeds_string[(row - 1) * 8 + (col - 1)][0]
    info("选择单张卡片 " + im_str + seed_str + ".")


@functools.singledispatch
def seed_to_crood(seed):
    """
    卡片转换为 (行, 列, 模仿者) 的标准形式.

    根据参数类型选择不同的实现.

    @参数 seed(int/tuple/str): 卡片

    @示例:

    >>> seed_to_crood(14 + 48)
    (2, 7, True)

    >>> seed_to_crood((2, 7, True))
    (2, 7, True)

    >>> seed_to_crood("复制冰")
    (2, 7, True)
    """
    error("卡片参数不支持 %s 类型." % type(seed))


@seed_to_crood.register(int)
def _(seed):
    if seed == 1437:
        row = 4
        col = 6
        imitater = False
    else:
        imitater = seed >= 48
        index = seed % 48
        row, col = divmod(index, 8)
    return row + 1, col + 1, imitater


@seed_to_crood.register(tuple)
def _(seed):
    if len(seed) == 2:
        row, col = seed
        imitater = False
    elif len(seed) == 3:
        row, col, im = seed
        imitater = im not in (False, 0)
    return row, col, imitater


@seed_to_crood.register(str)
def _(seed):
    if not seed in seeds_string_dict:
        error("未知卡片名称: %s." % seed)
    seed_index = seeds_string_dict[seed]  # 卡片代号(+48)
    imitater = seed_index >= 48
    index = seed_index % 48
    row, col = divmod(index, 8)
    return row + 1, col + 1, imitater


# 检查已选卡片是否完全相符
def slots_exact_match(seeds_selected):
    slots_count = read_memory("int", 0x6A9EC0, 0x768, 0x144, 0x24)
    slots_selected = read_memory("int", 0x6A9EC0, 0x774, 0xD24)
    if slots_selected < slots_count:
        return False
    match = True
    for i in range(slots_count):
        row, col, imitater = seeds_selected[i]
        seed_index = (row - 1) * 8 + (col - 1)
        if imitater:
            seed_index = 48
        seed_plant = read_memory("int", 0x6A9EC0, 0x774, 0xC4 + seed_index * 0x3C)
        seed_status = read_memory("int", 0x6A9EC0, 0x774, 0xC8 + seed_index * 0x3C)
        # !卡片对应的植物正确并且位于卡槽中
        if not (seed_plant == seed_index and seed_status == 1):
            match = False
            break
    return match


# 清空卡槽所有卡片
def clear_slots():
    slots_count = read_memory("int", 0x6A9EC0, 0x768, 0x144, 0x24)
    for slot_index in reversed(range(slots_count)):  # 逆序
        slot_index += 1
        if slots_count == 10:
            x = 63 + 51 * slot_index
        elif slots_count == 9:
            x = 63 + 52 * slot_index
        elif slots_count == 8:
            x = 61 + 54 * slot_index
        elif slots_count == 7:
            x = 61 + 59 * slot_index
        else:
            x = 61 + 59 * slot_index
        x -= 10
        y = 12
        special_button_click(x, y)
        thread_sleep_for(5)
    thread_sleep_for(5)


def select_all_seeds(seeds_selected=None):
    """
    选择所有卡片.
    """

    # 不小心点进了图鉴或者商店
    window_type = read_memory("int", 0x6A9EC0, 0x320, 0x88, 0xC)
    if window_type == 1:
        left_click(720, 580)
        thread_sleep_for(5)
    elif window_type == 4:
        left_click(430, 550)
        thread_sleep_for(5)

    default_seeds = [40, 41, 42, 43, 44, 45, 46, 47, 8, 8 + 48]
    slots_count = read_memory("int", 0x6A9EC0, 0x768, 0x144, 0x24)

    # 默认八张紫卡和两张免费卡
    if seeds_selected is None:
        seeds_selected = default_seeds[0:slots_count]

    # 参数个数小于卡槽数则用默认卡片填充
    while len(seeds_selected) < slots_count:
        for seed in default_seeds:
            if seed_to_crood(seed) not in [seed_to_crood(s) for s in seeds_selected]:
                seeds_selected += [seed]
                break

    if len(seeds_selected) > slots_count:
        critical("卡片数量 %d 超过卡槽格数 %d." % (len(seeds_selected), slots_count))

    # 卡片列表转换为标准形式
    seeds_selected = [seed_to_crood(seed) for seed in seeds_selected]
    info("所选卡片转换为标准形式 %s." % seeds_selected)

    clear_slots()  # 清空卡槽已选卡片
    retry_count = 0

    while not slots_exact_match(seeds_selected):

        if retry_count > 3:
            critical("选卡重试多次失败.")
        retry_count += 1
        info("选卡过程未完成, 正在重试.")

        # 清空卡槽并选择所有卡片
        clear_slots()
        for seed in seeds_selected:
            row, col, imitater = seed
            select_seed_by_crood(row, col, imitater)
        thread_sleep_for(5)  # 等内存变化

    thread_sleep_for(5)  # 等内存变化


def lets_rock():
    while read_memory("bool", 0x6A9EC0, 0x768, 0x15C, 0x2C):  # 位于选卡界面
        left_down(234, 567)
        thread_sleep_for(1)
        left_up(234, 567)
        thread_sleep_for(10)
        while read_memory("int", 0x6A9EC0, 0x320, 0x94) != 0:  # 出现了对话框
            left_click(320, 400)
            thread_sleep_for(10)


def select_seeds_and_lets_rock(seeds_selected=None):
    """
    选卡并开始游戏.

    选择所有卡片, 点击开始游戏, 更新场景数据, 更新卡片列表, 更新加农炮列表, 等待开场红字消失.

    建议把鼠标光标移出窗口外以避免可能出现的模仿者选卡失败.

    @参数 seeds_selected(list): 卡片列表, 长度不大于卡槽格数.

    列表为空默认选择八张紫卡和两张免费卡, 卡片个数小于卡槽数则用默认卡片填充.

    单张卡片 seed 可用 int/tuple/str 表示, 不同的表示方法可混用.

    seed(int): 卡片序号, 0 为豌豆射手, 47 为玉米加农炮, 对于模仿者这个数字再加上 48.

    seed(tuple): 卡片位置, 用 (行, 列, 是否模仿者) 表示, 第三项可省略, 默认非模仿者.

    seed(str): 卡片名称, 参考 seeds_string, 包含了一些常用名字.

    @示例:

    >>> SelectCards()

    >>> SelectCards([14, 14 + 48, 17, 2, 3, 30, 33, 13, 9, 8])

    >>> SelectCards([(2, 7), (2, 7, True), (3, 2), (1, 3, False), (1, 4, False), (4, 7), (5, 2), (2, 6), (2, 2), (2, 1),])

    >>> SelectCards(["寒冰菇", "复制冰", "窝瓜", "樱桃", "坚果", "南瓜", "花盆", "胆小", "阳光", "小喷"])

    >>> SelectCards(["小喷菇", "模仿者小喷菇"])
    """
    gc.collect()

    # 激活并提高运行优先级
    set_pvz_foreground()
    set_pvz_high_priority()

    # 等待战斗结束进入选卡界面
    while game_ui() != 2:
        thread_sleep_for(1)

    # 选卡
    select_all_seeds(seeds_selected)
    lets_rock()

    # 更新相关数据
    update_game_scene()
    update_seeds_list()
    update_cob_cannon_list()

    # 选卡后等待直至正式开始战斗
    while game_ui() != 3:
        thread_sleep_for(1)


### 获取卡槽信息

# 每张卡片在卡槽里的位置, 用于根据卡片代号找卡槽位置
seeds_in_slot = [None] * (48 * 2)

# 卡槽中每张卡片的代号, 用于根据卡槽位置找卡片代号
slot_seeds = [None] * 10


def update_seeds_list():
    """
    更新卡片相关数据. 该函数须在点击 "Let's Rock!" 后调用.
    """
    global seeds_in_slot, slot_seeds
    seeds_in_slot = [None] * (48 * 2)
    slot_seeds = [None] * 10

    slots_count = read_memory("int", 0x6A9EC0, 0x768, 0x144, 0x24)
    slots_offset = read_memory("unsigned int", 0x6A9EC0, 0x768, 0x144)
    for i in range(slots_count):
        seed_type = read_memory("int", slots_offset + 0x5C + i * 0x50)
        seed_imitater_type = read_memory("int", slots_offset + 0x60 + i * 0x50)
        if seed_type == 48:
            seed = seed_imitater_type + 48
        else:
            seed = seed_type
        seeds_in_slot[seed] = i + 1
        slot_seeds[i] = seed

    # info("更新卡片位置 %s." % str(seeds_in_slot))
    info("更新卡槽代号 %s." % str(slot_seeds))


# 卡片名字 name
# 卡片代号 seed
# 卡槽位置 index


# (name: str) -> int
def get_seed_by_name(name):
    """
    根据卡片名字得到卡片代号. (模仿者 +48)
    """
    if name not in seeds_string_dict:
        error("未知卡片名称: %s." % name)
    return seeds_string_dict[name]


# (seed: int) -> int
def get_index_by_seed(seed):
    """
    根据卡片代号得到卡槽位置. 不在返回 None.
    """
    if seed not in range(48 * 2):
        error("卡片代号 %d 超出有效范围." % seed)
    return seeds_in_slot[seed]


# (name: str) -> int
def get_index_by_name(name):
    """
    根据卡片名字得到卡槽位置. 不在返回 None.
    """
    if name not in seeds_string_dict:
        error("未知卡片名称: %s." % name)
    return seeds_in_slot[seeds_string_dict[name]]


# (index: int) -> int
def get_seed_by_index(index):
    """
    根据卡槽位置得到卡片代号.
    """
    if index not in range(1, 11):
        error("卡槽位置 %d 超出有效范围." % index)
    return slot_seeds[index - 1]


### 场景相关信息

# 卡槽格数, 选卡和用卡函数需要
slots_count = 10

# 场景地图, 点击场上格子相关函数需要
game_scene = 2

scenes = {
    0: "Day",
    1: "Night",
    2: "Pool",
    3: "Fog",
    4: "Roof",
    5: "Moon",
    6: "Mushroom Garden",
    7: "Zen Garden",
    8: "Aquarium Garden",
    9: "Tree of Wisdom",
}


# 更新卡槽格数和场景地图
def update_game_scene():
    global slots_count, game_scene
    slots_count = read_memory("int", 0x6A9EC0, 0x768, 0x144, 0x24)
    game_scene = read_memory("int", 0x6A9EC0, 0x768, 0x554C)
    info("更新卡槽格数 %d." % slots_count)
    info("更新场景地图 %s." % scenes[game_scene])


### 场景点击操作

# 唯一内置鼠标锁
mouse_lock = threading.Lock()


def get_mouse_lock():
    """
    获取鼠标锁, 进行完整的 (不可分割的) 鼠标操作前加锁, 操作完毕后释放.

    @返回值 (object): 唯一内置鼠标锁.

    @示例:

    >>> MouseLock().acquire()  # 获取鼠标操作权
    >>> SafeClick()            # 安全右键避免冲突
    >>> pass                   # 干点什么
    >>> MouseLock().release()  # 释放鼠标操作权

    >>> with MouseLock():  # 获取鼠标操作权, 代码块结束后自动释放
    >>>     SafeClick()    # 安全右键避免冲突
    >>>     pass           # 干点什么
    """

    return mouse_lock


def safe_click():
    """
    安全右键.

    即右键单击左上角, 用于取消之前的 (可能未完成的) 操作以避免冲突.
    """
    right_click(0, 0)


def click_seed(seed):
    """
    点击卡槽中的卡片.

    @参数 seed(int/str): 卡槽第几格或者卡片名称.

    @示例:

    >>> ClickSeed(5)  # 点击第 5 格卡槽

    >>> ClickSeed("樱桃")  # 点击卡槽中的樱桃卡片
    """

    if isinstance(seed, str):
        slot_index = get_index_by_name(seed)
        if slot_index is None:
            error("卡槽当中没有 %s 卡片, 操作失败." % seed)
    else:  # int
        slot_index = seed
        if slot_index not in range(1, 11):
            error("卡槽格数 %d 超出有效范围, 操作失败." % slot_index)

    if slots_count == 10:
        x = 63 + 51 * slot_index
    elif slots_count == 9:
        x = 63 + 52 * slot_index
    elif slots_count == 8:
        x = 61 + 54 * slot_index
    elif slots_count == 7:
        x = 61 + 59 * slot_index
    else:
        x = 61 + 59 * slot_index
    y = 12
    left_click(x, y)


def click_shovel():
    """
    点击铲子.
    """
    if slots_count == 10:
        x = 640
    elif slots_count == 9:
        x = 600
    elif slots_count == 8:
        x = 570
    elif slots_count == 7:
        x = 550
    else:
        x = 490
    y = 36
    left_click(x, y)


# 坐标转换
def rc2xy(*crood):
    """
    row, col -> x, y
    """

    if isinstance(crood[0], tuple):
        row, col = crood[0]
    else:
        row, col = crood

    x = 80 * col
    if game_scene in (2, 3):
        y = 55 + 85 * row
    elif game_scene in (4, 5):
        if col >= 6:
            y = 45 + 85 * row
        else:
            y = 45 + 85 * row + 20 * (6 - col)
    else:
        y = 40 + 100 * row

    return int(x), int(y)  # 取整


def click_grid(*crood):
    """
    点击场上格点.

    @参数 crood(float/tuple): 坐标, 两个分别表示 行/列 的数字或者一个 (行, 列) 元组, 数字可为小数.

    @示例:

    >>> ClickGrid((2, 9))  # 点击 2 行 9 列

    >>> ClickGrid(2, 9)  # 同上
    """
    x, y = rc2xy(*crood)
    left_click(x, y)


### 更新炮列表

# 炮列表 (row, col) x n
cob_list = []

# 用炮序号
cob_index = 0

# 炮列表锁
cob_lock = threading.Lock()


def update_cob_cannon_list(cobs=None):
    """
    更新玉米加农炮列表.

    选卡时会自动调用, 空参数则自动找炮. 若需要自定义顺序请在选卡函数后面使用.

    @参数 cobs(list): 加农炮列表, 包括若干个 (行, 列) 元组, 以后轮坐标为准.

    @示例:

    >>> UpdatePaoList()

    >>> UpdatePaoList([(3, 1), (4, 1), (3, 3), (4, 3), (1, 5), (2, 5), (3, 5), (4, 5), (5, 5), (6, 5)])

    >>> UpdatePaoList(
    >>>     [
    >>>         (r, c)
    >>>         for r in (1, 2, 3, 4, 5, 6)
    >>>         for c in (1, 3, 5, 7)
    >>>         if not (r in (3, 4) and c == 7)
    >>>     ]
    >>> )

    >>> UpdatePaoList([
    >>>                     (1, 5), (1, 7),
    >>>     (2, 1),         (2, 5), (2, 7),
    >>>     (3, 1), (3, 3), (3, 5), (3, 7),
    >>>     (4, 1), (4, 3), (4, 5), (4, 7),
    >>>     (5, 1),         (5, 5), (5, 7),
    >>>                     (6, 5), (6, 7),
    >>>     ])
    """

    global cob_list, cob_index

    cob_list_tmp = []
    plants_count_max = read_memory("unsigned int", 0x6A9EC0, 0x768, 0xB0)
    plants_offset = read_memory("unsigned int", 0x6A9EC0, 0x768, 0xAC)
    for i in range(plants_count_max):
        plant_dead = read_memory("bool", plants_offset + 0x141 + 0x14C * i)
        plant_crushed = read_memory("bool", plants_offset + 0x142 + 0x14C * i)
        plant_type = read_memory("int", plants_offset + 0x24 + 0x14C * i)
        if not plant_dead and not plant_crushed and plant_type == 47:
            cob_row = read_memory("int", plants_offset + 0x1C + 0x14C * i)
            cob_col = read_memory("int", plants_offset + 0x28 + 0x14C * i)
            cob_list_tmp.append((cob_col + 1, cob_row + 1))  # 优先按列排
    cob_list_tmp.sort()  # 排序
    cob_list_tmp = [(r, c) for c, r in cob_list_tmp]  # 再反过来

    cob_lock.acquire()  # 加锁

    cob_list = []
    cob_index = 0

    # 自动查找
    if cobs is None:
        cob_list = cob_list_tmp
        info("查找场上玉米炮 %s." % str(cob_list))

    # 手动更新
    else:
        cobs_not_exist = []
        for cob in cobs:
            if cob not in cob_list_tmp:
                cobs_not_exist.append(cob)
        if len(cobs_not_exist) > 0:
            error("玉米炮 %s 不存在." % str(cobs_not_exist))
        cob_list = cobs
        info("手动更新炮列表 %s." % str(cob_list))

    cob_lock.release()  # 解锁


### 用卡操作


def use_seed(seed, *crood):
    """
    用卡操作.

    @参数 seed(int/str): 卡槽第几格或者卡片名称.

    @参数 crood(int/tuple): 坐标, 两个分别表示 行/列 的数字或者一个 (行, 列) 元组, 数字均为整数.

    @示例:

    >>> Card(1, (2, 3))  # 将卡槽中的第 1 张卡片种在 2 行 3 列

    >>> Card(1, 2, 3)  # 同上

    >>> Card("樱桃", (5, 9))  # 将樱桃种在 5 行 9 列

    >>> Card("樱桃", 5, 9)  # 同上
    """

    if isinstance(seed, str):
        seed_type = get_seed_by_name(seed)
        slot_index = get_index_by_seed(seed_type)
    else:  # int
        seed_type = get_seed_by_index(seed)
        slot_index = seed

    # 墓碑/咖啡豆 理想种植坐标偏上约 30px
    if seed_type in (11, 35, 11 + 48, 35 + 48):
        row_fix = -0.3
    else:
        row_fix = 0
    if isinstance(crood[0], tuple):
        row, col = crood[0]
    else:
        row, col = crood
    row += row_fix

    mouse_lock.acquire()
    safe_click()
    click_seed(slot_index)
    click_grid((row, col))
    safe_click()
    mouse_lock.release()

    if isinstance(seed, str):
        info("向 %s 种植 %s 卡片." % (str(crood), str(seed)))
    else:  # int
        info("向 %s 种植卡槽第 %s 张卡片." % (str(crood), str(seed)))


### 用铲子操作


def use_shovel(*croods):
    """
    用铲子操作.

    @参数 croods(float/tuple): 坐标, 两个分别表示 行/列 的数字或者一至多个 (行, 列) 元组, 数字可为小数.

    @示例:

    >>> Shovel((3, 4))  # 铲掉 3 行 4 列的普通植物

    >>> Shovel(3, 4)  # 同上

    >>> Shovel((5 + 0.1, 6))  # 铲掉 5 行 6 列的南瓜头

    >>> Shovel((1, 9), (2, 9), (5, 9), (6, 9))  # 铲掉所有 9 列垫材
    """

    mouse_lock.acquire()
    safe_click()

    if isinstance(croods[0], tuple):
        for crood in croods:
            click_shovel()
            click_grid(crood)
    else:  # float/int
        click_shovel()
        click_grid(*croods)

    safe_click()
    mouse_lock.release()

    info("对格子 %s 使用铲子." % str(croods))


### 用炮操作


@functools.singledispatch
def fire_cob(*croods):
    """
    用炮操作.

    @参数 croods(float/tuple/list): 落点, 一至多个格式为 (行, 列) 的元组, 或者一个包含了这些元组的列表.

    @示例:

    >>> Pao((2, 9))

    >>> Pao(2, 9)

    >>> Pao((2, 9), (5, 9))

    >>> Pao((2, 9), (5, 9), (2, 9), (5, 9))

    >>> Pao([(2, 9), (5, 9), (2, 9), (5, 9)])
    """
    error("炮落点参数格式不正确.")


@fire_cob.register(int)
def _(fall_row, fall_col):
    global cob_list, cob_index
    cob_count = len(cob_list)
    if cob_count == 0:
        error("炮列表为空.")

    cob_lock.acquire()
    cob_row, cob_col = cob_list[cob_index]
    fire_cob_by_crood(cob_row, cob_col, fall_row, fall_col)
    cob_index += 1
    cob_index %= cob_count
    cob_lock.release()


@fire_cob.register(tuple)
def _(*fall_grids):
    global cob_list, cob_index
    cob_count = len(cob_list)
    if cob_count == 0:
        error("炮列表为空.")

    cob_lock.acquire()
    for grid in fall_grids:
        cob_row, cob_col = cob_list[cob_index]
        fall_row, fall_col = grid
        fire_cob_by_crood(cob_row, cob_col, fall_row, fall_col)
        cob_index += 1
        cob_index %= cob_count
    cob_lock.release()


@fire_cob.register(list)
def _(fall_grids):
    fire_cob(*fall_grids)


### 屋顶用炮操作

# 屋顶玉米炮飞行时间, 只考虑落点前场 7~9 列的情况
flying_time = {1: 359, 2: 362, 3: 364, 4: 367, 5: 369, 6: 372, 7: 373}


def get_cob_flying_time(cob_col, fall_col):
    # 暂不考虑 fall_col
    if cob_col in flying_time:
        return flying_time[cob_col]
    else:
        return 373


FLYING_TIME = 373


@running_in_thread
@functools.singledispatch
def fire_cob_on_roof(*croods):
    """
    屋顶修正飞行时间发炮. 参数格式与 `Pao()` 相同.

    此函数开新线程开销较大不适合精确键控, 只适用于前场落点 (约 7~9 列).
    """
    error("参数格式不正确.")


@fire_cob_on_roof.register(int)
def _(fall_row, fall_col):
    clock = game_clock()  # 参照时钟
    global cob_list, cob_index
    cob_count = len(cob_list)
    if cob_count == 0:
        error("炮列表为空.")

    cob_lock.acquire()
    cob_row, cob_col = cob_list[cob_index]
    cob_index += 1
    cob_index %= cob_count
    cob_lock.release()

    flying_time = get_cob_flying_time(cob_col, fall_col)
    while (game_clock() - clock) < (FLYING_TIME - flying_time):
        delay_a_little_time()
    fire_cob_by_crood(cob_row, cob_col, fall_row, fall_col)


@fire_cob_on_roof.register(tuple)
def _(*fall_grids):
    clock = game_clock()  # 参照时钟
    global cob_list, cob_index
    cob_count = len(cob_list)
    if cob_count == 0:
        error("炮列表为空.")

    # (flying_time, cob_row, cob_col, fall_row, fall_col) x n
    operate_list = []

    cob_lock.acquire()
    for grid in fall_grids:
        cob_row, cob_col = cob_list[cob_index]
        fall_row, fall_col = grid
        flying_time = get_cob_flying_time(cob_col, fall_col)
        operate_list.append((flying_time, cob_row, cob_col, fall_row, fall_col))
        cob_index += 1
        cob_index %= cob_count
    cob_lock.release()

    operate_list.sort()  # 根据飞行时间排序
    for op in reversed(operate_list):  # 逆序发射
        flying_time, cob_row, cob_col, fall_row, fall_col = op
        while (game_clock() - clock) < (FLYING_TIME - flying_time):
            delay_a_little_time()
        fire_cob_by_crood(cob_row, cob_col, fall_row, fall_col)


@fire_cob_on_roof.register(list)
def _(fall_grids):
    return fire_cob_on_roof(*fall_grids)


### 跳炮


def skip_cob_index(num):
    """
    按炮列表顺序跳过即将发射的一定数量的玉米炮, 通常用于 wave9/19 手动收尾.

    @参数 num(int): 数量.
    """
    global cob_list, cob_index

    cob_lock.acquire()
    cob_index += num
    cob_index %= len(cob_list)
    cob_lock.release()

    info("跳过炮列表中的 %d 门炮." % num)


### 直接发炮

# 炮身点击次数
CLICK_COUNT = 3


# 无视内置炮列表直接指定炮位和落点
def fire_cob_by_crood(cob_row, cob_col, fall_row, fall_col):

    mouse_lock.acquire()
    safe_click()
    for _ in range(CLICK_COUNT):
        # 点炮位置稍微偏离, 配合改内存解决炮粘手的问题
        click_grid(cob_row + 2 / 85, cob_col - 2 / 80)
    click_grid(fall_row, fall_col)
    safe_click()
    mouse_lock.release()

    info("从 (%d, %d) 向 (%d, %d) 发射玉米炮." % (cob_row, cob_col, fall_row, fall_col))


### 阻塞延时

# 当前波次刷新时间点
refresh_time_point = 0


def game_delay_for(time_cs):
    """
    游戏内部时钟延时. 相对于线程睡眠更准确.

    只能在战斗界面 `[[0x6A9EC0]+0x7FC] == 3` 使用, 游戏暂停时计时同样暂停.

    @参数 time_cs(int): 时间, 单位 cs, 精度 1.
    """

    if time_cs > 0:
        clock = game_clock()
        while (game_clock() - clock) < time_cs:
            delay_a_little_time()
    elif time_cs == 0:
        pass
    else:
        error("游戏延时参数不能小于零.")


def until_countdown(time_cs, hugewave=False):
    """
    等待直至刷新倒计时数值达到指定值.

    调用时需要保证上一波已经刷出. 该函数仅保留兼容旧式写法, 已不建议使用.

    @参数 time_cs(int): 倒计时数值, 单位 cs, 精度 1. 建议范围 [200, 1].

    第一波最早 599, 旗帜波最早 750.

    @参数 hugewave(bool): 是否为旗帜波, 默认不是. 可用 (波数 % 10 == 0) 判断.

    @示例:

    >>> Countdown(100)  # 非旗帜波 100cs 预判

    >>> Countdown(55, True)  # 旗帜波 55cs 预判

    >>> Countdown(95, wave % 10 == 0)  # 第 wave 波 95cs 预判
    """

    if not hugewave:
        while wave_countdown() > time_cs:
            delay_a_little_time()
    else:
        while wave_countdown() > 5:  # 这里用 5 而不用 4, 为了支持大波 750cs 预判
            delay_a_little_time()
        while huge_wave_countdown() > time_cs:
            delay_a_little_time()


# 倒计时(大波倒计时/初始倒计时)小于等于 200(750/599) 才算激活刷新
refresh_trigger = [750 if wave % 10 == 0 else 599 if wave == 1 else 200 for wave in range(1, 21)]


def until_relative_time_after_refresh(time_relative_cs, wave):
    """
    读内存获取刷新状况, 等待直至与设定波次刷新时间点的差值达到指定值.

    该函数须在每波操作开始时执行一次. 通常用于预判 (在设定波次刷新前调用), 也可以在设定波次刷新之后调用.

    @参数 time_relative_cs(int): 与刷新时间点的相对时间, 单位 cs, 精度 1. 建议范围 [-200, 400].

    第一波最早 -599, 旗帜波最早 -750. 为了方便可统一给每波设置类似 -180 等数值.

    因为脚本语言的精度问题, 设置成 -599/-750/-200 等过早的边界值时可能会因为实际达到时间已经超过该值而引起报错.

    @参数 wave(int): 波数. 用于内部判断刷新状况以及本波是否为旗帜波.

    @示例:

    >>> Prejudge(-100, wave)  # 第 wave 波刷新前 100cs 预判

    >>> Prejudge(-150, 20)  # 第 20 波预判炮炸珊瑚时机

    >>> Prejudge(300, wave)  # 第 wave 波刷新后 300cs

    >>> Prejudge(900 - 200 - 373, wave)  # 第 wave 波 900cs 波长激活炸时机
    """

    # 设定波次的刷新时间点
    global refresh_time_point

    _current_wave = current_wave()

    # 设定波次还未刷出
    if _current_wave < wave:

        # 等待设定预判波次的上一波刷出
        if _current_wave < wave - 1:
            while current_wave() < (wave - 1):
                delay_a_little_time()

        # 等到本波触发刷新
        is_huge_wave = wave % 10 == 0
        until_countdown(refresh_trigger[wave - 1], is_huge_wave)

        # 计算实际倒计时数值
        _wave_countdown = wave_countdown()
        _huge_wave_countdown = huge_wave_countdown()
        if is_huge_wave:
            if _wave_countdown in (4, 5):
                countdown = _huge_wave_countdown
            else:
                countdown = _wave_countdown - 5 + 750
        else:
            countdown = _wave_countdown

        # 计算刷新时间点(倒计时变为下一波初始值时)的时钟数值
        _game_clock = game_clock()
        refresh_time_point = _game_clock + countdown

        # 等待 目标相对时间 和 当前相对时间(即倒计时数值负值) 的差值
        time_to_wait = time_relative_cs + countdown
        if time_to_wait >= 0:
            game_delay_for(time_to_wait)
        else:
            error("第 %d 波设定时间 %d 已经过去, 当前相对时间 %d." % (wave, time_relative_cs, time_relative_cs - time_to_wait))

    # 设定波次已经刷出
    elif _current_wave == wave:

        # 获取当前时钟/倒计时数值/倒计时初始数值
        _game_clock = game_clock()
        _wave_countdown = wave_countdown()
        _wave_init_countdown = wave_init_countdown()

        if _wave_countdown <= 200:
            warning("设定波次 %d 的下一波即将刷新, 请调整脚本写法." % wave)

        # 计算刷新时间点(倒计时变为下一波初始值时)的时钟数值
        refresh_time_point = _game_clock - (_wave_init_countdown - _wave_countdown)

        # 等到设定时间
        time_to_wait = time_relative_cs - (_wave_init_countdown - _wave_countdown)
        if time_to_wait >= 0:
            game_delay_for(time_to_wait)
        else:
            error("第 %d 波设定时间 %d 已经过去, 当前相对时间 %d." % (wave, time_relative_cs, time_relative_cs - time_to_wait))

    # 设定波次的下一波已经刷出
    else:
        error("设定波次 %d 的下一波已经刷新, 请调整脚本写法." % wave)


def until_relative_time(time_relative_cs):
    """
    等待直至当前时间戳与本波刷新时间点的差值达到指定值.

    该函数需要配合 Prejudge() 使用. 多个 Until() 连用时注意调用顺序必须符合时间先后顺序.

    @参数 time_relative_cs(int): 相对时间, 单位 cs, 精度 1. 建议范围 [-200, 2300].

    @示例:

    >>> Until(-95)  # 刷新前 95cs

    >>> Until(180)  # 刷新后 180cs

    >>> Until(-150)  # 炮炸珊瑚可用时机

    >>> Until(444 - 373)  # 444cs 生效炮发射时机

    >>> Until(601 + 20 - 298)  # 加速波下一波 20cs 预判冰点咖啡豆时机

    >>> Until(601 + 5 - 100 - 320)  # 加速波下一波 5cs 预判冰复制冰种植时机

    >>> Until(1200 - 200 - 373)  # 1200cs 波长激活炸时机

    >>> Until(4500 - 5)  # 收尾波拖满时红字出现时机

    >>> Until(5500)  # 最后一大波白字出现时机
    """

    # while (game_clock() - refresh_time_point) < time_relative_cs:
    #     delay_a_little_time()

    time_to_wait = time_relative_cs - (game_clock() - refresh_time_point)
    if time_to_wait >= 0:
        game_delay_for(time_to_wait)
    else:
        error("设定时间 %d 已经过去, 当前相对时间 %d." % (time_relative_cs, time_relative_cs - time_to_wait))


### 自动收集线程

collect_items_dict = {
    "银币": 1,
    "金币": 2,
    "钻石": 3,
    "阳光": 4,
    "小阳光": 5,
    "大阳光": 6,
    "太阳": 4,
    "小太阳": 5,
    "大太阳": 6,
    "幼苗": 17,
    "花苗": 17,
    "盆栽": 17,
    "花盆": 17,
    "礼盒": 17,
    "礼品盒": 17,
    1: 1,
    2: 2,
    3: 3,
    4: 4,
    5: 5,
    6: 6,
    17: 17,
}

item_type_names = {1: "银币", 2: "金币", 3: "钻石", 4: "阳光", 5: "小阳光", 6: "大阳光", 17: "幼苗"}


@running_in_thread
def auto_collect(collect_items=None, interval_cs=12):
    """
    自动收集场上资源, 在单独的子线程运行.

    为了避免操作冲突, 当鼠标选中 卡片/铲子/玉米炮 时会暂停收集.

    建议把鼠标光标移出窗口外以避免可能出现的游戏卡顿.

    @参数 collect_items(list[str/int]): 包含需要收集的资源类型的列表, 默认所有.

    可选值物品名称 ["银币", "金币", "钻石", "阳光", "小阳光", "大阳光", "幼苗"] 或者代号 [1, 2, 3, 4, 5, 6, 17].

    @参数 interval_cs(float/int): 点击间隔, 单位 cs, 默认 12.

    @示例:

    >>> AutoCollect()  # 自动收集所有资源

    >>> AutoCollect(["钻石", "阳光", "小阳光", "大阳光"], 20)  # 只收集钻石和各种阳光, 间隔 0.2s
    """

    if collect_items is None:
        collect_items = ["银币", "金币", "钻石", "阳光", "小阳光", "大阳光", "幼苗"]
    collect_items_list = [collect_items_dict[item] for item in collect_items]

    while game_ui() != 3:
        thread_sleep_for(10)

    info("启动自动收集线程.")

    while game_ui() == 3:
        items_count = read_memory("int", 0x6A9EC0, 0x768, 0xF4)
        items_count_max = read_memory("int", 0x6A9EC0, 0x768, 0xE8)
        items_offset = read_memory("int", 0x6A9EC0, 0x768, 0xE4)

        if items_count == 0:
            thread_sleep_for(interval_cs)
            continue

        uncollected_item_count = 0
        for i in range(items_count_max):
            disappeared = read_memory("bool", items_offset + 0x38 + 0xD8 * i)
            collected = read_memory("bool", items_offset + 0x50 + 0xD8 * i)
            item_type = read_memory("int", items_offset + 0x58 + 0xD8 * i)
            if not disappeared and not collected and item_type in collect_items_list:
                uncollected_item_count += 1
        if uncollected_item_count == 0:
            thread_sleep_for(interval_cs * 10)  # 等久一点
            continue

        for i in range(items_count_max):
            if game_ui() != 3:
                break

            # while game_paused():  # 一直收集
            # while game_paused() or mouse_in_game():  # 鼠标移出时收集
            while game_paused() or (mouse_in_game() and mouse_have_something()):  # 没选中卡炮铲时收集
                thread_sleep_for(interval_cs)

            disappeared = read_memory("bool", items_offset + 0x38 + 0xD8 * i)
            collected = read_memory("bool", items_offset + 0x50 + 0xD8 * i)
            item_type = read_memory("int", items_offset + 0x58 + 0xD8 * i)
            if not disappeared and not collected and item_type in collect_items_list:

                item_x = read_memory("float", items_offset + 0x24 + 0xD8 * i)
                item_y = read_memory("float", items_offset + 0x28 + 0xD8 * i)
                if item_x >= 0.0 and item_y >= 70.0:
                    # write_memory("bool", True, items_offset + 0x50 + 0xd8 * i)
                    x, y = int(item_x + 30), int(item_y + 30)
                    mouse_lock.acquire()
                    safe_click()
                    left_click(x, y)
                    safe_click()
                    mouse_lock.release()

                    debug("收集位于 (%d, %d) 的物品 %s." % (x, y, item_type_names[item_type]))
                    thread_sleep_for(interval_cs)
                    # thread_sleep_for(random.randint(int(interval_cs * 0.5), int(interval_cs * 1.5)))  # 时间波动

    info("停止自动收集线程.")


### 自动存冰线程


def get_seeds_index(seed):
    """
    获取某种卡片在卡槽里的所有位置.

    @参数 seed(str): 卡片名称.

    @返回值 (list[int]): 某种卡片 (包括其模仿者) 在卡槽的数组下标列表.
    """
    seed = get_seed_by_name(seed)
    seed %= 48

    seed_indexes = []
    slots_count = read_memory("int", 0x6A9EC0, 0x768, 0x144, 0x24)
    slots_offset = read_memory("unsigned int", 0x6A9EC0, 0x768, 0x144)
    for i in range(slots_count):
        seed_type = read_memory("int", slots_offset + 0x5C + i * 0x50)
        seed_imitater_type = read_memory("int", slots_offset + 0x60 + i * 0x50)
        if seed_type == seed or (seed_type == 48 and seed_imitater_type == seed):
            seed_indexes.append(i)
    return seed_indexes


def get_plants_croods():
    """
    获取场上植物坐标.
    """
    croods = []
    plants_count_max = read_memory("unsigned int", 0x6A9EC0, 0x768, 0xB0)
    plants_offset = read_memory("unsigned int", 0x6A9EC0, 0x768, 0xAC)
    for i in range(plants_count_max):
        plant_dead = read_memory("bool", plants_offset + 0x141 + 0x14C * i)
        plant_crushed = read_memory("bool", plants_offset + 0x142 + 0x14C * i)
        if not plant_dead and not plant_crushed:
            plant_type = read_memory("int", plants_offset + 0x24 + 0x14C * i)
            plant_row = read_memory("int", plants_offset + 0x1C + 0x14C * i)
            plant_col = read_memory("int", plants_offset + 0x28 + 0x14C * i)
            croods.append((plant_type, plant_row + 1, plant_col + 1))
    return croods


def get_block_type(*crood):
    """
    获取格子类型. 1.lawn 2.bare 3.pool
    """
    if isinstance(crood[0], tuple):
        row, col = crood[0]
    else:
        row, col = crood
    row, col = row - 1, col - 1
    return read_memory("int", 0x6a9ec0, 0x768, 0x168 + row * 0x04 + col * 0x18)


# 存冰位
ice_spots = []
ice_total = 0


@running_in_thread
def auto_fill_ice(spots=None, total=0x7FFFFFFF):
    """
    设置存冰位置和要存的数量, 将会在单独的子线程运行自动存冰.

    @参数 spots(list): 存冰点, 包括若干个 (行, 列) 元组. 临时位在后. 默认为场上现有存冰的位置.

    @参数 total(int): 总个数, 默认无限.

    @示例:

    >>> IceSpots()

    >>> IceSpots([(6, 1), (5, 1), (2, 1), (1, 1)], 10)  # 往指定位置总计存 10 个冰
    """

    while game_ui() != 3:
        thread_sleep_for(1)

    info("启动自动存冰线程.")

    # 默认为场上现有存冰的位置
    if spots is None:
        spots = []
        plants = get_plants_croods()
        for plant_type, plant_row, plant_col in plants:
            if plant_type == get_seed_by_name("寒冰菇"):
                spots.append((plant_row, plant_col))
        if spots == []:
            error("场上没有寒冰菇, 退出自动存冰.")
            return

    global ice_spots, ice_total
    ice_spots = spots
    ice_total = total

    slots_offset = read_memory("unsigned int", 0x6A9EC0, 0x768, 0x144)

    ice_seeds_index = get_seeds_index("寒冰菇")  # 获取所有寒冰菇卡片的下标
    if ice_seeds_index == []:
        error("卡槽没有寒冰菇, 退出自动存冰.")

    filled = 0  # 已存数量
    while game_ui() == 3 and filled < total:

        while game_paused():
            thread_sleep_for(1)  # 等待暂停取消
        if game_ui() != 3:
            break

        croods_which_has_plant = []
        plants = get_plants_croods()
        for plant_type, plant_row, plant_col in plants:
            if plant_type not in (16, 30, 33):  # 睡莲/南瓜/花盆
                croods_which_has_plant.append((plant_row, plant_col))
                if plant_type == 47:  # 玉米炮占两格
                    croods_which_has_plant.append((plant_row, plant_col + 1))
        ice_spot_which_has_plant = [i for i in ice_spots if i in croods_which_has_plant]

        # 这句忘了有什么作用了 ...
        if game_ui() != 3 and ice_spot_which_has_plant == []:
            break

        if set(ice_spot_which_has_plant) >= set(spots):  # 存冰位植物满了
            ice_seeds_cd_left = []
            for i in ice_seeds_index:
                seed_usable = read_memory("bool", slots_offset + 0x70 + i * 0x50)
                seed_cd_past = read_memory("int", slots_offset + 0x4C + i * 0x50)
                seed_cd_total = read_memory("int", slots_offset + 0x50 + i * 0x50)
                ice_seeds_cd_left.append(0 if seed_usable else (seed_cd_total - seed_cd_past))
            if min(ice_seeds_cd_left) > 0:  # 冰卡都在冷却时等待最小的卡片 CD
                info("寒冰菇卡片冷却中, 等待 %d." % (min(ice_seeds_cd_left) + 1))
                game_delay_for(min(ice_seeds_cd_left) + 1)
                continue
            else:  # TODO 冰卡可用时等待正在用的咖啡豆
                thread_sleep_for(2)  # 延时以减小遍历植物的 CPU 消耗
                continue

        # 遍历指定的存冰位
        for spot in spots:
            if game_ui() != 3:
                break

            # 如果该位置无植物则尝试存冰
            if pvz_ver() == "1.0.0.1051":
                seed_ice_cost = read_memory("int", 0x69F2C0 + 14 * 0x24)
            else:
                seed_ice_cost = read_memory("int", 0x69F2D0 + 14 * 0x24)
            sun = read_memory("int", 0x6A9EC0, 0x768, 0x5560)
            if sun < seed_ice_cost:
                thread_sleep_for(1)
                continue
            block_type = get_block_type(spot)
            # 1.草地 2.裸地 3.泳池 16.睡莲 33.花盆
            if (spot not in ice_spot_which_has_plant \
                and sun >= seed_ice_cost \
                and ((block_type == 1 and game_scene not in (4, 5)) \
                    or (block_type == 1 and game_scene in (4, 5) and (33, spot[0], spot[1]) in plants) \
                    or (block_type == 3 and (16, spot[0], spot[1]) in plants))):
                # 遍历寒冰菇卡片, 通常为 原版冰 x 1 + 复制冰 x 1
                for i in ice_seeds_index:
                    seed_usable = read_memory("bool", slots_offset + 0x70 + i * 0x50)
                    if seed_usable:
                        while game_paused():
                            thread_sleep_for(1)  # 等待暂停取消
                        mouse_lock.acquire()
                        safe_click()
                        click_seed(i + 1)
                        click_grid(spot)
                        safe_click()
                        mouse_lock.release()
                        filled += 1
                        info("往 %s 存冰 (第 %d 张卡)." % (str(spot), i + 1))
                        game_delay_for(1)  # 等待内存数据更新
                        break
                    else:
                        thread_sleep_for(1)
                break  # 不管有没有成功都重新遍历存冰位以保证顺序(先永久位后临时位)
            else:
                pass

    info("停止自动存冰线程.")


def activate_ice():
    """
    点冰. 使用咖啡豆激活存冰, 优先点临时位.

    该函数需要配合自动存冰线程 IceSpots() 使用.
    """
    coffee_index = get_index_by_seed(35)  # 咖啡豆位置
    if coffee_index is None:
        error("卡槽没有咖啡豆, 点冰失败.")

    mouse_lock.acquire()
    safe_click()
    click_seed(coffee_index)
    for spot in reversed(ice_spots):  # 优先点临时位
        row, col = spot
        row -= 0.3  # 咖啡豆 理想种植坐标偏上约 30px
        click_grid((row, col))
    safe_click()
    mouse_lock.release()
