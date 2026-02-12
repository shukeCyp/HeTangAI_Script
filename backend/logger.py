"""
HeTangAI 日志系统
- Mac: ~/Library/Logs/HeTangAI/
- Windows: %APPDATA%/HeTangAI/logs/
- 每次启动创建新的日志文件
"""

import logging
import os
import platform
import glob
from datetime import datetime
from pathlib import Path


APP_NAME = "HeTangAIScript"

_log_dir: Path | None = None
_current_log_file: Path | None = None


def get_log_dir() -> Path:
    """获取日志目录路径（跨平台）"""
    system = platform.system()
    if system == "Darwin":
        log_dir = Path.home() / "Library" / "Logs" / APP_NAME
    elif system == "Windows":
        appdata = os.environ.get("APPDATA", Path.home() / "AppData" / "Roaming")
        log_dir = Path(appdata) / APP_NAME / "logs"
    else:
        # Linux fallback
        log_dir = Path.home() / ".local" / "share" / APP_NAME / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    return log_dir


def setup_logger() -> logging.Logger:
    """初始化日志系统，每次调用创建新的日志文件"""
    global _log_dir, _current_log_file

    _log_dir = get_log_dir()

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    _current_log_file = _log_dir / f"hetangai_{timestamp}.log"

    logger = logging.getLogger(APP_NAME)
    logger.setLevel(logging.DEBUG)

    # 清除已有 handler（避免重复）
    logger.handlers.clear()

    # 文件 handler
    file_handler = logging.FileHandler(str(_current_log_file), encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)

    # 控制台 handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    # 日志格式
    formatter = logging.Formatter(
        "[%(asctime)s] [%(levelname)s] [%(module)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    logger.info("日志系统已初始化: %s", _current_log_file)
    return logger


def get_logger() -> logging.Logger:
    """获取已初始化的 logger"""
    return logging.getLogger(APP_NAME)


def get_current_log_file() -> Path | None:
    """获取当前日志文件路径"""
    return _current_log_file


def get_log_files() -> list[Path]:
    """获取所有日志文件"""
    if _log_dir is None:
        return []
    return sorted(_log_dir.glob("hetangai_*.log"), reverse=True)


def get_log_dir_size() -> int:
    """获取日志目录总大小（字节）"""
    if _log_dir is None:
        return 0
    total = 0
    for f in _log_dir.glob("hetangai_*.log"):
        total += f.stat().st_size
    return total


def clear_old_logs() -> int:
    """清理所有旧日志文件（保留当前日志），返回清理的文件数"""
    if _log_dir is None:
        return 0
    count = 0
    for f in _log_dir.glob("hetangai_*.log"):
        if f != _current_log_file:
            try:
                f.unlink()
                count += 1
            except OSError:
                pass
    return count
