import time
import tkinter as tk
from tkinter import ttk
import pygetwindow as gw


def find_target_window(window_title: str, exact_match: bool = True):
    """Find the target window by title."""
    all_matches = gw.getWindowsWithTitle(window_title)

    for win in all_matches:
        # Skip terminal windows
        if (
            "cmd.exe" in win.title
            or "py.exe" in win.title
            or "PowerShell" in win.title
        ):
            continue

        if exact_match:
            if win.title == window_title:
                return win
        else:
            if window_title.lower() in win.title.lower():
                return win

    return None


def resize_target_window(window_title: str, new_width: int, new_height: int, exact_match: bool = True):
    """Resize the target window and return success flag plus a message."""
    target_win = find_target_window(window_title, exact_match)

    if not target_win:
        return False, f"Could not find an open window matching '{window_title}'."

    try:
        if target_win.isMinimized:
            target_win.restore()
            time.sleep(0.1)

        target_win.resizeTo(new_width, new_height)
        return True, f"{target_win.title} resized to {new_width} x {new_height} pixels."      
    except Exception as e:
        return False, f"Error while resizing window: {e}"


def is_positive_integer(value: str) -> bool:
    return value.isdigit() and int(value) > 0


def set_preset(width: int, height: int):
    width_var.set(str(width))
    height_var.set(str(height))


def on_resize_click():
    window_title = title_var.get().strip()
    width_text = width_var.get().strip()
    height_text = height_var.get().strip()
    exact_match = exact_match_var.get()

    if not window_title:
        status_var.set("Please enter a window title.")
        status_label.config(foreground="#c62828")
        return

    if not is_positive_integer(width_text):
        status_var.set("Please enter a valid positive whole number for width.")
        status_label.config(foreground="#c62828")
        return

    if not is_positive_integer(height_text):
        status_var.set("Please enter a valid positive whole number for height.")
        status_label.config(foreground="#c62828")
        return

    width = int(width_text)
    height = int(height_text)

    success, message = resize_target_window(window_title, width, height, exact_match)

    # Try to bring focus back to this utility after resizing the target window.
    root.after(100, lambda: root.focus_force())
    root.after(120, lambda: root.lift())

    if success:
        status_label.config(foreground="#66ff99")
    else:
        status_label.config(foreground="#ff6666")

    status_var.set(message)


# --------------------------
# GUI Setup
# --------------------------
root = tk.Tk()
root.title("Application Window Resizer")
root.geometry("620x330")
root.resizable(False, False)
root.configure(bg="#050505")

# Font choices
# Verdana looks cleaner than Segoe UI in this small utility window.
label_font = ("Verdana", 9, "bold")
normal_font = ("Verdana", 9)
button_font = ("Verdana", 9, "bold")
header_font = ("Verdana", 12, "bold")

# Colours
bg_colour = "#050505"
panel_colour = "#0d0d0d"
text_colour = "#f2f2f2"
muted_text_colour = "#cfcfcf"
entry_bg = "#111111"
button_bg = "#050505"
button_active_bg = "#1a1a1a"
border_colour = "#ffffff"

style = ttk.Style()
style.theme_use("clam")

style.configure(
    "Dark.TFrame",
    background=bg_colour
)

style.configure(
    "Dark.TLabel",
    background=bg_colour,
    foreground=text_colour,
    font=normal_font
)

style.configure(
    "Bold.Dark.TLabel",
    background=bg_colour,
    foreground=text_colour,
    font=label_font
)

style.configure(
    "Header.Dark.TLabel",
    background=bg_colour,
    foreground=text_colour,
    font=header_font
)

style.configure(
    "Status.Dark.TLabel",
    background=bg_colour,
    foreground=muted_text_colour,
    font=normal_font
)

style.configure(
    "Dark.TCheckbutton",
    background=bg_colour,
    foreground=text_colour,
    font=normal_font,
    focuscolor=bg_colour
)

style.map(
    "Dark.TCheckbutton",
    background=[("active", bg_colour)],
    foreground=[("active", text_colour)]
)

style.configure(
    "Dark.TEntry",
    fieldbackground=entry_bg,
    background=entry_bg,
    foreground=text_colour,
    insertcolor=text_colour,
    bordercolor=border_colour,
    lightcolor=border_colour,
    darkcolor=border_colour,
    padding=6,
    font=normal_font
)

style.configure(
    "Dark.TButton",
    background=button_bg,
    foreground=text_colour,
    bordercolor=border_colour,
    lightcolor=border_colour,
    darkcolor=border_colour,
    focusthickness=0,
    focuscolor=bg_colour,
    font=button_font,
    padding=(10, 6)
)

style.map(
    "Dark.TButton",
    background=[
        ("active", button_active_bg),
        ("pressed", "#000000")
    ],
    foreground=[
        ("active", text_colour),
        ("pressed", text_colour)
    ],
    bordercolor=[
        ("active", border_colour),
        ("pressed", border_colour)
    ]
)

style.configure(
    "Accent.Dark.TButton",
    background=button_bg,
    foreground=text_colour,
    bordercolor=border_colour,
    lightcolor=border_colour,
    darkcolor=border_colour,
    focusthickness=0,
    focuscolor=bg_colour,
    font=("Verdana", 10, "bold"),
    padding=(14, 9)
)

style.map(
    "Accent.Dark.TButton",
    background=[
        ("active", button_active_bg),
        ("pressed", "#000000")
    ],
    foreground=[
        ("active", text_colour),
        ("pressed", text_colour)
    ],
    bordercolor=[
        ("active", border_colour),
        ("pressed", border_colour)
    ]
)

main_frame = ttk.Frame(root, padding=18, style="Dark.TFrame")
main_frame.pack(fill="both", expand=True)

# Variables
title_var = tk.StringVar(value="")
width_var = tk.StringVar(value="1280")
height_var = tk.StringVar(value="720")
exact_match_var = tk.BooleanVar(value=True)
status_var = tk.StringVar(value="")

# Header
header_label = ttk.Label(
    main_frame,
    text="Resize any open application window",
    style="Header.Dark.TLabel"
)
header_label.grid(row=0, column=0, columnspan=5, sticky="w", pady=(0, 16))

# Window title
ttk.Label(
    main_frame,
    text="Window Title",
    style="Bold.Dark.TLabel"
).grid(row=1, column=0, sticky="w", pady=(0, 8))

title_entry = ttk.Entry(
    main_frame,
    textvariable=title_var,
    width=46,
    style="Dark.TEntry"
)
title_entry.grid(row=1, column=1, columnspan=4, sticky="ew", pady=(0, 8))

# Width
ttk.Label(
    main_frame,
    text="Width",
    style="Bold.Dark.TLabel"
).grid(row=2, column=0, sticky="w", pady=(0, 8))

width_entry = ttk.Entry(
    main_frame,
    textvariable=width_var,
    width=16,
    style="Dark.TEntry"
)
width_entry.grid(row=2, column=1, sticky="w", pady=(0, 8))

# Height
ttk.Label(
    main_frame,
    text="Height",
    style="Bold.Dark.TLabel"
).grid(row=3, column=0, sticky="w", pady=(0, 8))

height_entry = ttk.Entry(
    main_frame,
    textvariable=height_var,
    width=16,
    style="Dark.TEntry"
)
height_entry.grid(row=3, column=1, sticky="w", pady=(0, 8))

# Exact match checkbox
exact_checkbox = ttk.Checkbutton(
    main_frame,
    text="Exact match only",
    variable=exact_match_var,
    style="Dark.TCheckbutton"
)
exact_checkbox.grid(row=4, column=0, columnspan=5, sticky="w", pady=(4, 14))

# Presets label
ttk.Label(
    main_frame,
    text="Quick Presets",
    style="Bold.Dark.TLabel"
).grid(row=5, column=0, columnspan=5, sticky="w", pady=(0, 8))

# Presets row
preset_frame = ttk.Frame(main_frame, style="Dark.TFrame")
preset_frame.grid(row=6, column=0, columnspan=5, sticky="ew", pady=(0, 18))

preset_buttons = [
    ("1280×720", 1280, 720),
    ("1600×900", 1600, 900),
    ("1920×1080", 1920, 1080),
    ("2560×1440", 2560, 1440),
]

for i, (label, w, h) in enumerate(preset_buttons):
    btn = ttk.Button(
        preset_frame,
        text=label,
        style="Dark.TButton",
        command=lambda w=w, h=h: set_preset(w, h),
        width=13
    )
    btn.grid(
        row=0,
        column=i,
        padx=(0, 10) if i < len(preset_buttons) - 1 else (0, 0),
        sticky="ew"
    )
    preset_frame.columnconfigure(i, weight=1)

# Resize button
resize_button = ttk.Button(
    main_frame,
    text="Resize Window",
    style="Accent.Dark.TButton",
    command=on_resize_click
)
resize_button.grid(row=7, column=0, sticky="w", pady=(0, 0))

# Status, positioned next to the Resize Window button
status_label = ttk.Label(
    main_frame,
    textvariable=status_var,
    wraplength=390,
    style="Status.Dark.TLabel"
)
status_label.grid(row=7, column=1, columnspan=4, sticky="w", padx=(14, 0))

main_frame.columnconfigure(1, weight=1)

root.mainloop()