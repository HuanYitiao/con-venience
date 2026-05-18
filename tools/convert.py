#!/usr/bin/env python3
"""
con-venience image converter
将图片转换为128x128黑白位图，支持Floyd-Steinberg抖动算法
用法: python3 convert.py <input_image> [output.png]
"""

import sys
from PIL import Image
import numpy as np

def floyd_steinberg_dither(img_gray: np.ndarray) -> np.ndarray:
    """Floyd-Steinberg抖动算法，输入0-255灰度数组，输出0或255的数组"""
    img = img_gray.astype(np.float32).copy()
    h, w = img.shape

    for y in range(h):
        for x in range(w):
            old = img[y, x]
            new = 255.0 if old >= 128 else 0.0
            img[y, x] = new
            err = old - new

            if x + 1 < w:
                img[y, x + 1] += err * 7 / 16
            if y + 1 < h:
                if x - 1 >= 0:
                    img[y + 1, x - 1] += err * 3 / 16
                img[y + 1, x] += err * 5 / 16
                if x + 1 < w:
                    img[y + 1, x + 1] += err * 1 / 16

    return np.clip(img, 0, 255).astype(np.uint8)

def convert(input_path: str, output_path: str, size: tuple = (128, 128)):
    # 读取图片
    img = Image.open(input_path).convert("RGB")
    print(f"原图尺寸: {img.size}")

    # 裁剪成正方形（取中心）
    w, h = img.size
    min_side = min(w, h)
    left = (w - min_side) // 2
    top = (h - min_side) // 2
    img = img.crop((left, top, left + min_side, top + min_side))

    # 缩放到目标尺寸
    img = img.resize(size, Image.LANCZOS)
    print(f"缩放后: {img.size}")

    # 转灰度
    img_gray = np.array(img.convert("L"))

    # Floyd-Steinberg抖动
    img_dithered = floyd_steinberg_dither(img_gray)

    # 保存结果
    result = Image.fromarray(img_dithered, mode="L")
    result.save(output_path)
    print(f"已保存: {output_path}")

    return result

def convert_qr(input_path: str, output_path: str, size: tuple = (128, 128)):
    """QR码转换：直接阈值二值化，不使用抖动"""
    img = Image.open(input_path).convert("L")
    print(f"原图尺寸: {img.size}")

    # 缩放
    img = img.resize(size, Image.LANCZOS)

    # 简单阈值二值化
    img_arr = np.array(img)
    img_arr = np.where(img_arr >= 128, 255, 0).astype(np.uint8)

    result = Image.fromarray(img_arr, mode="L")
    result.save(output_path)
    print(f"已保存: {output_path}")
    return result

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法:")
        print("  头像: python3 convert.py --dither <input> [output.png]")
        print("  QR码: python3 convert.py --qr <input> [output.png]")
        sys.exit(1)

    mode = sys.argv[1]
    if mode not in ("--dither", "--qr") or len(sys.argv) < 3:
        print("用法:")
        print("  头像: python3 convert.py --dither <input> [output.png]")
        print("  QR码: python3 convert.py --qr <input> [output.png]")
        sys.exit(1)

    input_path = sys.argv[2]
    output_path = sys.argv[3] if len(sys.argv) > 3 else "output.png"

    if mode == "--dither":
        convert(input_path, output_path)
    elif mode == "--qr":
        convert_qr(input_path, output_path)