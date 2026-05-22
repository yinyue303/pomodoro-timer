# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 运行

```bash
py pomodoro.py
```

## 架构

单文件 tkinter 桌面应用，`PomodoroTimer` 类封装全部逻辑：

- **计时核心**: `root.after(1000, self.countdown)` 实现每秒倒计时，按 `work_seconds`(25min) / `break_seconds`(5min) 自动切换工作/休息模式
- **通知**: `winsound.MessageBeep` (Windows only) 播放系统提示音，结束后弹 `messagebox`
- **UI**: tkinter `pack` 布局，Canvas 进度条 + Label 时间显示 + 三个按钮(开始/暂停/重置)

状态变量: `is_running` 控制计时启停，`is_working` 区分工作/休息模式，`timer_id` 保存 after() 返回的定时器 ID 以便取消。
