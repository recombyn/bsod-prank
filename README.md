# 仿蓝屏恶搞程序

一个纯娱乐的假蓝屏界面。**不会真的让电脑蓝屏、重启或删除任何东西。**

## 在线版

打开：<https://recombyn.github.io/bsod-prank/>

## Windows 桌面版

**推荐：直接下载 exe（无需安装 Python）**

- 下载：[bsod_prank.exe](https://github.com/recombyn/bsod-prank/releases/latest/download/bsod_prank.exe)，双击即可运行
- 单文件约 12 MB，首次启动会解压到临时目录，稍慢几秒
- 如被杀毒软件误报，选择允许即可（PyInstaller 打包的程序常见误报）

**源码运行**

1. 下载仓库文件，保持 `bsod_prank.py` 和 `run_bsod.bat` 在同一目录
2. 双击 `run_bsod.bat` 即可全屏运行
3. 也可以手动运行：`python bsod_prank.py`

> 启动器默认使用 `C:\Users\DELL\AppData\Local\Programs\Python\Python314\pythonw.exe`。
> 如果路径不同，用记事本打开 `run_bsod.bat` 改成你本机的 Python 路径，或确保 `pyw` 在 PATH 中。

## 玩法

- **退出**：全程只有一个退出按钮，鼠标一靠近或点击就随机跑开，永远点不到，并弹出嘲讽文案
- **倒计时**：屏幕上的“xx 秒后重新启动”每躲一次按钮就增加 5~15 秒，归零后假装重启失败并重新开始
- **继续**：第一次点击变成「确定继续吗？」，第二次进入假关机；随后蓝屏“恢复”，按钮复位，重复 4 轮才真正退出
- **网页版**：还会在鼠标旁飘出嘲讽文字；浏览器不允许脚本主动关闭普通标签页，最后需手动关闭
- 桌面版随时可按 **Alt+F4** 或 **Alt+Tab** 脱身

## 文件

- `bsod_prank.py` — Python/tkinter 桌面版源码
- `run_bsod.bat` — Windows 源码双击启动器
- `index.html` — 浏览器版（GitHub Pages）
- Releases 中的 `bsod_prank.exe` — 免安装单文件版
