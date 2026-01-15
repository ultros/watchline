#!/usr/bin/env python3
"""
Terminal:
- masked typing (shows *)
- Enter SUBMITS
- Ctrl+C also SUBMITS (instead of aborting)

GUI:
- thin always-on-top top-centered strip
- width equals text width
- click copies
- Ctrl+C copies only when strip focused
- Esc closes
"""

import argparse
import sys
import os


def parse_args():
    p = argparse.ArgumentParser(description="Terminal-masked input -> top strip banner.")
    p.add_argument("--height", type=int, default=34, help="Strip height in pixels (Firefox title bar-ish).")
    p.add_argument("--padx", type=int, default=18, help="Horizontal padding inside the strip.")
    p.add_argument("--top-offset", type=int, default=0, help="Pixels from top of screen.")
    p.add_argument("--bg", default="#111111", help="Background color (hex).")
    p.add_argument("--fg", default="#EAEAEA", help="Text color (hex).")
    p.add_argument("--border", default="#5A5A5A", help="Bottom border color (hex).")
    p.add_argument("--border-thickness", type=int, default=2, help="Bottom border thickness in pixels.")
    p.add_argument("--font", default="TkDefaultFont", help="Font family name.")
    p.add_argument("--font-size", type=int, default=12, help="Font size.")
    p.add_argument("--opacity", type=float, default=0.98, help="Window opacity 0.2..1.0 (platform-dependent).")
    p.add_argument("--max-width", type=int, default=0, help="Optional max width in pixels (0 = no cap).")
    p.add_argument("--prompt", default="Enter banner text (masked): ", help="Terminal prompt.")
    return p.parse_args()


def masked_input(prompt: str) -> str:
    """
    Read from terminal with '*' echo.

    Behavior:
    - Enter submits
    - Backspace deletes
    - Ctrl+C submits immediately (NOT interrupt)
    """
    # If stdin isn't a real terminal, fall back (can't do per-char masking)
    if not sys.stdin.isatty():
        try:
            import getpass
            return getpass.getpass(prompt)
        except Exception:
            return input(prompt)

    if os.name == "nt":
        import msvcrt
        sys.stdout.write(prompt)
        sys.stdout.flush()
        buf = []
        while True:
            ch = msvcrt.getwch()

            # ENTER submits
            if ch in ("\r", "\n"):
                sys.stdout.write("\n")
                return "".join(buf)

            # CTRL+C submits immediately
            if ch == "\x03":
                sys.stdout.write("\n")
                return "".join(buf)

            # backspace
            if ch in ("\x08", "\x7f"):
                if buf:
                    buf.pop()
                    sys.stdout.write("\b \b")
                    sys.stdout.flush()
                continue

            # ignore special keys
            if ch in ("\x00", "\xe0"):
                _ = msvcrt.getwch()
                continue

            buf.append(ch)
            sys.stdout.write("*")
            sys.stdout.flush()

    else:
        import termios
        import tty

        fd = sys.stdin.fileno()
        old = termios.tcgetattr(fd)
        sys.stdout.write(prompt)
        sys.stdout.flush()
        buf = []

        try:
            tty.setraw(fd)
            while True:
                ch = sys.stdin.read(1)

                # ENTER submits
                if ch in ("\r", "\n"):
                    sys.stdout.write("\n")
                    return "".join(buf)

                # CTRL+C submits immediately
                if ch == "\x03":
                    sys.stdout.write("\n")
                    return "".join(buf)

                # backspace/delete
                if ch in ("\x7f", "\b"):
                    if buf:
                        buf.pop()
                        sys.stdout.write("\b \b")
                        sys.stdout.flush()
                    continue

                # ignore arrow keys / escape sequences
                if ch == "\x1b":
                    # swallow common sequences
                    try:
                        sys.stdin.read(2)
                    except Exception:
                        pass
                    continue

                buf.append(ch)
                sys.stdout.write("*")
                sys.stdout.flush()

        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old)


def show_top_strip(message: str, args):
    import tkinter as tk
    from tkinter import font as tkfont

    root = tk.Tk()
    root.configure(bg=args.bg)

    # borderless + always-on-top
    root.overrideredirect(True)
    root.attributes("-topmost", True)

    try:
        root.attributes("-alpha", max(0.2, min(1.0, args.opacity)))
    except tk.TclError:
        pass

    screen_w = root.winfo_screenwidth()
    h = max(18, args.height)
    y = max(0, args.top_offset)

    frame = tk.Frame(root, bg=args.bg)
    frame.pack(fill="both", expand=True)

    label = tk.Label(
        frame,
        text=message,
        bg=args.bg,
        fg=args.fg,
        font=(args.font, args.font_size),
        anchor="center",
        padx=args.padx
    )
    label.pack(fill="both", expand=True)

    border = tk.Frame(root, bg=args.border, height=max(1, args.border_thickness))
    border.pack(fill="x", side="bottom")

    # measure width to text
    root.update_idletasks()
    f = tkfont.Font(family=args.font, size=args.font_size)
    text_px = f.measure(message)

    w = text_px + (args.padx * 2) + 12  # small fudge
    if args.max_width and args.max_width > 0:
        w = min(w, args.max_width)
    w = max(140, min(w, screen_w))

    x = max(0, (screen_w // 2) - (w // 2))
    root.geometry(f"{w}x{h}+{x}+{y}")

    def flash_confirm():
        frame.configure(bg="#222222")
        label.configure(bg="#222222")
        root.after(120, lambda: (frame.configure(bg=args.bg), label.configure(bg=args.bg)))

    def copy_to_clipboard(_evt=None):
        root.clipboard_clear()
        root.clipboard_append(message)
        root.update()
        flash_confirm()

    def close(_evt=None):
        root.destroy()

    # bindings
    root.bind("<Escape>", close)
    root.bind("<Button-1>", copy_to_clipboard)
    label.bind("<Button-1>", copy_to_clipboard)
    root.bind("<Control-c>", copy_to_clipboard)
    root.bind("<Control-C>", copy_to_clipboard)

    root.mainloop()


def main():
    args = parse_args()
    msg = masked_input(args.prompt)

    if not msg.strip():
        print("Empty message; exiting.")
        sys.exit(0)

    show_top_strip(msg, args)


if __name__ == "__main__":
    main()
