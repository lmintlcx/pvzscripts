# -*- coding: utf-8 -*-

"""
植物大战僵尸脚本挂机框架 Python vs. Zombies
"""

__author__ = "lmintlcx"
__copyright__ = "Copyright 2018, lmintlcx"
__credits__ = ["no_doudle"]
__license__ = "GPL"
__date__ = "2018-10-31"
__version__ = "3.0.1"
__maintainer__ = "lmintlcx"
__email__ = "lmintlcx@gmail.com"
__status__ = "Prototype"
__description__ = "PvZ Framework"


import logging
import platform
import sys
import ctypes
import struct
import time
import functools
import threading
import gc
import atexit


### init logger

_log_formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

_console_handler = logging.StreamHandler()
_console_handler.setFormatter(_log_formatter)
_console_handler.setLevel(logging.DEBUG)

_logger = logging.getLogger(__name__)
_logger.addHandler(_console_handler)
_logger.setLevel(logging.DEBUG)


def _enable_logger(on=True):
    """
    日志. 默认启用.

    @参数 on(bool): 是否启用.
    """

    if on:
        _logger.disabled = False
    else:
        _logger.disabled = True


def _set_logger_level(level="INFO"):
    """
    日志级别.

    @参数 level(str): 可选值 ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"].
    """

    logging_level = {
        "DEBUG": logging.DEBUG,
        "INFO": logging.INFO,
        "WARNING": logging.WARNING,
        "ERROR": logging.ERROR,
        "CRITICAL": logging.CRITICAL,
    }
    _logger.setLevel(logging_level[level])


### check operating system and python version

if platform.system() != "Windows":
    raise Exception("This module only works on Windows.")

if sys.hexversion < 0x03050000:
    raise Exception("Python 3.5 or newer is required to run this module.")


### win32 types

_POINTER = ctypes.POINTER
_SIZE_T = ctypes.c_size_t

from ctypes import wintypes

_BOOL = wintypes.BOOL
_DWORD = wintypes.DWORD
_INT = wintypes.INT
_UINT = wintypes.UINT
_LONG = wintypes.LONG
_HWND = wintypes.HWND
_HANDLE = wintypes.HANDLE
_HDC = wintypes.HDC
_LPVOID = wintypes.LPVOID
_LPCVOID = wintypes.LPCVOID
_LPCWSTR = wintypes.LPCWSTR
_LPDWORD = wintypes.LPDWORD
_POINT = wintypes.POINT
_LPPOINT = wintypes.LPPOINT
_RECT = wintypes.RECT
_LPRECT = wintypes.LPRECT
_WPARAM = wintypes.WPARAM
_LPARAM = wintypes.LPARAM

# typedef struct _SECURITY_ATTRIBUTES {
#   DWORD  nLength;
#   LPVOID lpSecurityDescriptor;
#   BOOL   bInheritHandle;
# } SECURITY_ATTRIBUTES, *PSECURITY_ATTRIBUTES, *LPSECURITY_ATTRIBUTES;
class _SECURITY_ATTRIBUTES(ctypes.Structure):
    _fields_ = [
        ("nLength", _DWORD),
        ("lpSecurityDescriptor", _LPVOID),
        ("bInheritHandle", _BOOL),
    ]


_LPSECURITY_ATTRIBUTES = ctypes.POINTER(_SECURITY_ATTRIBUTES)

# typedef DWORD (__stdcall *LPTHREAD_START_ROUTINE) (
#     [in] LPVOID lpThreadParameter
# );
_LPTHREAD_START_ROUTINE = ctypes.WINFUNCTYPE(_DWORD, _LPVOID)


### win32 dlls

_user32 = ctypes.windll.user32
_kernel32 = ctypes.windll.kernel32
_winmm = ctypes.windll.winmm
_gdi32 = ctypes.windll.gdi32


### win32 apis

# int MessageBoxW(
#   HWND    hWnd,
#   LPCWSTR lpText,
#   LPCWSTR lpCaption,
#   UINT    uType
# );
_MessageBoxW = _user32.MessageBoxW
_MessageBoxW.argtypes = [_HWND, _LPCWSTR, _LPCWSTR, _UINT]
_MessageBoxW.restype = _INT

# HWND FindWindowW(
#   LPCWSTR lpClassName,
#   LPCWSTR lpWindowName
# );
_FindWindowW = _user32.FindWindowW
_FindWindowW.argtypes = [_LPCWSTR, _LPCWSTR]
_FindWindowW.restype = _HWND

# DWORD GetWindowThreadProcessId(
#   HWND    hWnd,
#   LPDWORD lpdwProcessId
# );
_GetWindowThreadProcessId = _user32.GetWindowThreadProcessId
_GetWindowThreadProcessId.argtypes = [_HWND, _LPDWORD]
_GetWindowThreadProcessId.restype = _DWORD

# HANDLE OpenProcess(
#   DWORD dwDesiredAccess,
#   BOOL  bInheritHandle,
#   DWORD dwProcessId
# );
_OpenProcess = _kernel32.OpenProcess
_OpenProcess.argtypes = [_DWORD, _BOOL, _DWORD]
_OpenProcess.restype = _HANDLE

# BOOL GetExitCodeProcess(
#   HANDLE  hProcess,
#   LPDWORD lpExitCode
# );
_GetExitCodeProcess = _kernel32.GetExitCodeProcess
_GetExitCodeProcess.argtypes = [_HANDLE, _LPDWORD]
_GetExitCodeProcess.restype = _BOOL

# BOOL WINAPI CloseHandle(
#   _In_ HANDLE hObject
# );
_CloseHandle = _kernel32.CloseHandle
_CloseHandle.argtypes = [_HANDLE]
_CloseHandle.restype = _BOOL

# BOOL WINAPI ReadProcessMemory(
#   _In_  HANDLE  hProcess,
#   _In_  LPCVOID lpBaseAddress,
#   _Out_ LPVOID  lpBuffer,
#   _In_  SIZE_T  nSize,
#   _Out_ SIZE_T  *lpNumberOfBytesRead
# );
_ReadProcessMemory = _kernel32.ReadProcessMemory
_ReadProcessMemory.argtypes = [_HANDLE, _LPCVOID, _LPVOID, _SIZE_T, _POINTER(_SIZE_T)]
_ReadProcessMemory.restype = _BOOL

# BOOL WINAPI WriteProcessMemory(
#   _In_  HANDLE  hProcess,
#   _In_  LPVOID  lpBaseAddress,
#   _In_  LPCVOID lpBuffer,
#   _In_  SIZE_T  nSize,
#   _Out_ SIZE_T  *lpNumberOfBytesWritten
# );
_WriteProcessMemory = _kernel32.WriteProcessMemory
_WriteProcessMemory.argtypes = [_HANDLE, _LPVOID, _LPCVOID, _SIZE_T, _POINTER(_SIZE_T)]
_WriteProcessMemory.restype = _BOOL

# LPVOID WINAPI VirtualAllocEx(
#   _In_     HANDLE hProcess,
#   _In_opt_ LPVOID lpAddress,
#   _In_     SIZE_T dwSize,
#   _In_     DWORD  flAllocationType,
#   _In_     DWORD  flProtect
# );
_VirtualAllocEx = _kernel32.VirtualAllocEx
_VirtualAllocEx.argtypes = [_HANDLE, _LPVOID, _SIZE_T, _DWORD, _DWORD]
_VirtualAllocEx.restype = _LPVOID

# BOOL WINAPI VirtualFreeEx(
#   _In_ HANDLE hProcess,
#   _In_ LPVOID lpAddress,
#   _In_ SIZE_T dwSize,
#   _In_ DWORD  dwFreeType
# );
_VirtualFreeEx = _kernel32.VirtualFreeEx
_VirtualFreeEx.argtypes = [_HANDLE, _LPVOID, _SIZE_T, _DWORD]
_VirtualFreeEx.restype = _BOOL

# HANDLE CreateRemoteThread(
#   HANDLE                 hProcess,
#   LPSECURITY_ATTRIBUTES  lpThreadAttributes,
#   SIZE_T                 dwStackSize,
#   LPTHREAD_START_ROUTINE lpStartAddress,
#   LPVOID                 lpParameter,
#   DWORD                  dwCreationFlags,
#   LPDWORD                lpThreadId
# );
_CreateRemoteThread = _kernel32.CreateRemoteThread
_CreateRemoteThread.argtypes = [
    _HANDLE,
    _LPSECURITY_ATTRIBUTES,
    _SIZE_T,
    _LPTHREAD_START_ROUTINE,
    _LPVOID,
    _DWORD,
    _LPDWORD,
]
_CreateRemoteThread.restype = _HANDLE

# DWORD WaitForSingleObject(
#   HANDLE hHandle,
#   DWORD  dwMilliseconds
# );
_WaitForSingleObject = _kernel32.WaitForSingleObject
_WaitForSingleObject.argtypes = [_HANDLE, _DWORD]
_WaitForSingleObject.restype = _DWORD

# DWORD WINAPI GetLastError(void);
_GetLastError = _kernel32.GetLastError
_GetLastError.argtypes = []
_GetLastError.restype = _DWORD

# MMRESULT timeBeginPeriod(
#   UINT uPeriod
# );
_timeBeginPeriod = _winmm.timeBeginPeriod
_timeBeginPeriod.argtypes = [_UINT]
_timeBeginPeriod.restype = _UINT

# MMRESULT timeEndPeriod(
#   UINT uPeriod
# );
_timeEndPeriod = _winmm.timeEndPeriod
_timeEndPeriod.argtypes = [_UINT]
_timeEndPeriod.restype = _UINT

# HWND WindowFromPoint(
#   POINT Point
# );
_WindowFromPoint = _user32.WindowFromPoint
_WindowFromPoint.argtypes = [_POINT]
_WindowFromPoint.restype = _HWND

# BOOL GetWindowRect(
#   HWND   hWnd,
#   LPRECT lpRect
# );
_GetWindowRect = _user32.GetWindowRect
_GetWindowRect.argtypes = [_HWND, _LPRECT]
_GetWindowRect.restype = _BOOL

# BOOL GetCursorPos(
#   LPPOINT lpPoint
# );
_GetCursorPos = _user32.GetCursorPos
_GetCursorPos.argtypes = [_LPPOINT]
_GetCursorPos.restype = _BOOL

# BOOL SetCursorPos(
#   int X,
#   int Y
# );
_SetCursorPos = _user32.SetCursorPos
_SetCursorPos.argtypes = [_INT, _INT]
_SetCursorPos.restype = _BOOL

# LRESULT SendMessageW(
#   HWND   hWnd,
#   UINT   Msg,
#   WPARAM wParam,
#   LPARAM lParam
# );
_SendMessageW = _user32.SendMessageW
_SendMessageW.argtypes = [_HWND, _UINT, _WPARAM, _LPARAM]
_SendMessageW.restype = _LONG

# BOOL PostMessageW(
#   HWND   hWnd,
#   UINT   Msg,
#   WPARAM wParam,
#   LPARAM lParam
# );
_PostMessageW = _user32.PostMessageW
_PostMessageW.argtypes = [_HWND, _UINT, _WPARAM, _LPARAM]
_PostMessageW.restype = _BOOL

# HANDLE GetCurrentProcess(
# );
_GetCurrentProcess = _kernel32.GetCurrentProcess
_GetCurrentProcess.argtypes = []
_GetCurrentProcess.restype = _HANDLE

# BOOL SetPriorityClass(
#   HANDLE hProcess,
#   DWORD  dwPriorityClass
# );
_SetPriorityClass = _kernel32.SetPriorityClass
_SetPriorityClass.argtypes = [_HANDLE, _DWORD]
_SetPriorityClass.restype = _BOOL

# HDC GetDC(
#   HWND hWnd
# );
_GetDC = _user32.GetDC
_GetDC.argtypes = [_HWND]
_GetDC.restype = _HDC

# int GetDeviceCaps(
#   HDC hdc,
#   int index
# );
_GetDeviceCaps = _gdi32.GetDeviceCaps
_GetDeviceCaps.argtypes = [_HDC, _INT]
_GetDeviceCaps.restype = _INT

# int ReleaseDC(
#   HWND hWnd,
#   HDC  hDC
# );
_ReleaseDC = _user32.ReleaseDC
_ReleaseDC.argtypes = [_HWND, _HDC]
_ReleaseDC.restype = _INT


### win32 constants

_PROCESS_ALL_ACCESS = 0x001F0FFF
_STILL_ACTIVE = 0x00000103

_TIMERR_NOERROR = 0

_MEM_COMMIT = 0x00001000
_PAGE_EXECUTE_READWRITE = 0x40
_INFINITE = 0xFFFFFFFF
_MEM_RELEASE = 0x8000

_WM_LBUTTONDOWN = 0x0201
_WM_LBUTTONUP = 0x0202
_WM_RBUTTONDOWN = 0x0204
_WM_RBUTTONUP = 0x0205

_MK_LBUTTON = 0x0001
_MK_RBUTTON = 0x0002

_WM_KEYDOWN = 0x0100
_WM_KEYUP = 0x0101

_VK_ESCAPE = 0x1B
_VK_SPACE = 0x20

_VK_LEFT = 0x25
_VK_UP = 0x26
_VK_RIGHT = 0x27
_VK_DOWN = 0x28

_HIGH_PRIORITY_CLASS = 0x00000080

_HORZRES = 8
_DESKTOPHORZRES = 118


### test


def _hello_world():
    _MB_OKCANCEL = _UINT(0x00000001)
    _MessageBoxW(None, _LPCWSTR("Hello pvz.py!"), _LPCWSTR("test"), _MB_OKCANCEL)


### Process / Memory

# window handle
_pvz_hwnd = _HWND()

# process identifier
_pvz_pid = _DWORD()

# process handle
_pvz_handle = _HANDLE()


# C/C++ data types
_typename = {
    "char": "b",
    "bool": "?",
    "unsigned char": "B",
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


def _is_process_valid():
    """
    检查目标进程是否可用.

    @返回值 (bool): 未找到或者已经退出则返回 False.
    """

    if _pvz_handle.value is None:
        return False

    exit_code = _DWORD()
    _GetExitCodeProcess(_pvz_handle, ctypes.byref(exit_code))
    return exit_code.value == _STILL_ACTIVE


def _read_memory(data_type, *address, array=1):
    """
    读取内存数据.

    @参数 data_type(str): 数据类型, 取自 C/C++ 语言关键字, 包括 ["char", "bool", "unsigned char", "short", "unsigned short", "int", "unsigned int", "long", "unsigned long", "long long", "unsigned long long", "float", "double"]

    @参数 address(int): 地址, 可为多级偏移.

    @参数 array(int): 数量. 默认一个, 大于一个时需要显式指定关键字.

    @返回值 (int/float/bool/tuple): 目标进程不可用时返回 None. 默认情况下返回单个数值, 获取多个数据则返回一个长度为指定数量的元组.

    @示例:

    >>> _read_memory("int", 0x6a9ec0, 0x768, 0x5560)
    9990

    >>> _read_memory("bool", 0x6a9ec0, 0x768, 0x54d4, array=33)
    (True, False, True, True, False, True, True, False, True, False, False, False, True, False, False, True, False, False, True, True, False, False, False, False, False, True, False, False, False, False, False, False, True)
    """

    if not _is_process_valid():
        _logger.error("Process not valid, read memory failed.")
        return

    level = len(address)  # 偏移级数
    offset = ctypes.c_void_p()  # 内存地址
    buffer = ctypes.c_uint()  # 中间数据缓冲

    for i in range(level):
        offset.value = buffer.value + address[i]

        if i != level - 1:
            _ReadProcessMemory(_pvz_handle, offset, ctypes.byref(buffer), 4, None)
        else:
            fmt_str = "<" + str(array) + _typename[data_type]
            size = struct.calcsize(fmt_str)  # 目标数据大小
            buff = ctypes.create_string_buffer(size)  # 目标数据缓冲
            _ReadProcessMemory(_pvz_handle, offset, buff, size, None)
            if array == 1:
                result = struct.unpack(fmt_str, buff.raw)[0]
            else:
                result = struct.unpack(fmt_str, buff.raw)

    _logger.debug(f"Read memory '{data_type}' {address} x {array} result {result}.")
    return result


def _write_memory(data_type, values, *address):
    """
    写入内存数据.

    @参数 data_type(str): 数据类型, 取自 C/C++ 语言关键字, 包括 ["char", "bool", "unsigned char", "short", "unsigned short", "int", "unsigned int", "long", "unsigned long", "long long", "unsigned long long", "float", "double"]

    @参数 values(int/float/bool/list/tuple): 需要写入的数据, 多个数据采用列表或者元组形式.

    @参数 address(int): 地址, 可为多级偏移.

    目标进程不可用时立即返回.

    @示例:

    >>> _write_memory("int", 9990, 0x6a9ec0, 0x768, 0x5560)

    >>> _write_memory("unsigned char", [0xb0, 0x01, 0xc3], 0x0041d7d0)
    """

    if not _is_process_valid():
        _logger.error("Process not valid, write memory failed.")
        return

    level = len(address)  # 偏移级数
    offset = ctypes.c_void_p()  # 内存地址
    buffer = ctypes.c_uint()  # 中间数据缓冲

    for i in range(level):
        offset.value = buffer.value + address[i]

        if i != level - 1:
            _ReadProcessMemory(_pvz_handle, offset, ctypes.byref(buffer), 4, None)
        else:
            if not isinstance(values, (tuple, list)):
                values = [values]  # 将单个数据转换为列表
            array = len(values)  # 目标数据的数量
            fmt_str = "<" + str(array) + _typename[data_type]
            size = struct.calcsize(fmt_str)  # 目标数据大小
            buff = ctypes.create_string_buffer(size)  # 创建目标数据缓冲
            buff = struct.pack(fmt_str, *values)  # 将参数载入缓冲区
            _WriteProcessMemory(_pvz_handle, offset, buff, size, None)

    _logger.debug(f"Write memory '{data_type}' {values} to {address}.")


def _open_process_by_window(class_name, window_name):
    """
    根据窗口标题打开进程.

    @参数 class_name(str): 窗口类名, 可省略为 None.

    @参数 window_name(str): 窗口标题, 可省略为 None.

    @返回值 (bool): 成功打开目标进程则返回 True.
    """

    global _pvz_hwnd, _pvz_pid, _pvz_handle

    # 关闭之前已经打开的句柄
    if _is_process_valid():
        _CloseHandle(_pvz_handle)

    _pvz_hwnd.value = None
    _pvz_pid.value = 0
    _pvz_handle.value = None

    _pvz_hwnd.value = _FindWindowW(class_name, window_name)
    if _pvz_hwnd.value is not None:
        _GetWindowThreadProcessId(_pvz_hwnd, ctypes.byref(_pvz_pid))
    if _pvz_pid.value != 0:
        _pvz_handle.value = _OpenProcess(_PROCESS_ALL_ACCESS, False, _pvz_pid)

    result = _pvz_handle.value is not None
    _logger.info(f"Find window '{class_name}' '{window_name}' success? {result}!")
    return result


def _find_pvz_1051():
    """
    查找原版植物大战僵尸游戏进程. 该函数会在导入本模块时自动运行.

    @返回值 (bool): 查找成功返回 True, 没找到或是版本不符则返回 False.
    """

    # 不推荐省略窗口类名, 因为可能存在其他标题相同的窗口从而引起查找失误.
    # 已知所有的植物大战僵尸一代电脑版的窗口类名均为"MainWindow".
    # 原版英文版的窗口标题为"Plants vs. Zombies".
    if not _open_process_by_window("MainWindow", "Plants vs. Zombies"):
        _open_process_by_window("MainWindow", "植物大战僵尸中文版")

    if _is_process_valid():
        if _read_memory("unsigned int", 0x0042748E) == 0xFF563DE8:
            _logger.info("Game found !!!")
            return True
        else:
            _logger.error("Unsupported game version !!!")
            return False
    else:
        _logger.error("Game not found !!!")
        return False


### get game info


def _game_on():
    """
    @返回值 (bool): 游戏是否开启, 没开则会尝试查找一次.
    """
    if _is_process_valid():
        return True
    else:
        return _find_pvz_1051()


# 13. Survival: Endless
def _game_mode():
    """
    @返回值 (int): 游戏模式
    """
    return _read_memory("int", 0x6A9EC0, 0x7F8)


# 1: 主界面, 2: 选卡, 3: 正常游戏, 4: 僵尸进屋, 7: 模式选择
def _game_ui():
    """
    @返回值 (int): 游戏界面
    """
    return _read_memory("int", 0x6A9EC0, 0x7FC)


# 0: 白天, 1: 黑夜, 2: 泳池, 3: 浓雾, 4: 屋顶, 5: 月夜
def _game_scene():
    """
    @返回值 (int): 游戏场景
    """
    return _read_memory("int", 0x6A9EC0, 0x768, 0x554C)


def _game_paused():
    """
    @返回值 (bool): 游戏是否暂停
    """
    return _read_memory("bool", 0x6A9EC0, 0x768, 0x164)


def _mouse_in_game():
    """
    @返回值 (bool): 鼠标是否在游戏窗口内部
    """
    return _read_memory("bool", 0x6A9EC0, 0x768, 0x59)
    # return _read_memory("bool", 0x6A9EC0, 0x768, 0x138, 0x18)


def _mouse_have_something():
    """
    @返回值 (bool): 鼠标是否选中卡炮或铲子
    """
    return _read_memory("int", 0x6A9EC0, 0x768, 0x138, 0x30) in (1, 6, 8)


def _game_clock():
    """
    @返回值 (int): 一个内部时钟, 游戏暂停时停止计时.
    """
    return _read_memory("int", 0x6A9EC0, 0x768, 0x5568)


def _wave_countdown():
    """
    @返回值 (int): 下一波刷新倒计时, 触发刷新时重置为 200, 减少至 0 刷出下一波.
    """
    return _read_memory("int", 0x6A9EC0, 0x768, 0x559C)


def _huge_wave_countdown():
    """
    @返回值 (int): 大波刷新倒计时, 对于旗帜波, 刷新倒计时减少至 4 后停滞, 由该值代替减少.
    """
    return _read_memory("int", 0x6A9EC0, 0x768, 0x55A4)


def _current_wave():
    """
    @返回值 (int): 当前波数
    """
    return _read_memory("int", 0x6A9EC0, 0x768, 0x557C)


def _dance_clock():
    """
    @返回值 (int): 一个内部时钟, 可用于判断舞王/伴舞的舞蹈/前进.
    """
    return _read_memory("int", 0x6A9EC0, 0x838)


### Delay 延时机制


_high_precision = False

_refresh_time_point = 0


def _wait_for_game_start():
    """
    选卡后等待直至正式开始战斗.
    """
    while _game_ui() != 3:
        time.sleep(0.01)


def _enable_high_precision(on=True):
    """
    启用高精度键控, 缺点是会占满一个核心的 CPU 资源.

    @参数 on(bool): 是否启用
    """
    global _high_precision
    _high_precision = on


def _thread_sleep_for(time_cs):
    """
    线程睡眠. 依赖于操作系统线程切换时间片精度, 误差较大.

    @参数 time_cs(float): 时间, 单位 cs, 精度 0.1.
    """
    if time_cs > 0.0:
        time.sleep(time_cs / 100)


def _delay_a_little_time():
    """
    细微延时. 高精度情况下采用自旋等待, 否则阻塞等待.
    """
    if _high_precision:
        pass
    else:
        _thread_sleep_for(0.1)  # 1ms


def _game_delay_for(time_cs):
    """
    游戏内部时钟延时. 相对于线程睡眠更精确.

    只能在战斗界面([[0x6A9EC0]+0x7FC] == 3)使用. 游戏暂停时计时同样暂停.

    @参数 time_cs(int): 时间, 单位 cs, 精度 1.
    """
    if time_cs > 0:
        game_clock = _game_clock()
        while (_game_clock() - game_clock) < time_cs:
            _delay_a_little_time()


def _until_countdown(time_cs, hugewave=False):
    """
    等待直至本波刷新倒计时数值达到指定值. 调用时需要保证上一波已经刷出.

    @参数 time_cs(int): 倒计时数值, 单位 cs, 精度 1. 范围 [200, 0].

    @参数 hugewave(bool): 是否为旗帜波, 默认不是. 可用 (波数 % 10 == 0) 判断.

    @示例:

    >>> _until_countdown(95)  # 非旗帜波 95cs 预判

    >>> _until_countdown(55, True)  # 旗帜波 55cs 预判
    """
    if not hugewave:
        while _wave_countdown() > time_cs:
            _delay_a_little_time()
    else:
        while _wave_countdown() > 4:
            _delay_a_little_time()
        while _huge_wave_countdown() > time_cs:
            _delay_a_little_time()


def _until_relative_time_after_refresh(time_relative_cs, wave):
    """
    等待上一波刷新并且当前时间戳与本波刷新时间点的差值达到指定值.

    该函数只能在每波操作开始时执行一次. 用于重置本波刷新时间点数值.

    @参数 time_relative_cs(int): 相对时间, 单位 cs, 精度 1. 建议范围 [-200, 400].

    @参数 wave(int): 波数. 用于判断上一波是否已经刷出以及本波是否为旗帜波.

    @示例:

    >>> _until_relative_time_after_refresh(-95, wave)  # 95cs 预判

    >>> _until_relative_time_after_refresh(-55, wave)  # 55cs 预判

    >>> _until_relative_time_after_refresh(-150, 20)  # 第 20 波炮炸珊瑚

    >>> _until_relative_time_after_refresh(900 - 200 - 373, wave)  # 900cs 波长反应炸
    """
    global _refresh_time_point

    while _current_wave() < (wave - 1):
        _delay_a_little_time()

    huge_wave = wave % 10 == 0
    _until_countdown(200, huge_wave)

    game_clock = _game_clock()
    if huge_wave:
        countdown = _huge_wave_countdown()
    else:
        countdown = _wave_countdown()

    _game_delay_for(countdown + time_relative_cs)
    _refresh_time_point = game_clock + countdown


def _until_relative_time(time_relative_cs):
    """
    等待直至当前时间戳与本波刷新时间点的差值达到指定值.

    该函数需要配合 Prejudge() 使用.

    @参数 time_relative_cs(int): 相对时间, 单位 cs, 精度 1. 建议范围 [-200, 2300].

    @示例:

    >>> _until_relative_time(-15)  # 刷新前 15cs
    """
    while (_game_clock() - _refresh_time_point) < time_relative_cs:
        _delay_a_little_time()


### Mouse

_dpi_scale = 1.0


def _get_dpi_scale():
    """
    获取 DPI 缩放比例.
    """
    screen = _GetDC(None)
    if screen is not None:
        virtual_width = _GetDeviceCaps(screen, _HORZRES)
        physical_width = _GetDeviceCaps(screen, _DESKTOPHORZRES)
        _ReleaseDC(None, screen)
        scale = physical_width / virtual_width
    else:
        scale = 1.0

    global _dpi_scale
    _dpi_scale = scale
    _logger.info(f"Get DPI scale {scale}.")


def _MAKELONG(low, high):
    if _dpi_scale != 1.0:
        low, high = int(low / _dpi_scale), int(high / _dpi_scale)
    return ((high & 0xFFFF) << 16) | (low & 0xFFFF)


# 参数 x, y 分别为横坐标和纵坐标.
# 游戏以窗口化运行, 窗口内容分辨率为 800 x 600.
# 左上角 (0, 0), 右下角 (799, 599).


def _mouse_left_down(x, y):
    """
    鼠标左键按下.
    """
    coord = _MAKELONG(x, y)
    _PostMessageW(_pvz_hwnd, _WM_LBUTTONDOWN, _MK_LBUTTON, coord)


def _mouse_left_up(x, y):
    """
    鼠标左键弹起.
    """
    coord = _MAKELONG(x, y)
    _PostMessageW(_pvz_hwnd, _WM_LBUTTONUP, _MK_LBUTTON, coord)


def _mouse_left_click(x, y):
    """
    鼠标左键单击.

    @参数 x(int): 横坐标, 单位像素. 建议范围 [0, 799].

    @参数 y(int): 纵坐标, 单位像素. 建议范围 [0, 599].

    @示例:

    >>> _mouse_left_click(108, 42)  # 左键单击卡槽第一张卡片的位置
    """
    coord = _MAKELONG(x, y)
    _PostMessageW(_pvz_hwnd, _WM_LBUTTONDOWN, _MK_LBUTTON, coord)
    _PostMessageW(_pvz_hwnd, _WM_LBUTTONUP, _MK_LBUTTON, coord)


_mouse_click = _mouse_left_click


def _mouse_right_down(x, y):
    """
    鼠标右键按下.
    """
    coord = _MAKELONG(x, y)
    _PostMessageW(_pvz_hwnd, _WM_RBUTTONDOWN, _MK_RBUTTON, coord)


def _mouse_right_up(x, y):
    """
    鼠标右键弹起.
    """
    coord = _MAKELONG(x, y)
    _PostMessageW(_pvz_hwnd, _WM_RBUTTONUP, _MK_RBUTTON, coord)


def _mouse_right_click(x, y):
    """
    鼠标右键单击.

    @参数 x(int): 横坐标, 单位像素. 建议范围 [0, 799].

    @参数 y(int): 纵坐标, 单位像素. 建议范围 [0, 599].

    @示例:

    >>> _mouse_right_click(399, 299)  # 右键单击场地中间位置
    """
    coord = _MAKELONG(x, y)
    _PostMessageW(_pvz_hwnd, _WM_RBUTTONDOWN, _MK_RBUTTON, coord)
    _PostMessageW(_pvz_hwnd, _WM_RBUTTONUP, _MK_RBUTTON, coord)


# safe click


def _safe_click():
    """
    安全右键. 用于避免操作冲突.
    """
    _mouse_right_click(0, 0)


# special button click


def _special_button_click(x, y):
    """
    适用于模仿者按钮和菜单按钮的特殊点击.

    @参数 x(int): 横坐标, 单位像素. 建议范围 [0, 799].

    @参数 y(int): 纵坐标, 单位像素. 建议范围 [0, 599].

    @示例:

    >>> _special_button_click(490, 550)  # 选卡界面左键单击模仿者卡片
    """
    point = _POINT()
    _GetCursorPos(ctypes.byref(point))
    x_0 = point.x
    y_0 = point.y
    rect = _RECT()
    _GetWindowRect(_pvz_hwnd, ctypes.byref(rect))
    border_width = (rect.right - rect.left - 800) / 2
    title_height = rect.bottom - rect.top - border_width - 600
    x_1 = int(rect.left + border_width + x)
    y_1 = int(rect.top + title_height + y)
    _SetCursorPos(x_1, y_1)
    time.sleep(0.02)
    _SetCursorPos(x_1, y_1)

    window_hwnd = _WindowFromPoint(point)
    if window_hwnd == _pvz_hwnd.value:
        _mouse_left_click(x, y)
        time.sleep(0.01)
    else:
        _mouse_left_click(x, y)
        time.sleep(0.02)
        _mouse_left_click(0, 0)

    _SetCursorPos(x_0, y_0)


### Keyboard


def _press_esc():
    """
    敲击 退出 键.
    """
    _PostMessageW(_pvz_hwnd, _WM_KEYDOWN, _VK_ESCAPE, 0)
    _PostMessageW(_pvz_hwnd, _WM_KEYUP, _VK_ESCAPE, 0)


def _press_space():
    """
    敲击 空格 键.
    """
    _PostMessageW(_pvz_hwnd, _WM_KEYDOWN, _VK_SPACE, 0)
    _PostMessageW(_pvz_hwnd, _WM_KEYUP, _VK_SPACE, 0)


def _press_left():
    """
    敲击 左方向 键.
    """
    _PostMessageW(_pvz_hwnd, _WM_KEYDOWN, _VK_LEFT, 0)
    _PostMessageW(_pvz_hwnd, _WM_KEYUP, _VK_LEFT, 0)


def _press_up():
    """
    敲击 上方向 键.
    """
    _PostMessageW(_pvz_hwnd, _WM_KEYDOWN, _VK_UP, 0)
    _PostMessageW(_pvz_hwnd, _WM_KEYUP, _VK_UP, 0)


def _press_right():
    """
    敲击 右方向 键.
    """
    _PostMessageW(_pvz_hwnd, _WM_KEYDOWN, _VK_RIGHT, 0)
    _PostMessageW(_pvz_hwnd, _WM_KEYUP, _VK_RIGHT, 0)


def _press_down():
    """
    敲击 下方向 键.
    """
    _PostMessageW(_pvz_hwnd, _WM_KEYDOWN, _VK_DOWN, 0)
    _PostMessageW(_pvz_hwnd, _WM_KEYUP, _VK_DOWN, 0)


def _press_key(key):
    """
    敲击按键. 可选值 '0' - '9' 'A' - 'Z'
    """
    code = ord(key)
    _PostMessageW(_pvz_hwnd, _WM_KEYDOWN, code, 0)
    _PostMessageW(_pvz_hwnd, _WM_KEYUP, code, 0)


### Select Seeds


_seeds_string = [
    ["Peashooter", "豌豆射手", "豌豆", "单发"],
    ["Sunflower", "向日葵", "小向", "花"],
    ["Cherry Bomb", "樱桃炸弹", "樱桃", "炸弹", "爆炸", "草莓", "樱"],
    ["Wall-nut", "坚果墙", "坚果", "墙果", "柠檬圆"],
    ["Potato Mine", "土豆雷", "土豆", "地雷", "土豆地雷"],
    ["Snow Pea", "寒冰射手", "冰豆", "冰豌豆", "雪花豌豆", "雪花"],
    ["Chomper", "大嘴花", "大嘴", "食人花", "食"],
    ["Repeater", "双发射手", "双发", "双发豌豆"],
    ["Puff-shroom", "小喷菇", "小喷", "喷汽蘑菇", "免费蘑菇", "炮灰菇", "小蘑菇", "免费货", "免费"],
    ["Sun-shroom", "阳光菇", "阳光", "阳光蘑菇"],
    ["Fume-shroom", "大喷菇", "大喷", "烟雾蘑菇", "大蘑菇", "喷子", "喷"],
    ["Grave Buster", "墓碑吞噬者", "墓碑", "墓碑苔藓", "苔藓", "咬咬碑"],
    ["Hypno-shroom", "魅惑菇", "魅惑", "迷惑菇", "催眠蘑菇", "催眠", "花蘑菇", "毒蘑菇"],
    ["Scaredy-shroom", "胆小菇", "胆小", "胆怯蘑菇", "胆小鬼蘑菇", "杠子蘑菇"],
    ["Ice-shroom", "寒冰菇", "冰菇", "冷冻蘑菇", "冰蘑菇", "面瘫", "冰"],
    ["Doom-shroom", "毁灭菇", "核蘑菇", "核弹", "核武", "毁灭", "末日蘑菇", "末日菇", "末日", "核"],
    ["Lily Pad", "睡莲", "荷叶", "莲叶"],
    ["Squash", "窝瓜", "倭瓜", "窝瓜大叔", "倭瓜大叔", "镇压者"],
    ["Threepeater", "三线射手", "三线", "三头豌豆", "三头", "三管", "管"],
    ["Tangle Kelp", "缠绕海草", "海草", "缠绕海藻", "海藻", "毛线"],
    ["Jalapeno", "火爆辣椒", "辣椒", "墨西哥胡椒", "辣", "椒"],
    ["Spikeweed", "地刺", "刺", "尖刺", "尖刺杂草", "棘草"],
    ["Torchwood", "火炬树桩", "火树", "火炬", "树桩", "火炬木", "火"],
    ["Tall-nut", "高坚果", "搞基果", "高建国", "巨大墙果", "巨大", "高墙果", "大土豆"],
    ["Sea-shroom", "海蘑菇", "水兵菇"],
    ["Plantern", "路灯花", "灯笼", "路灯", "灯笼草", "灯笼花", "吐槽灯", "灯"],
    ["Cactus", "仙人掌", "小仙", "掌"],
    ["Blover", "三叶草", "三叶", "风扇", "吹风", "愤青"],
    ["Split Pea", "裂荚射手", "裂荚", "双头", "分裂豌豆", "双头豌豆"],
    ["Starfruit", "杨桃", "星星", "星星果", "五角星", "1437", "桃"],
    ["Pumpkin", "南瓜头", "南瓜", "南瓜罩", "套"],
    ["Magnet-shroom", "磁力菇", "磁铁", "磁力蘑菇", "磁"],
    ["Cabbage-pult", "卷心菜投手", "包菜", "卷心菜", "卷心菜投抛者"],
    ["Flower Pot", "花盆", "盆"],
    ["Kernel-pult", "玉米投手", "玉米", "黄油投手", "玉米投抛者"],
    ["Coffee Bean", "咖啡豆", "咖啡", "兴奋剂", "春药"],
    ["Garlic", "大蒜", "蒜"],
    ["Umbrella Leaf", "叶子保护伞", "莴苣", "白菜", "保护伞", "伞叶", "叶子", "伞", "叶"],
    ["Marigold", "金盏花", "金盏草", "金盏菊", "吐钱花"],
    ["Melon-pult", "西瓜投手", "西瓜", "绿皮瓜", "瓜", "西瓜投抛者"],
    ["Gatling Pea", "机枪射手", "机枪", "加特林豌豆", "加特林", "格林豌豆", "枪"],
    ["Twin Sunflower", "双子向日葵", "双子", "双向", "双花"],
    ["Gloom-shroom", "忧郁蘑菇", "忧郁", "忧郁菇", "章鱼", "曾哥", "曾哥蘑菇", "曾"],
    ["Cattail", "香蒲", "猫尾", "猫尾香蒲", "小猫", "猫"],
    ["Winter Melon", "冰瓜", "冰西瓜", "冰冻西瓜"],
    ["Gold Magnet", "吸金磁", "吸金", "吸金草", "金磁铁"],
    ["Spikerock", "地刺王", "钢刺", "钢地刺", "尖刺岩石", "石荆棘"],
    ["Cob Cannon", "玉米加农炮", "玉米炮", "加农炮", "春哥", "春哥炮", "炮", "春", "神"],
]

# 确保没有重复项, 发布时注释掉
# _seeds_string_total = []
# for items in _seeds_string:
#     _seeds_string_total += items
# assert len(_seeds_string_total) == len(set(_seeds_string_total))


_seeds_imitater_string = ["Imitater", "模仿者", "模仿", "复制"]

# 卡槽格数, 选卡和用卡函数需要, 在导入脚本时和选卡操作前更新
_slots_count = 10


# 场景地图, 点击场上格子相关函数需要, 在导入脚本时和选卡操作前更新
# 0. day
# 1. night
# 2. pool
# 3. fog
# 4. roof
# 5. moon
# 6. mushroom garden
# 7. zen garden
# 8. aquarium garden
# 9. tree of wisdom
_game_scene = 2


# (row, col, imitater) * n for 1 <= n <= 10
_seeds_list = []

# 卡片序号, 目前用到的仅有咖啡豆
_seeds_index = [None] * (48 * 2)


def _update_seeds_list():
    """
    更新卡槽卡片列表和常用卡片序号. 该函数须在点击"Let's Rock!"后调用.
    """
    seeds_list = []
    slots_count = _read_memory("int", 0x6A9EC0, 0x768, 0x144, 0x24)
    slots_offset = _read_memory("unsigned int", 0x6A9EC0, 0x768, 0x144)
    for i in range(slots_count):
        seed_type = _read_memory("int", slots_offset + 0x5C + i * 0x50)
        seed_imitater_type = _read_memory("int", slots_offset + 0x60 + i * 0x50)
        if seed_type == 48:
            row, col = divmod(seed_imitater_type, 8)
            imitater = True
        else:
            row, col = divmod(seed_type, 8)
            imitater = False
        seed = row + 1, col + 1, imitater
        seeds_list.append(seed)

    _logger.info(f"Update seeds list {seeds_list}.")
    global _seeds_list
    _seeds_list = seeds_list

    seeds_index = [None] * (48 * 2)
    for index, seed in enumerate(seeds_list):
        row, col, imitater = seed
        i = (row - 1) * 8 + (col - 1) + (48 if imitater else 0)
        seeds_index[i] = index

    _logger.info(f"Update seeds index {seeds_index}.")
    global _seeds_index
    _seeds_index = seeds_index


def _select_seed_by_crood(row, col, imitater=False):
    """
    选择单张卡片.

    @参数 row(int): 行

    @参数 col(int): 列

    @参数 imitater(bool): 是否为模仿者
    """

    if imitater:
        if row not in (1, 2, 3, 4, 5):
            raise Exception("'row' out of range.")
        if col not in (1, 2, 3, 4, 5, 6, 7, 8):
            raise Exception("'col' out of range.")
    else:
        if row not in (1, 2, 3, 4, 5, 6):
            raise Exception("'row' out of range.")
        if col not in (1, 2, 3, 4, 5, 6, 7, 8):
            raise Exception("'col' out of range.")

    # (50, 160) 为左上角卡片中心坐标, (215, 160) 为模仿者选卡界面左上角卡片中心坐标, 单张卡片宽度约 50px 高度约 70px.
    # 对于模仿者卡片, 需要把鼠标移动到目标位置 (490, 550) 才能成功点击, 单击完毕后移回原位, 延迟 0.3s 等待界面出现再选卡.
    # 每次选完卡均等待 0.2s.

    if imitater:
        _special_button_click(490, 550)
        time.sleep(0.3)
        x = 215 + (col - 1) * 51
        y = 160 + (row - 1) * 72
    else:
        x = 50 + (col - 1) * 53
        y = 160 + (row - 1) * 70
    _mouse_left_click(x, y)
    time.sleep(0.2)

    if imitater:
        im = _seeds_imitater_string[0] + " "
    else:
        im = ""
    seed = _seeds_string[(row - 1) * 8 + (col - 1)][0]
    _logger.info(f"Select seed {im}{seed}.")


@functools.singledispatch
def _seed_to_crood(seed):
    """
    卡片转换为 (行, 列, 模仿者) 的标准形式.
    
    根据参数类型选择不同的实现.

    @参数 seed(int/tuple/str): 卡片

    @示例:

    >>> _seed_to_crood(14 + 48)
    (2, 7, True)

    >>> _seed_to_crood((2, 7, True))
    (2, 7, True)

    >>> _seed_to_crood("复制冰")
    (2, 7, True)

    """
    raise Exception(f"Unknown seed type {type(seed)}.")


@_seed_to_crood.register(int)
def _(seed):
    if seed == 1437:
        row = 4
        col = 6
        imitater = False
    else:
        imitater = seed >= 48
        index = seed % 48
        row, col = divmod(index, 8)
        row += 1
        col += 1
    return row, col, imitater


@_seed_to_crood.register(tuple)
def _(seed):
    if len(seed) == 2:
        row, col = seed
        imitater = False
    elif len(seed) == 3:
        row, col, im = seed
        imitater = im not in (False, 0)
    return row, col, imitater


@_seed_to_crood.register(str)
def _(seed):

    imitater = False
    for im in _seeds_imitater_string:
        if seed.find(im) != -1:
            imitater = True
            seed = seed.strip(im).strip()
            break

    index = -1
    for i in range(48):
        if seed in _seeds_string[i]:
            index = i
            break
    if index == -1:
        raise Exception(f"Unknown seed: {seed}.")

    row, col = divmod(index, 8)
    row += 1
    col += 1
    return row, col, imitater


def _select_all_seeds(seeds=None):
    """
    选择所有卡片.
    """

    # 更新卡槽格数, 顺便更新场景地图
    global _slots_count, _game_scene
    _slots_count = _read_memory("int", 0x6A9EC0, 0x768, 0x144, 0x24)
    _game_scene = _read_memory("int", 0x6A9EC0, 0x768, 0x554C)

    # 默认八张紫卡和两张免费卡
    if seeds is None:
        seeds = [40, 41, 42, 43, 44, 45, 46, 47, 8, 8 + 48][0:_slots_count]

    if len(seeds) != _slots_count:
        raise Exception(f"Seeds count {len(seeds)} != slots count {_slots_count}.")

    # 卡片列表转换为标准形式
    seeds_list = [_seed_to_crood(seed) for seed in seeds]
    _logger.info(f"Seeds {seeds} transfer to {seeds_list}.")

    # TODO : check if exact match
    while _read_memory("int", 0x6A9EC0, 0x774, 0xD24) < _slots_count:
        _logger.info(f"Incomplete seeds selection, try again now.")

        # clear all seeds in slots
        for _ in range(10):
            _mouse_left_click(108, 42)
            time.sleep(0.1)
        time.sleep(0.2)

        # select all seeds
        for seed in seeds_list:
            row, col, imitater = seed
            _select_seed_by_crood(row, col, imitater)
        time.sleep(0.8)


def _lets_rock():
    # if still in seeds select ui
    while _read_memory("bool", 0x6A9EC0, 0x768, 0x15C, 0x2C):
        _mouse_left_down(234, 567)
        time.sleep(0.1)
        _mouse_left_up(234, 567)
        time.sleep(0.2)
        # if there is dialog
        while _read_memory("bool", 0x6A9EC0, 0x320, 0x94, 0x54):
            _mouse_left_click(320, 400)
            time.sleep(0.3)


# (row, col) x n
_cob_list = []

# index of current cob in list
_cob_index = 0

# 修改以上两个变量时加锁
_cob_lock = threading.Lock()


# TODO 排序
def _update_cob_cannon_list(cobs=None):
    """
    更新玉米加农炮列表.
    
    选卡时自动调用, 空参数则自动找炮. 若需要自定义炮组请在选卡函数后面使用.

    如果出现炮落点位于自身附近快速点击无法发射的现象可通过调整炮序解决.

    @参数 cobs(list): 加农炮列表, 包括若干个 (行, 列) 元组, 以后轮坐标为准.

    @示例:

    >>> _update_cob_cannon_list()

    >>> _update_cob_cannon_list([(3, 1), (4, 1), (3, 3), (4, 3), (1, 5), (2, 5), (3, 5), (4, 5), (5, 5), (6, 5)])
    """

    global _cob_list, _cob_index

    if cobs is not None:
        _cob_lock.acquire()
        _cob_list = cobs
        _cob_index = 0
        _cob_lock.release()

    else:
        _cob_lock.acquire()
        _cob_list = []
        plant_count_max = _read_memory("unsigned int", 0x6A9EC0, 0x768, 0xB0)
        plant_offset = _read_memory("unsigned int", 0x6A9EC0, 0x768, 0xAC)
        for i in range(plant_count_max):
            plant_disappeared = _read_memory("bool", plant_offset + 0x141 + 0x14C * i)
            plant_crushed = _read_memory("bool", plant_offset + 0x142 + 0x14C * i)
            plant_type = _read_memory("int", plant_offset + 0x24 + 0x14C * i)
            if not plant_disappeared and not plant_crushed and plant_type == 47:
                plant_row = _read_memory("int", plant_offset + 0x1C + 0x14C * i)
                plant_col = _read_memory("int", plant_offset + 0x28 + 0x14C * i)
                cob = (plant_row + 1, plant_col + 1)
                _cob_list.append(cob)
        _cob_list.sort()
        _cob_index = 0
        _cob_lock.release()

    _logger.info(f"Update Cob Cannon list {_cob_list}.")


def _select_seeds_and_lets_rock(seeds=None):
    """
    选卡并开始游戏.

    选择所有卡片. 点击开始. 更新加农炮列表. 等待开场红字消失.

    @参数 seeds(list): 卡片列表, 参数为空默认选择八张紫卡和两张免费卡.
    
    列表长度需与卡槽格数相同. 单张卡片 seed 可用 int/tuple/str 表示, 不同表示方法可混用.

    seed(int): 卡片序号, 0 为豌豆射手, 47 为玉米加农炮, 对于模仿者这个数字再加上 48.

    seed(tuple): 卡片位置, 用 (行, 列, 是否模仿者) 表示, 第三项可省略, 默认非模仿者.

    seed(str): 卡片名称, 参考 _seeds_string, 包含了一些常用名字.

    @示例:

    >>> _select_all_seeds()

    >>> _select_all_seeds([14, 14 + 48, 17, 2, 3, 30, 33, 13, 9, 8])

    >>> _select_all_seeds([(2, 7), (2, 7, True), (3, 2), (1, 3), (1, 4), (4, 7), (5, 2), (2, 6), (2, 2), (2, 1),])

    >>> _select_all_seeds(["寒冰菇", "复制冰", "窝瓜", "樱桃", "坚果", "南瓜", "花盆", "胆小", "阳光", "小喷"])
    """
    gc.collect()

    _select_all_seeds(seeds)
    _lets_rock()
    _update_cob_cannon_list()
    _update_seeds_list()
    _wait_for_game_start()


### Scene Click


# 完整的鼠标操作前加锁
_mouse_lock = threading.Lock()


def _click_seed(index):
    """
    点击卡槽中的卡片.

    @参数 index(int): 第几格
    """

    # 自动针对不同卡槽格数使用不同的坐标转换过程.
    if _slots_count == 10:
        x = 63 + 51 * index
    elif _slots_count == 9:
        x = 63 + 52 * index
    elif _slots_count == 8:
        x = 61 + 54 * index
    elif _slots_count == 7:
        x = 61 + 59 * index
    else:
        x = 61 + 59 * index
    y = 42
    _mouse_left_click(x, y)


def _click_shovel():
    """
    点击铲子.
    """

    # 自动针对不同卡槽格数使用不同的坐标转换过程.
    if _slots_count == 10:
        x = 640
    elif _slots_count == 9:
        x = 600
    elif _slots_count == 8:
        x = 570
    elif _slots_count == 7:
        x = 550
    else:
        x = 490
    y = 42
    _mouse_left_click(x, y)


# TODO int/tuple
def _click_grid(row, col):
    """
    点击场上格点.

    @参数 row(float): 行, 可为小数

    @参数 col(float): 列, 可为小数
    """

    # 自动针对不同场地使用不同的坐标转换过程.
    x = 80 * col
    if _game_scene in (2, 3):
        y = 55 + 85 * row
    elif _game_scene in (4, 5):
        if col > 5.5:
            y = 50 + 85 * row
        else:
            y = 50 + 85 * row + 20 * (5.5 - col)
    else:
        y = 40 + 100 * row

    x, y = int(x), int(y)
    _mouse_left_click(x, y)


def _use_seed(index, row, col):
    """
    用卡操作.

    @参数 index(int): 卡槽第几张卡片

    @参数 row(float): 作用行

    @参数 col(float): 作用列

    @示例:

    >>> _use_seed(10, 2, 9)  # 将第 10 张卡片种在 2 行 9 列
    """
    _mouse_lock.acquire()
    _safe_click()
    _click_seed(index)
    _click_grid(row, col)
    _mouse_lock.release()

    _logger.info(f"Use seed {index} to {(row, col)}.")


@functools.singledispatch
def _fire_cob(*params):
    """
    用炮操作.

    @参数 params(int/tuple/list): 落点.

    用两个数字指定落点行数和列数, 为了避免炮落点位于自身附近点击失效可设置第三个延时参数.

    落点还可以为一至多个格式为 (行, 列) 的元组, 或者一个包含了这些元组的列表. 

    @示例:

    >>> _fire_cob(2, 9)

    >>> _fire_cob(5, 7, delay=30)

    >>> _fire_cob((2, 9))

    >>> _fire_cob((2, 9), (5, 9))

    >>> _fire_cob([(2, 9), (5, 9), (2, 9), (5, 9)])
    """
    raise Exception("参数格数不对啊...")


@_fire_cob.register(int)
def _(fall_row, fall_col, time_delay_cs=0):
    cob_count = len(_cob_list)

    if cob_count == 0:
        raise Exception("你他娘的意大利炮呢...")

    global _cob_index
    _cob_lock.acquire()
    _cob_index %= cob_count
    cob_row = _cob_list[_cob_index][0]
    cob_col = _cob_list[_cob_index][1]
    _fire_cob_by_crood(cob_row, cob_col, fall_row, fall_col, time_delay_cs)
    _cob_index += 1
    _cob_lock.release()


@_fire_cob.register(tuple)
def _(*fall_grids):
    cob_count = len(_cob_list)

    if cob_count == 0:
        raise Exception("你他娘的意大利炮呢...")

    global _cob_index
    _cob_lock.acquire()
    for i in range(len(fall_grids)):
        _cob_index %= cob_count
        cob_row = _cob_list[_cob_index][0]
        cob_col = _cob_list[_cob_index][1]
        fall_row = fall_grids[i][0]
        fall_col = fall_grids[i][1]
        _fire_cob_by_crood(cob_row, cob_col, fall_row, fall_col)
        _cob_index += 1
    _cob_lock.release()


@_fire_cob.register(list)
def _(fall_grids):
    _fire_cob(*fall_grids)


# 炮身点击次数
_click_count = 3

# TODO 无视内置炮列表直接指定炮位和落点的函数
def _fire_cob_by_crood(cob_row, cob_col, fall_row, fall_col, time_delay_cs=0):
    _mouse_lock.acquire()
    _safe_click()
    for _ in range(_click_count):
        _click_grid(cob_row, cob_col)
    if time_delay_cs > 0:
        _game_delay_for(time_delay_cs)
    _click_grid(fall_row, fall_col)
    _mouse_lock.release()

    _logger.info(
        f"Fire Cob Cannon index {_cob_index} from {(cob_row, cob_col)} to {(fall_row, fall_col)} delay {time_delay_cs}."
    )


def _skip_cob_index(num):
    """
    跳过列表中一定数量的玉米炮, 通常用于 wave9/19 手动收尾.

    @参数 num(int): 数量.
    """
    _cob_lock.acquire()
    global _cob_index
    _cob_index += num
    _cob_lock.release()


def _use_shovel(row, col):
    """
    用铲子操作.

    @参数 row(float): 作用行

    @参数 col(float): 作用列

    @示例:

    >>> _use_shovel(2, 3)  # 铲掉 2 行 3 列的植物
    """
    _mouse_lock.acquire()
    _safe_click()
    _click_shovel()
    _click_grid(row, col)
    _mouse_lock.release()


### 子线程装饰器

# TODO 守护线程?
def _running_in_thread(func):
    """
    将此装饰器应用到需要在子线程运行的函数上.
    """

    @functools.wraps(func)  # 复制原函数元信息
    def wrapper(*args, **kwargs):
        thread = threading.Thread(target=func, args=args, kwargs=kwargs)
        thread.start()

    return wrapper


### Auto Collect Thread


# 1.silver_coin 2.gold_coin 3.diamond 4.sun 5.small_sun 6.big_sun 17.sprout
# TODO  接受列表参数包括汉字
@_running_in_thread
def _auto_collect(collect_items=[1, 2, 3, 4, 5, 6, 17], interval_cs=12):
    """
    自动收集场上资源. 在单独的子线程运行.

    为了避免操作冲突, 鼠标光标放到游戏窗口内部时会暂停收集.

    @参数 collect_items(list): 需要收集的资源类型.

    1.银币 2.金币 3.钻石 4.阳光 5.小阳光 6.大阳光 17.幼苗

    @参数 interval_cs(float): 间隔, 单位 cs, 默认 12.

    @示例:

    >>> _auto_collect()

    >>> _auto_collect([3, 4, 5, 6], 20)  # 只收集钻石和阳光, 间隔 0.2s
    """
    interval = interval_cs / 100

    while _game_ui() != 3:
        time.sleep(0.1)

    _logger.info("Start automatic collection.")

    while _game_ui() == 3:
        item_count = _read_memory("int", 0x6A9EC0, 0x768, 0xF4)
        item_count_max = _read_memory("int", 0x6A9EC0, 0x768, 0xE8)
        item_offset = _read_memory("int", 0x6A9EC0, 0x768, 0xE4)

        if item_count == 0:
            time.sleep(interval)
            continue

        uncollected_item_count = 0
        for i in range(item_count_max):
            disappeared = _read_memory("bool", item_offset + 0x38 + 0xD8 * i)
            collected = _read_memory("bool", item_offset + 0x50 + 0xD8 * i)
            item_type = _read_memory("int", item_offset + 0x58 + 0xD8 * i)
            if not disappeared and not collected and item_type in collect_items:
                uncollected_item_count += 1
        if uncollected_item_count == 0:
            time.sleep(interval)
            continue

        for i in range(item_count_max):
            if _game_ui() != 3:
                break
            # while _game_paused() or (_mouse_in_game() and _mouse_have_something()):
            while _game_paused() or _mouse_in_game():
                time.sleep(interval)

            disappeared = _read_memory("bool", item_offset + 0x38 + 0xD8 * i)
            collected = _read_memory("bool", item_offset + 0x50 + 0xD8 * i)
            item_type = _read_memory("int", item_offset + 0x58 + 0xD8 * i)
            if not disappeared and not collected and item_type in collect_items:
                # _write_memory("bool", True, item_offset + 0x50 + 0xd8 * i)
                # time.sleep(interval)

                item_x = _read_memory("float", item_offset + 0x24 + 0xD8 * i)
                item_y = _read_memory("float", item_offset + 0x28 + 0xD8 * i)
                if item_x >= 0.0 and item_y >= 70.0:
                    _mouse_lock.acquire()
                    _safe_click()
                    x, y = int(item_x + 30), int(item_y + 30)
                    _mouse_left_click(x, y)
                    _safe_click()
                    _mouse_lock.release()

                    _logger.info(f"Collect item {item_type} at {(x, y)}.")
                    time.sleep(interval)

    _logger.info("Stop automatic collection.")


### Auto Fill Ice Thread


# 存冰位
_ice_spots = []


def _get_ice_seed_list():
    """
    获取所有寒冰菇卡片的下标.

    @返回值 (list): 包含卡槽所有寒冰菇卡片数组下标的列表.
    """
    ice_seeds = []
    slots_count = _read_memory("int", 0x6A9EC0, 0x768, 0x144, 0x24)
    slots_offset = _read_memory("unsigned int", 0x6A9EC0, 0x768, 0x144)
    for i in range(slots_count):
        seed_type = _read_memory("int", slots_offset + 0x5C + i * 0x50)
        seed_imitater_type = _read_memory("int", slots_offset + 0x60 + i * 0x50)
        if seed_type == 14 or (seed_type == 48 and seed_imitater_type == 14):
            ice_seeds.append(i)
    _logger.info(f"Get ice seed index {[i + 1 for i in ice_seeds]}.")
    return ice_seeds


def _get_ice_spots_list():
    """
    获取所有场上寒冰菇的坐标.

    @返回值 (list): 包含场上所有寒冰菇位置 (行, 列) 的列表.
    """
    ice_spots = []
    plant_count_max = _read_memory("unsigned int", 0x6A9EC0, 0x768, 0xB0)
    plant_offset = _read_memory("unsigned int", 0x6A9EC0, 0x768, 0xAC)
    for i in range(plant_count_max):
        plant_disappeared = _read_memory("bool", plant_offset + 0x141 + 0x14C * i)
        plant_crushed = _read_memory("bool", plant_offset + 0x142 + 0x14C * i)
        plant_type = _read_memory("int", plant_offset + 0x24 + 0x14C * i)
        plant_imitater_type = _read_memory("int", plant_offset + 0x138 + 0x14C * i)
        if (
            not plant_disappeared
            and not plant_crushed
            and (plant_type == 14 or (plant_type == 48 and plant_imitater_type == 14))
        ):
            plant_row = _read_memory("int", plant_offset + 0x1C + 0x14C * i)
            plant_col = _read_memory("int", plant_offset + 0x28 + 0x14C * i)
            ice = (plant_row + 1, plant_col + 1)
            ice_spots.append(ice)
    _logger.info(f"Get ice spots list {ice_spots}.")
    return ice_spots


@_running_in_thread
def _auto_fill_ice(spots=None, total=0xFFFFFFFF):
    """
    自动存冰. 在单独的子线程运行.

    @参数 spots(list): 存冰点, 包括若干个 (行, 列) 元组. 永久位在前, 临时位在后. 默认为场上现有存冰的位置.

    @参数 total(int): 总个数, 默认无限.

    @示例:

    >>> _auto_fill_ice()

    >>> _auto_fill_ice([(6, 1), (5, 1), (2, 1), (1, 1)], 10)
    """

    while _game_ui() != 3:
        time.sleep(0.01)

    _logger.info("Start automatic fill ice.")

    if spots is None:
        spots = _get_ice_spots_list()
    global _ice_spots
    _ice_spots = spots

    slots_offset = _read_memory("unsigned int", 0x6A9EC0, 0x768, 0x144)

    _ice_seeds_index = _get_ice_seed_list()  # 保存所有寒冰菇卡片的序号

    filled = 0  # 已存数量
    while _game_ui() == 3 and filled < total:

        while _game_paused():
            _game_delay_for(1)  # 等待暂停取消

        current_ice_spots = _get_ice_spots_list()
        if set(current_ice_spots) >= set(spots):
            time.sleep(0.1)  # TODO 0.01
            continue

        # 遍历指定的存冰位
        for spot in spots:
            if _game_ui() != 3:
                break

            # 如果该位置无冰则尝试存冰
            if spot not in current_ice_spots:

                # 遍历寒冰菇卡片, 通常为 原版冰 x 1 + 复制冰 x 1
                for i in _ice_seeds_index:
                    seed_usable = _read_memory("bool", slots_offset + 0x70 + i * 0x50)
                    seed_ice_cost = _read_memory("int", 0x69F2C0 + 14 * 0x24)
                    sun = _read_memory("int", 0x6A9EC0, 0x768, 0x5560)
                    if seed_usable and sun >= seed_ice_cost:  # TODO 无视阳光
                        while _game_paused():
                            _game_delay_for(1)  # 等待暂停取消
                        _mouse_lock.acquire()
                        _safe_click()
                        _click_seed(i + 1)
                        row, col = spot
                        _click_grid(row, col)
                        _safe_click()
                        _mouse_lock.release()
                        filled += 1
                        _logger.info(f"Fill ice spot {spot} with seed {i+1}.")
                        _game_delay_for(1)  # 等待内存数据更新
                        break
                    else:
                        time.sleep(0.01)

                break  # 不管有没有成功都重新遍历存冰位以保证顺序(先永久位后临时位)

    _logger.info("Stop automatic fill ice.")


def _activate_ice():
    """
    点冰. 使用咖啡豆激活存冰.
    
    优先点临时位. 该函数需要配合自动存冰线程使用.
    """
    _mouse_lock.acquire()
    _safe_click()
    _click_seed(_seeds_index[35] + 1)  # 咖啡豆
    for spot in reversed(_ice_spots):
        row, col = spot
        _click_grid(row, col)
    _safe_click()
    _mouse_lock.release()


### Immobilize Dancer Thread


def _pause_game():
    """
    暂停游戏.
    """
    if not _game_paused():
        _press_space()


def _restore_game():
    """
    恢复游戏.
    """
    if _game_paused():
        _press_space()


@_running_in_thread
def _immobilize_dancer():
    """
    女仆秘籍. 通过暂停控制舞王/伴舞的跳舞/行走.

    参考资料 https://tieba.baidu.com/p/3937751350
    """

    while _game_ui() != 3:
        time.sleep(0.1)

    _logger.info("Start immobilize dancer.")

    while _game_ui() == 3:
        while (((_dance_clock() + 10) % (23 * 20)) // 20) > 11:
            time.sleep(0.01)
        _pause_game()
        time.sleep(0.5)
        while (((_dance_clock()) % (23 * 20)) // 20) <= 11:
            time.sleep(0.01)
        _restore_game()

    _logger.info("Stop immobilize dancer.")


# TODO roof flytime
# TODO update plant


### documented api

## 进程内存读写

FindWindow = _open_process_by_window
FindPvZ = _find_pvz_1051
ReadMemory = _read_memory
WriteMemory = _write_memory

## 模拟鼠标点击

LeftClick = _mouse_left_click
RightClick = _mouse_right_click
SafeClick = _safe_click
ButtonClick = _special_button_click

## 延时机制

Sleep = _thread_sleep_for
Delay = _game_delay_for
Countdown = _until_countdown
Prejudge = _until_relative_time_after_refresh
Until = _until_relative_time

## 选卡

SelectCards = _select_seeds_and_lets_rock
UpdatePaoList = _update_cob_cannon_list

## 场地相关点击函数

ClickSeed = _click_seed
ClickShovel = _click_shovel
ClickGrid = _click_grid

## 用卡用炮点冰操作

Card = _use_seed
Pao = _fire_cob
Coffee = _activate_ice
SkipPao = _skip_cob_index
Shovel = _use_shovel

## 子线程操作

RunningInThread = _running_in_thread
StartAutoCollectThread = _auto_collect
StartAutoFillIceThread = _auto_fill_ice
StartStopDancerThread = _immobilize_dancer


__all__ = [
    "FindWindow",
    "FindPvZ",
    "ReadMemory",
    "WriteMemory",
    "LeftClick",
    "RightClick",
    "SafeClick",
    "ButtonClick",
    "Sleep",
    "Delay",
    "Countdown",
    "Prejudge",
    "Until",
    "SelectCards",
    "UpdatePaoList",
    "ClickSeed",
    "ClickShovel",
    "ClickGrid",
    "Card",
    "Pao",
    "Coffee",
    "SkipPao",
    "Shovel",
    "RunningInThread",
    "StartAutoCollectThread",
    "StartAutoFillIceThread",
    "StartStopDancerThread",
]


### start and exit works


def _on_start():
    # don't need actually, will set to 0.5ms if game started
    _timeBeginPeriod(1)  # res == _TIMERR_NOERROR

    # this mudule is time-critical which needs real-time
    gc.disable()

    _SetPriorityClass(_GetCurrentProcess(), _HIGH_PRIORITY_CLASS)

    # disable log
    _enable_logger(False)  # TODO
    _set_logger_level("INFO")

    _get_dpi_scale()

    if _find_pvz_1051():
        _SetPriorityClass(_pvz_handle, _HIGH_PRIORITY_CLASS)

        if _game_ui() in (2, 3):
            global _slots_count, _game_scene
            _slots_count = _read_memory("int", 0x6A9EC0, 0x768, 0x144, 0x24)
            _game_scene = _read_memory("int", 0x6A9EC0, 0x768, 0x554C)
            _update_cob_cannon_list()
            _update_seeds_list()


def _on_exit():
    _timeEndPeriod(1)  # res == _TIMERR_NOERROR

    if _is_process_valid():
        _CloseHandle(_pvz_handle)


_on_start()
atexit.register(_on_exit)
time.sleep(1.437)


###########################################


# def main():
#     _hello_world()

# if __name__ == "__main__":
#     main()
