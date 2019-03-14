# coding=utf-8

"""
Process / Memory
"""

import ctypes
import struct
import threading

from . import logger
from . import win32


# window handle
pvz_hwnd = win32.HWND()

# process identifier
pvz_pid = win32.DWORD()

# process handle
pvz_handle = win32.HANDLE()


# C/C++ data types
cpp_typename = {
    "char": "b",
    "signed char": "b",
    "int8_t": "b",
    "unsigned char": "B",
    "byte": "B",
    "uint8_t": "B",
    "bool": "?",
    "short": "h",
    "int16_t": "h",
    "unsigned short": "H",
    "uint16_t": "H",
    "int": "i",
    "int32_t": "i",
    "intptr_t": "i",
    "unsigned int": "I",
    "uint32_t": "I",
    "uintptr_t": "I",
    "size_t": "I",
    "long": "l",
    "unsigned long": "L",
    "long long": "q",
    "int64_t": "q",
    "intmax_t": "q",
    "unsigned long long": "Q",
    "uint64_t": "Q",
    "uintmax_t": "Q",
    "float": "f",
    "double": "d",
}


def is_valid():
    """
    检查目标进程是否可用.

    @返回值 (bool): 未找到或者已经退出则返回 False.
    """

    if pvz_handle.value is None:
        return False

    exit_code = win32.DWORD()
    win32.GetExitCodeProcess(pvz_handle, ctypes.byref(exit_code))
    return exit_code.value == win32.STILL_ACTIVE


# TODO 读写内存时加锁
# memory_lock = threading.Lock()


def read_memory(data_type, *address, array=1):
    """
    读取内存数据.

    @参数 data_type(str): 数据类型, 取自 C/C++ 语言关键字, 可选值 ["char", "bool", "unsigned char", "short", "unsigned short", "int", "unsigned int", "long", "unsigned long", "long long", "unsigned long long", "float", "double"]

    @参数 address(int): 地址, 可为多级偏移.

    @参数 array(int): 数量. 默认一个, 大于一个时需要显式指定关键字参数.

    @返回值 (int/float/bool/tuple): 默认情况下返回单个数值, 获取多个数据则返回一个长度为指定数量的元组.

    @示例:

    >>> ReadMemory("int", 0x6a9ec0, 0x768, 0x5560)
    8000

    >>> ReadMemory("byte", 0x0041d7d0, array=3)
    (81, 131, 248)
    """

    if not is_valid():
        logger.critical("目标进程不可用, 读内存失败.")

    # memory_lock.acquire()

    level = len(address)  # 偏移级数
    offset = ctypes.c_void_p()  # 内存地址
    buffer = ctypes.c_uint()  # 中间数据缓冲
    bytes_read = ctypes.c_ulong()  # 已读字节数

    for i in range(level):
        offset.value = buffer.value + address[i]

        if i != level - 1:
            size = ctypes.sizeof(buffer)
            success = win32.ReadProcessMemory(pvz_handle, offset, ctypes.byref(buffer), size, ctypes.byref(bytes_read))
            if success == 0 or bytes_read.value != size:
                logger.critical(f"读取内存失败, 错误代码 {win32.GetLastError()}.")

        else:
            fmt_str = "<" + str(array) + cpp_typename[data_type]
            size = struct.calcsize(fmt_str)  # 目标数据大小
            buff = ctypes.create_string_buffer(size)  # 目标数据缓冲
            success = win32.ReadProcessMemory(pvz_handle, offset, ctypes.byref(buff), size, ctypes.byref(bytes_read))
            if success == 0 or bytes_read.value != size:
                logger.critical(f"读取内存失败, 错误代码 {win32.GetLastError()}.")

            result = struct.unpack(fmt_str, buff.raw)

    # memory_lock.release()

    logger.debug(f"读取内存, 类型 {data_type}, 地址 {address}, 数量 {array}, 结果 {result}.")
    if array == 1:
        return result[0]
    else:
        return result


### 以下几个读内存函数仅供内部使用


def read_memory_bool(address):
    offset = ctypes.c_void_p(address)
    buff = ctypes.c_bool(False)
    win32.ReadProcessMemory(pvz_handle, offset, ctypes.byref(buff), 1, None)
    return buff.value


def read_memory_byte(address):
    offset = ctypes.c_void_p(address)
    buff = ctypes.c_byte(0)
    win32.ReadProcessMemory(pvz_handle, offset, ctypes.byref(buff), 1, None)
    return buff.value


def read_memory_short(address):
    offset = ctypes.c_void_p(address)
    buff = ctypes.c_short(0)
    win32.ReadProcessMemory(pvz_handle, offset, ctypes.byref(buff), 2, None)
    return buff.value


def read_memory_int(address):
    offset = ctypes.c_void_p(address)
    buff = ctypes.c_int(0)
    win32.ReadProcessMemory(pvz_handle, offset, ctypes.byref(buff), 4, None)
    return buff.value


def read_memory_long(address):
    offset = ctypes.c_void_p(address)
    buff = ctypes.c_long(0)
    win32.ReadProcessMemory(pvz_handle, offset, ctypes.byref(buff), 4, None)
    return buff.value


def read_memory_longlong(address):
    offset = ctypes.c_void_p(address)
    buff = ctypes.c_longlong(0)
    win32.ReadProcessMemory(pvz_handle, offset, ctypes.byref(buff), 8, None)
    return buff.value


def read_memory_float(address):
    offset = ctypes.c_void_p(address)
    buff = ctypes.c_float(0.0)
    win32.ReadProcessMemory(pvz_handle, offset, ctypes.byref(buff), 4, None)
    return buff.value


def read_memory_double(address):
    offset = ctypes.c_void_p(address)
    buff = ctypes.c_double(0.0)
    win32.ReadProcessMemory(pvz_handle, offset, ctypes.byref(buff), 8, None)
    return buff.value


def write_memory(data_type, values, *address):
    """
    写入内存数据.

    @参数 data_type(str): 数据类型, 取自 C/C++ 语言关键字, 可选值 ["char", "bool", "unsigned char", "short", "unsigned short", "int", "unsigned int", "long", "unsigned long", "long long", "unsigned long long", "float", "double"]

    @参数 values(int/float/bool/list/tuple): 需要写入的数据, 多个数据采用列表或者元组形式.

    @参数 address(int): 地址, 可为多级偏移.

    @示例:

    >>> WriteMemory("int", 8000, 0x6a9ec0, 0x768, 0x5560)

    >>> WriteMemory("unsigned char", [0xb0, 0x01, 0xc3], 0x0041d7d0)
    """

    if not is_valid():
        logger.critical("目标进程不可用, 写内存失败.")

    # 将单个数据转换为列表方便统一处理
    if not isinstance(values, (tuple, list)):
        values = [values]

    # memory_lock.acquire()

    level = len(address)  # 偏移级数
    offset = ctypes.c_void_p()  # 内存地址
    buffer = ctypes.c_uint()  # 中间数据缓冲
    bytes_read = ctypes.c_ulong()  # 已读字节数
    bytes_written = ctypes.c_ulong()  # 已写字节数

    for i in range(level):
        offset.value = buffer.value + address[i]

        if i != level - 1:
            size = ctypes.sizeof(buffer)
            success = win32.ReadProcessMemory(pvz_handle, offset, ctypes.byref(buffer), size, ctypes.byref(bytes_read))
            if success == 0 or bytes_read.value != size:
                logger.critical(f"读取内存失败, 错误代码 {win32.GetLastError()}.")

        else:
            array = len(values)  # 目标数据的数量
            fmt_str = "<" + str(array) + cpp_typename[data_type]
            size = struct.calcsize(fmt_str)  # 目标数据大小
            buff = ctypes.create_string_buffer(size)  # 创建目标数据缓冲
            buff.value = struct.pack(fmt_str, *values)  # 将目标数据载入缓冲区
            success = win32.WriteProcessMemory(pvz_handle, offset, ctypes.byref(buff), size, ctypes.byref(bytes_written))
            if success == 0 or bytes_written.value != size:
                logger.critical(f"写入内存失败, 错误代码 {win32.GetLastError()}.")

    # memory_lock.release()

    logger.debug(f"写入内存, 类型 {data_type}, 数值 {values}, 地址 {address}.")


def open_process_by_window(class_name, window_name):
    """
    根据窗口标题打开进程.

    @参数 class_name(str): 窗口类名, 可省略为 None.

    @参数 window_name(str): 窗口标题, 可省略为 None.

    @返回值 (bool): 成功打开目标进程则返回 True.
    """

    global pvz_hwnd, pvz_pid, pvz_handle

    # 关闭之前已经打开的句柄
    if is_valid():
        win32.CloseHandle(pvz_handle)

    pvz_hwnd.value = None
    pvz_pid.value = 0
    pvz_handle.value = None

    pvz_hwnd.value = win32.FindWindowW(class_name, window_name)
    if pvz_hwnd.value is not None:
        win32.GetWindowThreadProcessId(pvz_hwnd, ctypes.byref(pvz_pid))
    if pvz_pid.value != 0:
        pvz_handle.value = win32.OpenProcess(win32.PROCESS_ALL_ACCESS, False, pvz_pid)

    result = pvz_handle.value is not None
    logger.info(f"查找游戏窗口, 类名 '{class_name}', 标题 '{window_name}', 结果 {result}.")
    return result


def find_pvz_1051():
    """
    查找原版植物大战僵尸游戏进程.

    @返回值 (bool): 查找成功返回 True, 没找到或是版本不符则返回 False.
    """

    # 不推荐省略窗口类名, 因为可能存在其他标题相同的窗口从而引起查找失误.
    # 已知所有的植物大战僵尸一代电脑版的窗口类名均为"MainWindow".
    # 原版英文版的窗口标题为"Plants vs. Zombies".
    if not open_process_by_window("MainWindow", "Plants vs. Zombies"):
        open_process_by_window("MainWindow", "植物大战僵尸中文版")

    if is_valid():
        if read_memory("unsigned int", 0x0042748E) == 0xFF563DE8:
            logger.info("已找到游戏 !!!")
            return True
        else:
            logger.warning("不支持的游戏版本 !!!")
            return False
    else:
        logger.warning("未找到游戏 !!!")
        return False


def active_pvz():
    """
    激活 PvZ 窗口. (后台时不激活.)
    """
    if pvz_hwnd.value is not None:
        win32.SetActiveWindow(pvz_hwnd)


def set_pvz_foreground():
    """
    激活并前台显示 PvZ 窗口.
    """
    if pvz_hwnd.value is not None:
        win32.SetForegroundWindow(pvz_hwnd)


def set_pvz_top_most(on=True):
    """
    置顶显示游戏窗口.

    @参数 on(bool): 是否开启.
    """
    if pvz_hwnd.value is not None:
        win32.SetWindowPos(
            pvz_hwnd,  #
            win32.HWND_TOPMOST if on else win32.HWND_NOTOPMOST,  #
            0,  #
            0,  #
            0,  #
            0,  #
            win32.SWP_NOMOVE | win32.SWP_NOSIZE | win32.SWP_SHOWWINDOW,  #
        )
