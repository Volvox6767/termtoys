#!/usr/bin/env python3
"""
termtoys - 6 tiny terminal toys in one file. Offline, zero dependencies.

EN: Matrix rain, fire, starfield, Conway's Life, marquee and a DVD-logo
    bouncer - all in your terminal, one Python file, no installs.
TR: Terminalde Matrix yagmuru, ates, yildiz alani, Yasam Oyunu, kayan yazi
    ve DVD logosu - tek Python dosyasi, kurulum gerektirmez.

by Ahmet Gedik - instagram.com/ahmetgedik67
"""

import argparse
import os
import random
import shutil
import sys
import time

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

AUTHOR = "Ahmet Gedik"
INSTAGRAM = "instagram.com/ahmetgedik67"
VERSION = "1.0.0"

TEST_FRAMES = int(os.environ.get("TERMTOYS_FRAMES", "0") or 0)

CLEAR = "\x1b[2J\x1b[H"
HIDE_CURSOR = "\x1b[?25l"
SHOW_CURSOR = "\x1b[?25h"


def enable_vt():
    """Windows 10+ konsolunda ANSI escape kodlarini ac."""
    if os.name == "nt":
        try:
            import ctypes
            kernel32 = ctypes.windll.kernel32
            kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
        except Exception:
            pass
    os.system("")  # yaygin ANSI acma hilesi


def term_size():
    cols, lines = shutil.get_terminal_size((80, 24))
    return max(20, cols - 1), max(10, lines - 1)


def run_animation(frame_fn, fps=18):
    enable_vt()
    sys.stdout.write(HIDE_CURSOR)
    frames = 0
    try:
        while True:
            w, h = term_size()
            art = frame_fn(w, h)
            sys.stdout.write(CLEAR + art + "\x1b[0m")
            sys.stdout.flush()
            frames += 1
            if TEST_FRAMES and frames >= TEST_FRAMES:
                break
            time.sleep(1.0 / fps)
    except KeyboardInterrupt:
        pass
    finally:
        sys.stdout.write("\n" + SHOW_CURSOR + "\x1b[0m")
        sys.stdout.flush()


# ---------------------------------------------------------------- matrix ----
def toy_matrix():
    chars = "01<>+*-=:.|"
    state = {}

    def frame(w, h):
        drops = state.setdefault("drops", {})
        # her kolonun kafasi: rastgele yeniden dogar
        for x in range(w):
            if x not in drops and random.random() < 0.35:
                drops[x] = random.randint(-h, 0)
        canvas = [[" "] * w for _ in range(h)]
        colors = {}
        for x in list(drops):
            y = drops[x]
            if y - 8 > h or y > h + 20:
                del drops[x]
                continue
            if 0 <= y < h:
                canvas[y][x] = random.choice(chars)
                colors[(y, x)] = "\x1b[1;97m"          # parlak beyaz kafa
            for dy in range(1, 8):
                ty = y - dy
                if 0 <= ty < h:
                    canvas[ty][x] = random.choice(chars)
                    colors[(ty, x)] = ("\x1b[92m" if dy < 3 else
                                       "\x1b[32m" if dy < 6 else "\x1b[2;32m")
            drops[x] = y + 1
        rows = []
        for y in range(h):
            row = []
            for x in range(w):
                col = colors.get((y, x), "")
                ch = canvas[y][x]
                row.append(col + ch if col else ch)
            rows.append("".join(row) + "\x1b[0m")
        return "\n".join(rows)

    return frame


# ------------------------------------------------------------------ fire ----
def toy_fire():
    palette = ["\x1b[48;5;16m ", "\x1b[48;5;52m ", "\x1b[48;5;88m ",
               "\x1b[48;5;124m", "\x1b[48;5;160m ", "\x1b[48;5;202m ",
               "\x1b[48;5;208m ", "\x1b[48;5;214m ", "\x1b[48;5;220m ",
               "\x1b[48;5;226m ", "\x1b[48;5;231m "]
    state = {"buf": None}

    def frame(w, h):
        buf = state["buf"]
        if buf is None or len(buf) != w * (h + 1):
            buf = [0] * (w * (h + 1))
            state["buf"] = buf
        # en alt satir = tam isi
        for x in range(w):
            buf[h * w + x] = 10 if random.random() < 0.92 else random.randint(6, 10)
        # yukari dogru yayilim + soguma
        for y in range(h):
            for x in range(w):
                sx = min(w - 1, max(0, x + random.randint(-1, 1)))
                below = buf[(y + 1) * w + sx]
                buf[y * w + x] = max(0, below - random.randint(0, 2))
        rows = []
        for y in range(h):
            rows.append("".join(palette[buf[y * w + x]] for x in range(w)))
        return "\n".join(rows) + "\x1b[0m\n\x1b[2m" + INSTAGRAM + "\x1b[0m"

    return frame


# ----------------------------------------------------------------- star ----
def toy_star():
    state = {"stars": []}

    def frame(w, h):
        stars = state["stars"]
        while len(stars) < 140:
            stars.append([random.uniform(-1, 1), random.uniform(-1, 1),
                          random.uniform(0.05, 1.0)])
        canvas = [[" "] * w for _ in range(h)]
        for s in stars:
            s[2] -= 0.018
            if s[2] <= 0.03:
                s[0] = random.uniform(-1, 1)
                s[1] = random.uniform(-1, 1)
                s[2] = 1.0
            px = int(w / 2 + s[0] / s[2] * w / 2)
            py = int(h / 2 + s[1] / s[2] * h / 2)
            if 0 <= px < w and 0 <= py < h:
                b = 1.0 - s[2]
                ch = (" " if b < 0.25 else "." if b < 0.45 else
                      "+" if b < 0.65 else "*" if b < 0.85 else "@")
                canvas[py][px] = ch
        return "\n".join("".join(r) for r in canvas)

    return frame


# ----------------------------------------------------------------- life ----
def toy_life():
    state = {"grid": None, "gen": 0}

    def seed(w, h):
        g = [[1 if random.random() < 0.16 else 0 for _ in range(w)] for _ in range(h)]
        state["grid"] = g
        state["gen"] = 0

    def step(g, w, h):
        ng = [[0] * w for _ in range(h)]
        for y in range(h):
            up, dn = (y - 1) % h, (y + 1) % h
            for x in range(w):
                lf, rt = (x - 1) % w, (x + 1) % w
                n = (g[up][lf] + g[up][x] + g[up][rt] +
                     g[y][lf] + g[y][rt] +
                     g[dn][lf] + g[dn][x] + g[dn][rt])
                ng[y][x] = 1 if (g[y][x] and n in (2, 3)) or (n == 3) else 0
        return ng

    def frame(w, h):
        g = state["grid"]
        if g is None or len(g) != h or len(g[0]) != w:
            seed(w, h)
            g = state["grid"]
        pop = sum(map(sum, g))
        state["gen"] += 1
        if pop == 0 or state["gen"] > 500:
            seed(w, h)
            g = state["grid"]
            pop = sum(map(sum, g))
        else:
            state["grid"] = step(g, w, h)
        body = "\n".join("".join("\x1b[32m#\x1b[0m" if c else " " for c in row) for row in g)
        return body + "\n\x1b[2m Game of Life — pop " + str(pop) + " — gen " + \
               str(state["gen"]) + " — " + INSTAGRAM + " \x1b[0m"

    return frame


# -------------------------------------------------------------- marquee ----
def toy_marquee(text):
    text = text + "   "
    n = len(text)
    t = 0

    def frame(w, h):
        nonlocal t
        t += 1
        row = max(0, h // 2)
        lines = [" " * w for _ in range(h)]
        out = []
        for x in range(w):
            ch = text[(x + t) % n]
            hue = 16 + ((x * 5 + t * 3) % 216)
            out.append("\x1b[38;5;" + str(hue) + "m" + ch + "\x1b[0m")
        lines[row] = "".join(out)
        lines[min(h - 1, row + 2)] = "\x1b[2m" + INSTAGRAM.center(w)[:w] + "\x1b[0m"
        return "\n".join(lines)

    return frame


# ------------------------------------------------------------------ dvd ----
def toy_dvd(text):
    colors = ["\x1b[91m", "\x1b[92m", "\x1b[93m",
              "\x1b[94m", "\x1b[95m", "\x1b[96m", "\x1b[97m"]
    state = {"x": 2.0, "y": 2.0, "vx": 0.9, "vy": 0.6, "ci": 0}

    def frame(w, h):
        s = state
        tw = len(text)
        s["x"] += s["vx"]
        s["y"] += s["vy"]
        bounced = False
        if s["x"] <= 0 or s["x"] + tw >= w:
            s["vx"] *= -1
            s["x"] = max(0.0, min(w - tw - 0.01, s["x"]))
            bounced = True
        if s["y"] <= 0 or s["y"] >= h - 2:
            s["vy"] *= -1
            s["y"] = max(0.0, min(h - 2, s["y"]))
            bounced = True
        if bounced:
            s["ci"] = (s["ci"] + 1) % len(colors)
        lines = [[" "] * w for _ in range(h)]
        x, y = int(s["x"]), int(s["y"])
        for i, ch in enumerate(text):
            if x + i < w:
                lines[y][x + i] = ch
        body = "\n".join("".join(r) for r in lines)
        return colors[s["ci"]] + body + "\x1b[0m\n\x1b[2m" + INSTAGRAM + "\x1b[0m"

    return frame


# ------------------------------------------------------------------ main ----
TOYS = {
    "matrix": ("Matrix yagmuru / Matrix rain", toy_matrix, False),
    "fire":   ("Ates / Fire", toy_fire, False),
    "star":   ("Yildiz alani / Starfield", toy_star, False),
    "life":   ("Conway'in Yasam Oyunu / Game of Life", toy_life, False),
    "marquee": ("Kayan yazi / Marquee", toy_marquee, True),
    "dvd":    ("DVD logosu / DVD bounce", toy_dvd, True),
}


def main():
    ap = argparse.ArgumentParser(
        prog="termtoys",
        description="6 tiny terminal toys - offline, zero deps. / "
                    "Terminalde 6 minik oyuncak - cevrimdisi, bagimlilik yok.",
        epilog=f"Made with \u2764 by {AUTHOR} - {INSTAGRAM}\nVersion {VERSION} (MIT)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    ap.add_argument("toy", nargs="?",
                    help="matrix | fire | star | life | marquee | dvd (bos birak: menu)")
    ap.add_argument("--text", default=INSTAGRAM,
                    help="marquee/dvd text (default: instagram handle)")
    ap.add_argument("--version", action="version", version=f"termtoys {VERSION}")
    args = ap.parse_args()

    name = (args.toy or "").strip().lower()
    if not name:
        # interaktif menu
        keys = list(TOYS)
        print("\ntermtoys — terminal oyuncak kutusu / terminal toy box\n")
        for i, k in enumerate(keys, 1):
            print(f"  {i}. {TOYS[k][0]}")
        print("")
        try:
            pick = input("seçim / pick [1-6]: ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            print()
            return
        if pick.isdigit() and 1 <= int(pick) <= len(keys):
            name = keys[int(pick) - 1]
        elif pick in TOYS:
            name = pick
        else:
            print("geçersiz seçim / invalid choice")
            return
    if name not in TOYS:
        print("Bilinmeyen oyuncak / unknown toy:", name)
        print("Seçenekler / options:", ", ".join(TOYS))
        sys.exit(1)

    factory = TOYS[name][1]
    takes_text = TOYS[name][2]
    frame = factory(args.text) if takes_text else factory()
    if TEST_FRAMES:
        run_animation(frame)
        print(f"[test] {name}: {TEST_FRAMES} frame OK")
        return
    print("\x1b[2mCtrl+C ile çık / Ctrl+C to exit\x1b[0m")
    run_animation(frame)


if __name__ == "__main__":
    main()
