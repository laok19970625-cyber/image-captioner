"""命令行入口：图像描述 / 文字识别。用法: python main.py describe <图片> | extract <图片>"""

import sys

sys.path.insert(0, __import__("os").path.dirname(__file__))

from captioner import LLMClient, describe_image, extract_text  # noqa: E402


def main():
    if len(sys.argv) < 3:
        print("用法：")
        print("  python main.py describe <图片路径>")
        print("  python main.py extract <图片路径>")
        return
    cmd, path = sys.argv[1], sys.argv[2]
    try:
        if cmd == "describe":
            print("=== 图片描述 ===")
            print(describe_image(path, LLMClient()))
        elif cmd == "extract":
            print("=== 文字识别 ===")
            print(extract_text(path, LLMClient()))
        else:
            print(f"未知命令：{cmd}")
    except RuntimeError as e:
        print(f"[错误] {e}")


if __name__ == "__main__":
    main()
