"""
HeTangAI JS API 桥接
- 暴露给前端 (window.pywebview.api) 的所有方法
- 任务制图片生成，通过 TaskManager 管理
"""

import json
import base64

import requests
import webview

from backend.logger import (
    get_logger,
    get_current_log_file,
    get_log_dir,
    get_log_dir_size,
    get_log_files,
    clear_old_logs,
)
from backend.database import (
    get_setting,
    set_setting,
    get_all_settings,
    get_db_path,
    get_db_file_size,
)
from backend.task_manager import TaskManager


class Api:
    """pywebview JS API 类，所有 public 方法都会暴露给前端"""

    def __init__(self, task_manager: TaskManager):
        self._window: webview.Window | None = None
        self._task_manager = task_manager

    def set_window(self, window: webview.Window):
        """由 main.py 在窗口创建后调用"""
        self._window = window
        self._task_manager.set_window(window)

    # ===================== 版本号 =====================

    def get_version(self) -> str:
        """获取应用版本号"""
        from backend.main import get_version
        return get_version()

    # ===================== 设置相关 =====================

    def get_setting(self, key: str) -> str:
        return get_setting(key)

    def set_setting(self, key: str, value: str):
        set_setting(key, value)
        get_logger().info("配置已更新: %s", key)
        # 线程池大小变更时动态调整
        if key == "thread_pool_size":
            self._task_manager.resize_pool()

    def get_all_settings(self) -> dict:
        return get_all_settings()

    # ===================== 文件状态 =====================

    def get_file_status(self) -> dict:
        """获取日志和数据库文件状态"""
        log_file = get_current_log_file()
        log_files = get_log_files()
        return {
            "log_dir": str(get_log_dir()),
            "log_current_file": str(log_file) if log_file else "",
            "log_file_count": len(log_files),
            "log_total_size": get_log_dir_size(),
            "db_path": str(get_db_path()),
            "db_size": get_db_file_size(),
        }

    def clear_logs(self) -> dict:
        """清理旧日志文件"""
        count = clear_old_logs()
        get_logger().info("已清理 %d 个旧日志文件", count)
        return {"cleared": count, "log_total_size": get_log_dir_size()}

    # ===================== 任务制图片生成 =====================

    def add_image_task(self, prompt: str, model: str, mode: str, image_base64: str = "") -> dict:
        """
        添加图片生成任务到队列
        - prompt: 提示词
        - model: 模型名
        - mode: "text2img" 或 "img2img"
        - image_base64: 图生图时的参考图 base64
        返回: 任务摘要 dict
        """
        return self._task_manager.add_task(prompt, model, mode, image_base64)

    def get_all_tasks(self) -> list:
        """获取所有任务列表"""
        return self._task_manager.get_all_tasks()

    def get_task(self, task_id: str) -> dict:
        """获取单个任务详情"""
        return self._task_manager.get_task(task_id)

    def cancel_task(self, task_id: str) -> bool:
        """取消排队中的任务"""
        return self._task_manager.cancel_task(task_id)

    def delete_task(self, task_id: str) -> bool:
        """删除任务记录"""
        return self._task_manager.delete_task(task_id)

    def clear_done_tasks(self) -> int:
        """清除所有已完成/失败的任务"""
        return self._task_manager.clear_done_tasks()

    # ===================== 图片保存 =====================

    def save_task_image(self, task_id: str) -> str:
        """弹出保存对话框，保存指定任务的图片"""
        if not self._window:
            return ""

        image_data, image_type = self._task_manager.get_task_image(task_id)
        if not image_data:
            return ""

        result = self._window.create_file_dialog(
            webview.SAVE_DIALOG,
            save_filename="hetangai_image.jpg",
            file_types=("JPEG 图片 (*.jpg)",),
        )

        if result:
            file_path = result if isinstance(result, str) else result[0]
            try:
                if image_type == "url":
                    resp = requests.get(image_data, timeout=60)
                    resp.raise_for_status()
                    image_bytes = resp.content
                else:
                    image_bytes = base64.b64decode(image_data)

                with open(file_path, "wb") as f:
                    f.write(image_bytes)
                get_logger().info("图片已保存: %s", file_path)
                return file_path
            except Exception as e:
                get_logger().error("保存图片失败: %s", e)
                return ""
        return ""

    def select_download_path(self) -> str:
        """弹出目录选择对话框，返回选中的路径"""
        if not self._window:
            return ""

        result = self._window.create_file_dialog(webview.FOLDER_DIALOG)
        if result:
            path = result if isinstance(result, str) else result[0]
            get_logger().info("已选择下载路径: %s", path)
            return path
        return ""
