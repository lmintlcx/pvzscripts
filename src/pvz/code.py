# coding=utf-8

"""
Assembly Code
"""

import struct
import time
import ctypes

from . import logger
from . import win32
from . import process

#

asm_code = bytes()

# init


def asm_init():
    global asm_code
    asm_code = bytes()


# basic


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


# mov exx, 0x12345678

asm_mov_exx_code = {"eax": [0xB8], "ebx": [0xBB], "ecx": [0xB9], "edx": [0xBA], "esi": [0xBE], "edi": [0xBF], "ebp": [0xBD], "esp": [0xBC]}


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

asm_push_exx_code = {"eax": [0x50], "ebx": [0x53], "ecx": [0x51], "edx": [0x52], "esi": [0x56], "edi": [0x57], "ebp": [0x55], "esp": [0x54]}


def asm_push_exx(register):
    asm_add_bytes(asm_push_exx_code[register])


# pop exx

asm_pop_exx_code = {"eax": [0x58], "ebx": [0x5B], "ecx": [0x59], "edx": [0x5A], "esi": [0x5E], "edi": [0x5F], "ebp": [0x5D], "esp": [0x5C]}


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
    thread_addr = win32.VirtualAllocEx(process.pvz_handle, None, size, win32.MEM_COMMIT, win32.PAGE_EXECUTE_READWRITE)

    if thread_addr is not None:

        bytes_written = ctypes.c_ulong()
        success = win32.WriteProcessMemory(process.pvz_handle, thread_addr, asm_code, size, ctypes.byref(bytes_written))
        if success == 0 or bytes_written.value != size:
            logger.critical(f"写入汇编代码失败, 错误代码 {win32.GetLastError()}.")

        # thread_handle = HANDLE()
        start = win32.LPTHREAD_START_ROUTINE(thread_addr)
        thread_handle = win32.CreateRemoteThread(process.pvz_handle, None, 0, start, None, 0, None)

        if thread_handle is not None:
            success = win32.WaitForSingleObject(thread_handle, win32.INFINITE)
            if success == win32.WAIT_FAILED:
                logger.critical(f"等待对象返回失败, 错误代码 {win32.GetLastError()}.")
            success = win32.CloseHandle(thread_handle)
            if success == 0:
                logger.critical(f"关闭远程线程句柄失败, 错误代码 {win32.GetLastError()}.")
        else:
            logger.critical(f"创建远程线程失败, 错误代码 {win32.GetLastError()}.")

        success = win32.VirtualFreeEx(process.pvz_handle, thread_addr, 0, win32.MEM_RELEASE)
        if success == 0:
            logger.critical(f"释放内存失败, 错误代码 {win32.GetLastError()}.")

    else:
        logger.critical(f"分配内存失败, 错误代码 {win32.GetLastError()}.")

    logger.info(f"远程注入代码成功: {[hex(x) for x in asm_code]}.")


# 避免崩溃
def asm_code_inject_safely():
    process.write_memory("unsigned char", 0xFE, 0x00552014)
    time.sleep(0.01)
    if process.is_valid():
        asm_code_inject()
    process.write_memory("unsigned char", 0xDB, 0x00552014)
