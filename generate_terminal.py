"""Generates an animated terminal GIF for the profile README.

Scenes:
  1. ssh into github
  2. neofetch with ASCII banner + live GitHub stats
  3. dynamic top-language skill bars (pulled from real repo data)
  4. status outro with resting prompt

Requires: pip install github-readme-terminal  (GITHUB_TOKEN env var must be set)
"""

import gifos

USER = "IndraTensei"

# ---- dracula-flavored 4-bit ANSI palette ----
R = "\x1b[0m"
B = "\x1b[1m"
PURPLE = "\x1b[95m"
CYAN = "\x1b[96m"
GREEN = "\x1b[92m"
YELLOW = "\x1b[93m"
GRAY = "\x1b[90m"

PROMPT = f"{GREEN}indra{GRAY}@{PURPLE}github{GRAY}:{CYAN}~{R}$ "

# figlet-style banner assembled per-glyph so it provably spells "IndraTensei"
GLYPHS = {
    "I": [" ___ ", "|_ _|", " | | ", " | | ", "|___|"],
    "n": ["       ", " _ __  ", "| '_ \\ ", "| | | |", "|_| |_|"],
    "d": ["     _ ", "  __| |", " / _` |", "| (_| |", " \\__,_|"],
    "r": ["      ", " _ __ ", "| '__|", "| |   ", "|_|   "],
    "a": ["       ", "  __ _ ", " / _` |", "| (_| |", " \\__,_|"],
    "T": [" _____ ", "|_   _|", "  | |  ", "  | |  ", "  |_|  "],
    "e": ["      ", "  ___ ", " / _ \\", "|  __/", " \\___|"],
    "s": ["     ", " ___ ", "/ __|", "\\__ \\", "|___/"],
    "i": [" _ ", "(_)", "| |", "| |", "|_|"],
}
ART = ["  " + "".join(GLYPHS[ch][row] for ch in "IndraTensei") for row in range(5)]

t = gifos.Terminal(width=900, height=720, xpad=20, ypad=20)

# ---- fetch live stats, but never fail the build ----
try:
    stats = gifos.utils.fetch_github_stats(user_name=USER)
except Exception:
    stats = None


def stat(attr, default="-"):
    val = getattr(stats, attr, None) if stats else None
    return default if val in (None, "") else val


def top_langs(n=5):
    fallback = [
        ("Python", 40.0),
        ("TypeScript", 25.0),
        ("JavaScript", 15.0),
        ("C++", 12.0),
        ("Go", 8.0),
    ]
    excluded = {"php"}  # side-project noise, keep it out of the top langs
    raw = getattr(stats, "languages_sorted", None) if stats else None
    if not raw:
        return fallback
    out = []
    for item in raw:
        try:
            name, pct = str(item[0]), float(item[1])
        except Exception:
            continue
        if name.lower() in excluded:
            continue
        out.append((name, pct))
        if len(out) == n:
            break
    return out or fallback


def cmd(row, text, pause=8):
    """Render prompt, then type the command keystroke-by-keystroke."""
    t.gen_text(PROMPT, row, contin=True)
    t.gen_typing_text(text, row, contin=True)
    t.clone_frame(pause)


def line(row, text):
    t.gen_text(text, row, contin=True)


# ---- opening pause ----
t.gen_text("", 1, count=10)

# ---- scene 1: connect ----
cmd(1, "ssh indratensei@github.com")
line(2, f"  {GREEN}[ok]{R} connection established {GRAY}(auth: ed25519){R}")
t.clone_frame(6)

# ---- scene 2: neofetch ----
cmd(4, "neofetch")
for i, art_line in enumerate(ART):
    line(6 + i, f"{PURPLE}{art_line}{R}")
line(12, f"  {B}{PURPLE}indratensei{R}{GRAY}@{R}{B}{CYAN}github{R}")
line(13, f"  {GRAY}{'-' * 47}{R}")

info = [
    ("OS", "Ubuntu 24.04 LTS x86_64"),
    ("Shell", "zsh + tmux + neovim"),
    ("Location", "Mumbai, India (UTC+5:30)"),
    ("Focus", "Full-Stack / DevOps / Cloud / AI"),
    ("Followers", str(stat("total_followers"))),
    ("Stars", str(stat("total_stargazers"))),
    ("Commits", str(stat("total_commits_all_time"))),
    ("PRs Merged", str(stat("total_pull_requests_merged"))),
]
for i, (key, val) in enumerate(info):
    line(14 + i, f"  {CYAN}{key:<12}{R}{val}")
t.clone_frame(15)

# ---- scene 3: dynamic skill bars ----
cmd(24, "./skills --top 5")
langs = top_langs()
max_pct = max(pct for _, pct in langs) or 1.0
BAR_WIDTH = 20
for i, (name, pct) in enumerate(langs):
    filled = max(1, round(pct / max_pct * BAR_WIDTH))
    bar = f"{PURPLE}{'#' * filled}{GRAY}{'-' * (BAR_WIDTH - filled)}{R}"
    line(25 + i, f"  {YELLOW}{name[:12]:<14}{R}[{bar}] {pct:.1f}%")
t.clone_frame(12)

# ---- scene 4: status outro ----
cmd(31, "echo $STATUS")
line(32, f"  {GREEN}* online{R} {GRAY}--{R} building, shipping, repeating")
t.clone_frame(10)

# ---- resting prompt ----
line(34, PROMPT)
t.clone_frame(40)

t.gen_gif()

# ---- locate the generated gif and move it into the repo root ----
# newer gifos versions write output to the OS temp dir instead of cwd
import glob
import os
import shutil
import tempfile

candidates = []
for base in (os.getcwd(), tempfile.gettempdir()):
    candidates += glob.glob(os.path.join(base, "output.gif"))
    candidates += glob.glob(os.path.join(base, "**", "output.gif"), recursive=True)

candidates = [c for c in candidates if os.path.isfile(c)]
if not candidates:
    raise SystemExit("ERROR: output.gif not found in cwd or temp dir")

newest = max(set(candidates), key=os.path.getmtime)
shutil.move(newest, os.path.join(os.getcwd(), "terminal.gif"))
print(f"terminal gif generated: moved {newest} -> terminal.gif")
