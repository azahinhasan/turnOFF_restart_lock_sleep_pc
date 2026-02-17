import tkinter as tk
from tkinter import ttk, messagebox
import os
import ctypes
import threading
import time


def create_rounded_button(parent, text, command, bg_color, fg_color="#ffffff", width=200, height=50, corner_radius=15):
    """Create a button with rounded corners using Canvas"""
    canvas = tk.Canvas(parent, width=width, height=height, bg=parent.cget('bg'), highlightthickness=0)
    
    def round_rectangle(x1, y1, x2, y2, radius=25, **kwargs):
        points = [x1+radius, y1,
                  x1+radius, y1,
                  x2-radius, y1,
                  x2-radius, y1,
                  x2, y1,
                  x2, y1+radius,
                  x2, y1+radius,
                  x2, y2-radius,
                  x2, y2-radius,
                  x2, y2,
                  x2-radius, y2,
                  x2-radius, y2,
                  x1+radius, y2,
                  x1+radius, y2,
                  x1, y2,
                  x1, y2-radius,
                  x1, y2-radius,
                  x1, y1+radius,
                  x1, y1+radius,
                  x1, y1]
        return canvas.create_polygon(points, **kwargs, smooth=True)
    
    rect = round_rectangle(2, 2, width-2, height-2, radius=corner_radius, fill=bg_color, outline=bg_color)
    text_id = canvas.create_text(width//2, height//2, text=text, fill=fg_color, font=("Segoe UI", 13, "bold"))
    
    def on_enter(e):
        canvas.itemconfig(rect, fill=adjust_color(bg_color, -20))
    
    def on_leave(e):
        canvas.itemconfig(rect, fill=bg_color)
    
    def on_click(e):
        command()
    
    canvas.bind("<Enter>", on_enter)
    canvas.bind("<Leave>", on_leave)
    canvas.bind("<Button-1>", on_click)
    canvas.config(cursor="hand2")
    
    return canvas, rect, text_id


def adjust_color(color, amount):
    """Adjust hex color brightness"""
    color = color.lstrip('#')
    r, g, b = tuple(int(color[i:i+2], 16) for i in (0, 2, 4))
    r = max(0, min(255, r + amount))
    g = max(0, min(255, g + amount))
    b = max(0, min(255, b + amount))
    return f'#{r:02x}{g:02x}{b:02x}'


class RoundedFrame(tk.Canvas):
    """A Frame with rounded corners"""
    def __init__(self, parent, bg_color, corner_radius=15, **kwargs):
        width = kwargs.pop('width', 200)
        height = kwargs.pop('height', 100)
        super().__init__(parent, width=width, height=height, bg=parent.cget('bg'), highlightthickness=0, **kwargs)
        self.bg_color = bg_color
        self.corner_radius = corner_radius
        self.rect = self._create_rounded_rect(2, 2, width-2, height-2, corner_radius, fill=bg_color, outline=bg_color)
        
    def _create_rounded_rect(self, x1, y1, x2, y2, radius=25, **kwargs):
        points = [x1+radius, y1,
                  x1+radius, y1,
                  x2-radius, y1,
                  x2-radius, y1,
                  x2, y1,
                  x2, y1+radius,
                  x2, y1+radius,
                  x2, y2-radius,
                  x2, y2-radius,
                  x2, y2,
                  x2-radius, y2,
                  x2-radius, y2,
                  x1+radius, y2,
                  x1+radius, y2,
                  x1, y2,
                  x1, y2-radius,
                  x1, y2-radius,
                  x1, y1+radius,
                  x1, y1+radius,
                  x1, y1]
        return self.create_polygon(points, **kwargs, smooth=True)


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
        
        header_canvas = tk.Canvas(main_frame, width=550, height=100, bg="#0f172a", highlightthickness=0)
        header_canvas.pack(fill=tk.X)
        # header_canvas.create_polygon([15, 5, 535, 5, 535, 95, 15, 95], fill="#1e293b", smooth=True, outline="#1e293b")
        header_canvas.create_text(275, 50, text="⏰ PC Action Timer", fill="#f1f5f9", font=("Segoe UI", 28, "bold"))
        
        content_frame = tk.Frame(main_frame, bg="#0f172a", padx=30, pady=20)
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        action_canvas = tk.Canvas(content_frame, width=490, height=200, bg="#0f172a", highlightthickness=0)
        action_canvas.pack(pady=(0, 20))
        self._create_rounded_rect(action_canvas, 0, 0, 490, 200, 20, fill="#1e293b", outline="#1e293b")
        action_canvas.create_text(30, 25, text="Select Action", fill="#cbd5e1", font=("Segoe UI", 13, "bold"), anchor="w")
        
        self.action_var = tk.StringVar(value="shutdown")
        
        actions = [
            ("🔴 Shutdown", "shutdown", 30, 50),
            ("🔄 Restart", "restart", 260, 50),
            ("🔒 Lock", "lock", 30, 120),
            ("💤 Sleep", "sleep", 260, 120)
        ]
        
        self.action_buttons = {}
        for text, value, x, y in actions:
            btn_canvas = tk.Canvas(action_canvas, width=200, height=50, bg="#1e293b", highlightthickness=0)
            btn_canvas.place(x=x, y=y)
            rect = self._create_rounded_rect(btn_canvas, 2, 2, 198, 48, 12, fill="#334155", outline="#334155")
            text_id = btn_canvas.create_text(100, 25, text=text, fill="#f1f5f9", font=("Segoe UI", 11, "bold"))
            
            def make_handler(val, r, c):
                def handler(e):
                    self.action_var.set(val)
                    self.update_action_selection()
                return handler
            
            btn_canvas.bind("<Button-1>", make_handler(value, rect, btn_canvas))
            btn_canvas.config(cursor="hand2")
            self.action_buttons[value] = (btn_canvas, rect)
        
        self.update_action_selection()
        
        time_canvas = tk.Canvas(content_frame, width=490, height=150, bg="#0f172a", highlightthickness=0)
        time_canvas.pack(pady=(0, 20))
        self._create_rounded_rect(time_canvas, 0, 0, 490, 150, 20, fill="#1e293b", outline="#1e293b")
        time_canvas.create_text(30, 25, text="Set Timer", fill="#cbd5e1", font=("Segoe UI", 13, "bold"), anchor="w")
        
        time_units = [
            ("Hours", "hours_var", 0, 23, 50),
            ("Minutes", "minutes_var", 0, 59, 200),
            ("Seconds", "seconds_var", 10, 59, 350)
        ]
        
        for label, var_name, default, max_val, x_pos in time_units:
            unit_canvas = tk.Canvas(time_canvas, width=110, height=80, bg="#1e293b", highlightthickness=0)
            unit_canvas.place(x=x_pos, y=50)
            self._create_rounded_rect(unit_canvas, 2, 2, 108, 78, 12, fill="#334155", outline="#334155")
            unit_canvas.create_text(55, 15, text=label, fill="#94a3b8", font=("Segoe UI", 9))
            
            var = tk.StringVar(value=str(default))
            setattr(self, var_name, var)
            
            spinbox = tk.Spinbox(
                unit_canvas,
                from_=0,
                to=max_val,
                textvariable=var,
                width=4,
                font=("Segoe UI", 16, "bold"),
                justify="center",
                bg="#475569",
                fg="#f1f5f9",
                buttonbackground="#64748b",
                relief=tk.FLAT,
                bd=0,
                highlightthickness=0
            )
            unit_canvas.create_window(55, 50, window=spinbox)
        
        countdown_canvas = tk.Canvas(content_frame, width=490, height=150, bg="#0f172a", highlightthickness=0)
        countdown_canvas.pack(pady=(0, 20))
        self._create_rounded_rect(countdown_canvas, 0, 0, 490, 150, 20, fill="#1e293b", outline="#1e293b")
        
        self.countdown_label_id = countdown_canvas.create_text(245, 60, text="00:00:00", fill="#60a5fa", font=("Segoe UI", 42, "bold"))
        self.status_label_id = countdown_canvas.create_text(245, 110, text="Ready to start", fill="#94a3b8", font=("Segoe UI", 11))
        self.countdown_canvas = countdown_canvas
        
        button_frame = tk.Frame(content_frame, bg="#0f172a")
        button_frame.pack(fill=tk.X, pady=(10, 15))
        
        self.start_pause_canvas, self.start_rect, self.start_text = create_rounded_button(
            button_frame, "▶  Start Timer", self.toggle_start_pause, "#10b981", width=230, height=50, corner_radius=15
        )
        self.start_pause_canvas.pack(side=tk.LEFT, padx=(0, 10))
        
        self.cancel_canvas, self.cancel_rect, self.cancel_text = create_rounded_button(
            button_frame, "⬛  Cancel", self.cancel_timer, "#64748b", width=230, height=50, corner_radius=15
        )
        self.cancel_canvas.pack(side=tk.LEFT)
        self.cancel_canvas.unbind("<Button-1>")
        self.cancel_canvas.config(cursor="arrow")
        
    def _create_rounded_rect(self, canvas, x1, y1, x2, y2, radius=25, **kwargs):
        points = [x1+radius, y1,
                  x1+radius, y1,
                  x2-radius, y1,
                  x2-radius, y1,
                  x2, y1,
                  x2, y1+radius,
                  x2, y1+radius,
                  x2, y2-radius,
                  x2, y2-radius,
                  x2, y2,
                  x2-radius, y2,
                  x2-radius, y2,
                  x1+radius, y2,
                  x1+radius, y2,
                  x1, y2,
                  x1, y2-radius,
                  x1, y2-radius,
                  x1, y1+radius,
                  x1, y1+radius,
                  x1, y1]
        return canvas.create_polygon(points, **kwargs, smooth=True)
    
    def update_action_selection(self):
        for value, (canvas, rect) in self.action_buttons.items():
            if value == self.action_var.get():
                canvas.itemconfig(rect, fill="#475569", outline="#475569")
            else:
                canvas.itemconfig(rect, fill="#334155", outline="#334155")
    
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
        
        self.start_pause_canvas.itemconfig(self.start_rect, fill="#f59e0b")
        self.start_pause_canvas.itemconfig(self.start_text, text="⏸  Pause")
        
        self.cancel_canvas.itemconfig(self.cancel_rect, fill="#ef4444")
        self.cancel_canvas.bind("<Button-1>", lambda e: self.cancel_timer())
        self.cancel_canvas.config(cursor="hand2")
        
        self.countdown_thread = threading.Thread(target=self.countdown, daemon=True)
        self.countdown_thread.start()
    
    def toggle_pause(self):
        self.is_paused = not self.is_paused
        
        if self.is_paused:
            self.start_pause_canvas.itemconfig(self.start_rect, fill="#10b981")
            self.start_pause_canvas.itemconfig(self.start_text, text="▶  Resume")
            self.countdown_canvas.itemconfig(self.status_label_id, text="⏸ Paused")
            self.countdown_canvas.itemconfig(self.countdown_label_id, fill="#f59e0b")
        else:
            self.start_pause_canvas.itemconfig(self.start_rect, fill="#f59e0b")
            self.start_pause_canvas.itemconfig(self.start_text, text="⏸  Pause")
            self.countdown_canvas.itemconfig(self.countdown_label_id, fill="#60a5fa")
    
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
        self.countdown_canvas.itemconfig(self.countdown_label_id, text=time_str)
        
        action_names = {
            "shutdown": "Shutting down",
            "restart": "Restarting",
            "lock": "Locking",
            "sleep": "Going to sleep"
        }
        
        if not self.is_paused:
            self.countdown_canvas.itemconfig(self.status_label_id, text=f"{action_names[self.selected_action]} in {time_str}")
    
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
        self.countdown_canvas.itemconfig(self.countdown_label_id, text="00:00:00", fill="#60a5fa")
        self.countdown_canvas.itemconfig(self.status_label_id, text="Ready to start")
        
        self.start_pause_canvas.itemconfig(self.start_rect, fill="#10b981")
        self.start_pause_canvas.itemconfig(self.start_text, text="▶  Start Timer")
        
        self.cancel_canvas.itemconfig(self.cancel_rect, fill="#64748b")
        self.cancel_canvas.unbind("<Button-1>")
        self.cancel_canvas.config(cursor="arrow")


def main():
    root = tk.Tk()
    app = TimerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
