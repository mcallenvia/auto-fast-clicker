# Developed by McAllen
# - Soft UI theme
# - Responsive layout using pack(fill/expand) only
# - Font scaling on resize
# - Rounded-look buttons (Canvas-based) that behave like Buttons

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import threading
import time
import math

# optional libs
try:
    import pyautogui
    pyautogui.PAUSE = 0
    pyautogui.FAILSAFE = False
except Exception:
    pyautogui = None

try:
    import keyboard
except Exception:
    keyboard = None

# ----------------------------
# Helper: Rounded-like Button (Canvas) — visually modern but API like Button
# ----------------------------
class FancyButton(tk.Canvas):
    def __init__(self, master, text="", command=None, height=34, radius=14,
                 bg="#4a90ff", fg="#ffffff", hover="#5ea0ff", font=None, padx=16, **kwargs):
        super().__init__(master, height=height, highlightthickness=0, bd=0, bg=master.cget("bg"))
        self._text = text
        self._cmd = command
        self._bg = bg
        self._fg = fg
        self._hover = hover
        self._radius = radius
        self._height = height
        self._font = font or ("Segoe UI", 10, "bold")
        self._padx = padx
        self._is_hover = False
        self.bind("<Configure>", lambda e: self._draw())
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)
        self.bind("<Button-1>", lambda e: self._on_click())
        self._draw()

    def _on_enter(self, e):
        self._is_hover = True
        self._draw()

    def _on_leave(self, e):
        self._is_hover = False
        self._draw()

    def _on_click(self):
        if callable(self._cmd):
            try:
                self._cmd()
            except Exception as e:
                print("Button command error:", e)

    def configure_colors(self, bg=None, fg=None, hover=None):
        if bg: self._bg = bg
        if fg: self._fg = fg
        if hover: self._hover = hover
        self._draw()

    def configure_text(self, text):
        self._text = text
        self._draw()

    def _draw(self):
        self.delete("all")
        w = self.winfo_width() or 120
        h = self._height
        r = min(self._radius, h//2)
        bg = self._hover if self._is_hover else self._bg
        # draw rounded rectangle as polygon with smoothing
        pts = [
            2+r, 2,
            w-r-2, 2,
            w-2, 2,
            w-2, 2+r,
            w-2, h-r-2,
            w-2, h-2,
            w-r-2, h-2,
            2+r, h-2,
            2, h-2,
            2, h-r-2,
            2, 2+r,
            2, 2
        ]
        try:
            self.create_polygon(pts, smooth=True, fill=bg, outline="")
        except Exception:
            # fallback rectangle
            self.create_rectangle(2,2,w-2,h-2, fill=bg, outline="")
        self.create_text(w/2, h/2, text=self._text, font=self._font, fill=self._fg)

# ----------------------------
# Main App — all original logic preserved and relocated into class
# ----------------------------
class McAllenClicker:
    def __init__(self, root):
        self.root = root
        self.root.title("FastClicker")
        self.root.geometry("960x540")
        self.root.minsize(720, 420)
        self.root.configure(bg='#0f1113')

        # Variables (preserve original names / behavior)
        self.is_clicking = False
        self.cps = tk.DoubleVar(value=10.0)
        self.total_clicks = 0
        self.session_clicks = 0
        self.click_mode = tk.StringVar(value="toggle")
        self.hotkey = tk.StringVar(value="NOT SET")
        self.current_hotkey = None
        self.button_type = tk.StringVar(value="left")
        self.click_type = tk.StringVar(value="single")
        self.start_time = None
        self.actual_cps = 0
        self.last_second_clicks = []
        self.is_recording_hotkey = False

        # fonts base (will scale)
        self.base_font_large = ("Segoe UI", 28, "bold")
        self.base_font_med = ("Segoe UI", 12)
        self.base_font_small = ("Segoe UI", 9)

        # Build responsive UI (pack + expand only)
        self._build_ui()

        # Bind resize for font scaling
        self.root.bind("<Configure>", self._on_root_resize_throttled())

    # ------------- UI BUILD -------------
    def _build_ui(self):
        # Header (top)
        self.header = tk.Frame(self.root, bg="#0b0d0e")
        self.header.pack(side="top", fill="x")
        self.header.pack_propagate(False)
        self.header.configure(height=64)

        title_frame = tk.Frame(self.header, bg="#0b0d0e")
        title_frame.pack(side="left", padx=18, pady=10)
        self.title_label = tk.Label(title_frame, text="FastClicker", font=("Segoe UI", 16, "bold"),
                                    fg="#f4f7fb", bg="#0b0d0e")
        self.title_label.pack(anchor="w")
        self.subtitle_label = tk.Label(title_frame, text="Developed by McAllen",
                                       font=("Segoe UI", 9), fg="#9aa6b2", bg="#0b0d0e")
        self.subtitle_label.pack(anchor="w")

        # Main content container
        self.main = tk.Frame(self.root, bg="#0f1113")
        self.main.pack(fill="both", expand=True, padx=12, pady=12)

        # Use three columns via frames — pack with expand to get responsive columns
        self.left = tk.Frame(self.main, bg="#121417")
        self.left.pack(side="left", fill="both", expand=True, padx=(0,8))
        self.center = tk.Frame(self.main, bg="#13161a")
        self.center.pack(side="left", fill="both", expand=True, padx=(0,8))
        self.right = tk.Frame(self.main, bg="#121417")
        self.right.pack(side="left", fill="both", expand=True)

        # Left content (Hotkey, Mode, Button)
        self._build_left(self.left)
        # Center content (CPS slider and presets)
        self._build_center(self.center)
        # Right content (stats + actions)
        self._build_right(self.right)

        # Status bar bottom
        self.status = tk.Label(self.root, text="Developed by McAllen ~ 2025", anchor="w",
                               font=self.base_font_small, bg="#0b0d0e", fg="#94a3b8")
        self.status.pack(side="bottom", fill="x")

    def _build_left(self, parent):
        pad = 12
        container = tk.Frame(parent, bg=parent.cget("bg"))
        container.pack(fill="both", expand=True, padx=12, pady=12)

        tk.Label(container, text="Hotkey", font=self.base_font_med, bg=container.cget("bg"), fg="#9aa6b2").pack(anchor="w")
        self.hotkey_label = tk.Label(container, textvariable=self.hotkey, font=("Segoe UI", 14, "bold"),
                                     bg="#0f1113", fg="#4a9eff", width=12, height=2, relief="flat")
        self.hotkey_label.pack(pady=(8,10))

        self.hotkey_btn = FancyButton(container, text="Set Hotkey", command=self.start_recording_hotkey,
                                      bg="#2a2f36", hover="#3a4f77", fg="#fff", font=("Segoe UI",10,"bold"))
        self.hotkey_btn.pack(pady=(0,14), fill="x")

        # Mode
        tk.Label(container, text="Mode", font=self.base_font_med, bg=container.cget("bg"), fg="#9aa6b2").pack(anchor="w", pady=(6,2))
        mode_frame = tk.Frame(container, bg=container.cget("bg"))
        mode_frame.pack(anchor="w", pady=(0,12))
        for text, val in [("Toggle", "toggle"), ("Hold", "hold")]:
            rb = tk.Radiobutton(mode_frame, text=text, variable=self.click_mode, value=val,
                                font=self.base_font_small, bg=container.cget("bg"),
                                fg="#d1d5db", selectcolor=container.cget("bg"), activebackground=container.cget("bg"),
                                anchor="w", highlightthickness=0, bd=0)
            rb.pack(anchor="w", pady=2)

        # Button selection
        tk.Label(container, text="Button", font=self.base_font_med, bg=container.cget("bg"), fg="#9aa6b2").pack(anchor="w", pady=(6,2))
        btn_frame = tk.Frame(container, bg=container.cget("bg"))
        btn_frame.pack(anchor="w")
        for text, val in [("Left", "left"), ("Right", "right"), ("Middle", "middle")]:
            rb = tk.Radiobutton(btn_frame, text=text, variable=self.button_type, value=val,
                                font=self.base_font_small, bg=container.cget("bg"),
                                fg="#d1d5db", selectcolor=container.cget("bg"), activebackground=container.cget("bg"))
            rb.pack(anchor="w")

    def _build_center(self, parent):
        container = tk.Frame(parent, bg=parent.cget("bg"))
        container.pack(fill="both", expand=True, padx=12, pady=12)

        tk.Label(container, text="Target CPS", font=self.base_font_med, bg=container.cget("bg"), fg="#9aa6b2").pack()
        self.cps_display = tk.Label(container, text=f"{self.cps.get():.1f}", font=self.base_font_large,
                                    bg=container.cget("bg"), fg="#4a9eff")
        self.cps_display.pack(pady=(6,12))

        slider_frame = tk.Frame(container, bg=container.cget("bg"))
        slider_frame.pack(fill="x", padx=8)
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TScale", background=container.cget("bg"))
        self.cps_slider = ttk.Scale(slider_frame, from_=1, to=100, variable=self.cps,
                                    orient='horizontal', command=self.update_cps_display)
        self.cps_slider.pack(fill="x")

        # presets
        presets = tk.Frame(container, bg=container.cget("bg"))
        presets.pack(pady=(12,10))
        for i, cps in enumerate([10, 20, 50, 100]):
            b = FancyButton(presets, text=str(cps), command=lambda c=cps: self.set_cps_preset(c),
                            bg="#2b2f34", hover="#3a4f77", fg="#fff", font=("Segoe UI",10,"bold"))
            b.pack(side="left", padx=6, pady=4, ipadx=6)

        tk.Label(container, text="Click Type", font=self.base_font_med, bg=container.cget("bg"), fg="#9aa6b2").pack(pady=(12,6))
        type_frame = tk.Frame(container, bg=container.cget("bg"))
        type_frame.pack()
        for text, val in [("Single", "single"), ("Double", "double")]:
            rb = tk.Radiobutton(type_frame, text=text, variable=self.click_type, value=val,
                                font=self.base_font_small, bg=container.cget("bg"),
                                fg="#d1d5db", selectcolor=container.cget("bg"), activebackground=container.cget("bg"))
            rb.pack(anchor="w")

    def _build_right(self, parent):
        container = tk.Frame(parent, bg=parent.cget("bg"))
        container.pack(fill="both", expand=True, padx=12, pady=12)

        tk.Label(container, text="Real-time CPS", font=self.base_font_med, bg=container.cget("bg"), fg="#9aa6b2").pack()
        self.actual_cps_label = tk.Label(container, text="0.0", font=("Segoe UI", 36, "bold"),
                                         bg=container.cget("bg"), fg="#4a9eff")
        self.actual_cps_label.pack(pady=(6,18))

        stats_container = tk.Frame(container, bg=container.cget("bg"))
        stats_container.pack(pady=(0,12), fill="x")

        # Three stat boxes stacked horizontally but responsive
        stat1 = tk.Frame(stats_container, bg="#0f1113")
        stat1.pack(side="left", expand=True, fill="both", padx=6)
        tk.Label(stat1, text="Total", font=self.base_font_small, bg=stat1.cget("bg"), fg="#9aa6b2").pack(pady=(8,4))
        self.total_label = tk.Label(stat1, text="0", font=("Segoe UI", 18, "bold"), bg=stat1.cget("bg"), fg="#ffffff")
        self.total_label.pack()

        stat2 = tk.Frame(stats_container, bg="#0f1113")
        stat2.pack(side="left", expand=True, fill="both", padx=6)
        tk.Label(stat2, text="Session", font=self.base_font_small, bg=stat2.cget("bg"), fg="#9aa6b2").pack(pady=(8,4))
        self.session_label = tk.Label(stat2, text="0", font=("Segoe UI", 18, "bold"), bg=stat2.cget("bg"), fg="#ffffff")
        self.session_label.pack()

        stat3 = tk.Frame(stats_container, bg="#0f1113")
        stat3.pack(side="left", expand=True, fill="both", padx=6)
        tk.Label(stat3, text="Time", font=self.base_font_small, bg=stat3.cget("bg"), fg="#9aa6b2").pack(pady=(8,4))
        self.time_label = tk.Label(stat3, text="00:00", font=("Segoe UI", 18, "bold"), bg=stat3.cget("bg"), fg="#ffffff")
        self.time_label.pack()

        # Action buttons
        actions = tk.Frame(container, bg=container.cget("bg"))
        actions.pack(pady=(18,6))
        self.start_btn = FancyButton(actions, text="START", command=self.toggle_clicking,
                                     bg="#4a9eff", hover="#66b0ff", fg="#fff", font=("Segoe UI",11,"bold"))
        self.start_btn.pack(side="left", padx=8, ipadx=4)
        self.reset_btn = FancyButton(actions, text="RESET", command=self.reset_stats,
                                     bg="#2b2f34", hover="#3a4f77", fg="#fff", font=("Segoe UI",11,"bold"))
        self.reset_btn.pack(side="left", padx=8, ipadx=4)

        # Initially disable start until hotkey set (preserve original behavior)
        self.start_btn_state_update(disable= (self.hotkey.get() == "NOT SET"))

    # -------------------------
    # UI utility helpers
    # -------------------------
    def start_recording_hotkey(self):
        if self.is_clicking:
            messagebox.showwarning("Warning", "Stop clicking first")
            return

        self.is_recording_hotkey = True
        self.hotkey_btn.configure_text("Press a key...")
        self.status.config(text="Waiting for key press...")

        # Unhook previous if any
        try:
            if self.current_hotkey:
                keyboard.unhook_key(self.current_hotkey)
        except Exception:
            pass

        # If keyboard not available, fallback to dialog
        if keyboard is None:
            k = simpledialog.askstring("Hotkey", "Enter hotkey (e.g. F6, a, ctrl+shift+x):", parent=self.root)
            if k:
                self.hotkey.set(k.upper())
                self.current_hotkey = k.lower()
                self.start_btn_state_update(disable=False)
                self.hotkey_btn.configure_text("Set Hotkey")
                self.hotkey_btn._draw()
                self.status.config(text=f"Ready - Press {k.upper()} to start")
            self.is_recording_hotkey = False
            return

        # watcher callback
        def _on_press(event):
            if not self.is_recording_hotkey:
                return
            name = getattr(event, "name", None)
            if not name:
                return
            try:
                keyboard.unhook_all()
            except Exception:
                pass
            self.is_recording_hotkey = False
            name_upper = name.upper()
            self.hotkey.set(name_upper)
            self.current_hotkey = name.lower()
            # register
            try:
                keyboard.on_press_key(self.current_hotkey, lambda e: self.toggle_clicking())
            except Exception:
                pass
            self.start_btn_state_update(disable=False)
            self.hotkey_btn.configure_text("Set Hotkey")
            self.status.config(text=f"Ready - Press {name_upper} to start")

        try:
            keyboard.on_press(_on_press)
        except Exception:
            messagebox.showerror("Error", "Unable to record hotkey")
            self.is_recording_hotkey = False
            self.hotkey_btn.configure_text("Set Hotkey")
            self.status.config(text="")

    def start_btn_state_update(self, disable=True):
        # tweak visual disabled state by changing color
        if disable:
            self.start_btn.configure_colors(bg="#5a6570", fg="#e6eef8", hover="#6b7a85")
        else:
            self.start_btn.configure_colors(bg="#4a90ff", fg="#ffffff", hover="#66b0ff")

    # This method provides a small wrapper so FancyButton can reconfigure colors
    def _ensure_fancy_methods(self):
        # ensure buttons have configure_colors method (they do)
        for b in (self.start_btn, self.reset_btn, self.hotkey_btn):
            if not hasattr(b, "configure_colors"):
                # no-op
                b.configure_colors = lambda **k: None

    # -------------------------
    # Functional behavior (unchanged logic, improved safety)
    # -------------------------
    def update_cps_display(self, value):
        try:
            self.cps_display.config(text=f"{float(value):.1f}")
        except Exception:
            pass

    def set_cps_preset(self, value):
        self.cps.set(value)
        self.update_cps_display(value)

    def toggle_clicking(self):
        if self.hotkey.get() == "NOT SET":
            return
        if not self.is_clicking:
            self.start_clicking()
        else:
            self.stop_clicking()

    def start_clicking(self):
        self.is_clicking = True
        self.start_time = time.time()
        self.session_clicks = 0
        self.last_second_clicks = []

        self.start_btn.configure_text("STOP")
        self.start_btn.configure_colors(bg="#ff534f", hover="#ff6763", fg="#fff")
        self.hotkey_btn.configure_text("Set Hotkey")
        # disable hotkey during run visually (no actual disable needed)
        self.hotkey_btn.configure_colors(bg="#2b2f34", hover="#3a4f77")

        # register hotkey if keyboard available
        if keyboard:
            try:
                keyboard.unhook_all()
                if self.current_hotkey:
                    keyboard.on_press_key(self.current_hotkey, lambda e: self.toggle_clicking())
            except Exception:
                pass

        # threads as original
        t1 = threading.Thread(target=self.click_loop, daemon=True)
        t2 = threading.Thread(target=self.monitor_cps, daemon=True)
        t3 = threading.Thread(target=self.update_timer, daemon=True)
        t1.start(); t2.start(); t3.start()
        self.status.config(text=f"Active - Press {self.hotkey.get()} to stop")

    def stop_clicking(self):
        self.is_clicking = False
        self.start_btn.configure_text("START")
        self.start_btn.configure_colors(bg="#4a90ff", hover="#66b0ff", fg="#fff")
        # re-enable hotkey visually
        self.hotkey_btn.configure_colors(bg="#2a2f34", hover="#3a4f77")
        self.status.config(text=f"Stopped - Press {self.hotkey.get()} to restart")

    def click_loop(self):
        while self.is_clicking:
            try:
                # hold mode check
                if self.click_mode.get() == "hold" and keyboard:
                    try:
                        if not keyboard.is_pressed(self.current_hotkey):
                            time.sleep(0.001)
                            continue
                    except Exception:
                        pass

                clicks = 2 if self.click_type.get() == "double" else 1

                # perform clicks
                # Use mouseDown/up similarly to original; keep try/except
                try:
                    pyautogui.mouseDown(button=self.button_type.get())
                    pyautogui.mouseUp(button=self.button_type.get())
                    if clicks == 2:
                        pyautogui.mouseDown(button=self.button_type.get())
                        pyautogui.mouseUp(button=self.button_type.get())
                except Exception:
                    # if pyautogui fails for any reason, stop to avoid busy loop
                    print("pyautogui.click failed; stopping clicking")
                    self.stop_clicking()
                    return

                self.total_clicks += clicks
                self.session_clicks += clicks
                self.last_second_clicks.append(time.time())

                # update labels occasionally (reduce UI thrash)
                if self.session_clicks % 10 == 0:
                    try:
                        self.total_label.config(text=str(self.total_clicks))
                        self.session_label.config(text=str(self.session_clicks))
                    except Exception:
                        pass

                interval = max(0.002, 1.0 / (max(0.1, float(self.cps.get()))))
                time.sleep(interval)
            except Exception as e:
                print("Click error:", e)
                time.sleep(0.01)

    def monitor_cps(self):
        while self.is_clicking:
            try:
                now = time.time()
                self.last_second_clicks = [t for t in self.last_second_clicks if now - t <= 1.0]
                self.actual_cps = len(self.last_second_clicks)
                try:
                    self.actual_cps_label.config(text=f"{self.actual_cps:.1f}")
                except Exception:
                    pass
                time.sleep(0.1)
            except Exception:
                time.sleep(0.1)

    def update_timer(self):
        while self.is_clicking:
            try:
                elapsed = int(time.time() - self.start_time)
                minutes = elapsed // 60
                seconds = elapsed % 60
                self.time_label.config(text=f"{minutes:02d}:{seconds:02d}")
                time.sleep(1)
            except Exception:
                time.sleep(1)

    def reset_stats(self):
        if self.is_clicking:
            messagebox.showwarning("Warning", "Stop clicking first")
            return
        if messagebox.askyesno("Confirm", "Reset all statistics?"):
            self.total_clicks = 0
            self.session_clicks = 0
            self.last_second_clicks = []
            self.actual_cps = 0
            try:
                self.total_label.config(text="0")
                self.session_label.config(text="0")
                self.time_label.config(text="00:00")
                self.actual_cps_label.config(text="0.0")
            except Exception:
                pass
            self.status.config(text="Statistics reset")

    def on_closing(self):
        if self.is_clicking:
            if not messagebox.askyesno("Exit", "Clicking is active. Exit anyway?"):
                return
        self.is_clicking = False
        try:
            if keyboard:
                keyboard.unhook_all()
        except Exception:
            pass
        self.root.destroy()

    # -------------------------
    # Responsive adjustments: font scaling on resize
    # -------------------------
    def _on_root_resize_throttled(self):
        # Return a throttled callback to avoid over-calling on resize events
        last = {"t": 0}
        def cb(event=None):
            now = time.time()
            if now - last["t"] < 0.06:
                return
            last["t"] = now
            self._on_root_resize()
        return cb

    def _on_root_resize(self):
        try:
            w = max(720, self.root.winfo_width())
            # scale factor relative to base 960 width
            scale = min(1.45, max(0.8, w / 960.0))
            # adjust fonts
            big = int(28 * scale)
            med = int(12 * scale)
            small = int(9 * scale)

            self.cps_display.config(font=("Segoe UI", max(14,big), "bold"))
            self.actual_cps_label.config(font=("Segoe UI", max(16,int(36*scale)), "bold"))
            self.title_label.config(font=("Segoe UI", max(10,int(16*scale)), "bold"))
            self.subtitle_label.config(font=("Segoe UI", max(8,int(9*scale))))
            # adjust fancy button heights by reconfiguring Canvas height
            for btn in (self.start_btn, self.reset_btn, self.hotkey_btn):
                try:
                    h = max(28, int(34 * scale))
                    btn.config(height=h)
                    btn._height = h
                    btn._radius = max(10, int(14 * scale))
                    btn._draw()
                except Exception:
                    pass
        except Exception:
            pass

# ----------------------------
# Run
# ----------------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = McAllenClicker(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()



