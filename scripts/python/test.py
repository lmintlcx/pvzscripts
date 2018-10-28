# -*- coding: utf-8 -*-













# ### Assembly Code

# _asm_code = bytes()

# # init


# def _asm_init():
#     global _asm_code
#     _asm_code = bytes()


# # basic


# # unsigned char
# def _asm_add_byte(value):
#     global _asm_code
#     _asm_code += struct.pack("<1B", value)


# # unsigned short
# def _asm_add_word(value):
#     global _asm_code
#     _asm_code += struct.pack("<1H", value)


# # unsigned int
# def _asm_add_dword(value):
#     global _asm_code
#     _asm_code += struct.pack("<1I", value)


# # bytes from list/tuple
# def _asm_add_bytes(values):
#     for code in values:
#         _asm_add_byte(code)


# # push 0x12345678


# def _asm_push(value):
#     _asm_add_byte(0x68)
#     _asm_add_dword(value)


# # mov exx, 0x12345678

# _asm_mov_exx_code = {
#     "eax": [0xB8],
#     "ebx": [0xBB],
#     "ecx": [0xB9],
#     "edx": [0xBA],
#     "esi": [0xBE],
#     "edi": [0xBF],
#     "ebp": [0xBD],
#     "esp": [0xBC],
# }


# def _asm_mov_exx(register, value):
#     _asm_add_bytes(_asm_mov_exx_code[register])
#     _asm_add_dword(value)


# # add exx, 0x12345678

# _asm_add_exx_code = {
#     "eax": [0x05],
#     "ebx": [0x81, 0xC3],
#     "ecx": [0x81, 0xC1],
#     "edx": [0x81, 0xC2],
#     "esi": [0x81, 0xC6],
#     "edi": [0x81, 0xC7],
#     "ebp": [0x81, 0xC5],
#     "esp": [0x81, 0xC4],
# }


# def _asm_add_exx(register, value):
#     _asm_add_bytes(_asm_add_exx_code[register])
#     _asm_add_dword(value)


# # mov exx, ds:[0x12345678]

# _asm_mov_exx_dword_ptr_code = {
#     "eax": [0x3E, 0xA1],
#     "ebx": [0x3E, 0x8B, 0x1D],
#     "ecx": [0x3E, 0x8B, 0x0D],
#     "edx": [0x3E, 0x8B, 0x15],
#     "esi": [0x3E, 0x8B, 0x35],
#     "edi": [0x3E, 0x8B, 0x3D],
#     "ebp": [0x3E, 0x8B, 0x2D],
#     "esp": [0x3E, 0x8B, 0x25],
# }


# def _asm_mov_exx_dword_ptr(register, value):
#     _asm_add_bytes(_asm_mov_exx_dword_ptr_code[register])
#     _asm_add_dword(value)


# # mov exx, [exx + 0x12345678]

# _asm_mov_exx_dword_ptr_exx_add_code = {
#     "eax": [0x8B, 0x80],
#     "ebx": [0x8B, 0x9B],
#     "ecx": [0x8B, 0x89],
#     "edx": [0x8B, 0x92],
#     "esi": [0x8B, 0xB6],
#     "edi": [0x8B, 0xBF],
#     "ebp": [0x8B, 0xAD],
#     "esp": [0x8B, 0xA4, 0x24],
# }


# def _asm_mov_exx_dword_ptr_exx_add(register, value):
#     _asm_add_bytes(_asm_mov_exx_dword_ptr_exx_add_code[register])
#     _asm_add_dword(value)


# # push exx

# _asm_push_exx_code = {
#     "eax": [0x50],
#     "ebx": [0x53],
#     "ecx": [0x51],
#     "edx": [0x52],
#     "esi": [0x56],
#     "edi": [0x57],
#     "ebp": [0x55],
#     "esp": [0x54],
# }


# def _asm_push_exx(register):
#     _asm_add_bytes(_asm_push_exx_code[register])


# # pop exx

# _asm_pop_exx_code = {
#     "eax": [0x58],
#     "ebx": [0x5B],
#     "ecx": [0x59],
#     "edx": [0x5A],
#     "esi": [0x5E],
#     "edi": [0x5F],
#     "ebp": [0x5D],
#     "esp": [0x5C],
# }


# def _asm_pop_exx(register):
#     _asm_add_bytes(_asm_pop_exx_code[register])


# # ret


# def _asm_ret():
#     _asm_add_byte(0xC3)


# # call 0x12345678

# # call $ + 7
# # jmp short $ + 8
# # push 0x12345678
# # ret
# def _asm_call(address):
#     _asm_add_bytes([0xE8, 0x02, 0x00, 0x00, 0x00])
#     _asm_add_bytes([0xEB, 0x06])
#     _asm_push(address)
#     _asm_ret()


# # inject


# def _asm_code_inject():
#     """
#     远程注入汇编代码.
#     """

#     length = len(_asm_code)

#     # thread_addr = _LPVOID()
#     thread_addr = _VirtualAllocEx(
#         _pvz_handle, None, length, _MEM_COMMIT, _PAGE_EXECUTE_READWRITE
#     )

#     if thread_addr is not None:
#         _WriteProcessMemory(_pvz_handle, thread_addr, _asm_code, length, None)

#         # thread_handle = _HANDLE()
#         start = _LPTHREAD_START_ROUTINE(thread_addr)
#         thread_handle = _CreateRemoteThread(_pvz_handle, None, 0, start, None, 0, None)

#         if thread_handle is not None:
#             _WaitForSingleObject(thread_handle, _INFINITE)
#             _CloseHandle(thread_handle)

#         _VirtualFreeEx(_pvz_handle, thread_addr, 0, _MEM_RELEASE)

#     _logger.debug(f"Inject assembly code {[hex(x) for x in _asm_code]}.")


# # 避免崩溃
# def _asm_code_inject_safely():
#     _write_memory("unsigned char", 0xFE, 0x00552014)
#     time.sleep(0.01)
#     if _is_process_valid():
#         _asm_code_inject()
#     _write_memory("unsigned char", 0xDB, 0x00552014)


# ### utils


# def _get_gold_sunflower_trophy():
#     """
#     解锁金向日葵.
#     """

#     if _is_game_on():

#         # Adventure 2 times
#         if _read_memory("int", 0x6A9EC0, 0x82C, 0x2C) < 2:
#             _write_memory("int", 2, 0x6A9EC0, 0x82C, 0x2C)

#         # Mini-games
#         for i in range(33):
#             if _read_memory("int", 0x6A9EC0, 0x82C, 0x6C + i * 4) == 0:
#                 _write_memory("int", 1, 0x6A9EC0, 0x82C, 0x6C + i * 4)

#         # Vasebreaker
#         for i in range(9):
#             if _read_memory("int", 0x6A9EC0, 0x82C, 0xF8 + i * 4) == 0:
#                 _write_memory("int", 1, 0x6A9EC0, 0x82C, 0xF8 + i * 4)

#         # I, Zombie
#         for i in range(9):
#             if _read_memory("int", 0x6A9EC0, 0x82C, 0x120 + i * 4) == 0:
#                 _write_memory("int", 1, 0x6A9EC0, 0x82C, 0x120 + i * 4)

#         # Survival
#         for i in range(5):
#             if _read_memory("int", 0x6A9EC0, 0x82C, 0x30 + i * 4) < 5:
#                 _write_memory("int", 5, 0x6A9EC0, 0x82C, 0x30 + i * 4)

#         # Survival Hard
#         for i in range(5):
#             if _read_memory("int", 0x6A9EC0, 0x82C, 0x44 + i * 4) < 10:
#                 _write_memory("int", 10, 0x6A9EC0, 0x82C, 0x44 + i * 4)


# def _get_all_shop_items():
#     """
#     获得所有商店物品.
#     """

#     if _is_game_on():

#         _write_memory("int", 1, 0x6A9EC0, 0x82C, 0x1C0)  # Gatling Pea
#         _write_memory("int", 1, 0x6A9EC0, 0x82C, 0x1C4)  # Twin Sunflower
#         _write_memory("int", 1, 0x6A9EC0, 0x82C, 0x1C8)  # Gloom-shroom
#         _write_memory("int", 1, 0x6A9EC0, 0x82C, 0x1CC)  # Cattail
#         _write_memory("int", 1, 0x6A9EC0, 0x82C, 0x1D0)  # Winter Melon
#         _write_memory("int", 1, 0x6A9EC0, 0x82C, 0x1D4)  # Gold Magnet
#         _write_memory("int", 1, 0x6A9EC0, 0x82C, 0x1D8)  # Spikerock
#         _write_memory("int", 1, 0x6A9EC0, 0x82C, 0x1DC)  # Cob Cannon

#         _write_memory("int", 1, 0x6A9EC0, 0x82C, 0x1E0)  # Imitater
#         _write_memory("int", 1, 0x6A9EC0, 0x82C, 0x234)  # Wall-nut First Aid

#         _write_memory("int", 4, 0x6A9EC0, 0x82C, 0x214)  # 10 seed slots
#         _write_memory("int", 1, 0x6A9EC0, 0x82C, 0x218)  # Pool Cleaner
#         _write_memory("int", 1, 0x6A9EC0, 0x82C, 0x21C)  # Roof Cleaner
#         _write_memory("int", 1, 0x6A9EC0, 0x82C, 0x220)  # Garden Rake (left)

#         _write_memory("int", 0, 0x6A9EC0, 0x82C, 0x1E8)  # Marigold Sprout #1
#         _write_memory("int", 0, 0x6A9EC0, 0x82C, 0x1EC)  # Marigold Sprout #2
#         _write_memory("int", 0, 0x6A9EC0, 0x82C, 0x1F0)  # Marigold Sprout #3
#         _write_memory("int", 1, 0x6A9EC0, 0x82C, 0x1F4)  # Golden Watering
#         if _read_memory("int", 0x6A9EC0, 0x82C, 0x1F8) == 0:  #
#             _write_memory("int", 1020, 0x6A9EC0, 0x82C, 0x1F8)  # Fertilizer 20->1020
#         if _read_memory("int", 0x6A9EC0, 0x82C, 0x1FC) == 0:  #
#             _write_memory("int", 1020, 0x6A9EC0, 0x82C, 0x1FC)  # Bug Spray 20->1020
#         _write_memory("int", 1, 0x6A9EC0, 0x82C, 0x200)  # Phonograph
#         _write_memory("int", 1, 0x6A9EC0, 0x82C, 0x204)  # Gardening Glove

#         _write_memory("int", 1, 0x6A9EC0, 0x82C, 0x208)  # Mushroom Garden
#         _write_memory("int", 1, 0x6A9EC0, 0x82C, 0x224)  # Aquarium Garden
#         _write_memory("int", 1, 0x6A9EC0, 0x82C, 0x22C)  # Tree of Wisdom
#         if _read_memory("int", 0x6A9EC0, 0x82C, 0x230) == 0:  #
#             _write_memory("int", 1020, 0x6A9EC0, 0x82C, 0x230)  # Tree Food 20->1020
#         _write_memory("int", 1, 0x6A9EC0, 0x82C, 0x20C)  # Wheel Barrow
#         _write_memory("int", 1, 0x6A9EC0, 0x82C, 0x210)  # Snail
#         if _read_memory("int", 0x6A9EC0, 0x82C, 0x228) == 0:  #
#             _write_memory("int", 1020, 0x6A9EC0, 0x82C, 0x228)  # Chocolate 20->1020


# def _unlock_all_mode(on=True):
#     """
#     临时解锁所有模式.
#     """

#     if _is_game_on():

#         if on:
#             _write_memory("unsigned char", 0x70, 0x00454109)
#             _write_memory("unsigned char", 0x70, 0x0044a514)
#             _write_memory("unsigned char", [0x31, 0xc0, 0xc3], 0x0042e440)
#             _write_memory("unsigned char", 0xeb, 0x00449e9d)
#             _write_memory("unsigned char", [0x30, 0xc0, 0xc3], 0x0048aad0)
#             _write_memory("unsigned char", 0xeb, 0x0048a54c)
#             _write_memory("unsigned char", 0xeb, 0x0048d32b)
#             _write_memory("unsigned char", 0xeb, 0x0048c491)
#             _write_memory("unsigned char", 0xeb, 0x00449e7a)
#             _write_memory("unsigned char", 0xeb, 0x00453ad1)
#             _write_memory("int", 0x5beb01b0, 0x00403a10)
#             _write_memory("int", 0x00000000, 0x0069dca0)
#             _write_memory("unsigned char", [0xb0, 0x01, 0xc3], 0x00403b30)
#         else:
#             _write_memory("unsigned char", 0x7e, 0x00454109)
#             _write_memory("unsigned char", 0x7e, 0x0044a514)
#             _write_memory("unsigned char", [0x51, 0x53, 0x55], 0x0042e440)
#             _write_memory("unsigned char", 0x7f, 0x00449e9d)
#             _write_memory("unsigned char", [0x53, 0x8b, 0xd9], 0x0048aad0)
#             _write_memory("unsigned char", 0x7f, 0x0048a54c)
#             _write_memory("unsigned char", 0x7f, 0x0048d32b)
#             _write_memory("unsigned char", 0x7f, 0x0048c491)
#             _write_memory("unsigned char", 0x7f, 0x00449e7a)
#             _write_memory("unsigned char", 0x7f, 0x00453ad1)
#             _write_memory("int", 0x6c8b5551, 0x00403a10)
#             _write_memory("int", 0x00000028, 0x0069dca0)
#             _write_memory("unsigned char", [0x8b, 0x80, 0x6c], 0x00403b30)


# def _direct_win():
#     """
#     直接过关.
#     """
#     if _is_game_on() and _get_game_ui() in [3]:
#         _asm_init()
#         _asm_mov_exx_dword_ptr("ecx", 0x6a9ec0)
#         _asm_mov_exx_dword_ptr_exx_add("ecx", 0x768)
#         _asm_call(0x0040c3e0)
#         _asm_ret()
#         _asm_code_inject()


# def _mix_mode(mode, level=1):
#     """
#     混乱模式.

#     @参数 mode(int): 模式代号, 范围 0~72.

#     @参数 level(int): 冒险模式关卡数
#     """

#     if _is_game_on() and _get_game_ui() in [2, 3]:
#         if mode == 0:
#             _write_memory("int", level, 0x6a9ec0, 0x82c, 0x24)
#             _write_memory("int", level, 0x6a9ec0, 0x768, 0x5550)
#         _write_memory("int", mode, 0x6a9ec0, 0x7f8)


# def _show_hide_games(on=True):
#     """
#     显式隐藏小游戏.
#     """
#     if _is_game_on():
#         if on:
#             _write_memory("unsigned char", 0x38, 0x0042df5d)
#         else:
#             _write_memory("unsigned char", 0x88, 0x0042df5d)


# def _jump_level(level=1008):
#     """
#     无尽模式跳关.

#     @参数 level(int): 关卡数.
#     """

#     if _is_game_on() and _get_game_ui() in [2, 3]:
#         mode = _get_game_mode()
#         if mode in [60, 70, 11, 12, 13, 14, 15]:
#             _write_memory("int", level, 0x6a9ec0, 0x768, 0x160, 0x6c)


# def _asm_put_ladder(row, col):
#     _asm_mov_exx("edi", row)
#     _asm_push(col)
#     _asm_mov_exx_dword_ptr("eax", 0x6A9EC0)
#     _asm_mov_exx_dword_ptr_exx_add("eax", 0x768)
#     _asm_call(0x00408F40)


# def Ladder(row, col):
#     _asm_init()
#     _asm_put_ladder(row - 1, col - 1)
#     _asm_ret()
#     _asm_code_inject()
