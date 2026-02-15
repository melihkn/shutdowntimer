"""
Shutdown Timer - A simple Windows shutdown timer application.
Double-click the .exe to run. Set hours, minutes, seconds and click Start.
"""

import tkinter as tk
from tkinter import messagebox
import subprocess
import os


class ShutdownTimer:
    def __init__(self, root):
        self.root = root
        self.root.title("Shutdown Timer")
        self.root.resizable(False, False)
        self.root.configure(bg="#1e1e2e")

        # Center window on screen
        window_width, window_height = 420, 380
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")

        self.remaining_seconds = 0
        self.timer_id = None
        self.is_running = False

        # Colors
        self.BG = "#1e1e2e"
        self.CARD_BG = "#2a2a3d"
        self.ACCENT = "#7c3aed"
        self.ACCENT_HOVER = "#6d28d9"
        self.DANGER = "#ef4444"
        self.DANGER_HOVER = "#dc2626"
        self.TEXT = "#e2e8f0"
        self.TEXT_DIM = "#94a3b8"
        self.INPUT_BG = "#363650"
        self.SUCCESS = "#22c55e"

        self._build_ui()

    def _build_ui(self):
        # Title
        tk.Label(
            self.root, text="⏻ Shutdown Timer", font=("Segoe UI", 18, "bold"),
            fg=self.TEXT, bg=self.BG
        ).pack(pady=(20, 5))

        tk.Label(
            self.root, text="Set the time and your PC will shut down automatically.",
            font=("Segoe UI", 9), fg=self.TEXT_DIM, bg=self.BG
        ).pack(pady=(0, 15))

        # Time selection card
        card = tk.Frame(self.root, bg=self.CARD_BG, padx=20, pady=18)
        card.pack(padx=25, fill="x")

        # Time inputs row
        time_frame = tk.Frame(card, bg=self.CARD_BG)
        time_frame.pack()

        self.hour_var = tk.StringVar(value="0")
        self.min_var = tk.StringVar(value="30")
        self.sec_var = tk.StringVar(value="0")

        for label_text, var in [("Hours", self.hour_var), ("Minutes", self.min_var), ("Seconds", self.sec_var)]:
            col = tk.Frame(time_frame, bg=self.CARD_BG)
            col.pack(side="left", padx=12)

            tk.Label(col, text=label_text, font=("Segoe UI", 9), fg=self.TEXT_DIM, bg=self.CARD_BG).pack()

            entry = tk.Entry(
                col, textvariable=var, font=("Segoe UI", 22, "bold"),
                width=3, justify="center",
                bg=self.INPUT_BG, fg=self.TEXT, insertbackground=self.TEXT,
                relief="flat", bd=0, highlightthickness=2,
                highlightbackground=self.INPUT_BG, highlightcolor=self.ACCENT
            )
            entry.pack(pady=(4, 0), ipady=4)

        # Countdown display
        self.countdown_label = tk.Label(
            self.root, text="00:00:00", font=("Consolas", 32, "bold"),
            fg=self.TEXT_DIM, bg=self.BG
        )
        self.countdown_label.pack(pady=(20, 5))

        self.status_label = tk.Label(
            self.root, text="Ready", font=("Segoe UI", 10),
            fg=self.TEXT_DIM, bg=self.BG
        )
        self.status_label.pack()

        # Buttons
        btn_frame = tk.Frame(self.root, bg=self.BG)
        btn_frame.pack(pady=(15, 20))

        self.start_btn = tk.Button(
            btn_frame, text="▶  Start", font=("Segoe UI", 11, "bold"),
            bg=self.ACCENT, fg="white", activebackground=self.ACCENT_HOVER,
            activeforeground="white", relief="flat", cursor="hand2",
            padx=24, pady=8, command=self.start_timer
        )
        self.start_btn.pack(side="left", padx=6)

        self.cancel_btn = tk.Button(
            btn_frame, text="✕  Cancel", font=("Segoe UI", 11, "bold"),
            bg=self.DANGER, fg="white", activebackground=self.DANGER_HOVER,
            activeforeground="white", relief="flat", cursor="hand2",
            padx=24, pady=8, command=self.cancel_timer, state="disabled"
        )
        self.cancel_btn.pack(side="left", padx=6)

    def _validate_input(self):
        try:
            h = int(self.hour_var.get())
            m = int(self.min_var.get())
            s = int(self.sec_var.get())
            if h < 0 or m < 0 or s < 0:
                raise ValueError
            total = h * 3600 + m * 60 + s
            if total <= 0:
                raise ValueError("Total time must be greater than 0")
            return total
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter valid non-negative numbers.\nTotal time must be greater than 0.")
            return None

    def start_timer(self):
        total = self._validate_input()
        if total is None:
            return

        # Schedule Windows shutdown
        subprocess.run(["shutdown", "/s", "/t", str(total)], creationflags=subprocess.CREATE_NO_WINDOW)

        self.remaining_seconds = total
        self.is_running = True
        self.start_btn.config(state="disabled")
        self.cancel_btn.config(state="normal")
        self.status_label.config(text="Shutdown scheduled", fg=self.SUCCESS)
        self._tick()

    def cancel_timer(self):
        # Abort Windows shutdown
        subprocess.run(["shutdown", "/a"], creationflags=subprocess.CREATE_NO_WINDOW)

        if self.timer_id:
            self.root.after_cancel(self.timer_id)
            self.timer_id = None

        self.is_running = False
        self.remaining_seconds = 0
        self.countdown_label.config(text="00:00:00", fg=self.TEXT_DIM)
        self.status_label.config(text="Cancelled", fg=self.DANGER)
        self.start_btn.config(state="normal")
        self.cancel_btn.config(state="disabled")

    def _tick(self):
        if self.remaining_seconds <= 0:
            self.countdown_label.config(text="00:00:00", fg=self.DANGER)
            self.status_label.config(text="Shutting down...", fg=self.DANGER)
            return

        h = self.remaining_seconds // 3600
        m = (self.remaining_seconds % 3600) // 60
        s = self.remaining_seconds % 60
        self.countdown_label.config(text=f"{h:02d}:{m:02d}:{s:02d}", fg=self.TEXT)

        # Flash red in last 60 seconds
        if self.remaining_seconds <= 60:
            self.countdown_label.config(fg=self.DANGER)
            self.status_label.config(text="⚠ Shutting down soon!", fg=self.DANGER)

        self.remaining_seconds -= 1
        self.timer_id = self.root.after(1000, self._tick)

    def on_close(self):
        if self.is_running:
            if messagebox.askyesno("Exit", "Timer is running. Cancel shutdown and exit?"):
                self.cancel_timer()
                self.root.destroy()
        else:
            self.root.destroy()


def main():
    root = tk.Tk()
    app = ShutdownTimer(root)
    root.protocol("WM_DELETE_CLOSE", app.on_close)
    root.mainloop()


if __name__ == "__main__":
    main()
