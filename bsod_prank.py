# -*- coding: utf-8 -*-
"""仿 Windows 蓝屏恶搞程序：退出按钮会跑，继续按钮点两次才退出。"""

import ctypes
import random
import sys
import tkinter as tk

# 高 DPI 屏幕上保持字体清晰
try:
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
except Exception:
    try:
        ctypes.windll.user32.SetProcessDPIAware()
    except Exception:
        pass

BLUE = "#0078D4"

root = tk.Tk()
root.withdraw()
root.title("Windows")
root.configure(bg=BLUE)
root.resizable(False, False)
root.attributes("-topmost", True)
root.attributes("-fullscreen", True)

SW = root.winfo_screenwidth()
SH = root.winfo_screenheight()
root.geometry(f"{SW}x{SH}+0+0")
root.deiconify()

SCALE = max(0.7, min(SW / 1920, SH / 1080))


def px(value):
    return int(value * SCALE)


FONT = "Microsoft YaHei UI"

# ---------- 蓝屏内容 ----------
tk.Label(root, text=":(", fg="white", bg=BLUE,
         font=(FONT, px(100))).place(x=px(90), y=px(55))

tk.Label(root, text="你的电脑遇到问题，需要重新启动。",
         fg="white", bg=BLUE,
         font=(FONT, px(30))).place(x=px(90), y=px(220))

tk.Label(root, text="我们只收集某些错误信息，然后为你重新启动。",
         fg="white", bg=BLUE,
         font=(FONT, px(18))).place(x=px(90), y=px(280))

tk.Label(root, text="终止代码: SYSTEM_THREAD_EXCEPTION_NOT_HANDLED",
         fg="white", bg=BLUE,
         font=(FONT, px(17))).place(x=px(90), y=px(380))

tk.Label(root, text="出错的文件: ntoskrnl.exe",
         fg="white", bg=BLUE,
         font=(FONT, px(17))).place(x=px(90), y=px(415))

# ---------- 按钮 ----------
btn_y = SH - px(170)
cont_x = SW // 2 - px(260)
exit_x = SW // 2 + px(30)
btn_w, btn_h = px(120), px(44)

btn_style = dict(
    bg="#f2f2f2", fg="#111111", activebackground="#e4e4e4",
    activeforeground="#111111", font=(FONT, px(16)),
    relief="solid", bd=1, highlightthickness=0,
    width=11, height=2,
)

cont_btn = tk.Button(root, text="继续", **btn_style)
cont_btn.place(x=cont_x, y=btn_y)

exit_btn = tk.Button(root, text="退出", **btn_style)
exit_btn.place(x=exit_x, y=btn_y)


def dodge_exit(event=None):
    """退出按钮：鼠标靠近或点击时随机跑开。"""
    w = exit_btn.winfo_width() or btn_w
    h = exit_btn.winfo_height() or btn_h
    mx, my = root.winfo_pointerx(), root.winfo_pointery()
    for _ in range(30):
        nx = random.randint(10, max(11, SW - w - 10))
        ny = random.randint(10, max(11, SH - h - 10))
        # 不落在“继续”按钮上，也不落在当前鼠标位置（避免反复触发）
        if nx < cont_x + btn_w + px(20) and nx + w > cont_x - px(20) \
                and ny < btn_y + btn_h + px(20) and ny + h > btn_y - px(20):
            continue
        if nx - 5 <= mx <= nx + w + 5 and ny - 5 <= my <= ny + h + 5:
            continue
        exit_btn.place(x=nx, y=ny)
        return


exit_btn.bind("<Enter>", dodge_exit)
exit_btn.bind("<ButtonPress-1>", dodge_exit)
exit_btn.config(command=dodge_exit)

state = {"confirmed": False}


def on_continue():
    """继续按钮：第一次变成“确定继续吗？”，第二次退出。"""
    if not state["confirmed"]:
        state["confirmed"] = True
        cont_btn.config(text="确定继续吗？")
    else:
        root.destroy()


cont_btn.config(command=on_continue)

# 自测模式：短暂显示后自动关闭
if "--selftest" in sys.argv:
    root.after(500, root.destroy)

root.mainloop()
