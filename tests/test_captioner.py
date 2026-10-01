"""图像描述工具单元测试（验证 base64 编码逻辑，不依赖真实 API）。"""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from captioner import _image_to_base64_url  # noqa: E402


class TestImageEncoding(unittest.TestCase):
    def test_png_encoding(self):
        # 生成一个 1x1 PNG
        png_bytes = bytes.fromhex(
            "89504e470d0a1a0a0000000d494844520000000100000001080600000"
            "01f15c4890000000d49444154789c626001000000ffff030000060005"
            "57bfabd40000000049454e44ae426082"
        )
        tmp = Path(__file__).parent / "_test.png"
        tmp.write_bytes(png_bytes)
        try:
            url = _image_to_base64_url(str(tmp))
            self.assertTrue(url.startswith("data:image/png;base64,"))
        finally:
            tmp.unlink()


if __name__ == "__main__":
    unittest.main(verbosity=2)
