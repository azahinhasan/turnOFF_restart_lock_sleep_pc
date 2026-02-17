import tkinter as tk
from tkinter import ttk, messagebox
import os
import ctypes
import threading
import time


class TimerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PC Action Timer - Shutdown/Restart/Lock/Sleep")
        self.root.geometry("550x800")
        self.root.resizable(False, False)
        
        try:
            icon_path = os.path.join(os.path.dirname(__file__), "plug.ico")
            if os.path.exists(icon_path):
                self.root.iconbitmap(icon_path)
        except:
            pass
        
        self.countdown_active = False
        self.is_paused = False
        self.countdown_thread = None
        self.remaining_seconds = 0
        self.selected_action = None
        
        self.setup_ui()
        
    def setup_ui(self):
        main_frame = tk.Frame(self.root, bg="#0f172a")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        header_frame = tk.Frame(main_frame, bg="#1e293b", height=100)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(
            header_frame,
            text="⏰ PC Action Timer",
            font=("Segoe UI", 28, "bold"),
            bg="#1e293b",
            fg="#f1f5f9"
        )
        title_label.pack(pady=25)
        
        content_frame = tk.Frame(main_frame, bg="#0f172a", padx=30, pady=20)
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        action_frame = tk.Frame(content_frame, bg="#1e293b", relief=tk.RAISED, bd=2)
        action_frame.pack(fill=tk.X, pady=(0, 20))
        
        action_header = tk.Label(
            action_frame,
            text="Select Action",
            font=("Segoe UI", 13, "bold"),
            bg="#1e293b",
            fg="#cbd5e1",
            anchor="w"
        )
        action_header.pack(fill=tk.X, padx=20, pady=(15, 10))
        
        self.action_var = tk.StringVar(value="shutdown")
        
        actions = [
            ("Shutdown", "shutdown", "🔴", "#ef4444"),
            ("Restart", "restart", "🔄", "#3b82f6"),
            ("Lock", "lock", "🔒", "#f59e0b"),
            ("Sleep", "sleep", "💤", "#8b5cf6")
        ]
        
        actions_grid = tk.Frame(action_frame, bg="#1e293b")
        actions_grid.pack(padx=20, pady=(0, 15))
        
        for i, (text, value, emoji, color) in enumerate(actions):
            btn_frame = tk.Frame(actions_grid, bg="#334155", relief=tk.RAISED, bd=1)
            btn_frame.grid(row=i//2, column=i%2, padx=8, pady=8, sticky="ew")
            
            rb = tk.Radiobutton(
                btn_frame,
                text=f"{emoji}  {text}",
                variable=self.action_var,
                value=value,
                font=("Segoe UI", 11, "bold"),
                bg="#334155",
                fg="#f1f5f9",
                selectcolor="#475569",
                activebackground="#334155",
                activeforeground="#f1f5f9",
                cursor="hand2",
                indicatoron=0,
                width=12,
                height=2,
                relief=tk.RAISED,
                bd=2,
                highlightthickness=0,
                overrelief=tk.RAISED
            )
            rb.pack(fill=tk.BOTH, expand=True, padx=3, pady=3)
        
        actions_grid.columnconfigure(0, weight=1)
        actions_grid.columnconfigure(1, weight=1)
        
        time_frame = tk.Frame(content_frame, bg="#1e293b", relief=tk.RAISED, bd=2)
        time_frame.pack(fill=tk.X, pady=(0, 20))
        
        time_header = tk.Label(
            time_frame,
            text="Set Timer",
            font=("Segoe UI", 13, "bold"),
            bg="#1e293b",
            fg="#cbd5e1",
            anchor="w"
        )
        time_header.pack(fill=tk.X, padx=20, pady=(15, 10))
        
        time_inputs_frame = tk.Frame(time_frame, bg="#1e293b")
        time_inputs_frame.pack(pady=(0, 15))
        
        time_units = [
            ("Hours", "hours_var", 0, 23),
            ("Minutes", "minutes_var", 0, 59),
            ("Seconds", "seconds_var", 10, 59)
        ]
        
        for i, (label, var_name, default, max_val) in enumerate(time_units):
            unit_frame = tk.Frame(time_inputs_frame, bg="#334155", relief=tk.RAISED, bd=1)
            unit_frame.grid(row=0, column=i, padx=10, pady=5)
            
            tk.Label(
                unit_frame,
                text=label,
                font=("Segoe UI", 9),
                bg="#334155",
                fg="#94a3b8"
            ).pack(pady=(8, 2))
            
            var = tk.StringVar(value=str(default))
            setattr(self, var_name, var)
            
            spinbox = tk.Spinbox(
                unit_frame,
                from_=0,
                to=max_val,
                textvariable=var,
                width=6,
                font=("Segoe UI", 16, "bold"),
                justify="center",
                bg="#475569",
                fg="#f1f5f9",
                buttonbackground="#64748b",
                relief=tk.RAISED,
                bd=1,
                highlightthickness=0
            )
            spinbox.pack(padx=10, pady=(0, 8))
        
        countdown_frame = tk.Frame(content_frame, bg="#1e293b", relief=tk.RAISED, bd=2)
        countdown_frame.pack(fill=tk.X, pady=(0, 20))
        
        countdown_display = tk.Frame(countdown_frame, bg="#0f172a")
        countdown_display.pack(padx=20, pady=15)
        
        self.countdown_label = tk.Label(
            countdown_display,
            text="00:00:00",
            font=("Segoe UI", 42, "bold"),
            bg="#0f172a",
            fg="#60a5fa"
        )
        self.countdown_label.pack(pady=10)
        
        self.status_label = tk.Label(
            countdown_display,
            text="Ready to start",
            font=("Segoe UI", 11),
            bg="#0f172a",
            fg="#94a3b8"
        )
        self.status_label.pack()
        
        button_frame = tk.Frame(content_frame, bg="#0f172a")
        button_frame.pack(fill=tk.X, pady=(10, 15))
        
        self.start_pause_button = tk.Button(
            button_frame,
            text="▶  Start Timer",
            command=self.toggle_start_pause,
            font=("Segoe UI", 13, "bold"),
            bg="#10b981",
            fg="white",
            activebackground="#059669",
            activeforeground="white",
            cursor="hand2",
            relief=tk.RAISED,
            bd=3,
            height=2,
            overrelief=tk.RAISED
        )
        self.start_pause_button.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(0, 8))
        
        self.cancel_button = tk.Button(
            button_frame,
            text="⬛  Cancel",
            command=self.cancel_timer,
            font=("Segoe UI", 13, "bold"),
            bg="#64748b",
            fg="white",
            activebackground="#475569",
            activeforeground="white",
            cursor="hand2",
            relief=tk.RAISED,
            bd=3,
            height=2,
            state=tk.DISABLED,
            overrelief=tk.RAISED
        )
        self.cancel_button.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(8, 0))
        
    def get_total_seconds(self):
        try:
            hours = int(self.hours_var.get())
            minutes = int(self.minutes_var.get())
            seconds = int(self.seconds_var.get())
            return hours * 3600 + minutes * 60 + seconds
        except ValueError:
            return 0
    
    def toggle_start_pause(self):
        if not self.countdown_active:
            self.start_timer()
        else:
            self.toggle_pause()
    
    def start_timer(self):
        total_seconds = self.get_total_seconds()
        
        if total_seconds <= 0:
            messagebox.showerror("Error", "Please set a valid time (greater than 0)")
            return
        
        action = self.action_var.get()
        action_names = {
            "shutdown": "Shutdown",
            "restart": "Restart",
            "lock": "Lock",
            "sleep": "Sleep"
        }
        
        confirm = messagebox.askyesno(
            "Confirm Action",
            f"Are you sure you want to {action_names[action]} your PC after {self.format_time(total_seconds)}?"
        )
        
        if not confirm:
            return
        
        self.countdown_active = True
        self.is_paused = False
        self.remaining_seconds = total_seconds
        self.selected_action = action
        
        self.start_pause_button.config(
            text="⏸  Pause",
            bg="#f59e0b",
            activebackground="#d97706"
        )
        self.cancel_button.config(state=tk.NORMAL, bg="#ef4444", activebackground="#dc2626")
        
        self.countdown_thread = threading.Thread(target=self.countdown, daemon=True)
        self.countdown_thread.start()
    
    def toggle_pause(self):
        self.is_paused = not self.is_paused
        
        if self.is_paused:
            self.start_pause_button.config(
                text="▶  Resume",
                bg="#10b981",
                activebackground="#059669"
            )
            self.status_label.config(text="⏸ Paused")
            self.countdown_label.config(fg="#f59e0b")
        else:
            self.start_pause_button.config(
                text="⏸  Pause",
                bg="#f59e0b",
                activebackground="#d97706"
            )
            self.countdown_label.config(fg="#60a5fa")
    
    def countdown(self):
        while self.countdown_active and self.remaining_seconds > 0:
            if not self.is_paused:
                self.root.after(0, self.update_countdown_display)
                time.sleep(1)
                self.remaining_seconds -= 1
            else:
                time.sleep(0.1)
        
        if self.countdown_active and self.remaining_seconds == 0:
            self.root.after(0, self.execute_action)
    
    def update_countdown_display(self):
        time_str = self.format_time(self.remaining_seconds)
        self.countdown_label.config(text=time_str)
        
        action_names = {
            "shutdown": "Shutting down",
            "restart": "Restarting",
            "lock": "Locking",
            "sleep": "Going to sleep"
        }
        
        if not self.is_paused:
            self.status_label.config(text=f"{action_names[self.selected_action]} in {time_str}")
    
    def format_time(self, seconds):
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        secs = seconds % 60
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"
    
    def execute_action(self):
        action = self.selected_action
        
        try:
            if action == "shutdown":
                os.system("shutdown /s /t 1")
            elif action == "restart":
                os.system("shutdown /r /t 1")
            elif action == "lock":
                ctypes.windll.user32.LockWorkStation()
            elif action == "sleep":
                os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to execute action: {str(e)}")
        
        self.reset_timer()
    
    def cancel_timer(self):
        if messagebox.askyesno("Cancel Timer", "Are you sure you want to cancel the timer?"):
            self.countdown_active = False
            self.is_paused = False
            self.reset_timer()
    
    def reset_timer(self):
        self.countdown_active = False
        self.is_paused = False
        self.remaining_seconds = 0
        self.countdown_label.config(text="00:00:00", fg="#60a5fa")
        self.status_label.config(text="Ready to start")
        self.start_pause_button.config(
            text="▶  Start Timer",
            state=tk.NORMAL,
            bg="#10b981",
            activebackground="#059669"
        )
        self.cancel_button.config(state=tk.DISABLED, bg="#64748b", activebackground="#475569")


def main():
    root = tk.Tk()
    app = TimerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
