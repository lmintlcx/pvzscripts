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
    "bool": "?",
    "unsigned char": "B",
    "byte": "B",  # byte = unsigned char
    "short": "h",
    "unsigned short": "H",
    "int": "i",
    "unsigned int": "I",
    "long": "l",
    "unsigned long": "L",
    "long long": "q",
    "unsigned long long": "Q",
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
memory_lock = threading.Lock()


def read_memory(data_type, *address, array=1):
    """
    读取内存数据.

    @参数 data_type(str): 数据类型, 取自 C/C++ 语言关键字, 包括 ["char", "bool", "unsigned char", "short", "unsigned short", "int", "unsigned int", "long", "unsigned long", "long long", "unsigned long long", "float", "double"]

    @参数 address(int): 地址, 可为多级偏移.

    @参数 array(int): 数量. 默认一个, 大于一个时需要显式指定关键字.

    @返回值 (int/float/bool/tuple): 目标进程不可用时返回 None. 默认情况下返回单个数值, 获取多个数据则返回一个长度为指定数量的元组.

    @示例:

    >>> read_memory("int", 0x6a9ec0, 0x768, 0x5560)
    9990

    >>> read_memory("bool", 0x6a9ec0, 0x768, 0x54d4, array=33)
    (True, False, True, True, False, True, True, False, True, False, False, False, True, False, False, True, False, False, True, True, False, False, False, False, False, True, False, False, False, False, False, False, True)
    """

    if not is_valid():
        logger.error("Process not valid, read memory failed.")
        return

    # memory_lock.acquire()

    level = len(address)  # 偏移级数
    offset = ctypes.c_void_p()  # 内存地址
    buffer = ctypes.c_uint()  # 中间数据缓冲

    for i in range(level):
        offset.value = buffer.value + address[i]

        if i != level - 1:
            win32.ReadProcessMemory(pvz_handle, offset, ctypes.byref(buffer), 4, None)
        else:
            fmt_str = "<" + str(array) + cpp_typename[data_type]
            size = struct.calcsize(fmt_str)  # 目标数据大小
            buff = ctypes.create_string_buffer(size)  # 目标数据缓冲
            win32.ReadProcessMemory(pvz_handle, offset, buff, size, None)
            if array == 1:
                result = struct.unpack(fmt_str, buff.raw)[0]
            else:
                result = struct.unpack(fmt_str, buff.raw)

    # memory_lock.release()

    logger.debug(f"Read memory '{data_type}' {address} x {array} result {result}.")
    return result


def write_memory(data_type, values, *address):
    """
    写入内存数据.

    @参数 data_type(str): 数据类型, 取自 C/C++ 语言关键字, 包括 ["char", "bool", "unsigned char", "short", "unsigned short", "int", "unsigned int", "long", "unsigned long", "long long", "unsigned long long", "float", "double"]

    @参数 values(int/float/bool/list/tuple): 需要写入的数据, 多个数据采用列表或者元组形式.

    @参数 address(int): 地址, 可为多级偏移.

    目标进程不可用时立即返回.

    @示例:

    >>> write_memory("int", 9990, 0x6a9ec0, 0x768, 0x5560)

    >>> write_memory("unsigned char", [0xb0, 0x01, 0xc3], 0x0041d7d0)
    """

    if not is_valid():
        logger.error("Process not valid, write memory failed.")
        return

    # memory_lock.acquire()

    level = len(address)  # 偏移级数
    offset = ctypes.c_void_p()  # 内存地址
    buffer = ctypes.c_uint()  # 中间数据缓冲

    for i in range(level):
        offset.value = buffer.value + address[i]

        if i != level - 1:
            win32.ReadProcessMemory(pvz_handle, offset, ctypes.byref(buffer), 4, None)
        else:
            if not isinstance(values, (tuple, list)):
                values = [values]  # 将单个数据转换为列表
            array = len(values)  # 目标数据的数量
            fmt_str = "<" + str(array) + cpp_typename[data_type]
            size = struct.calcsize(fmt_str)  # 目标数据大小
            # buff = ctypes.create_string_buffer(size)  # 创建目标数据缓冲
            buff = struct.pack(fmt_str, *values)  # 将目标数据载入缓冲区
            win32.WriteProcessMemory(pvz_handle, offset, buff, size, None)

    # memory_lock.release()

    logger.debug(f"Write memory '{data_type}' {values} to {address}.")


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
    logger.info(f"Find window '{class_name}' '{window_name}' success? {result}!")
    return result


def find_pvz_1051():
    """
    查找原版植物大战僵尸游戏进程. 该函数会在导入本项目时自动运行.

    @返回值 (bool): 查找成功返回 True, 没找到或是版本不符则返回 False.
    """

    # 不推荐省略窗口类名, 因为可能存在其他标题相同的窗口从而引起查找失误.
    # 已知所有的植物大战僵尸一代电脑版的窗口类名均为"MainWindow".
    # 原版英文版的窗口标题为"Plants vs. Zombies".
    if not open_process_by_window("MainWindow", "Plants vs. Zombies"):
        open_process_by_window("MainWindow", "植物大战僵尸中文版")

    if is_valid():
        if read_memory("unsigned int", 0x0042748E) == 0xFF563DE8:
            logger.info("Game found !!!")
            return True
        else:
            logger.error("Unsupported game version !!!")
            return False
    else:
        logger.error("Game not found !!!")
        return False
