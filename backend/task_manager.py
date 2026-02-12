"""
HeTangAI 任务管理器
- 使用 ThreadPoolExecutor 并发执行图片生成任务
- 支持流式 SSE 解析、进度推送、自动下载
"""

import json
import re
import time
import base64
import threading
from uuid import uuid4
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, Future

import requests
import webview

from backend.logger import get_logger
from backend.database import get_setting


class TaskManager:
    """管理图片生成任务队列"""

    def __init__(self):
        self._window: webview.Window | None = None
        self._tasks: dict[str, dict] = {}  # task_id -> task
        self._task_order: list[str] = []    # 保持插入顺序
        self._futures: dict[str, Future] = {}
        self._lock = threading.Lock()
        self._pool: ThreadPoolExecutor | None = None
        self._init_pool()

    def set_window(self, window: webview.Window):
        self._window = window

    def _init_pool(self):
        """初始化线程池"""
        size = self._get_pool_size()
        self._pool = ThreadPoolExecutor(max_workers=size)
        get_logger().info("线程池已初始化, 线程数: %d", size)

    def _get_pool_size(self) -> int:
        try:
            size = int(get_setting("thread_pool_size") or "2")
            return max(1, min(size, 10))
        except (ValueError, TypeError):
            return 2

    def resize_pool(self):
        """重新创建线程池（设置页修改线程数后调用）"""
        old_pool = self._pool
        self._pool = ThreadPoolExecutor(max_workers=self._get_pool_size())
        get_logger().info("线程池已调整, 新线程数: %d", self._get_pool_size())
        # 旧的池不 shutdown，让正在运行的任务自然完成
        if old_pool:
            old_pool.shutdown(wait=False)

    # ===================== 任务操作 =====================

    def add_task(self, prompt: str, model: str, mode: str, image_base64: str = "") -> dict:
        """添加一个图片生成任务，返回任务摘要"""
        task_id = str(uuid4())[:8]
        task = {
            "id": task_id,
            "prompt": prompt,
            "model": model,
            "mode": mode,
            "image_base64": image_base64,
            "status": "pending",
            "progress": [],
            "result_image": "",
            "result_image_type": "",
            "error": "",
            "created_at": time.time(),
            "file_path": "",
        }

        with self._lock:
            self._tasks[task_id] = task
            self._task_order.append(task_id)

        get_logger().info("任务已添加: %s - %s", task_id, prompt[:30])

        # 提交到线程池
        future = self._pool.submit(self._execute_task, task_id)
        self._futures[task_id] = future

        return self._task_summary(task)

    def get_all_tasks(self) -> list[dict]:
        """获取所有任务摘要列表（不含 image_base64 大字段）"""
        with self._lock:
            return [self._task_summary(self._tasks[tid]) for tid in self._task_order if tid in self._tasks]

    def get_task(self, task_id: str) -> dict:
        """获取单个任务详情"""
        with self._lock:
            task = self._tasks.get(task_id)
            if task:
                return self._task_summary(task)
            return {}

    def cancel_task(self, task_id: str) -> bool:
        """取消排队中的任务"""
        with self._lock:
            task = self._tasks.get(task_id)
            if task and task["status"] == "pending":
                task["status"] = "cancelled"
                future = self._futures.get(task_id)
                if future:
                    future.cancel()
                self._push_task_update(task_id, {"type": "cancelled"})
                get_logger().info("任务已取消: %s", task_id)
                return True
        return False

    def delete_task(self, task_id: str) -> bool:
        """删除任务记录"""
        with self._lock:
            if task_id in self._tasks:
                del self._tasks[task_id]
                if task_id in self._task_order:
                    self._task_order.remove(task_id)
                self._futures.pop(task_id, None)
                return True
        return False

    def clear_done_tasks(self) -> int:
        """清除所有已完成/失败/取消的任务，返回清除数量"""
        count = 0
        with self._lock:
            to_remove = [
                tid for tid, t in self._tasks.items()
                if t["status"] in ("done", "error", "cancelled")
            ]
            for tid in to_remove:
                del self._tasks[tid]
                self._task_order.remove(tid)
                self._futures.pop(tid, None)
                count += 1
        return count

    # ===================== 任务执行 =====================

    def _execute_task(self, task_id: str):
        """在线程池中执行单个任务"""
        logger = get_logger()

        with self._lock:
            task = self._tasks.get(task_id)
            if not task or task["status"] == "cancelled":
                return
            task["status"] = "running"

        self._push_task_update(task_id, {"type": "status", "status": "running"})

        api_base = get_setting("api_base_url") or "http://hetang.lyvideo.top"
        api_key = get_setting("api_key")

        if not api_key:
            self._fail_task(task_id, "请先在设置中配置 API Key")
            return

        url = f"{api_base.rstrip('/')}/v1/chat/completions"

        # 构建 messages
        if task["mode"] == "img2img" and task["image_base64"]:
            content = [
                {"type": "text", "text": task["prompt"]},
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:image/jpeg;base64,{task['image_base64']}"},
                },
            ]
        else:
            content = task["prompt"]

        payload = {
            "model": task["model"],
            "messages": [{"role": "user", "content": content}],
            "stream": True,
        }

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }

        logger.info("[%s] 开始生成 - 模型: %s, 提示词: %s", task_id, task["model"], task["prompt"][:30])

        try:
            response = requests.post(url, json=payload, headers=headers, stream=True, timeout=300)
            response.raise_for_status()

            full_content = ""
            buffer = ""

            for line in response.iter_lines(decode_unicode=True):
                # 检查任务是否被取消
                with self._lock:
                    t = self._tasks.get(task_id)
                    if not t or t["status"] == "cancelled":
                        logger.info("[%s] 任务已被取消，终止请求", task_id)
                        return

                if not line:
                    buffer = ""
                    continue

                if line.startswith("data: "):
                    data_str = line[6:]
                    if data_str.strip() == "[DONE]":
                        break
                    buffer = data_str
                else:
                    buffer += line

                try:
                    data = json.loads(buffer)
                except json.JSONDecodeError:
                    continue

                buffer = ""
                try:
                    delta = data["choices"][0]["delta"]

                    reasoning = delta.get("reasoning_content", "")
                    if reasoning:
                        text = reasoning.strip()
                        if text:
                            with self._lock:
                                task["progress"].append(text)
                            self._push_task_update(task_id, {
                                "type": "progress",
                                "progress_text": text,
                            })

                    content_piece = delta.get("content", "")
                    if content_piece:
                        full_content += content_piece

                except (KeyError, IndexError):
                    continue

            # 提取图片
            image_data, image_type = self._extract_image(full_content)
            if image_data:
                logger.info("[%s] 图片生成成功 (类型: %s)", task_id, image_type)
                with self._lock:
                    task["status"] = "done"
                    task["result_image"] = image_data
                    task["result_image_type"] = image_type
                    # 清除 image_base64 释放内存
                    task["image_base64"] = ""

                # 自动下载
                file_path = self._auto_download(task_id, image_data, image_type, task["prompt"])

                self._push_task_update(task_id, {
                    "type": "done",
                    "result_image": image_data,
                    "result_image_type": image_type,
                    "file_path": file_path,
                })
            else:
                logger.warning("[%s] 未能提取图片, content: %s", task_id, full_content[:200])
                self._fail_task(task_id, "未能从响应中提取图片")

        except requests.exceptions.Timeout:
            self._fail_task(task_id, "请求超时，请重试")
        except requests.exceptions.ConnectionError:
            self._fail_task(task_id, "无法连接到 API 服务器")
        except Exception as e:
            logger.error("[%s] 生成失败: %s", task_id, e)
            self._fail_task(task_id, str(e))

    def _fail_task(self, task_id: str, error: str):
        """标记任务失败"""
        with self._lock:
            task = self._tasks.get(task_id)
            if task:
                task["status"] = "error"
                task["error"] = error
                task["image_base64"] = ""
        self._push_task_update(task_id, {"type": "error", "error": error})
        get_logger().error("[%s] 任务失败: %s", task_id, error)

    # ===================== 自动下载 =====================

    def _auto_download(self, task_id: str, image_data: str, image_type: str, prompt: str) -> str:
        """如果启用自动下载，保存图片到本地，返回文件路径"""
        auto = get_setting("auto_download")
        if auto != "true":
            return ""

        download_path = get_setting("download_path")
        if not download_path:
            return ""

        dl_dir = Path(download_path)
        if not dl_dir.exists():
            try:
                dl_dir.mkdir(parents=True, exist_ok=True)
            except OSError as e:
                get_logger().error("[%s] 无法创建下载目录: %s", task_id, e)
                return ""

        # 文件名：hetangai_时间戳_提示词前几个字.jpg
        ts = time.strftime("%Y%m%d_%H%M%S")
        safe_prompt = re.sub(r'[^\w\u4e00-\u9fff]', '', prompt)[:10]
        filename = f"hetangai_{ts}_{safe_prompt}.jpg"
        file_path = dl_dir / filename

        try:
            if image_type == "url":
                resp = requests.get(image_data, timeout=60)
                resp.raise_for_status()
                image_bytes = resp.content
            else:
                image_bytes = base64.b64decode(image_data)

            with open(file_path, "wb") as f:
                f.write(image_bytes)

            with self._lock:
                task = self._tasks.get(task_id)
                if task:
                    task["file_path"] = str(file_path)

            get_logger().info("[%s] 图片已自动保存: %s", task_id, file_path)
            return str(file_path)

        except Exception as e:
            get_logger().error("[%s] 自动下载失败: %s", task_id, e)
            return ""

    # ===================== 推送与工具方法 =====================

    def _push_task_update(self, task_id: str, data: dict):
        """通过 evaluate_js 推送任务状态更新到前端"""
        if not self._window:
            return
        data["task_id"] = task_id
        try:
            json_str = json.dumps(data, ensure_ascii=True)
            self._window.evaluate_js(
                f"window.__onTaskUpdate && window.__onTaskUpdate({json_str})"
            )
        except Exception:
            pass

    def _task_summary(self, task: dict) -> dict:
        """生成任务摘要（不含 image_base64 大字段）"""
        return {
            "id": task["id"],
            "prompt": task["prompt"],
            "model": task["model"],
            "mode": task["mode"],
            "status": task["status"],
            "progress": task["progress"],
            "result_image": task["result_image"],
            "result_image_type": task["result_image_type"],
            "error": task["error"],
            "created_at": task["created_at"],
            "file_path": task["file_path"],
        }

    def get_task_image(self, task_id: str) -> tuple[str, str]:
        """获取任务的图片数据和类型"""
        with self._lock:
            task = self._tasks.get(task_id)
            if task and task["status"] == "done":
                return task["result_image"], task["result_image_type"]
        return "", ""

    @staticmethod
    def _extract_image(content: str) -> tuple[str, str]:
        """
        从 markdown 图片格式中提取图片数据
        返回: (image_data, image_type)
        """
        # 1. markdown 图片语法 ![...](...)
        md_match = re.search(r"!\[.*?\]\((.+?)\)", content)
        if md_match:
            src = md_match.group(1).strip()
            if src.startswith("data:image/"):
                b64_match = re.search(r"base64,([A-Za-z0-9+/=\s]+)", src)
                if b64_match:
                    return b64_match.group(1).replace("\n", "").replace(" ", ""), "base64"
            if src.startswith("http://") or src.startswith("https://"):
                return src, "url"

        # 2. 直接匹配 data:image base64
        b64_match = re.search(r"data:image/[^;]+;base64,([A-Za-z0-9+/=\s]+)", content)
        if b64_match:
            return b64_match.group(1).replace("\n", "").replace(" ", ""), "base64"

        # 3. 直接匹配 URL
        url_match = re.search(r"(https?://\S+\.(?:jpg|jpeg|png|webp|gif)\S*)", content, re.IGNORECASE)
        if url_match:
            return url_match.group(1), "url"

        return "", ""

    def shutdown(self):
        """关闭线程池"""
        if self._pool:
            self._pool.shutdown(wait=False)
