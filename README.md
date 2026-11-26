# 仿蓝屏恶搞程序

一个纯娱乐的假蓝屏界面。**不会真的让电脑蓝屏、重启或删除任何东西。**

## 在线版

打开：<https://recombyn.github.io/bsod-prank/>

## Windows 桌面版

1. 下载仓库文件，保持 `bsod_prank.py` 和 `run_bsod.bat` 在同一目录
2. 双击 `run_bsod.bat` 即可全屏运行
3. 也可以手动运行：`python bsod_prank.py`

> 启动器默认使用 `C:\Users\DELL\AppData\Local\Programs\Python\Python314\pythonw.exe`。
> 如果路径不同，用记事本打开 `run_bsod.bat` 改成你本机的 Python 路径，或确保 `pyw` 在 PATH 中。

## 玩法

- **退出**：鼠标一靠近或点击就随机跑开；每点 3 次还会**分裂出一个新的退出按钮**（最多 5 个），并弹出嘲讽文案
- **倒计时**：屏幕上的“xx 秒后重新启动”每躲一次按钮就增加 5~15 秒，归零后假装重启失败并重新开始
- **继续**：第一次点击变成「确定继续吗？」，再点一次才会进入假关机画面
- **网页版**：还会在鼠标旁飘出嘲讽文字；浏览器不允许脚本主动关闭普通标签页，最后需手动关闭
- 桌面版随时可按 **Alt+F4** 或 **Alt+Tab** 脱身

## 文件

- `bsod_prank.py` — Python/tkinter 桌面版
- `run_bsod.bat` — Windows 双击启动器
- `index.html` — 浏览器版（GitHub Pages）
