import tkinter as tk
from tkinter import messagebox
import winsound

class PomodoroTimer:
    def __init__(self, root):
        self.root = root
        self.root.title("番茄钟")
        self.root.geometry("340x380")
        self.root.resizable(False, False)
        self.root.configure(bg="#fafafa")

        # colors
        self.c_work = "#e74c3c"    # tomato red - work
        self.c_break = "#2ecc71"   # green - break
        self.c_bg = "#fafafa"
        self.c_text = "#2c3e50"
        self.c_progress_bg = "#ecf0f1"

        # timer state
        self.work_seconds = 25 * 60
        self.break_seconds = 5 * 60
        self.current_seconds = self.work_seconds
        self.is_working = True
        self.is_running = False
        self.timer_id = None

        self.create_widgets()
        self.update_display()

    def create_widgets(self):
        # title
        self.title_label = tk.Label(
            self.root, text="番茄钟",
            font=("Microsoft YaHei", 20, "bold"),
            fg=self.c_work, bg=self.c_bg
        )
        self.title_label.pack(pady=(30, 10))

        # mode label
        self.mode_label = tk.Label(
            self.root, text="工作模式",
            font=("Microsoft YaHei", 13),
            fg=self.c_work, bg=self.c_bg
        )
        self.mode_label.pack(pady=(0, 15))

        # progress bar (canvas)
        self.canvas = tk.Canvas(
            self.root, width=260, height=16,
            bg=self.c_progress_bg, bd=0, highlightthickness=0
        )
        self.canvas.pack(pady=(0, 20))
        self.progress_bar = self.canvas.create_rectangle(
            0, 0, 260, 16, fill=self.c_work, width=0
        )

        # time display
        self.time_label = tk.Label(
            self.root, text="25:00",
            font=("Consolas", 48, "bold"),
            fg=self.c_text, bg=self.c_bg
        )
        self.time_label.pack(pady=(0, 25))

        # button frame
        btn_frame = tk.Frame(self.root, bg=self.c_bg)
        btn_frame.pack()

        self.start_btn = tk.Button(
            btn_frame, text="开始", command=self.start_timer,
            font=("Microsoft YaHei", 11), width=8,
            bg=self.c_work, fg="white", activebackground="#c0392b",
            activeforeground="white", relief="flat", cursor="hand2"
        )
        self.start_btn.pack(side="left", padx=5)

        self.pause_btn = tk.Button(
            btn_frame, text="暂停", command=self.pause_timer,
            font=("Microsoft YaHei", 11), width=8,
            bg="#95a5a6", fg="white", activebackground="#7f8c8d",
            activeforeground="white", relief="flat", cursor="hand2",
            state="disabled"
        )
        self.pause_btn.pack(side="left", padx=5)

        self.reset_btn = tk.Button(
            btn_frame, text="重置", command=self.reset_timer,
            font=("Microsoft YaHei", 11), width=8,
            bg="#bdc3c7", fg="white", activebackground="#95a5a6",
            activeforeground="white", relief="flat", cursor="hand2"
        )
        self.reset_btn.pack(side="left", padx=5)

    def start_timer(self):
        if not self.is_running:
            self.is_running = True
            self.start_btn.config(state="disabled", bg="#c0392b")
            self.pause_btn.config(state="normal")
            self.countdown()

    def pause_timer(self):
        if self.is_running:
            self.is_running = False
            if self.timer_id:
                self.root.after_cancel(self.timer_id)
                self.timer_id = None
            self.start_btn.config(state="normal", text="继续", bg="#e74c3c")
            self.pause_btn.config(state="disabled")

    def reset_timer(self):
        if self.timer_id:
            self.root.after_cancel(self.timer_id)
            self.timer_id = None
        self.is_running = False
        self.is_working = True
        self.current_seconds = self.work_seconds
        self.start_btn.config(state="normal", text="开始", bg=self.c_work)
        self.pause_btn.config(state="disabled")
        self.update_display()

    def countdown(self):
        if self.is_running and self.current_seconds > 0:
            self.current_seconds -= 1
            self.update_display()
            self.timer_id = self.root.after(1000, self.countdown)
        elif self.current_seconds == 0:
            self.is_running = False
            self.timer_id = None
            self.play_notification()

    def update_display(self):
        minutes = self.current_seconds // 60
        seconds = self.current_seconds % 60
        self.time_label.config(text=f"{minutes:02d}:{seconds:02d}")

        # mode label
        if self.is_working:
            self.mode_label.config(text="工作模式", fg=self.c_work)
            total = self.work_seconds
            bar_color = self.c_work
        else:
            self.mode_label.config(text="休息模式", fg=self.c_break)
            total = self.break_seconds
            bar_color = self.c_break

        # progress bar
        ratio = self.current_seconds / total if total > 0 else 0
        bar_width = int(260 * ratio)
        self.canvas.coords(self.progress_bar, 0, 0, bar_width, 16)
        self.canvas.itemconfig(self.progress_bar, fill=bar_color)

        self.title_label.config(fg=bar_color)

    def play_notification(self):
        for _ in range(3):
            winsound.MessageBeep(winsound.MB_ICONEXCLAMATION)
        self.root.after(200, self._show_done_dialog)

    def _show_done_dialog(self):
        if self.is_working:
            msg = "工作时间结束！休息一下吧~"
            self.is_working = False
            self.current_seconds = self.break_seconds
        else:
            msg = "休息时间结束！开始新的番茄钟吧~"
            self.is_working = True
            self.current_seconds = self.work_seconds

        self.start_btn.config(state="normal", text="开始", bg=self.c_work)
        self.pause_btn.config(state="disabled")
        self.update_display()
        self.root.lift()
        self.root.focus_force()
        messagebox.showinfo("番茄钟", msg)


if __name__ == "__main__":
    root = tk.Tk()
    app = PomodoroTimer(root)
    root.mainloop()
