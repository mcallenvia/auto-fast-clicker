# ============================================================
#  FastClicker v1.2  —  Developed by McAllen
#  3-Tab UI: Home | Left Macro | Right Macro
#  Independent engines, separate keyboard hooks, no conflicts
#  + Passive Mode  |  TR/EN bilingual
# ============================================================

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import threading
import time
import random

try:
    import pyautogui
    pyautogui.PAUSE = 0
    pyautogui.FAILSAFE = False
    _HAS_PYAUTOGUI = True
except Exception:
    pyautogui = None
    _HAS_PYAUTOGUI = False

try:
    import keyboard
    _HAS_KEYBOARD = True
except Exception:
    keyboard = None
    _HAS_KEYBOARD = False

# ── Palette ───────────────────────────────────────────────
BG      = "#0d0f12"
PANEL   = "#13161b"
CARD    = "#1a1e25"
BORDER  = "#252a33"
ACC_L   = "#4a9eff"
ACC_L_H = "#6eb3ff"
ACC_R   = "#ff7043"
ACC_R_H = "#ff9068"
STOP_L  = "#f44336"
STOP_R  = "#ff9800"
MUTED   = "#5a6478"
FG      = "#dde3ee"
FG_DIM  = "#8a96a8"
GREEN   = "#22dd77"
BTN_N   = "#1e2430"
BTN_N_H = "#2a3345"
TAB_SEL = "#1a1e25"
TAB_NOR = "#0d0f12"
PASSIVE_BG  = "#1a1210"
PASSIVE_ACT = "#ff9800"
PASSIVE_OFF = "#22c55e"

# ── Language ──────────────────────────────────────────────
_LANG = "TR"

STRINGS = {
    "TR": {
        "passive_label":    "PASİF MOD",
        "passive_active":   "AKTİF  ●",
        "passive_inactive": "DEAKTİF  ○",
        "passive_btn_on":   "Deaktif Et",
        "passive_btn_off":  "Aktif Et",
        "passive_desc":     "Bu mod açıkken makronuz tamamen devre dışıdır.\n"
                            "Hotkey tuşuna bassanız bile hiçbir tıklama gerçekleşmez.",
        "set_hotkey":       "Kısayol Ata",
        "press_key":        "Tuşa bas…",
        "start":            "BAŞLAT",
        "stop":             "DURDUR",
        "reset":            "Sıfırla",
        "warn_stop":        "Önce makroyu durdurun!",
        "warn_hotkey":      "Lütfen önce bir kısayol atayın.",
        "ask_exit":         "Bir makro aktif. Yine de çıkılsın mı?",
        "exit_title":       "Çıkış",
        "developed":        "McAllen tarafından geliştirildi",
        "tab_home":         "Ana Sayfa",
        "tab_left":         "Sol Tık",
        "tab_right":        "Sağ Tık",
        "dashboard":        "Kontrol Paneli",
        "dash_sub":         "Her iki makronun canlı özeti",
        "left_macro":       "SOL TIK MAKROSU",
        "right_macro":      "SAG TIK MAKROSU",
        "status_ready":     "FastClicker v1.2  ·  Hazır  ·  Fare düğmeleri engellendi",
        "idle":             "BEKLİYOR",
        "active":           "● AKTİF",
        "no_hotkey":        "Atanmadı",
        "not_set":          "ATANMADI",
    },
    "EN": {
        "passive_label":    "PASSIVE MODE",
        "passive_active":   "ACTIVE  ●",
        "passive_inactive": "INACTIVE  ○",
        "passive_btn_on":   "Deactivate",
        "passive_btn_off":  "Activate",
        "passive_desc":     "When this mode is ON, your macro is completely disabled.\n"
                            "Even if you press the hotkey, no clicks will be performed.",
        "set_hotkey":       "Set Hotkey",
        "press_key":        "Press a key…",
        "start":            "START",
        "stop":             "STOP",
        "reset":            "Reset",
        "warn_stop":        "Stop the macro first!",
        "warn_hotkey":      "Please set a hotkey first.",
        "ask_exit":         "A macro is active. Exit anyway?",
        "exit_title":       "Exit",
        "developed":        "Developed by McAllen",
        "tab_home":         "Home",
        "tab_left":         "Left Click",
        "tab_right":        "Right Click",
        "dashboard":        "Dashboard",
        "dash_sub":         "Live overview of both macros",
        "left_macro":       "LEFT CLICK MACRO",
        "right_macro":      "RIGHT CLICK MACRO",
        "status_ready":     "FastClicker v1.2  ·  Ready  ·  Mouse buttons blocked",
        "idle":             "IDLE",
        "active":           "● ACTIVE",
        "no_hotkey":        "Not assigned",
        "not_set":          "NOT SET",
    },
}

def S(key):
    return STRINGS[_LANG].get(key, key)


# ============================================================
#  FancyButton
# ============================================================
class FancyButton(tk.Canvas):
    def __init__(self, master, text="", command=None,
                 h=34, r=10, bg=BTN_N, fg=FG, hov=BTN_N_H, font=None, **kw):
        super().__init__(master, height=h, highlightthickness=0, bd=0,
                         bg=master.cget("bg"))
        self._t = text; self._cmd = command
        self._bg = bg; self._fg = fg; self._hov = hov
        self._r = r; self._h = h
        self._font = font or ("Segoe UI", 9, "bold")
        self._over = False
        self.bind("<Configure>", lambda e: self._draw())
        self.bind("<Enter>",     lambda e: self._enter())
        self.bind("<Leave>",     lambda e: self._leave())
        self.bind("<Button-1>",  lambda e: self._click())

    def _enter(self): self._over = True;  self._draw()
    def _leave(self): self._over = False; self._draw()

    def _click(self):
        if callable(self._cmd):
            try: self._cmd()
            except Exception as ex: print("btn err:", ex)

    def set_text(self, t): self._t = t; self._draw()
    def set_colors(self, bg=None, fg=None, hov=None):
        if bg  is not None: self._bg  = bg
        if fg  is not None: self._fg  = fg
        if hov is not None: self._hov = hov
        self._draw()

    def _draw(self):
        self.delete("all")
        w = self.winfo_width() or 120
        h = self._h; r = min(self._r, h // 2)
        c = self._hov if self._over else self._bg
        pts = [2+r,2, w-r-2,2, w-2,2, w-2,2+r,
               w-2,h-r-2, w-2,h-2, w-r-2,h-2,
               2+r,h-2, 2,h-2, 2,h-r-2, 2,2+r, 2,2]
        try:    self.create_polygon(pts, smooth=True, fill=c, outline="")
        except: self.create_rectangle(2,2,w-2,h-2, fill=c, outline="")
        self.create_text(w/2, h/2, text=self._t, font=self._font, fill=self._fg)


# ============================================================
#  MacroEngine  — fully independent per side
# ============================================================
class MacroEngine:
    def __init__(self, side="left"):
        self.side           = side
        self.is_clicking    = False
        self.passive_mode   = False      # NEW: when True, all clicks are blocked
        self.cps            = 10.0
        self.click_type     = "single"
        self.mode           = "toggle"
        self.hotkey_name    = "NOT SET"
        self.hotkey_raw     = None
        self.jitter         = False
        self.jitter_r       = 3
        self.burst          = False
        self.burst_n        = 5
        self.burst_pause    = 1.0
        self.sched_delay    = 0
        self.sched_dur      = 0
        self.cpu_opt        = True
        self.session_clicks = 0
        self.total_clicks   = 0
        self.last_sec       = []
        self.actual_cps     = 0.0
        self.start_time     = None
        self._last_toggle   = 0.0
        self._debounce      = 0.35
        self._stop          = threading.Event()
        self._hook          = None
        self.on_state       = None
        self.on_stats       = None
        self.on_burst       = None

    def toggle(self):
        if self.passive_mode: return          # passive mode blocks everything
        now = time.time()
        if now - self._last_toggle < self._debounce: return
        self._last_toggle = now
        if self.is_clicking: self.stop()
        else:                self.start()

    def start(self):
        if self.passive_mode: return
        if self.is_clicking or self.hotkey_name == "NOT SET": return
        self.is_clicking = True
        self._stop.clear()
        self.session_clicks = 0
        self.last_sec = []
        self.start_time = time.time()
        threading.Thread(target=self._run, daemon=True).start()
        threading.Thread(target=self._mon, daemon=True).start()
        if self.on_state: self.on_state()

    def stop(self):
        if not self.is_clicking: return
        self.is_clicking = False
        self._stop.set()
        if self.on_state: self.on_state()

    def reset(self):
        self.session_clicks = 0
        self.total_clicks   = 0
        self.last_sec       = []
        self.actual_cps     = 0.0
        self.start_time     = None

    def elapsed(self):
        if not self.start_time: return "00:00"
        e = int(time.time() - self.start_time) if self.is_clicking else 0
        return f"{e//60:02d}:{e%60:02d}"

    def register_hotkey(self, callback):
        self.unhook()
        if not _HAS_KEYBOARD or not self.hotkey_raw: return
        try:
            self._hook = keyboard.on_press_key(
                self.hotkey_raw, callback, suppress=False)
        except Exception as ex:
            print(f"[{self.side}] hook err:", ex)

    def unhook(self):
        if self._hook is not None:
            try: keyboard.unhook(self._hook)
            except: pass
            self._hook = None

    def _run(self):
        if self.sched_delay > 0:
            t0 = time.perf_counter()
            while time.perf_counter() - t0 < self.sched_delay:
                if not self.is_clicking: return
                time.sleep(0.05)
        if self.sched_dur > 0:
            threading.Thread(target=self._watchdog, daemon=True).start()
        if self.burst: self._burst_loop()
        else:          self._cont_loop()

    def _watchdog(self):
        t0 = time.perf_counter()
        while self.is_clicking:
            if time.perf_counter() - t0 >= self.sched_dur:
                self.stop(); return
            time.sleep(0.05)

    def _cont_loop(self):
        ivl = max(0.002, 1.0 / max(0.1, self.cps))
        while self.is_clicking and not self._stop.is_set():
            try:
                if self.passive_mode: self.stop(); return
                if self.mode == "hold" and _HAS_KEYBOARD and self.hotkey_raw:
                    if not keyboard.is_pressed(self.hotkey_raw):
                        time.sleep(0.002); continue
                t0 = time.perf_counter()
                self._do_click()
                spent = time.perf_counter() - t0
                wait = max(0.0, ivl - spent)
                if self.cpu_opt:
                    if wait > 0.003: time.sleep(wait - 0.002)
                    while time.perf_counter() - t0 < ivl: pass
                else:
                    time.sleep(wait)
            except Exception as ex:
                print(ex); time.sleep(0.01)

    def _burst_loop(self):
        ivl   = max(0.002, 1.0 / max(0.1, self.cps))
        n     = max(1, self.burst_n)
        pause = max(0.05, self.burst_pause)
        while self.is_clicking and not self._stop.is_set():
            for i in range(n):
                if not self.is_clicking: return
                if self.passive_mode: self.stop(); return
                t0 = time.perf_counter()
                self._do_click()
                if self.on_burst: self.on_burst(i+1, n)
                spent = time.perf_counter() - t0
                wait = max(0.0, ivl - spent)
                if self.cpu_opt:
                    if wait > 0.003: time.sleep(wait - 0.002)
                    while time.perf_counter() - t0 < ivl: pass
                else:
                    time.sleep(wait)
            if not self.is_clicking: break
            tp = time.perf_counter()
            while time.perf_counter() - tp < pause:
                if not self.is_clicking: return
                time.sleep(0.02)

    def _do_click(self):
        if self.passive_mode: return
        n = 2 if self.click_type == "double" else 1
        if _HAS_PYAUTOGUI:
            try:
                dx = dy = 0
                if self.jitter:
                    dx = random.randint(-self.jitter_r, self.jitter_r)
                    dy = random.randint(-self.jitter_r, self.jitter_r)
                    pyautogui.moveRel(dx, dy, duration=0)
                pyautogui.mouseDown(button=self.side)
                pyautogui.mouseUp(button=self.side)
                if n == 2:
                    pyautogui.mouseDown(button=self.side)
                    pyautogui.mouseUp(button=self.side)
                if self.jitter:
                    pyautogui.moveRel(-dx, -dy, duration=0)
            except Exception:
                self.stop(); return
        self.session_clicks += n
        self.total_clicks   += n
        self.last_sec.append(time.time())
        if self.on_stats: self.on_stats()

    def _mon(self):
        while self.is_clicking:
            now = time.time()
            self.last_sec = [t for t in self.last_sec if now - t <= 1.0]
            self.actual_cps = float(len(self.last_sec))
            if self.on_stats: self.on_stats()
            time.sleep(0.1)


# ============================================================
#  PassiveModeWidget  — reusable passive mode panel
# ============================================================
class PassiveModeWidget(tk.Frame):
    """
    Shows a passive mode toggle at the top of each MacroPage.
    When passive = True → engine.passive_mode = True, macro blocked.
    """
    def __init__(self, master, engine: MacroEngine, acc_color: str, **kw):
        super().__init__(master, bg=PASSIVE_BG, **kw)
        self._engine = engine
        self._acc    = acc_color
        self._passive = False   # local state mirror

        self._build()

    def _build(self):
        # outer border frame for a subtle card feel
        tk.Frame(self, bg=BORDER, height=1).pack(fill="x")

        inner = tk.Frame(self, bg=PASSIVE_BG)
        inner.pack(fill="x", padx=14, pady=(8, 6))

        # Left: label + status badge
        left = tk.Frame(inner, bg=PASSIVE_BG)
        left.pack(side="left", fill="y")

        lbl_row = tk.Frame(left, bg=PASSIVE_BG)
        lbl_row.pack(anchor="w")
        tk.Label(lbl_row, text=S("passive_label"),
                 font=("Segoe UI", 8, "bold"), bg=PASSIVE_BG, fg=FG_DIM).pack(side="left")

        self._badge = tk.Label(lbl_row, text=f"  {S('passive_inactive')}  ",
                                font=("Segoe UI", 8, "bold"),
                                bg=PASSIVE_OFF, fg="#fff", padx=4, pady=1)
        self._badge.pack(side="left", padx=(10, 0))

        self._desc = tk.Label(left, text=S("passive_desc"),
                               font=("Segoe UI", 7), bg=PASSIVE_BG,
                               fg=MUTED, justify="left", anchor="w")
        self._desc.pack(anchor="w", pady=(4, 0))

        # Right: toggle button
        self._btn = FancyButton(inner, text=S("passive_btn_off"),
                                 command=self._toggle,
                                 h=32, r=8,
                                 bg=BTN_N, fg=FG_DIM, hov=BTN_N_H,
                                 font=("Segoe UI", 8, "bold"))
        self._btn.pack(side="right", padx=(10, 0))

        tk.Frame(self, bg=BORDER, height=1).pack(fill="x")

    def _toggle(self):
        self._passive = not self._passive
        self._engine.passive_mode = self._passive
        if self._passive and self._engine.is_clicking:
            self._engine.stop()
        self._refresh()

    def _refresh(self):
        if self._passive:
            self._badge.config(text=f"  {S('passive_active')}  ",
                                bg=PASSIVE_ACT, fg="#fff")
            self._btn.set_text(S("passive_btn_on"))
            self._btn.set_colors(bg="#7a2a10", fg="#ffb74d", hov="#8a3a20")
        else:
            self._badge.config(text=f"  {S('passive_inactive')}  ",
                                bg=PASSIVE_OFF, fg="#fff")
            self._btn.set_text(S("passive_btn_off"))
            self._btn.set_colors(bg=BTN_N, fg=FG_DIM, hov=BTN_N_H)

    def refresh_lang(self):
        self._desc.config(text=S("passive_desc"))
        self._refresh()


# ============================================================
#  MacroPage  — full settings page for one macro
# ============================================================
class MacroPage(tk.Frame):
    def __init__(self, master, engine: MacroEngine, status_cb=None, **kw):
        super().__init__(master, bg=PANEL, **kw)
        self.engine     = engine
        self._status_cb = status_cb
        self._recording = False
        self._acc       = ACC_L if engine.side == "left" else ACC_R
        self._acc_h     = ACC_L_H if engine.side == "left" else ACC_R_H
        self._stop_col  = STOP_L if engine.side == "left" else STOP_R

        self._cps_v   = tk.DoubleVar(value=10.0)
        self._mode_v  = tk.StringVar(value="toggle")
        self._type_v  = tk.StringVar(value="single")
        self._jit_v   = tk.BooleanVar(value=False)
        self._jitr_v  = tk.IntVar(value=3)
        self._bur_v   = tk.BooleanVar(value=False)
        self._burn_v  = tk.IntVar(value=5)
        self._burp_v  = tk.DoubleVar(value=1.0)
        self._del_v   = tk.IntVar(value=0)
        self._dur_v   = tk.IntVar(value=0)

        self.engine.on_state = lambda: self.after(0, self._sync_state)
        self.engine.on_stats = lambda: self.after(0, self._sync_stats)
        self.engine.on_burst = lambda i,n: self.after(0, lambda: self._sync_burst(i,n))

        self._build()

    def _build(self):
        acc       = self._acc
        side_name = S("left_macro") if self.engine.side == "left" else S("right_macro")

        # ── Top accent bar ──
        tk.Frame(self, bg=acc, height=3).pack(fill="x")

        # ── Passive Mode Widget ──
        self._passive_widget = PassiveModeWidget(self, self.engine, acc)
        self._passive_widget.pack(fill="x")

        # ── Title row ──
        title_row = tk.Frame(self, bg=PANEL)
        title_row.pack(fill="x", padx=14, pady=(10, 6))
        tk.Label(title_row, text="⬤", font=("Segoe UI", 8),
                 bg=PANEL, fg=acc).pack(side="left")
        tk.Label(title_row, text=f"  {side_name}",
                 font=("Segoe UI", 12, "bold"), bg=PANEL, fg=FG).pack(side="left")
        self._hk_badge = tk.Label(title_row,
                                   text=f" {S('not_set')} ",
                                   font=("Segoe UI", 9, "bold"),
                                   bg=MUTED, fg="#fff", padx=8, pady=2)
        self._hk_badge.pack(side="right")

        # ── Big CPS card ──
        cps_card = tk.Frame(self, bg=CARD)
        cps_card.pack(fill="x", padx=10, pady=(0, 8))
        self._cps_live = tk.Label(cps_card, text="0.0",
                                   font=("Segoe UI", 44, "bold"),
                                   bg=CARD, fg=acc)
        self._cps_live.pack(side="left", padx=16, pady=10)
        rc = tk.Frame(cps_card, bg=CARD)
        rc.pack(side="right", padx=16, pady=10, anchor="e")
        tk.Label(rc, text="real-time CPS", font=("Segoe UI", 8),
                 bg=CARD, fg=FG_DIM).pack(anchor="e")
        self._burst_lbl = tk.Label(rc, text="", font=("Segoe UI", 8),
                                    bg=CARD, fg=acc)
        self._burst_lbl.pack(anchor="e", pady=(2, 0))

        # ── Target CPS ──
        cps_row = tk.Frame(self, bg=PANEL)
        cps_row.pack(fill="x", padx=10, pady=(0, 6))
        tk.Label(cps_row, text="TARGET CPS", font=("Segoe UI", 7, "bold"),
                 bg=PANEL, fg=MUTED).pack(anchor="w")
        sl_row = tk.Frame(cps_row, bg=PANEL)
        sl_row.pack(fill="x")
        self._cps_val = tk.Label(sl_row, text="10.0",
                                  font=("Segoe UI", 13, "bold"),
                                  bg=PANEL, fg=FG, width=5)
        self._cps_val.pack(side="left")
        sf = tk.Frame(sl_row, bg=PANEL)
        sf.pack(side="left", fill="x", expand=True, padx=(4, 0))
        self._slider = ttk.Scale(sf, from_=1, to=100,
                                  variable=self._cps_v, orient="horizontal",
                                  command=self._on_cps)
        self._slider.pack(fill="x")

        # Presets
        pf = tk.Frame(self, bg=PANEL)
        pf.pack(fill="x", padx=10, pady=(0, 8))
        for v in [10, 20, 50, 100]:
            FancyButton(pf, text=str(v), command=lambda n=v: self._preset(n),
                        h=24, r=8, bg=CARD, fg=FG_DIM, hov=BTN_N_H,
                        font=("Segoe UI", 8, "bold")).pack(side="left", padx=(0, 4))

        tk.Frame(self, bg=BORDER, height=1).pack(fill="x", padx=10, pady=(0, 8))

        # ── Mode + Type ──
        opt_row = tk.Frame(self, bg=PANEL)
        opt_row.pack(fill="x", padx=10, pady=(0, 8))
        for label, var, opts in [
            ("MODE",       self._mode_v, [("Toggle","toggle"),("Hold","hold")]),
            ("CLICK TYPE", self._type_v, [("Single","single"),("Double","double")]),
        ]:
            f = tk.Frame(opt_row, bg=PANEL)
            f.pack(side="left", expand=True, anchor="w")
            tk.Label(f, text=label, font=("Segoe UI", 7, "bold"),
                     bg=PANEL, fg=MUTED).pack(anchor="w")
            for txt, val in opts:
                tk.Radiobutton(f, text=txt, variable=var, value=val,
                               font=("Segoe UI", 9), bg=PANEL, fg=FG,
                               selectcolor=acc, activebackground=PANEL,
                               highlightthickness=0, bd=0).pack(anchor="w")

        tk.Frame(self, bg=BORDER, height=1).pack(fill="x", padx=10, pady=(0, 8))

        # ── Advanced ──
        adv = tk.Frame(self, bg=PANEL)
        adv.pack(fill="x", padx=10, pady=(0, 6))
        tk.Label(adv, text="ADVANCED", font=("Segoe UI", 7, "bold"),
                 bg=PANEL, fg=MUTED).pack(anchor="w", pady=(0, 4))

        jr = tk.Frame(adv, bg=PANEL)
        jr.pack(fill="x", pady=(0, 3))
        tk.Checkbutton(jr, text="Jitter", variable=self._jit_v,
                       command=self._push, font=("Segoe UI", 9),
                       bg=PANEL, fg=FG, selectcolor=acc,
                       activebackground=PANEL, highlightthickness=0).pack(side="left")
        tk.Label(jr, text="  radius:", font=("Segoe UI", 8),
                 bg=PANEL, fg=FG_DIM).pack(side="left")
        tk.Spinbox(jr, from_=1, to=20, textvariable=self._jitr_v,
                   width=3, font=("Segoe UI", 8), bg=CARD, fg=FG,
                   insertbackground=FG, buttonbackground=CARD, relief="flat",
                   command=self._push).pack(side="left", padx=(3, 2))
        tk.Label(jr, text="px", font=("Segoe UI", 8), bg=PANEL, fg=FG_DIM).pack(side="left")

        br = tk.Frame(adv, bg=PANEL)
        br.pack(fill="x", pady=(0, 3))
        tk.Checkbutton(br, text="Burst", variable=self._bur_v,
                       command=self._push, font=("Segoe UI", 9),
                       bg=PANEL, fg=FG, selectcolor=acc,
                       activebackground=PANEL, highlightthickness=0).pack(side="left")
        tk.Label(br, text="  N:", font=("Segoe UI", 8),
                 bg=PANEL, fg=FG_DIM).pack(side="left")
        tk.Spinbox(br, from_=2, to=50, textvariable=self._burn_v,
                   width=3, font=("Segoe UI", 8), bg=CARD, fg=FG,
                   insertbackground=FG, buttonbackground=CARD, relief="flat",
                   command=self._push).pack(side="left", padx=(3, 0))
        tk.Label(br, text="  pause:", font=("Segoe UI", 8),
                 bg=PANEL, fg=FG_DIM).pack(side="left")
        tk.Spinbox(br, from_=0.1, to=60, increment=0.1, textvariable=self._burp_v,
                   width=4, font=("Segoe UI", 8), bg=CARD, fg=FG,
                   insertbackground=FG, buttonbackground=CARD, relief="flat",
                   command=self._push).pack(side="left", padx=(3, 2))
        tk.Label(br, text="s", font=("Segoe UI", 8), bg=PANEL, fg=FG_DIM).pack(side="left")

        sr = tk.Frame(adv, bg=PANEL)
        sr.pack(fill="x")
        tk.Label(sr, text="Start delay:", font=("Segoe UI", 8),
                 bg=PANEL, fg=FG_DIM).pack(side="left")
        tk.Spinbox(sr, from_=0, to=300, textvariable=self._del_v,
                   width=3, font=("Segoe UI", 8), bg=CARD, fg=FG,
                   insertbackground=FG, buttonbackground=CARD, relief="flat",
                   command=self._push).pack(side="left", padx=(3, 0))
        tk.Label(sr, text="s   Stop after:", font=("Segoe UI", 8),
                 bg=PANEL, fg=FG_DIM).pack(side="left")
        tk.Spinbox(sr, from_=0, to=7200, textvariable=self._dur_v,
                   width=4, font=("Segoe UI", 8), bg=CARD, fg=FG,
                   insertbackground=FG, buttonbackground=CARD, relief="flat",
                   command=self._push).pack(side="left", padx=(3, 2))
        tk.Label(sr, text="s  (0=∞)", font=("Segoe UI", 8),
                 bg=PANEL, fg=FG_DIM).pack(side="left")

        tk.Frame(self, bg=BORDER, height=1).pack(fill="x", padx=10, pady=(8, 8))

        # ── Stats ──
        stat_row = tk.Frame(self, bg=PANEL)
        stat_row.pack(fill="x", padx=10, pady=(0, 8))
        for attr, lbl, init in [("_sess_lbl","Session","0"),
                                  ("_total_lbl","Total","0"),
                                  ("_time_lbl","Time","00:00")]:
            box = tk.Frame(stat_row, bg=CARD)
            box.pack(side="left", expand=True, fill="both", padx=(0, 4))
            tk.Label(box, text=lbl, font=("Segoe UI", 7, "bold"),
                     bg=CARD, fg=MUTED).pack(pady=(5, 1))
            l = tk.Label(box, text=init, font=("Segoe UI", 13, "bold"),
                         bg=CARD, fg=FG)
            l.pack(pady=(0, 5))
            setattr(self, attr, l)

        # ── Action buttons ──
        btn_row = tk.Frame(self, bg=PANEL)
        btn_row.pack(fill="x", padx=10, pady=(0, 12))

        self._start_btn = FancyButton(btn_row, text=S("start"),
                                       command=self._toggle,
                                       h=40, r=10, bg=acc, fg="#fff", hov=self._acc_h,
                                       font=("Segoe UI", 11, "bold"))
        self._start_btn.pack(side="left", fill="x", expand=True, padx=(0, 5))

        self._hk_btn = FancyButton(btn_row, text=S("set_hotkey"),
                                    command=self._record_hk,
                                    h=40, r=10, bg=BTN_N, fg=FG_DIM, hov=BTN_N_H,
                                    font=("Segoe UI", 9, "bold"))
        self._hk_btn.pack(side="left", fill="x", expand=True, padx=(0, 5))

        self._reset_btn = FancyButton(btn_row, text="↺",
                                       command=self._reset,
                                       h=40, r=10, bg=BTN_N, fg=MUTED, hov=BTN_N_H,
                                       font=("Segoe UI", 13))
        self._reset_btn.pack(side="left", ipadx=6)

        self._update_start_style()

    # ── Hotkey ────────────────────────────────────────────
    def _record_hk(self):
        if self.engine.is_clicking:
            messagebox.showwarning("", S("warn_stop")); return
        self._recording = True
        self._hk_btn.set_text(S("press_key"))
        self._set_status(S("press_key"))
        self.engine.unhook()

        if not _HAS_KEYBOARD:
            k = simpledialog.askstring("Hotkey", S("set_hotkey"))
            if k: self._finalize_hk(k)
            self._recording = False
            self._hk_btn.set_text(S("set_hotkey")); return

        def _press(ev):
            if not self._recording: return
            name = getattr(ev, "name", None)
            if not name or "mouse" in name.lower(): return
            self._recording = False
            try:
                if hasattr(self, "_tmp_hook") and self._tmp_hook:
                    keyboard.unhook(self._tmp_hook)
                    self._tmp_hook = None
            except: pass
            self._finalize_hk(name)

        self._tmp_hook = keyboard.on_press(_press)

    def _finalize_hk(self, name):
        up = name.upper()
        self.engine.hotkey_name = up
        self.engine.hotkey_raw  = name.lower()
        self._hk_badge.config(text=f"  {up}  ", bg=self._acc, fg="#fff")
        self._hk_btn.set_text(S("set_hotkey"))
        self.engine.register_hotkey(self._kb_fire)
        self._update_start_style()
        self._set_status(f"[{self.engine.side.upper()}] → {up}")

    def _kb_fire(self, ev):
        if "mouse" in getattr(ev, "name", "").lower(): return
        self._push()
        self.engine.toggle()

    # ── Engine ────────────────────────────────────────────
    def _push(self):
        e = self.engine
        e.cps         = max(0.1, self._cps_v.get())
        e.mode        = self._mode_v.get()
        e.click_type  = self._type_v.get()
        e.jitter      = self._jit_v.get()
        e.jitter_r    = max(1, self._jitr_v.get())
        e.burst       = self._bur_v.get()
        e.burst_n     = max(1, self._burn_v.get())
        e.burst_pause = max(0.05, self._burp_v.get())
        e.sched_delay = max(0, self._del_v.get())
        e.sched_dur   = max(0, self._dur_v.get())

    def _toggle(self):
        if self.engine.passive_mode: return
        if self.engine.hotkey_name == "NOT SET":
            messagebox.showinfo("", S("warn_hotkey")); return
        self._push()
        self.engine.toggle()

    def _reset(self):
        if self.engine.is_clicking:
            messagebox.showwarning("", S("warn_stop")); return
        self.engine.reset()
        self._sess_lbl.config(text="0")
        self._total_lbl.config(text="0")
        self._time_lbl.config(text="00:00")
        self._cps_live.config(text="0.0")
        self._burst_lbl.config(text="")

    def _on_cps(self, val):
        try:
            self._cps_val.config(text=f"{float(val):.1f}")
            self.engine.cps = float(val)
        except: pass

    def _preset(self, val):
        self._cps_v.set(val); self._on_cps(val)

    # ── UI sync ───────────────────────────────────────────
    def _sync_state(self):
        if self.engine.is_clicking:
            self._start_btn.set_text("■ " + S("stop"))
            self._start_btn.set_colors(bg=self._stop_col, hov="#ff6767", fg="#fff")
            self.engine.register_hotkey(self._kb_fire)
        else:
            self._start_btn.set_text(S("start"))
            self._start_btn.set_colors(bg=self._acc, hov=self._acc_h, fg="#fff")
            self._cps_live.config(text="0.0")
            self._burst_lbl.config(text="")
            self.engine.register_hotkey(self._kb_fire)
        self._update_start_style()

    def _sync_stats(self):
        try:
            self._sess_lbl.config(text=str(self.engine.session_clicks))
            self._total_lbl.config(text=str(self.engine.total_clicks))
            self._time_lbl.config(text=self.engine.elapsed())
            self._cps_live.config(text=f"{self.engine.actual_cps:.1f}")
        except: pass

    def _sync_burst(self, i, n):
        try:
            bar = "█"*i + "░"*(n-i)
            self._burst_lbl.config(text=f"[{bar}] {i}/{n}")
        except: pass

    def _update_start_style(self):
        if self.engine.hotkey_name == "NOT SET":
            self._start_btn.set_colors(bg=BTN_N, fg=MUTED, hov=BTN_N_H)
        elif not self.engine.is_clicking:
            self._start_btn.set_colors(bg=self._acc, hov=self._acc_h, fg="#fff")

    def _set_status(self, msg):
        if self._status_cb: self._status_cb(msg)

    def stop_if_active(self):
        if self.engine.is_clicking: self.engine.stop()

    def refresh_lang(self):
        self._passive_widget.refresh_lang()
        self._hk_btn.set_text(S("set_hotkey"))
        if not self.engine.is_clicking:
            self._start_btn.set_text(S("start"))


# ============================================================
#  HomePage
# ============================================================
class HomePage(tk.Frame):
    def __init__(self, master, eng_l: MacroEngine, eng_r: MacroEngine, **kw):
        super().__init__(master, bg=PANEL, **kw)
        self._el = eng_l
        self._er = eng_r
        self._build()
        self._tick()

    def _build(self):
        tk.Frame(self, bg=ACC_L, height=3).pack(fill="x")

        tk.Label(self, text=S("dashboard"), font=("Segoe UI", 13, "bold"),
                 bg=PANEL, fg=FG).pack(anchor="w", padx=16, pady=(12, 2))
        tk.Label(self, text=S("dash_sub"), font=("Segoe UI", 9),
                 bg=PANEL, fg=MUTED).pack(anchor="w", padx=16, pady=(0, 14))

        cards = tk.Frame(self, bg=PANEL)
        cards.pack(fill="x", padx=10, pady=(0, 12))
        self._card_l = self._make_card(cards, S("left_macro"),  ACC_L)
        self._card_l.pack(side="left", expand=True, fill="both", padx=(0, 6))
        self._card_r = self._make_card(cards, S("right_macro"), ACC_R)
        self._card_r.pack(side="left", expand=True, fill="both")

        tk.Frame(self, bg=BORDER, height=1).pack(fill="x", padx=10, pady=(4, 14))

        info = tk.Frame(self, bg=PANEL)
        info.pack(fill="x", padx=14)
        rows = [
            ("Left hotkey",       lambda: self._el.hotkey_name),
            ("Right hotkey",      lambda: self._er.hotkey_name),
            ("Left total clicks", lambda: str(self._el.total_clicks)),
            ("Right total clicks",lambda: str(self._er.total_clicks)),
            ("Left target CPS",   lambda: f"{self._el.cps:.1f}"),
            ("Right target CPS",  lambda: f"{self._er.cps:.1f}"),
            ("Left passive mode", lambda: (S("passive_active") if self._el.passive_mode else S("passive_inactive"))),
            ("Right passive mode",lambda: (S("passive_active") if self._er.passive_mode else S("passive_inactive"))),
        ]
        self._info_vals = []
        for i, (label, fn) in enumerate(rows):
            row_f = tk.Frame(info, bg=CARD if i%2==0 else PANEL)
            row_f.pack(fill="x", pady=1)
            tk.Label(row_f, text=label, font=("Segoe UI", 9),
                     bg=row_f.cget("bg"), fg=FG_DIM, width=22, anchor="w").pack(side="left", padx=10, pady=5)
            val_lbl = tk.Label(row_f, text="—", font=("Segoe UI", 9, "bold"),
                               bg=row_f.cget("bg"), fg=FG, anchor="w")
            val_lbl.pack(side="left", padx=6)
            self._info_vals.append((val_lbl, fn))

        tk.Frame(self, bg=BORDER, height=1).pack(fill="x", padx=10, pady=(14, 10))

        leg = tk.Frame(self, bg=PANEL)
        leg.pack(fill="x", padx=14, pady=(0, 10))
        tk.Label(leg, text="FEATURES", font=("Segoe UI", 7, "bold"),
                 bg=PANEL, fg=MUTED).pack(anchor="w", pady=(0, 4))
        features = [
            ("", "Humanized Jitter",  "Random micro mouse offsets per click"),
            ("", "CPU Optimization",  "perf_counter adaptive sleep"),
            ("", "Click Burst Mode",  "N clicks then pause, repeating"),
            ("", "Macro Scheduling",  "Start delay + auto-stop"),
            ("", "Passive Mode",      "Instantly disable a macro without unhooking"),
            ("", "Mouse Safety",      "Mouse buttons cannot trigger macros"),
            ("", "Debounce 350ms",    "Prevents accidental double-fire"),
        ]
        for icon, name, desc in features:
            rf = tk.Frame(leg, bg=PANEL)
            rf.pack(fill="x", pady=1)
            tk.Label(rf, text=f"{icon} {name}", font=("Segoe UI", 8, "bold"),
                     bg=PANEL, fg=FG, width=22, anchor="w").pack(side="left")
            tk.Label(rf, text=desc, font=("Segoe UI", 8),
                     bg=PANEL, fg=FG_DIM, anchor="w").pack(side="left")

    def _make_card(self, parent, title, acc):
        f = tk.Frame(parent, bg=CARD)
        tk.Frame(f, bg=acc, height=2).pack(fill="x")
        tk.Label(f, text=title, font=("Segoe UI", 8, "bold"),
                 bg=CARD, fg=acc).pack(pady=(8, 2))
        cps_lbl = tk.Label(f, text="0.0", font=("Segoe UI", 32, "bold"),
                            bg=CARD, fg=acc)
        cps_lbl.pack()
        tk.Label(f, text="CPS", font=("Segoe UI", 7), bg=CARD, fg=MUTED).pack()
        status_lbl = tk.Label(f, text=S("idle"), font=("Segoe UI", 9, "bold"),
                               bg=CARD, fg=MUTED, pady=6)
        status_lbl.pack()
        hk_lbl = tk.Label(f, text=S("no_hotkey"), font=("Segoe UI", 8),
                           bg=CARD, fg=FG_DIM)
        hk_lbl.pack(pady=(0, 10))
        f._cps = cps_lbl; f._status = status_lbl; f._hk = hk_lbl; f._acc = acc
        return f

    def _tick(self):
        try: self._update()
        except: pass
        self.after(180, self._tick)

    def _update(self):
        for card, eng in [(self._card_l, self._el), (self._card_r, self._er)]:
            card._cps.config(text=f"{eng.actual_cps:.1f}" if eng.is_clicking else "0.0")
            if eng.passive_mode:
                card._status.config(text=S("passive_active"), fg=PASSIVE_ACT)
            elif eng.is_clicking:
                card._status.config(text=S("active"), fg=card._acc)
            else:
                card._status.config(text=S("idle"), fg=MUTED)
            card._hk.config(text=eng.hotkey_name if eng.hotkey_name != "NOT SET" else S("no_hotkey"))
        for lbl, fn in self._info_vals:
            lbl.config(text=fn())


# ============================================================
#  TabBar
# ============================================================
class TabBar(tk.Frame):
    def __init__(self, master, tabs, on_select, **kw):
        super().__init__(master, bg=BG, **kw)
        self._on_select = on_select
        self._btns      = []
        self._selected  = 0
        for i, (icon, label) in enumerate(tabs):
            self._add(i, icon, label)
        self._select(0, notify=False)

    def _add(self, idx, icon, label):
        f = tk.Frame(self, bg=BG, cursor="hand2")
        f.pack(side="left")
        inner = tk.Frame(f, bg=TAB_NOR)
        inner.pack(fill="both", expand=True, padx=(0, 1))
        lbl = tk.Label(inner, text=f"{icon}  {label}",
                       font=("Segoe UI", 10, "bold"),
                       bg=TAB_NOR, fg=MUTED, padx=20, pady=12, cursor="hand2")
        lbl.pack()
        bar = tk.Frame(inner, bg=TAB_NOR, height=3)
        bar.pack(fill="x")
        for w in (f, inner, lbl):
            w.bind("<Button-1>", lambda e, i=idx: self._select(i))
            w.bind("<Enter>",    lambda e, l=lbl: l.config(fg=FG))
            w.bind("<Leave>",    lambda e, l=lbl, i=idx: l.config(
                fg=FG if i == self._selected else MUTED))
        self._btns.append((inner, lbl, bar))

    def _select(self, idx, notify=True):
        self._selected = idx
        for i, (inner, lbl, bar) in enumerate(self._btns):
            sel = (i == idx)
            bg_use = TAB_SEL if sel else TAB_NOR
            inner.config(bg=bg_use); lbl.config(bg=bg_use, fg=FG if sel else MUTED)
            bar.config(bg=(ACC_L if idx <= 1 else ACC_R) if sel else TAB_NOR)
        if notify and self._on_select:
            self._on_select(idx)


# ============================================================
#  Main Window
# ============================================================
class McAllenClicker:
    def __init__(self, root):
        self.root = root
        self.root.title("FastClicker v1.2")
        # Larger default window — not too big, just comfortable
        self.root.geometry("680x820")
        self.root.minsize(600, 700)
        self.root.configure(bg=BG)

        self.eng_l = MacroEngine("left")
        self.eng_r = MacroEngine("right")
        self._lang_tr = True

        self._build()

    def _build(self):
        # ── Header ──
        hdr = tk.Frame(self.root, bg="#0b0d10", height=58)
        hdr.pack(fill="x"); hdr.pack_propagate(False)

        lf = tk.Frame(hdr, bg="#0b0d10")
        lf.pack(side="left", padx=18, pady=8)
        tk.Label(lf, text="FastClicker", font=("Segoe UI", 17, "bold"),
                 fg=FG, bg="#0b0d10").pack(anchor="w")
        self._sub_lbl = tk.Label(lf, text=S("developed"),
                                  font=("Segoe UI", 8), fg=MUTED, bg="#0b0d10")
        self._sub_lbl.pack(anchor="w")

        rf = tk.Frame(hdr, bg="#0b0d10")
        rf.pack(side="right", padx=16, pady=10)

        self._lang_btn = FancyButton(rf, text="🌐 EN", command=self._toggle_lang,
                                      h=26, r=7, bg=BTN_N, fg=FG_DIM, hov=BTN_N_H,
                                      font=("Segoe UI", 8, "bold"))
        self._lang_btn.pack(side="right", padx=(8, 0))

        tk.Label(rf, text="v1.2", font=("Segoe UI", 13, "bold"),
                 fg=GREEN, bg="#0b0d10").pack(side="right")

        # ── Tab bar ──
        self._tabbar = TabBar(
            self.root,
            tabs=[("⌂", S("tab_home")), ("◀", S("tab_left")), ("▶", S("tab_right"))],
            on_select=self._switch_tab,
        )
        self._tabbar.pack(fill="x")
        tk.Frame(self.root, bg=BORDER, height=1).pack(fill="x")

        # ── Pages ──
        self._container = tk.Frame(self.root, bg=PANEL)
        self._container.pack(fill="both", expand=True)

        self._page_home  = HomePage(self._container, self.eng_l, self.eng_r)
        self._page_left  = MacroPage(self._container, self.eng_l, self._set_status)
        self._page_right = MacroPage(self._container, self.eng_r, self._set_status)

        self._pages  = [self._page_home, self._page_left, self._page_right]
        self._current = 0
        self._page_home.pack(fill="both", expand=True)

        # ── Status bar ──
        self._status_lbl = tk.Label(
            self.root, text=S("status_ready"),
            anchor="w", font=("Segoe UI", 8),
            bg="#0b0d10", fg=MUTED)
        self._status_lbl.pack(side="bottom", fill="x", padx=10, pady=2)

    def _toggle_lang(self):
        global _LANG
        self._lang_tr = not self._lang_tr
        _LANG = "TR" if self._lang_tr else "EN"
        self._lang_btn.set_text("🌐 EN" if self._lang_tr else "🌐 TR")
        self._sub_lbl.config(text=S("developed"))
        self._status_lbl.config(text=S("status_ready"))
        for p in (self._page_left, self._page_right):
            p.refresh_lang()

    def _switch_tab(self, idx):
        self._pages[self._current].pack_forget()
        self._current = idx
        self._pages[idx].pack(fill="both", expand=True)

    def _set_status(self, msg):
        try: self._status_lbl.config(text=msg)
        except: pass

    def on_closing(self):
        if self.eng_l.is_clicking or self.eng_r.is_clicking:
            if not messagebox.askyesno(S("exit_title"), S("ask_exit")): return
        self.eng_l.stop(); self.eng_l.unhook()
        self.eng_r.stop(); self.eng_r.unhook()
        self.root.destroy()


# ── Entry point ───────────────────────────────────────────────
if __name__ == "__main__":
    root = tk.Tk()
    app  = McAllenClicker(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()

