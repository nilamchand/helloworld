import sys
import time
import math
import shutil

BANNER = r"""
 ██╗  ██╗███████╗██╗     ██╗      ██████╗     ██╗    ██╗ ██████╗ ██████╗ ██╗     ██████╗
 ██║  ██║██╔════╝██║     ██║     ██╔═══██╗    ██║    ██║██╔═══██╗██╔══██╗██║     ██╔══██╗
 ███████║█████╗  ██║     ██║     ██║   ██║    ██║ █╗ ██║██║   ██║██████╔╝██║     ██║  ██║
 ██╔══██║██╔══╝  ██║     ██║     ██║   ██║    ██║███╗██║██║   ██║██╔══██╗██║     ██║  ██║
 ██║  ██║███████╗███████╗███████╗╚██████╔╝    ╚███╔███╔╝╚██████╔╝██║  ██║███████╗██████╔╝
 ╚═╝  ╚═╝╚══════╝╚══════╝╚══════╝ ╚═════╝      ╚══╝╚══╝  ╚═════╝ ╚═╝  ╚═╝╚══════╝╚═════╝
"""

RESET = "\033[0m"
BOLD = "\033[1m"


def rgb(r, g, b):
    return f"\033[38;2;{r};{g};{b}m"


def rainbow_char(i, total, offset=0.0):
    hue = (i / max(total, 1) + offset) % 1.0
    r = int(127.5 * (math.sin(2 * math.pi * hue) + 1))
    g = int(127.5 * (math.sin(2 * math.pi * hue + 2 * math.pi / 3) + 1))
    b = int(127.5 * (math.sin(2 * math.pi * hue + 4 * math.pi / 3) + 1))
    return rgb(r, g, b)


def paint_rainbow(text, offset=0.0):
    out = []
    total = sum(1 for c in text if c != " " and c != "\n")
    idx = 0
    for ch in text:
        if ch in (" ", "\n"):
            out.append(ch)
        else:
            out.append(rainbow_char(idx, total, offset) + ch)
            idx += 1
    return "".join(out) + RESET


def animate_banner(lines, frames=24, delay=0.06):
    sys.stdout.write("\033[?25l")
    try:
        for f in range(frames):
            sys.stdout.write("\033[H")
            painted = "\n".join(paint_rainbow(line, offset=f / frames) for line in lines)
            sys.stdout.write(painted + "\n")
            sys.stdout.flush()
            time.sleep(delay)
    finally:
        sys.stdout.write("\033[?25h")


def typewriter(text, color="", delay=0.025):
    for ch in text:
        sys.stdout.write(color + ch + RESET)
        sys.stdout.flush()
        time.sleep(delay)
    sys.stdout.write("\n")


def sparkle_line(width):
    chars = "·•✦✧⋆∙"
    line = "".join(chars[(i * 7) % len(chars)] for i in range(width))
    return paint_rainbow(line, offset=time.time() % 1.0)


def main():
    width = shutil.get_terminal_size((80, 24)).columns
    sys.stdout.write("\033[2J\033[H")

    lines = BANNER.strip("\n").splitlines()
    animate_banner(lines, frames=30, delay=0.05)

    print()
    print(sparkle_line(min(width, 92)))
    print()

    typewriter("  > greeting the universe...", color=rgb(120, 200, 255), delay=0.02)
    time.sleep(0.2)
    typewriter('  > message: "Hello, World!"', color=rgb(255, 180, 90), delay=0.02)
    time.sleep(0.2)
    typewriter("  > status: ✓ delivered across all dimensions", color=rgb(120, 255, 160), delay=0.015)
    print()
    print(sparkle_line(min(width, 92)))
    print()

    finale = "  ✨  Hello, World!  ✨"
    print(BOLD + paint_rainbow(finale, offset=0.15) + RESET)
    print()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.stdout.write("\033[?25h" + RESET + "\n")
