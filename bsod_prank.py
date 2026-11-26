# -*- coding: utf-8 -*-
"""仿 Windows 蓝屏恶搞程序：会躲的退出按钮、倒计时嘲讽和循环假关机。"""

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
         font=(FONT, px(100))).place(x=px(90), y=px(45))

tk.Label(root, text="你的电脑遇到问题，需要重新启动。",
         fg="white", bg=BLUE,
         font=(FONT, px(30))).place(x=px(90), y=px(195))

tk.Label(root, text="我们只收集某些错误信息，然后为你重新启动。",
         fg="white", bg=BLUE,
         font=(FONT, px(18))).place(x=px(90), y=px(255))

tk.Label(root, text="终止代码: SYSTEM_THREAD_EXCEPTION_NOT_HANDLED",
         fg="white", bg=BLUE,
         font=(FONT, px(17))).place(x=px(90), y=px(340))

tk.Label(root, text="出错的文件: ntoskrnl.exe",
         fg="white", bg=BLUE,
         font=(FONT, px(17))).place(x=px(90), y=px(375))

status_var = tk.StringVar(value="正在收集错误信息... 0%")
taunt_var = tk.StringVar(value="")

tk.Label(root, textvariable=status_var, fg="white", bg=BLUE,
         font=(FONT, px(17))).place(x=px(90), y=px(430))

tk.Label(root, textvariable=taunt_var, fg="#ffe082", bg=BLUE,
         font=(FONT, px(18), "bold")).place(x=px(90), y=px(485))

# ---------- 按钮 ----------
btn_y = SH - px(180)
cont_x = SW // 2 - px(280)
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

TAUNTS = [
    "抓不到我~",
    "手速不行啊",
    "别追了，抓不到的",
    "退出按钮已隐藏",
    "再点也没用",
    "试试点“继续”？",
    "你还在点？",
    "放弃吧，人类",
]
dodge_count = 0
countdown = {"value": 30}


def overlaps(l, t, w, h, l2, t2, w2, h2, pad=0):
    return l < l2 + w2 + pad and l + w > l2 - pad and \
           t < t2 + h2 + pad and t + h > t2 - pad


def dodge(btn=None):
    """退出按钮：鼠标靠近或点击时随机跑开，还会分裂和嘲讽。"""
    global dodge_count
    btn = btn if btn is not None else exit_btn
    w = btn.winfo_width() or btn_w
    h = btn.winfo_height() or btn_h
    mx, my = root.winfo_pointerx(), root.winfo_pointery()
    for _ in range(40):
        nx = random.randint(10, max(11, SW - w - 10))
        ny = random.randint(10, max(11, SH - h - 10))
        if overlaps(nx, ny, w, h, cont_x, btn_y, btn_w, btn_h, px(20)):
            continue
        if overlaps(nx, ny, w, h, mx, my, 1, 1, px(8)):
            continue
        btn.place(x=nx, y=ny)
        btn.lift()
        break

    dodge_count += 1
    taunt_var.set(TAUNTS[min(dodge_count - 1, len(TAUNTS) - 1)])
    countdown["value"] += random.randint(5, 15)
    if dodge_count % 5 == 0:
        root.bell()


exit_btn.bind("<Enter>", lambda e: dodge(exit_btn))
exit_btn.bind("<ButtonPress-1>", lambda e: dodge(exit_btn))
exit_btn.config(command=lambda: dodge(exit_btn))

# ---------- 进度条 + 假倒计时 ----------
def collect(step=0):
    if step <= 100:
        status_var.set(f"正在收集错误信息... {step}%")
        root.after(30, lambda: collect(step + random.randint(2, 7)))
    else:
        countdown["value"] = 30
        tick_countdown()


def tick_countdown():
    value = countdown["value"] - 1
    if value <= 0:
        status_var.set("正在重新启动... (假的)")
        taunt_var.set("重启失败，倒计时重新开始")
        root.after(1000, restart_countdown)
        return
    countdown["value"] = value
    status_var.set(f"你的电脑将在 {value} 秒后重新启动。")
    root.after(1000, tick_countdown)


def restart_countdown():
    countdown["value"] = 30
    tick_countdown()


# ---------- 继续按钮：假关机循环，失败几次才真退 ----------
state = {"confirmed": False, "failures": 0}
MAX_FAILURES = 3


def finish_shutdown(overlay):
    overlay.destroy()
    state["failures"] += 1
    if state["failures"] > MAX_FAILURES:
        root.destroy()
        return
    # 假关机失败，蓝屏“恢复”，继续按钮重置，再来一轮
    state["confirmed"] = False
    cont_btn.config(text="继续", bg="#f2f2f2")
    taunt_var.set(f"第 {state['failures']} 次退出失败，蓝屏已恢复")
    status_var.set("正在重新启动... (假的)")
    countdown["value"] = 30


def fake_shutdown():
    overlay = tk.Frame(root, bg="#000000")
    overlay.place(x=0, y=0, width=SW, height=SH)
    tk.Label(overlay, text="正在退出...", fg="white", bg="#000000",
             font=(FONT, px(30))).place(relx=0.5, rely=0.5, anchor="center")
    overlay.lift()
    root.after(1300, lambda: finish_shutdown(overlay))


def on_continue():
    if not state["confirmed"]:
        state["confirmed"] = True
        cont_btn.config(text="确定继续吗？", bg="#ffe0b2")
        if state["failures"] >= MAX_FAILURES:
            taunt_var.set("这次应该是真的了...吧？")
        else:
            taunt_var.set("再点一次试试？")
        return
    fake_shutdown()


cont_btn.config(command=on_continue)

# 自测模式：短暂显示后自动关闭
if "--selftest" in sys.argv:
    root.after(500, root.destroy)

root.after(200, collect)
root.mainloop()
