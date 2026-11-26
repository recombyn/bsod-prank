# -*- coding: utf-8 -*-
"""把单帧表情图做成左右摇摆跳舞的 GIF。"""
import math
import os

from PIL import Image, ImageFilter

BASE = os.path.dirname(__file__)
SRC = os.path.join(BASE, "nailong_src.jpg")
OUT = os.path.join(BASE, "nailong.gif")

SIZE = 400
FRAMES = 12


def main():
    img = Image.open(SRC).convert("RGBA")

    # 居中放到正方形画布上
    w, h = img.size
    scale = min(SIZE / w, SIZE / h)
    img = img.resize((int(w * scale), int(h * scale)), Image.LANCZOS)
    img = img.filter(ImageFilter.SMOOTH_MORE)
    base = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    base.paste(img, ((SIZE - img.width) // 2, (SIZE - img.height) // 2), img)

    frames = []
    for i in range(FRAMES):
        t = i / FRAMES
        # 左右摇摆 + 轻微上下弹跳
        ang = math.sin(t * math.tau) * 10
        dy = abs(math.sin(t * math.tau)) * 8
        f = base.rotate(ang, resample=Image.BICUBIC, center=(SIZE / 2, SIZE / 2))
        f = f.transform(
            (SIZE, SIZE), Image.AFFINE,
            (1, 0, 0, 0, 1, dy), resample=Image.BICUBIC,
        )
        frames.append(f)

    frames[0].save(
        OUT, save_all=True, append_images=frames[1:], loop=0,
        duration=90, disposal=2,
    )
    print("saved:", OUT, os.path.getsize(OUT), "bytes")


if __name__ == "__main__":
    main()
