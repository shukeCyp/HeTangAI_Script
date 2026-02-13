"""
HeTangAI 数据库模块
- 使用 peewee + SQLite
- Mac: ~/Library/Application Support/HeTangAIScript/hetangai.db
- Windows: %APPDATA%/HeTangAIScript/hetangai.db
- Setting 表: key-value 形式存储配置
"""

import os
import platform
from pathlib import Path

from peewee import SqliteDatabase, Model, CharField, TextField


APP_NAME = "HeTangAIScript"

db = SqliteDatabase(None)  # 延迟初始化

_db_path: Path | None = None


def get_data_dir() -> Path:
    """获取应用数据目录（跨平台）"""
    system = platform.system()
    if system == "Darwin":
        data_dir = Path.home() / "Library" / "Application Support" / APP_NAME
    elif system == "Windows":
        appdata = os.environ.get("APPDATA", Path.home() / "AppData" / "Roaming")
        data_dir = Path(appdata) / APP_NAME
    else:
        data_dir = Path.home() / ".local" / "share" / APP_NAME
    data_dir.mkdir(parents=True, exist_ok=True)
    return data_dir


def get_db_path() -> Path:
    """获取数据库文件路径"""
    global _db_path
    if _db_path is None:
        _db_path = get_data_dir() / "hetangai.db"
    return _db_path


class BaseModel(Model):
    class Meta:
        database = db


class Setting(BaseModel):
    key = CharField(unique=True, primary_key=True)
    value = TextField(default="")

    class Meta:
        table_name = "settings"


# ---------- 便捷操作函数 ----------

DEFAULT_SETTINGS = {
    "api_key": "",
    "image_model": "gemini-3.0-pro-image-landscape",
    "video_model": "",
    "thread_pool_size": "2",
    "auto_download": "false",
    "download_path": "",
}


def init_db():
    """初始化数据库连接并创建表"""
    global _db_path
    _db_path = get_db_path()
    db.init(str(_db_path))
    db.connect(reuse_if_open=True)
    db.create_tables([Setting])

    # 写入默认值（仅当 key 不存在时）
    for key, value in DEFAULT_SETTINGS.items():
        Setting.get_or_create(key=key, defaults={"value": value})


def get_setting(key: str) -> str:
    """获取配置值"""
    try:
        return Setting.get_by_id(key).value
    except Setting.DoesNotExist:
        return ""


def set_setting(key: str, value: str):
    """设置配置值"""
    Setting.replace(key=key, value=value).execute()


def get_all_settings() -> dict[str, str]:
    """获取所有配置"""
    return {s.key: s.value for s in Setting.select()}


def get_db_file_size() -> int:
    """获取数据库文件大小（字节）"""
    p = get_db_path()
    if p.exists():
        return p.stat().st_size
    return 0
