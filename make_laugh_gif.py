# -*- coding: utf-8 -*-
"""生成一个笑哭表情动画 GIF（微信表情包风格）。"""
import math
import os

from PIL import Image, ImageDraw, ImageFilter

SIZE = 400          # 画布尺寸
FRAMES = 14         # 帧数
OUT = os.path.join(os.path.dirname(__file__), "laugh.gif")


def draw_face(t: float) -> Image.Image:
    """t: 0~1 的动画相位。"""
    img = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)

    bob = math.sin(t * math.tau) * 6          # 上下浮动
    cx, cy = SIZE / 2, SIZE / 2 + bob
    R = 150

    # ---- 脸（黄色，带简单立体感：多层圆叠加）----
    d.ellipse([cx - R, cy - R, cx + R, cy + R], fill=(250, 173, 20, 255))
    d.ellipse([cx - R + 18, cy - R + 10, cx + R - 10, cy + R - 18],
              fill=(255, 199, 62, 255))

    # ---- 眯起的笑眼（^ ^ 弧线）----
    eye_y = cy - 40
    for ex in (-60, 60):
        x0, x1 = cx + ex - 45, cx + ex + 45
        d.arc([x0, eye_y - 35, x1, eye_y + 25],
              start=200, end=340, fill=(90, 55, 10, 255), width=14)

    # ---- 张开大笑的嘴（随动画张合）----
    mouth_w = 110 + math.sin(t * math.tau) * 8
    mouth_h = 70 + math.sin(t * math.tau * 2) * 10
    my = cy + 45
    d.ellipse([cx - mouth_w, my - mouth_h / 2, cx + mouth_w, my + mouth_h],
              fill=(122, 46, 20, 255))
    # 舌头
    d.ellipse([cx - mouth_w * 0.55, my + mouth_h * 0.12,
               cx + mouth_w * 0.55, my + mouth_h],
              fill=(233, 90, 90, 255))

    # ---- 眼泪（两滴，从眼下往下滑，循环）----
    for side in (-1, 1):
        tx = cx + side * 78
        fall = (t + (0.0 if side < 0 else 0.5)) % 1.0
        ty = eye_y + 10 + fall * 55
        tr = 16 + 6 * fall          # 越落越大
        d.ellipse([tx - tr, ty - tr * 1.3, tx + tr, ty + tr * 1.3],
                  fill=(90, 170, 255, 230))
    return img


def main():
    frames = []
    for i in range(FRAMES):
        t = i / FRAMES
        f = draw_face(t)
        # 轻微旋转晃动，更像表情包
        ang = math.sin(t * math.tau) * 6
        f = f.rotate(ang, resample=Image.BICUBIC, center=(SIZE / 2, SIZE / 2))
        f = f.filter(ImageFilter.SMOOTH)
        frames.append(f)

    frames[0].save(
        OUT, save_all=True, append_images=frames[1:], loop=0,
        duration=80, disposal=2, transparency=0,
    )
    print("saved:", OUT, os.path.getsize(OUT), "bytes")


if __name__ == "__main__":
    main()
