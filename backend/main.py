"""
荷塘AI生成器 主入口
- 初始化日志、数据库、任务管理器
- 创建 pywebview 窗口加载编译后的 Vue 前端
"""

import os
import sys
from pathlib import Path

import webview

from backend.logger import setup_logger, get_logger
from backend.database import init_db
from backend.task_manager import TaskManager
from backend.video_task_manager import VideoTaskManager
from backend.api import Api


def get_base_dir() -> Path:
    """获取项目根目录，兼容 PyInstaller 打包"""
    if getattr(sys, "frozen", False):
        return Path(sys._MEIPASS)
    return Path(__file__).resolve().parent.parent


def get_web_dir() -> str:
    """获取前端编译输出目录"""
    web_dir = get_base_dir() / "web"
    if not web_dir.exists():
        raise FileNotFoundError(f"前端编译目录不存在: {web_dir}\n请先运行 run.sh 构建前端")
    return str(web_dir)


def get_version() -> str:
    """从 version.txt 读取版本号"""
    version_file = get_base_dir() / "version.txt"
    try:
        return version_file.read_text(encoding="utf-8").strip()
    except FileNotFoundError:
        return "V0.0.0"


def main():
    # 1. 初始化日志
    setup_logger()
    logger = get_logger()

    version = get_version()
    logger.info("荷塘AI生成器 %s 启动中...", version)

    # 2. 初始化数据库
    init_db()
    logger.info("数据库已初始化")

    # 3. 创建任务管理器
    task_manager = TaskManager()
    video_task_manager = VideoTaskManager()
    logger.info("任务管理器已初始化")

    # 4. 创建 API 实例
    api = Api(task_manager, video_task_manager)

    # 5. 获取前端目录
    try:
        web_dir = get_web_dir()
    except FileNotFoundError as e:
        logger.error(str(e))
        print(str(e))
        sys.exit(1)

    index_path = os.path.join(web_dir, "index.html")
    logger.info("加载前端: %s", index_path)

    # 6. 创建窗口
    window = webview.create_window(
        title=f"荷塘AI生成器 {version}",
        url=index_path,
        width=1200,
        height=800,
        min_size=(900, 600),
        js_api=api,
        text_select=True,
    )

    # 将 window 传入 api 和 task_manager
    api.set_window(window)

    logger.info("窗口已创建，启动 GUI")

    # 7. 启动 webview
    webview.start(debug=False)

    # 8. 清理
    task_manager.shutdown()
    video_task_manager.shutdown()
    logger.info("荷塘AI生成器已退出")


if __name__ == "__main__":
    main()
