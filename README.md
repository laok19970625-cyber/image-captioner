# 图像描述 / 文字识别工具

读入图片，生成详细文字描述，或识别图片中的文字（OCR）。

## 特性
- `describe`：图片内容描述
- `extract`：图片文字识别
- 多模态模型（默认智谱 GLM-4V）

## 快速开始
```bash
export LLM_API_KEY="你的Key"
python main.py describe photo.png
python main.py extract screenshot.png
```

## 应用场景
- 图片内容理解
- 截图文字提取
- 无障碍辅助描述

## License
MIT
