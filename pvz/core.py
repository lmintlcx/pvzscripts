# coding=utf-8

import logging
import ctypes
import struct
import threading
import time
import functools
import random
import gc

### 调试日志

fmt_str = "%(asctime)s.%(msecs)03d - %(name)s - %(levelname)s - %(message)s"
log_formatter = logging.Formatter(fmt=fmt_str, datefmt='%H:%M:%S')

console_handler = logging.StreamHandler()
console_handler.setFormatter(log_formatter)
console_handler.setLevel(logging.INFO)

pvz_logger = logging.getLogger("pvz")
pvz_logger.addHandler(console_handler)
pvz_logger.setLevel(logging.INFO)


def enable_logging(on=True):
    """
    启用日志.

    输出调试信息开销较大, 会影响操作精度, 建议在调试完成后正式运行的时候关闭.

    @参数 on(bool): 是否启用, 默认启用.
    """
    pvz_logger.disabled = not on


def set_logging_level(level="INFO"):
    """
    设置日志级别.

    @参数 level(str): 可选值 ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"].
    """
    logging_level = {
        "DEBUG": logging.DEBUG,
        "INFO": logging.INFO,
        "WARNING": logging.WARNING,
        "ERROR": logging.ERROR,
        "CRITICAL": logging.CRITICAL,
    }
    pvz_logger.setLevel(logging_level[level])


# 频繁出现的调试信息
def debug(txt):
    pvz_logger.debug(txt)


# 常规调试信息
def info(txt):
    pvz_logger.info(txt)


# 不影响运行的警告
def warning(txt):
    pvz_logger.warning(txt)


# 用户操作出错
def error(txt):
    pvz_logger.error(txt)
    raise Exception(txt)


# 内部严重错误
def critical(txt):
    pvz_logger.critical(txt)
    raise Exception(txt)


### win32 动态库

user32 = ctypes.windll.user32
kernel32 = ctypes.windll.kernel32
winmm = ctypes.windll.winmm
gdi32 = ctypes.windll.gdi32

### win32 类型

from ctypes import c_size_t as SIZE_T
from ctypes.wintypes import BOOL
from ctypes.wintypes import DWORD
from ctypes.wintypes import INT
from ctypes.wintypes import UINT
from ctypes.wintypes import LONG
from ctypes.wintypes import HWND
from ctypes.wintypes import HANDLE
from ctypes.wintypes import HDC
from ctypes.wintypes import LPVOID
from ctypes.wintypes import LPCVOID
from ctypes.wintypes import LPCWSTR
from ctypes.wintypes import LPDWORD
from ctypes.wintypes import POINT
from ctypes.wintypes import LPPOINT
from ctypes.wintypes import RECT
from ctypes.wintypes import LPRECT
from ctypes.wintypes import WPARAM
from ctypes.wintypes import LPARAM


# typedef struct SECURITY_ATTRIBUTES {
#   DWORD  nLength;
#   LPVOID lpSecurityDescriptor;
#   BOOL   bInheritHandle;
# } SECURITY_ATTRIBUTES, *PSECURITY_ATTRIBUTES, *LPSECURITY_ATTRIBUTES;
class SECURITY_ATTRIBUTES(ctypes.Structure):
    _fields_ = [("nLength", DWORD), ("lpSecurityDescriptor", LPVOID), ("bInheritHandle", BOOL)]


LPSECURITY_ATTRIBUTES = ctypes.POINTER(SECURITY_ATTRIBUTES)

# typedef DWORD (__stdcall *LPTHREAD_START_ROUTINE) (
#     [in] LPVOID lpThreadParameter
# );
LPTHREAD_START_ROUTINE = ctypes.WINFUNCTYPE(DWORD, LPVOID)

### win32 函数接口 和 参数常量

# int MessageBoxW(
#   HWND    hWnd,
#   LPCWSTR lpText,
#   LPCWSTR lpCaption,
#   UINT    uType
# );
MessageBoxW = user32.MessageBoxW
MessageBoxW.argtypes = [HWND, LPCWSTR, LPCWSTR, UINT]
MessageBoxW.restype = INT

# HWND FindWindowW(
#   LPCWSTR lpClassName,
#   LPCWSTR lpWindowName
# );
FindWindowW = user32.FindWindowW
FindWindowW.argtypes = [LPCWSTR, LPCWSTR]
FindWindowW.restype = HWND

# DWORD GetWindowThreadProcessId(
#   HWND    hWnd,
#   LPDWORD lpdwProcessId
# );
GetWindowThreadProcessId = user32.GetWindowThreadProcessId
GetWindowThreadProcessId.argtypes = [HWND, LPDWORD]
GetWindowThreadProcessId.restype = DWORD

# HANDLE OpenProcess(
#   DWORD dwDesiredAccess,
#   BOOL  bInheritHandle,
#   DWORD dwProcessId
# );
OpenProcess = kernel32.OpenProcess
OpenProcess.argtypes = [DWORD, BOOL, DWORD]
OpenProcess.restype = HANDLE

PROCESS_ALL_ACCESS = 0x001F0FFF

# BOOL GetExitCodeProcess(
#   HANDLE  hProcess,
#   LPDWORD lpExitCode
# );
GetExitCodeProcess = kernel32.GetExitCodeProcess
GetExitCodeProcess.argtypes = [HANDLE, LPDWORD]
GetExitCodeProcess.restype = BOOL

STILL_ACTIVE = 0x00000103

# BOOL WINAPI CloseHandle(
#   _In_ HANDLE hObject
# );
CloseHandle = kernel32.CloseHandle
CloseHandle.argtypes = [HANDLE]
CloseHandle.restype = BOOL

# BOOL WINAPI ReadProcessMemory(
#   _In_  HANDLE  hProcess,
#   _In_  LPCVOID lpBaseAddress,
#   _Out_ LPVOID  lpBuffer,
#   _In_  SIZE_T  nSize,
#   _Out_ SIZE_T  *lpNumberOfBytesRead
# );
ReadProcessMemory = kernel32.ReadProcessMemory
ReadProcessMemory.argtypes = [HANDLE, LPCVOID, LPVOID, SIZE_T, LPDWORD]
ReadProcessMemory.restype = BOOL

# BOOL WINAPI WriteProcessMemory(
#   _In_  HANDLE  hProcess,
#   _In_  LPVOID  lpBaseAddress,
#   _In_  LPCVOID lpBuffer,
#   _In_  SIZE_T  nSize,
#   _Out_ SIZE_T  *lpNumberOfBytesWritten
# );
WriteProcessMemory = kernel32.WriteProcessMemory
WriteProcessMemory.argtypes = [HANDLE, LPVOID, LPCVOID, SIZE_T, LPDWORD]
WriteProcessMemory.restype = BOOL

# DWORD WINAPI GetLastError(void);
GetLastError = kernel32.GetLastError
GetLastError.argtypes = []
GetLastError.restype = DWORD

# HWND SetActiveWindow(
#   HWND hWnd
# );
SetActiveWindow = user32.SetActiveWindow
SetActiveWindow.argtypes = [HWND]
SetActiveWindow.restype = HWND

# BOOL SetForegroundWindow(
#   HWND hWnd
# );
SetForegroundWindow = user32.SetForegroundWindow
SetForegroundWindow.argtypes = [HWND]
SetForegroundWindow.restype = BOOL

# BOOL SetWindowPos(
#   HWND hWnd,
#   HWND hWndInsertAfter,
#   int  X,
#   int  Y,
#   int  cx,
#   int  cy,
#   UINT uFlags
# );
SetWindowPos = user32.SetWindowPos
SetWindowPos.argtypes = [HWND, HWND, INT, INT, INT, INT, UINT]
SetWindowPos.restype = BOOL

HWND_NOTOPMOST = -2
HWND_TOPMOST = -1
SWP_NOMOVE = 0x0002
SWP_NOSIZE = 0x0001
SWP_SHOWWINDOW = 0x0040

# LPVOID WINAPI VirtualAllocEx(
#   _In_     HANDLE hProcess,
#   _In_opt_ LPVOID lpAddress,
#   _In_     SIZE_T dwSize,
#   _In_     DWORD  flAllocationType,
#   _In_     DWORD  flProtect
# );
VirtualAllocEx = kernel32.VirtualAllocEx
VirtualAllocEx.argtypes = [HANDLE, LPVOID, SIZE_T, DWORD, DWORD]
VirtualAllocEx.restype = LPVOID

MEM_COMMIT = 0x00001000
PAGE_EXECUTE_READWRITE = 0x40

# BOOL WINAPI VirtualFreeEx(
#   _In_ HANDLE hProcess,
#   _In_ LPVOID lpAddress,
#   _In_ SIZE_T dwSize,
#   _In_ DWORD  dwFreeType
# );
VirtualFreeEx = kernel32.VirtualFreeEx
VirtualFreeEx.argtypes = [HANDLE, LPVOID, SIZE_T, DWORD]
VirtualFreeEx.restype = BOOL

MEM_RELEASE = 0x00008000

# HANDLE CreateRemoteThread(
#   HANDLE                 hProcess,
#   LPSECURITY_ATTRIBUTES  lpThreadAttributes,
#   SIZE_T                 dwStackSize,
#   LPTHREAD_START_ROUTINE lpStartAddress,
#   LPVOID                 lpParameter,
#   DWORD                  dwCreationFlags,
#   LPDWORD                lpThreadId
# );
CreateRemoteThread = kernel32.CreateRemoteThread
CreateRemoteThread.argtypes = [HANDLE, LPSECURITY_ATTRIBUTES, SIZE_T, LPTHREAD_START_ROUTINE, LPVOID, DWORD, LPDWORD]
CreateRemoteThread.restype = HANDLE

# DWORD WaitForSingleObject(
#   HANDLE hHandle,
#   DWORD  dwMilliseconds
# );
WaitForSingleObject = kernel32.WaitForSingleObject
WaitForSingleObject.argtypes = [HANDLE, DWORD]
WaitForSingleObject.restype = DWORD

INFINITE = 0xFFFFFFFF
WAIT_FAILED = 0xFFFFFFFF

# LRESULT SendMessageW(
#   HWND   hWnd,
#   UINT   Msg,
#   WPARAM wParam,
#   LPARAM lParam
# );
SendMessageW = user32.SendMessageW
SendMessageW.argtypes = [HWND, UINT, WPARAM, LPARAM]
SendMessageW.restype = LONG

# BOOL PostMessageW(
#   HWND   hWnd,
#   UINT   Msg,
#   WPARAM wParam,
#   LPARAM lParam
# );
PostMessageW = user32.PostMessageW
PostMessageW.argtypes = [HWND, UINT, WPARAM, LPARAM]
PostMessageW.restype = BOOL

WM_KEYDOWN = 0x0100
WM_KEYUP = 0x0101
VK_ESCAPE = 0x1B
VK_SPACE = 0x20
VK_RETURN = 0x0D
VK_LEFT = 0x25
VK_UP = 0x26
VK_RIGHT = 0x27
VK_DOWN = 0x28

WM_LBUTTONDOWN = 0x0201
WM_LBUTTONUP = 0x0202
WM_RBUTTONDOWN = 0x0204
WM_RBUTTONUP = 0x0205

MK_LBUTTON = 0x0001
MK_RBUTTON = 0x0002

# HDC GetDC(
#   HWND hWnd
# );
GetDC = user32.GetDC
GetDC.argtypes = [HWND]
GetDC.restype = HDC

# int GetDeviceCaps(
#   HDC hdc,
#   int index
# );
GetDeviceCaps = gdi32.GetDeviceCaps
GetDeviceCaps.argtypes = [HDC, INT]
GetDeviceCaps.restype = INT

HORZRES = 8
DESKTOPHORZRES = 118

# int ReleaseDC(
#   HWND hWnd,
#   HDC  hDC
# );
ReleaseDC = user32.ReleaseDC
ReleaseDC.argtypes = [HWND, HDC]
ReleaseDC.restype = INT

# MMRESULT timeBeginPeriod(
#   UINT uPeriod
# );
timeBeginPeriod = winmm.timeBeginPeriod
timeBeginPeriod.argtypes = [UINT]
timeBeginPeriod.restype = UINT

# MMRESULT timeEndPeriod(
#   UINT uPeriod
# );
timeEndPeriod = winmm.timeEndPeriod
timeEndPeriod.argtypes = [UINT]
timeEndPeriod.restype = UINT

# HANDLE GetCurrentProcess(
# );
GetCurrentProcess = kernel32.GetCurrentProcess
GetCurrentProcess.argtypes = []
GetCurrentProcess.restype = HANDLE

# DWORD GetPriorityClass(
#   HANDLE hProcess
# );
GetPriorityClass = kernel32.GetPriorityClass
GetPriorityClass.argtypes = [HANDLE]
GetPriorityClass.restype = DWORD

# BOOL SetPriorityClass(
#   HANDLE hProcess,
#   DWORD  dwPriorityClass
# );
SetPriorityClass = kernel32.SetPriorityClass
SetPriorityClass.argtypes = [HANDLE, DWORD]
SetPriorityClass.restype = BOOL

HIGH_PRIORITY_CLASS = 0x00000080
REALTIME_PRIORITY_CLASS = 0x00000100

### 进程操作

# 窗口句柄
pvz_hwnd = HWND()

# 进程标识
pvz_pid = DWORD()

# 进程句柄
pvz_handle = HANDLE()

# 游戏版本
pvz_version = None


def is_valid():
    """
    检查目标进程是否可用.

    @返回值 (bool): 未找到或者已经退出则返回 False.
    """

    if pvz_handle.value is None:
        return False

    exit_code = DWORD()
    GetExitCodeProcess(pvz_handle, ctypes.byref(exit_code))
    return exit_code.value == STILL_ACTIVE


def open_process_by_window(class_name, window_name):
    """
    根据窗口的类名和标题打开进程.

    @参数 class_name(str): 窗口类名, 可省略为 None.

    @参数 window_name(str): 窗口标题, 可省略为 None.

    @返回值 (bool): 成功打开目标进程则返回 True.
    """

    global pvz_hwnd, pvz_pid, pvz_handle

    # 关闭之前已经打开的句柄
    if is_valid():
        CloseHandle(pvz_handle)

    pvz_hwnd.value = None
    pvz_pid.value = 0
    pvz_handle.value = None

    pvz_hwnd.value = FindWindowW(class_name, window_name)
    if pvz_hwnd.value is not None:
        GetWindowThreadProcessId(pvz_hwnd, ctypes.byref(pvz_pid))
    if pvz_pid.value != 0:
        pvz_handle.value = OpenProcess(PROCESS_ALL_ACCESS, False, pvz_pid)

    result = pvz_handle.value is not None
    info("查找游戏窗口, 类名 '%s', 标题 '%s', 结果 %s." % (class_name, window_name, result))
    return result


def find_pvz():
    """
    查找原版植物大战僵尸游戏进程.

    @返回值 (bool): 查找成功返回 True, 没找到或是版本不符则返回 False.
    """

    global pvz_version

    # 不建议省略窗口类名, 因为可能存在其他标题相同的窗口从而引起查找失误.
    # 已知所有的植物大战僵尸一代电脑版的窗口类名均为 "MainWindow".
    # 原版英文版的窗口标题为 "Plants vs. Zombies".
    if not open_process_by_window("MainWindow", "Plants vs. Zombies"):
        open_process_by_window("MainWindow", None)

    if is_valid():
        if read_memory("unsigned int", 0x004140C5) == 0x0019B337:
            pvz_version = "1.0.0.1051"
            info("已找到游戏 1.0.0.1051 !!!")
            return True
        elif read_memory("unsigned int", 0x004140D5) == 0x0019B827:
            pvz_version = "1.2.0.1065"
            info("已找到游戏 1.2.0.1065 !!!")
            return True
        else:
            pvz_version = None
            warning("不支持的游戏版本 !!!")
            return False
    else:
        pvz_version = None
        warning("未找到游戏 !!!")
        return False


def pvz_ver():
    return pvz_version


# C/C++ 数据类型
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

# 读写内存时加锁
memory_lock = threading.Lock()

### 读写内存


def read_memory(data_type, *address, array=1):
    """
    读取内存数据.

    @参数 data_type(str): 数据类型, 取自 C/C++ 语言关键字, 可选值 ["char", "bool", "unsigned char", "short", "unsigned short", "int", "unsigned int", "long", "unsigned long", "long long", "unsigned long long", "float", "double"].

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
        critical("目标进程不可用, 读内存失败.")

    memory_lock.acquire()

    level = len(address)  # 偏移级数
    offset = ctypes.c_void_p()  # 内存地址
    buffer = ctypes.c_uint()  # 中间数据缓冲
    bytes_read = ctypes.c_ulong()  # 已读字节数

    for i in range(level):
        offset.value = buffer.value + address[i]

        if i != level - 1:
            size = ctypes.sizeof(buffer)
            success = ReadProcessMemory(pvz_handle, offset, ctypes.byref(buffer), size, ctypes.byref(bytes_read))
            if success == 0 or bytes_read.value != size:
                critical("读取内存失败, 错误代码 %d." % GetLastError())

        else:
            fmt_str = "<" + str(array) + cpp_typename[data_type]
            size = struct.calcsize(fmt_str)  # 目标数据大小
            buff = ctypes.create_string_buffer(size)  # 目标数据缓冲
            success = ReadProcessMemory(pvz_handle, offset, ctypes.byref(buff), size, ctypes.byref(bytes_read))
            if success == 0 or bytes_read.value != size:
                critical("读取内存失败, 错误代码 %d." % GetLastError())

            result = struct.unpack(fmt_str, buff.raw)

    memory_lock.release()

    debug("读取内存, 类型 %s, 地址 %s, 数量 %d, 结果 %s." % (data_type, str(address), array, str(result)))
    if array == 1:
        return result[0]
    else:
        return result


def write_memory(data_type, values, *address):
    """
    写入内存数据.

    @参数 data_type(str): 数据类型, 取自 C/C++ 语言关键字, 可选值 ["char", "bool", "unsigned char", "short", "unsigned short", "int", "unsigned int", "long", "unsigned long", "long long", "unsigned long long", "float", "double"].

    @参数 values(int/float/bool/list/tuple): 需要写入的数据, 多个数据采用列表或者元组形式.

    @参数 address(int): 地址, 可为多级偏移.

    @示例:

    >>> WriteMemory("int", 8000, 0x6a9ec0, 0x768, 0x5560)

    >>> WriteMemory("unsigned char", [0xb0, 0x01, 0xc3], 0x0041d7d0)
    """

    if not is_valid():
        critical("目标进程不可用, 写内存失败.")

    # 将单个数据转换为列表方便统一处理
    if not isinstance(values, (tuple, list)):
        values = [values]

    memory_lock.acquire()

    level = len(address)  # 偏移级数
    offset = ctypes.c_void_p()  # 内存地址
    buffer = ctypes.c_uint()  # 中间数据缓冲
    bytes_read = ctypes.c_ulong()  # 已读字节数
    bytes_written = ctypes.c_ulong()  # 已写字节数

    for i in range(level):
        offset.value = buffer.value + address[i]

        if i != level - 1:
            size = ctypes.sizeof(buffer)
            success = ReadProcessMemory(pvz_handle, offset, ctypes.byref(buffer), size, ctypes.byref(bytes_read))
            if success == 0 or bytes_read.value != size:
                critical("读取内存失败, 错误代码 %d." % GetLastError())

        else:
            array = len(values)  # 目标数据的数量
            fmt_str = "<" + str(array) + cpp_typename[data_type]
            size = struct.calcsize(fmt_str)  # 目标数据大小
            buff = ctypes.create_string_buffer(size)  # 创建目标数据缓冲
            buff.value = struct.pack(fmt_str, *values)  # 将目标数据载入缓冲区
            success = WriteProcessMemory(pvz_handle, offset, ctypes.byref(buff), size, ctypes.byref(bytes_written))
            if success == 0 or bytes_written.value != size:
                critical("写入内存失败, 错误代码 %d." % GetLastError())

    memory_lock.release()

    debug("写入内存, 类型 %s, 数值 %s, 地址 %s." % (data_type, str(values), str(address)))


### 窗口置顶


def active_pvz():
    """
    激活 PvZ 窗口. (后台时不激活.)
    """
    if pvz_hwnd.value is not None:
        SetActiveWindow(pvz_hwnd)


def set_pvz_foreground():
    """
    激活并前台显示 PvZ 窗口.
    """
    if pvz_hwnd.value is not None:
        SetForegroundWindow(pvz_hwnd)


def set_pvz_top_most(on=True):
    """
    置顶显示游戏窗口.

    @参数 on(bool): 是否开启.
    """
    if pvz_hwnd.value is not None:
        SetWindowPos(
            pvz_hwnd,  #
            HWND_TOPMOST if on else HWND_NOTOPMOST,  #
            0,  #
            0,  #
            0,  #
            0,  #
            SWP_NOMOVE | SWP_NOSIZE | SWP_SHOWWINDOW,  #
        )


### 进程优先级


def set_pvz_high_priority():
    """
    游戏进程以高优先级运行. 可在一定程度上提高帧率.
    """
    if GetPriorityClass(pvz_handle) != REALTIME_PRIORITY_CLASS:
        SetPriorityClass(pvz_handle, HIGH_PRIORITY_CLASS)


# 汇编代码

asm_code = bytes()


# 初始化
def asm_init():
    global asm_code
    asm_code = bytes()


# unsigned char
def asm_add_byte(code):
    global asm_code
    asm_code += struct.pack("<1B", code)


# unsigned short
def asm_add_word(code):
    global asm_code
    asm_code += struct.pack("<1H", code)


# unsigned int
def asm_add_dword(code):
    global asm_code
    asm_code += struct.pack("<1I", code)


# bytes from list/tuple
def asm_add_bytes(codes):
    for code in codes:
        asm_add_byte(code)


# push 0x12345678
def asm_push(code):
    asm_add_byte(0x68)
    asm_add_dword(code)


# push 0x12
def asm_push_byte(code):
    asm_add_byte(0x6a)
    asm_add_byte(code)


# mov exx, 0x12345678
asm_mov_exx_code = {
    "eax": [0xB8],
    "ebx": [0xBB],
    "ecx": [0xB9],
    "edx": [0xBA],
    "esi": [0xBE],
    "edi": [0xBF],
    "ebp": [0xBD],
    "esp": [0xBC]
}


def asm_mov_exx(register, code):
    asm_add_bytes(asm_mov_exx_code[register])
    asm_add_dword(code)


# add exx, 0x12345678
asm_add_exx_code = {
    "eax": [0x05],
    "ebx": [0x81, 0xC3],
    "ecx": [0x81, 0xC1],
    "edx": [0x81, 0xC2],
    "esi": [0x81, 0xC6],
    "edi": [0x81, 0xC7],
    "ebp": [0x81, 0xC5],
    "esp": [0x81, 0xC4],
}


def asm_add_exx(register, code):
    asm_add_bytes(asm_add_exx_code[register])
    asm_add_dword(code)


# mov exx, ds:[0x12345678]
asm_mov_exx_dword_ptr_code = {
    "eax": [0x3E, 0xA1],
    "ebx": [0x3E, 0x8B, 0x1D],
    "ecx": [0x3E, 0x8B, 0x0D],
    "edx": [0x3E, 0x8B, 0x15],
    "esi": [0x3E, 0x8B, 0x35],
    "edi": [0x3E, 0x8B, 0x3D],
    "ebp": [0x3E, 0x8B, 0x2D],
    "esp": [0x3E, 0x8B, 0x25],
}


def asm_mov_exx_dword_ptr(register, code):
    asm_add_bytes(asm_mov_exx_dword_ptr_code[register])
    asm_add_dword(code)


# mov exx, [exx + 0x12345678]
asm_mov_exx_dword_ptr_exx_add_code = {
    "eax": [0x8B, 0x80],
    "ebx": [0x8B, 0x9B],
    "ecx": [0x8B, 0x89],
    "edx": [0x8B, 0x92],
    "esi": [0x8B, 0xB6],
    "edi": [0x8B, 0xBF],
    "ebp": [0x8B, 0xAD],
    "esp": [0x8B, 0xA4, 0x24],
}


def asm_mov_exx_dword_ptr_exx_add(register, code):
    asm_add_bytes(asm_mov_exx_dword_ptr_exx_add_code[register])
    asm_add_dword(code)


# push exx
asm_push_exx_code = {
    "eax": [0x50],
    "ebx": [0x53],
    "ecx": [0x51],
    "edx": [0x52],
    "esi": [0x56],
    "edi": [0x57],
    "ebp": [0x55],
    "esp": [0x54]
}


def asm_push_exx(register):
    asm_add_bytes(asm_push_exx_code[register])


# pop exx
asm_pop_exx_code = {
    "eax": [0x58],
    "ebx": [0x5B],
    "ecx": [0x59],
    "edx": [0x5A],
    "esi": [0x5E],
    "edi": [0x5F],
    "ebp": [0x5D],
    "esp": [0x5C]
}


def asm_pop_exx(register):
    asm_add_bytes(asm_pop_exx_code[register])


# ret
def asm_ret():
    asm_add_byte(0xC3)


# call 0x12345678
# call $ + 7
# jmp short $ + 8
# push 0x12345678
# ret
def asm_call(address):
    asm_add_bytes([0xE8, 0x02, 0x00, 0x00, 0x00])
    asm_add_bytes([0xEB, 0x06])
    asm_push(address)
    asm_ret()


# inject
def asm_code_inject():
    """
    远程注入汇编代码.
    """

    size = len(asm_code)

    # thread_addr = LPVOID()
    thread_addr = VirtualAllocEx(pvz_handle, None, size, MEM_COMMIT, PAGE_EXECUTE_READWRITE)

    if thread_addr is not None:

        bytes_written = ctypes.c_ulong()
        success = WriteProcessMemory(pvz_handle, thread_addr, asm_code, size, ctypes.byref(bytes_written))
        if success == 0 or bytes_written.value != size:
            critical("写入汇编代码失败, 错误代码 %d." % GetLastError())

        # thread_handle = HANDLE()
        start = LPTHREAD_START_ROUTINE(thread_addr)
        thread_handle = CreateRemoteThread(pvz_handle, None, 0, start, None, 0, None)

        if thread_handle is not None:
            success = WaitForSingleObject(thread_handle, INFINITE)
            if success == WAIT_FAILED:
                critical("等待对象返回失败, 错误代码 %d." % GetLastError())
            success = CloseHandle(thread_handle)
            if success == 0:
                critical("关闭远程线程句柄失败, 错误代码 %d." % GetLastError())
        else:
            critical("创建远程线程失败, 错误代码 %d." % GetLastError())

        success = VirtualFreeEx(pvz_handle, thread_addr, 0, MEM_RELEASE)
        if success == 0:
            critical("释放内存失败, 错误代码 %d." % GetLastError())

    else:
        critical("分配内存失败, 错误代码 %d." % GetLastError())

    info("远程注入代码: %s." % str([hex(x) for x in asm_code]))


# 避免崩溃
def asm_code_inject_safely():
    if pvz_ver() == "1.0.0.1051":
        write_memory("unsigned char", 0xFE, 0x00552014)
    else:
        write_memory("unsigned char", 0xFE, 0x00552244)
    time.sleep(0.01)
    if is_valid():
        asm_code_inject()
    if pvz_ver() == "1.0.0.1051":
        write_memory("unsigned char", 0xDB, 0x00552014)
    else:
        write_memory("unsigned char", 0xDB, 0x00552244)


### 键盘操作


def press_esc():
    """
    敲击 退出 键.
    """
    PostMessageW(pvz_hwnd, WM_KEYDOWN, VK_ESCAPE, 0)
    PostMessageW(pvz_hwnd, WM_KEYUP, VK_ESCAPE, 0)


def press_space():
    """
    敲击 空格 键.
    """
    PostMessageW(pvz_hwnd, WM_KEYDOWN, VK_SPACE, 0)
    PostMessageW(pvz_hwnd, WM_KEYUP, VK_SPACE, 0)


def press_enter():
    """
    敲击 回车 键.
    """
    PostMessageW(pvz_hwnd, WM_KEYDOWN, VK_RETURN, 0)
    PostMessageW(pvz_hwnd, WM_KEYUP, VK_RETURN, 0)


def press_left():
    """
    敲击 左方向 键.
    """
    PostMessageW(pvz_hwnd, WM_KEYDOWN, VK_LEFT, 0)
    PostMessageW(pvz_hwnd, WM_KEYUP, VK_LEFT, 0)


def press_up():
    """
    敲击 上方向 键.
    """
    PostMessageW(pvz_hwnd, WM_KEYDOWN, VK_UP, 0)
    PostMessageW(pvz_hwnd, WM_KEYUP, VK_UP, 0)


def press_right():
    """
    敲击 右方向 键.
    """
    PostMessageW(pvz_hwnd, WM_KEYDOWN, VK_RIGHT, 0)
    PostMessageW(pvz_hwnd, WM_KEYUP, VK_RIGHT, 0)


def press_down():
    """
    敲击 下方向 键.
    """
    PostMessageW(pvz_hwnd, WM_KEYDOWN, VK_DOWN, 0)
    PostMessageW(pvz_hwnd, WM_KEYUP, VK_DOWN, 0)


def press_key(key):
    """
    敲击按键. 可选值 '0' - '9' 'A' - 'Z'.
    """
    code = ord(key)
    PostMessageW(pvz_hwnd, WM_KEYDOWN, code, 0)
    PostMessageW(pvz_hwnd, WM_KEYUP, code, 0)


def press_keys(keys):
    """
    敲击一系列按键.

    @参数 keys(str): 按键字符串, 由 '0' - '9' 'A' - 'Z' 组成.

    @示例:

    >>> PressKeys("FUTURE")  # 智慧树指令, 使僵尸带上眼镜
    """
    for k in keys:
        press_key(k.upper())


### 鼠标操作

dpi_scale = 1.0


def get_dpi_scale():
    """
    获取 DPI 缩放比例.
    """
    screen = GetDC(None)
    if screen is not None:
        virtual_width = GetDeviceCaps(screen, HORZRES)
        physical_width = GetDeviceCaps(screen, DESKTOPHORZRES)
        ReleaseDC(None, screen)
        scale = physical_width / virtual_width
    else:
        scale = 1.0

    global dpi_scale
    dpi_scale = scale
    info("获取 DPI 缩放比例: %s." % dpi_scale)


def set_dpi_scale(scale):
    """
    设置 DPI 缩放比例.

    @参数 scale(float): 比例系数.
    """
    global dpi_scale
    dpi_scale = scale
    info("设置 DPI 缩放比例: %s." % dpi_scale)


def MAKELONG(low, high):
    # low += 0  # 加上画面横坐标偏移 [[[6a9ec0]+768]+30]
    if dpi_scale != 1.0:
        low, high = int(low / dpi_scale), int(high / dpi_scale)
    else:
        low, high = int(low), int(high)
    return ((high & 0xFFFF) << 16) | (low & 0xFFFF)


def left_down(x, y):
    """
    鼠标左键按下.
    """
    coord = MAKELONG(x, y)
    PostMessageW(pvz_hwnd, WM_LBUTTONDOWN, MK_LBUTTON, coord)


def left_up(x, y):
    """
    鼠标左键弹起.
    """
    coord = MAKELONG(x, y)
    PostMessageW(pvz_hwnd, WM_LBUTTONUP, MK_LBUTTON, coord)


def left_click(x, y):
    """
    鼠标左键单击.

    @参数 x(int): 横坐标, 单位像素. 建议范围 [0, 799].

    @参数 y(int): 纵坐标, 单位像素. 建议范围 [0, 599].

    @示例:

    >>> LeftClick(108, 42)  # 左键单击卡槽第一张卡片的位置
    """
    coord = MAKELONG(x, y)
    PostMessageW(pvz_hwnd, WM_LBUTTONDOWN, MK_LBUTTON, coord)
    PostMessageW(pvz_hwnd, WM_LBUTTONUP, MK_LBUTTON, coord)


def right_down(x, y):
    """
    鼠标右键按下.
    """
    coord = MAKELONG(x, y)
    PostMessageW(pvz_hwnd, WM_RBUTTONDOWN, MK_RBUTTON, coord)


def right_up(x, y):
    """
    鼠标右键弹起.
    """
    coord = MAKELONG(x, y)
    PostMessageW(pvz_hwnd, WM_RBUTTONUP, MK_RBUTTON, coord)


def right_click(x, y):
    """
    鼠标右键单击.

    @参数 x(int): 横坐标, 单位像素. 建议范围 [0, 799].

    @参数 y(int): 纵坐标, 单位像素. 建议范围 [0, 599].

    @示例:

    >>> RightClick(399, 299)  # 右键单击场地中间位置
    """
    coord = MAKELONG(x, y)
    PostMessageW(pvz_hwnd, WM_RBUTTONDOWN, MK_RBUTTON, coord)
    PostMessageW(pvz_hwnd, WM_RBUTTONUP, MK_RBUTTON, coord)


def special_button_click(x, y):
    """
    适用于模仿者按钮和菜单按钮的特殊点击.

    调用的时候不要把鼠标光标放在游戏窗口内.

    @参数 x(int): 横坐标, 单位像素. 建议范围 [0, 799].

    @参数 y(int): 纵坐标, 单位像素. 建议范围 [0, 599].

    @示例:

    >>> ButtonClick(490, 550)  # 选卡界面点击模仿者卡片

    >>> ButtonClick(740, 10)  # 点击菜单按钮
    """
    left_down(x, y)
    right_down(x, y)
    left_up(x, y)
    right_up(x, y)
    time.sleep(0.01)


### 卡片和僵尸名称

seeds_string = [
    ["Peashooter", "豌豆射手", "豌豆", "单发"],
    ["Sunflower", "向日葵", "小向", "太阳花", "花"],
    ["Cherry Bomb", "樱桃炸弹", "樱桃", "炸弹", "爆炸", "草莓", "樱"],
    ["Wall-nut", "坚果", "坚果墙", "墙果", "建国", "柠檬圆"],
    ["Potato Mine", "土豆地雷", "土豆", "地雷", "土豆雷"],
    ["Snow Pea", "寒冰射手", "冰豆", "冰冻豌豆", "冰豌豆", "雪花豌豆", "雪花"],
    ["Chomper", "大嘴花", "大嘴", "食人花", "咀嚼者", "食"],
    ["Repeater", "双重射手", "双发射手", "双重", "双发", "双发豌豆"],
    ["Puff-shroom", "小喷菇", "小喷", "喷汽蘑菇", "烟雾蘑菇", "免费蘑菇", "炮灰菇", "小蘑菇", "免费货", "免费", "紫蘑菇"],
    ["Sun-shroom", "阳光菇", "阳光", "阳光蘑菇"],
    ["Fume-shroom", "大喷菇", "大喷", "烟雾喷菇", "大蘑菇", "喷子", "喷"],
    ["Grave Buster", "咬咬碑", "墓碑吞噬者", "墓碑破坏者", "噬碑藤", "墓碑", "墓碑苔藓", "苔藓"],
    ["Hypno-shroom", "迷糊菇", "魅惑菇", "魅惑", "迷惑菇", "迷蘑菇", "催眠蘑菇", "催眠", "花蘑菇", "毒蘑菇"],
    ["Scaredy-shroom", "胆小菇", "胆小", "胆怯蘑菇", "胆小鬼蘑菇", "杠子蘑菇"],
    ["Ice-shroom", "冰川菇", "寒冰菇", "冰菇", "冷冻蘑菇", "冰蘑菇", "冰莲菇", "面瘫", "蓝冰", "原版冰", "冰"],
    ["Doom-shroom", "末日菇", "毁灭菇", "核蘑菇", "核弹", "核武", "毁灭", "末日蘑菇", "末日", "黑核", "原版核", "核"],
    ["Lily Pad", "莲叶", "睡莲", "荷叶", "莲"],
    ["Squash", "窝瓜", "倭瓜", "窝瓜大叔", "倭瓜大叔", "镇压者"],
    ["Threepeater", "三重射手", "三线射手", "三头豌豆", "三联装豌豆", "三重", "三线", "三头", "三管", "管"],
    ["Tangle Kelp", "缠绕水草", "缠绕海草", "缠绕海藻", "缠绕海带", "水草", "海草", "海藻", "海带", "马尾藻", "绿毛线", "毛线"],
    ["Jalapeno", "火爆辣椒", "辣椒", "墨西哥胡椒", "墨西哥辣椒", "辣", "椒"],
    ["Spikeweed", "地刺", "刺", "尖刺", "尖刺杂草", "棘草", "荆棘"],
    ["Torchwood", "火炬树桩", "火树桩", "火树", "火炬", "树桩", "火炬木", "火"],
    ["Tall-nut", "高坚果", "搞基果", "高建国", "巨大墙果", "巨大", "高墙果", "大墙果", "大土豆"],
    ["Sea-shroom", "水兵菇", "海蘑菇"],
    ["Plantern", "路灯花", "灯笼", "路灯", "灯笼草", "灯笼花", "吐槽灯", "灯"],
    ["Cactus", "仙人掌", "小仙", "掌"],
    ["Blover", "三叶草", "三叶", "风扇", "吹风", "愤青"],
    ["Split Pea", "双向射手", "裂荚射手", "裂荚", "双头", "分裂豌豆", "双头豌豆"],
    ["Starfruit", "星星果", "杨桃", "星星", "五角星", "五星黄果", "1437", "大帝", "桃"],
    ["Pumpkin", "南瓜头", "南瓜", "南瓜罩", "南瓜壳", "套"],
    ["Magnet-shroom", "磁力菇", "磁铁", "磁力蘑菇", "磁"],
    ["Cabbage-pult", "卷心菜投手", "包菜", "卷心菜", "卷心菜投抛者", "包菜投掷手"],
    ["Flower Pot", "花盆", "盆"],
    ["Kernel-pult", "玉米投手", "玉米", "黄油投手", "玉米投抛者", "玉米投掷手"],
    ["Coffee Bean", "咖啡豆", "咖啡", "兴奋剂", "春药"],
    ["Garlic", "大蒜", "蒜"],
    ["Umbrella Leaf", "萝卜伞", "叶子保护伞", "伞型保护叶", "莴苣", "萝卜", "白菜", "保护伞", "叶子伞", "伞叶", "叶子", "伞", "叶"],
    ["Marigold", "金盏花", "金盏草", "金盏菊", "吐钱花"],
    ["Melon-pult", "西瓜投手", "西瓜", "绿皮瓜", "瓜", "西瓜投抛者", "西瓜投掷手"],
    ["Gatling Pea", "机枪射手", "加特林豌豆", "格林豌豆", "加特林", "机枪", "枪"],
    ["Twin Sunflower", "双胞向日葵", "双子向日葵", "双头葵花", "双胞", "双子", "双向", "双花"],
    ["Gloom-shroom", "多嘴小蘑菇", "忧郁蘑菇", "忧郁", "忧郁菇", "章鱼", "曾哥", "曾哥蘑菇", "曾"],
    ["Cattail", "猫尾草", "香蒲", "猫尾", "猫尾香蒲", "小猫香蒲", "小猫", "猫"],
    ["Winter Melon", "冰西瓜", "'冰'瓜", '"冰"瓜', "冰瓜", "冰冻西瓜", "冬季西瓜"],
    ["Gold Magnet", "吸金菇", "吸金磁", "吸金草", "金磁铁", "吸金", "磁力金钱菇"],
    ["Spikerock", "钢地刺", "钢刺", "地刺王", "尖刺岩石", "尖刺石", "石荆棘"],
    ["Cob Cannon", "玉米加农炮", "玉米炮", "加农炮", "春哥", "春哥炮", "炮", "春", "神"],
]

# # 确保没有重复项, 发布时注释掉
# seeds_string_all = []
# for items in seeds_string:
#     seeds_string_all += items
# print(len(seeds_string_all))
# assert len(seeds_string_all) == len(set(seeds_string_all))

# 模仿者卡片前缀
seeds_imitater_string = ["Imitater", "imitater", "变身茄子", "模仿者", "模仿", "复制", "白", "小白", "克隆"]

# 整理成字典方便快速查找
# key: 卡片名称
# value: 卡片代号 0~47 (模仿者 +48)
seeds_string_dict = {}
for i, items in enumerate(seeds_string):
    for item in items:
        # 绿卡 紫卡
        seeds_string_dict[item] = i
        # 白卡
        for j, im in enumerate(seeds_imitater_string):
            seeds_string_dict[im + item] = i + 48
            seeds_string_dict[im + " " + item] = i + 48
# print(len(seeds_string_dict))  # it's huge!!!

zombies_string = [
    ["Zombie", "普僵", "普通", "领带"],
    ["Flag Zombie", "旗帜", "摇旗", "旗子"],
    ["Conehead Zombie", "路障"],
    ["Pole Vaulting Zombie", "撑杆", "撑杆跳"],
    ["Buckethead Zombie", "铁桶"],
    ["Newspaper Zombie", "读报", "报纸"],
    ["Screen Door Zombie", "铁门", "铁栅门", "门板"],
    ["Football Zombie", "橄榄", "橄榄球"],
    ["Dancing Zombie", "舞王", "MJ"],
    ["Backup Dancer", "伴舞", "舞伴"],
    ["Ducky Tube Zombie", "鸭子", "救生圈"],
    ["Snorkel Zombie", "潜水"],
    ["Zomboni", "冰车", "制冰车"],
    ["Zombie Bobsled Team", "雪橇", "雪橇队", "雪橇小队"],
    ["Dolphin Rider Zombie", "海豚", "海豚骑士"],
    ["Jack-in-the-Box Zombie", "小丑", "玩偶匣"],
    ["Balloon Zombie", "气球"],
    ["Digger Zombie", "矿工", "挖地"],
    ["Pogo Zombie", "跳跳", "弹跳"],
    ["Zombie Yeti", "雪人"],
    ["Bungee Zombie", "蹦极", "小偷"],
    ["Ladder Zombie", "扶梯", "梯子"],
    ["Catapult Zombie", "投篮", "投篮车", "篮球"],
    ["Gargantuar", "白眼", "伽刚特尔", "巨人"],
    ["Imp", "小鬼", "小恶魔", "IMP"],
    ["Dr. Zomboss", "僵王", "僵博"],
    ["Peashooter Zombie", "豌豆"],
    ["Wall-nut Zombie", "坚果"],
    ["Jalapeno Zombie", "辣椒"],
    ["Gatling Pea Zombie", "机枪", "加特林"],
    ["Squash Zombie", "倭瓜", "窝瓜"],
    ["Tall-nut Zombie", "高坚果"],
    ["GigaGargantuar", "红眼", "暴走伽刚特尔", "红眼巨人"],
]

zombies_string_dict = {}
for i, zombies in enumerate(zombies_string):
    for j, z in enumerate(zombies):
        if j == 0:  # 第一个英文名称
            zombies_string_dict[z] = i
        else:
            zombies_string_dict[z] = i
            zombies_string_dict[z + "僵尸"] = i
# print(len(zombies_string_dict))

### 延时


def thread_sleep_for(time_cs):
    """
    线程睡眠延时.

    实际睡眠时间依赖于操作系统线程切换时间片精度.

    @参数 time_cs(float): 时间, 单位 cs, 精度 0.1.
    """

    if time_cs > 0.0:
        time.sleep(time_cs / 100)
    elif time_cs == 0.0:
        pass
    else:
        error("线程睡眠时间不能小于零.")


# 细微延时
def delay_a_little_time():
    thread_sleep_for(0.1)  # 1ms


### 子线程装饰器


def running_in_thread(func):
    """
    将此装饰器应用到需要在子线程运行的函数上.

    定义一个函数, 应用该装饰器, 则函数在调用的时候会运行在单独的线程中.

    @示例:

    >>> @RunningInThread
    >>> def func():
    >>>     pass
    >>> # ...
    >>> func()
    """
    @functools.wraps(func)  # 复制原函数元信息
    def wrapper(*args, **kwargs):
        thread = threading.Thread(target=func, args=args, kwargs=kwargs)
        # thread.setDaemon(True)  # 守护线程
        thread.start()

    return wrapper
