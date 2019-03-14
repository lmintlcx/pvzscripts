# coding=utf-8

"""
Helper
"""

import time
import os
import shutil
import glob

from . import logger
from . import process
from . import utils
from . import mouse
from . import keyboard


# 1: 主界面, 2: 选卡, 3: 正常游戏/战斗, 4: 僵尸进屋, 7: 模式选择.


def goto_main_ui():
    """
    切换到主界面. 需要先开启后台运行.
    """
    ui = utils.game_ui()

    if ui == 1:
        time.sleep(0.5)  # 不动

    elif ui == 2:
        time.sleep(0.2)
        if utils.game_paused():
            keyboard.restore_game()  # 取消暂停
        time.sleep(0.2)
        while not process.read_memory("bool", 0x6A9EC0, 0x320, 0x94, 0x54):
            mouse.special_button_click(740, 10)  # Menu
            time.sleep(0.3)
        mouse.left_click(400, 400)  # Main Menu
        if process.read_memory("int", 0x6A9EC0, 0x768, 0x160, 0x6C) != 0:
            # 非首次选卡
            time.sleep(0.3)
            mouse.left_click(310, 420)  # Leave
        time.sleep(1)  # 等待进主界面

    elif ui == 3:
        time.sleep(0.2)
        if utils.game_paused():
            keyboard.restore_game()  # 取消暂停
        time.sleep(0.2)
        while not process.read_memory("bool", 0x6A9EC0, 0x320, 0x94, 0x54):
            mouse.special_button_click(740, 10)  # Menu
            time.sleep(0.3)
        mouse.left_click(400, 400)  # Main Menu
        time.sleep(0.3)
        mouse.left_click(310, 420)  # Leave
        time.sleep(1)

    elif ui == 4:
        time.sleep(0.2)
        while not process.read_memory("bool", 0x6A9EC0, 0x320, 0x94, 0x54):
            # 食脑后等待显示对话框
            time.sleep(0.2)
        time.sleep(0.3)
        mouse.special_button_click(740, 10)  # Menu
        time.sleep(0.3)
        mouse.left_click(70, 580)  # Back to Menu
        time.sleep(1)

    elif ui == 7:
        time.sleep(0.3)
        mouse.left_click(70, 580)  # Back to Menu
        time.sleep(1)


def goto_survival_endless():
    """
    切换到无尽模式选卡界面. 需要先开启后台运行.
    """
    ui = utils.game_ui()

    if ui == 1:
        time.sleep(1)
        mouse.left_click(530, 380)  # Survival
        time.sleep(0.3)
        mouse.left_click(400, 475)  # Survival: Endless
        time.sleep(0.3)  # 等待进场后才能读下面这个数据呀
        if process.read_memory("int", 0x6A9EC0, 0x768, 0x160, 0x6C) != 0:
            # 非首次选卡
            mouse.left_click(290, 370)  # Continue
        time.sleep(5)  # 等待界面切换到选卡

    elif ui == 2:
        # time.sleep(1)  # TODO
        goto_main_ui()
        goto_survival_endless()

    elif ui == 3:
        goto_main_ui()
        goto_survival_endless()

    elif ui == 4:
        goto_main_ui()
        goto_survival_endless()

    elif ui == 7:
        goto_main_ui()
        goto_survival_endless()


def backup_user_data():
    """
    备份存档. 退回主界面再调用.
    """
    source_path = "C:\\ProgramData\\PopCap Games\\PlantsVsZombies\\userdata\\"
    backup_path = os.path.join(os.getcwd(), "userdata")  # 当前工作目录下

    # 创建备份目录 userdata
    if not os.path.exists(backup_path):
        os.mkdir(backup_path)

    # 获取存档文件名
    user = process.read_memory("int", 0x6A9EC0, 0x82C, 0x20)
    mode = process.read_memory("int", 0x6A9EC0, 0x7F8)  # 退出战斗界面后这个值依然不变
    data_file = "game" + str(user) + "_" + str(mode) + ".dat"  # "game1_13.dat"

    # 根据当前时间创建备份子目录
    now = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime(time.time()))
    os.mkdir(os.path.join(backup_path, now))

    # 复制文件
    src_file = os.path.join(source_path, data_file)
    dst_file = os.path.join(backup_path, now, data_file)
    if not os.path.isfile(src_file):
        logger.error(f"未找到原始存档文件, 备份失败.")
        return
    shutil.copyfile(src_file, dst_file)

    logger.info(f"备份存档文件至 {dst_file}.")


def restore_user_data():
    """
    还原存档. 退回主界面再调用.
    """
    source_path = "C:\\ProgramData\\PopCap Games\\PlantsVsZombies\\userdata\\"
    backup_path = os.path.join(os.getcwd(), "userdata")  # 当前工作目录下

    # 没有备份目录
    if not os.path.exists(backup_path):
        logger.error(f"未找到存档备份目录, 还原失败.")
        return

    # 获取存档文件名
    user = process.read_memory("int", 0x6A9EC0, 0x82C, 0x20)
    mode = process.read_memory("int", 0x6A9EC0, 0x7F8)  # 退出战斗界面后这个值依然不变
    data_file = "game" + str(user) + "_" + str(mode) + ".dat"  # "game1_13.dat"

    # 获取最近备份时间
    time_list = []
    files = glob.glob(backup_path + "\\*")
    for f in files:
        if os.path.isdir(f):
            _, t = os.path.split(f)
            time_list.append(time.mktime(time.strptime(t, "%Y-%m-%d_%H-%M-%S")))  # 转为时间戳
    if len(time_list) == 0:
        logger.error(f"存档备份目录为空, 备份失败.")
        return
    last_backup_time = max(time_list)  # 找出最大值, 即最近的一次备份
    last_backup_time = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime(last_backup_time))  # 再转回字符串 ==

    # 复制文件
    src_file = os.path.join(backup_path, last_backup_time, data_file)
    dst_file = os.path.join(source_path, data_file)
    if not os.path.isfile(src_file):
        logger.error(f"未找到备份存档文件, 备份失败.")
        return
    if os.path.exists(dst_file):
        os.remove(dst_file)
    shutil.copyfile(src_file, dst_file)

    logger.info(f"从 {src_file} 还原存档文件.")
