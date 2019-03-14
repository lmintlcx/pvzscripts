# coding=utf-8

"""
Logger
"""

import logging

from . import win32
from . import utils
from . import keyboard


fmt_str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
log_formatter = logging.Formatter(fmt_str)

console_handler = logging.StreamHandler()
console_handler.setFormatter(log_formatter)
console_handler.setLevel(logging.DEBUG)

pvz_logger = logging.getLogger("pvz")
pvz_logger.addHandler(console_handler)
pvz_logger.setLevel(logging.DEBUG)


def enable_logger(on=True):
    """
    启用日志.

    输出调试信息开销较大, 会影响操作精度, 建议调试完成后关闭.

    @参数 on(bool): 是否启用, 默认启用.
    """
    pvz_logger.disabled = not on


def set_logger_level(level="INFO"):
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
    pvz_logger.setLevel(logging_level[level])


# 频繁出现的调试信息
def debug(txt):
    pvz_logger.debug(txt)


# 输出调试信息
def info(txt):
    pvz_logger.info(txt)


# 不影响运行的警告
def warning(txt):
    pvz_logger.warning(txt)


# 用户操作出错
def error(txt):
    pvz_logger.error(txt)
    if utils.game_ui() in (3,):
        keyboard.pause_game()
    raise Exception(txt)
    # win32.MessageBoxW(None, win32.LPCWSTR(txt), win32.LPCWSTR("错误"), win32.UINT(0x00000000))
    # exit(0)


# 内部严重错误
def critical(txt):
    pvz_logger.critical(txt)
    if utils.game_ui() in (3,):
        keyboard.pause_game()
    raise Exception(txt)
    # win32.MessageBoxW(None, win32.LPCWSTR(txt), win32.LPCWSTR("错误"), win32.UINT(0x00000000))
    # exit(0)
