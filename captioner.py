"""图像描述 / 识别工具：读入图片 -> 多模态模型生成文字描述。

支持两种模式：
- describe：生成图片的详细文字描述
- extract_text：识别图片中的文字（OCR）

默认使用智谱 GLM-4V（多模态），也可切换到其他 OpenAI 兼容的视觉模型。
"""

from __future__ import annotations

import base64
import json
import os
import urllib.request
from pathlib import Path


class LLMClient:
    def __init__(self, api_key=None, api_base=None, model=None):
        self.api_key = api_key or os.environ.get("LLM_API_KEY", "")
        self.api_base = (api_base or os.environ.get("LLM_API_BASE", "https://open.bigmodel.cn/api/paas/v4")).rstrip("/")
        self.model = model or os.environ.get("LLM_MODEL", "glm-4v-flash")

    def chat(self, messages, temperature=0.3):
        if not self.api_key:
            raise RuntimeError("未配置 LLM_API_KEY，请设置环境变量后重试。")
        url = f"{self.api_base}/chat/completions"
        payload = {"model": self.model, "messages": messages, "temperature": temperature}
        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json", "Authorization": f"Bearer {self.api_key}"},
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=120) as resp:
            body = json.loads(resp.read().decode("utf-8"))
        return body["choices"][0]["message"]["content"]


def _image_to_base64_url(path: str) -> str:
    data = Path(path).read_bytes()
    ext = Path(path).suffix.lower().lstrip(".")
    mime = {"jpg": "jpeg", "jpeg": "jpeg", "png": "png", "webp": "webp", "gif": "gif"}.get(ext, "jpeg")
    b64 = base64.b64encode(data).decode("utf-8")
    return f"data:image/{mime};base64,{b64}"


def describe_image(path: str, llm: LLMClient | None = None) -> str:
    """生成图片的详细文字描述。"""
    llm = llm or LLMClient()
    img_url = _image_to_base64_url(path)
    messages = [
        {"role": "user", "content": [
            {"type": "text", "text": "请详细描述这张图片的内容，包括主体、场景、细节和氛围。用中文。"},
            {"type": "image_url", "image_url": {"url": img_url}},
        ]},
    ]
    return llm.chat(messages)


def extract_text(path: str, llm: LLMClient | None = None) -> str:
    """识别图片中的文字。"""
    llm = llm or LLMClient()
    img_url = _image_to_base64_url(path)
    messages = [
        {"role": "user", "content": [
            {"type": "text", "text": "请识别并输出图片中的所有文字，保持原有格式。如果没有文字请说明。"},
            {"type": "image_url", "image_url": {"url": img_url}},
        ]},
    ]
    return llm.chat(messages)
