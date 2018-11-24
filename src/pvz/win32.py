# coding=utf-8

"""
Windows API
"""

import ctypes

### win32 types

from ctypes import POINTER
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


### win32 constants

PROCESS_ALL_ACCESS = 0x001F0FFF

STILL_ACTIVE = 0x00000103

TIMERR_NOERROR = 0

MEM_COMMIT = 0x00001000
MEM_RELEASE = 0x00008000
PAGE_EXECUTE_READWRITE = 0x40
INFINITE = 0xFFFFFFFF

WM_LBUTTONDOWN = 0x0201
WM_LBUTTONUP = 0x0202
WM_RBUTTONDOWN = 0x0204
WM_RBUTTONUP = 0x0205

MK_LBUTTON = 0x0001
MK_RBUTTON = 0x0002

WM_KEYDOWN = 0x0100
WM_KEYUP = 0x0101

VK_ESCAPE = 0x1B
VK_SPACE = 0x20

VK_LEFT = 0x25
VK_UP = 0x26
VK_RIGHT = 0x27
VK_DOWN = 0x28

REALTIME_PRIORITY_CLASS = 0x00000100
HIGH_PRIORITY_CLASS = 0x00000080
ABOVE_NORMAL_PRIORITY_CLASS = 0x00008000
NORMAL_PRIORITY_CLASS = 0x00000020
BELOW_NORMAL_PRIORITY_CLASS = 0x00004000
IDLE_PRIORITY_CLASS = 0x00000040

HORZRES = 8
DESKTOPHORZRES = 118


### win32 dlls

user32 = ctypes.windll.user32
kernel32 = ctypes.windll.kernel32
winmm = ctypes.windll.winmm
gdi32 = ctypes.windll.gdi32


### win32 apis

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

# BOOL GetExitCodeProcess(
#   HANDLE  hProcess,
#   LPDWORD lpExitCode
# );
GetExitCodeProcess = kernel32.GetExitCodeProcess
GetExitCodeProcess.argtypes = [HANDLE, LPDWORD]
GetExitCodeProcess.restype = BOOL

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

# BOOL WINAPI VirtualFreeEx(
#   _In_ HANDLE hProcess,
#   _In_ LPVOID lpAddress,
#   _In_ SIZE_T dwSize,
#   _In_ DWORD  dwFreeType
# );
VirtualFreeEx = kernel32.VirtualFreeEx
VirtualFreeEx.argtypes = [HANDLE, LPVOID, SIZE_T, DWORD]
VirtualFreeEx.restype = BOOL

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

# DWORD WINAPI GetLastError(void);
GetLastError = kernel32.GetLastError
GetLastError.argtypes = []
GetLastError.restype = DWORD

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

# HWND WindowFromPoint(
#   POINT Point
# );
WindowFromPoint = user32.WindowFromPoint
WindowFromPoint.argtypes = [POINT]
WindowFromPoint.restype = HWND

# BOOL GetWindowRect(
#   HWND   hWnd,
#   LPRECT lpRect
# );
GetWindowRect = user32.GetWindowRect
GetWindowRect.argtypes = [HWND, LPRECT]
GetWindowRect.restype = BOOL

# BOOL GetCursorPos(
#   LPPOINT lpPoint
# );
GetCursorPos = user32.GetCursorPos
GetCursorPos.argtypes = [LPPOINT]
GetCursorPos.restype = BOOL

# BOOL SetCursorPos(
#   int X,
#   int Y
# );
SetCursorPos = user32.SetCursorPos
SetCursorPos.argtypes = [INT, INT]
SetCursorPos.restype = BOOL

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

# int ReleaseDC(
#   HWND hWnd,
#   HDC  hDC
# );
ReleaseDC = user32.ReleaseDC
ReleaseDC.argtypes = [HWND, HDC]
ReleaseDC.restype = INT
