# coding=utf-8

"""
Logger
"""

import logging

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
    日志. 默认启用.

    @参数 on(bool): 是否启用.
    """

    if on:
        pvz_logger.disabled = False
    else:
        pvz_logger.disabled = True


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


def debug(txt):
    pvz_logger.debug(txt)


def info(txt):
    pvz_logger.info(txt)


def warning(txt):
    pvz_logger.warning(txt)


def error(txt):
    pvz_logger.error(txt)


def critical(txt):
    pvz_logger.critical(txt)

