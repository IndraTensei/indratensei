"""Builds the profile art: art/header.svg and art/loadout.svg.

Same look as indratensei.me: ink, paper, blood red, halftone, kanji.
Fonts are subset from Google Fonts and embedded, icons come from simple-icons,
so the SVGs render the same everywhere GitHub shows them.

    python art/build.py
"""

import base64
import os
import re
import string
import urllib.parse
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130 Safari/537.36"

INK, PAPER, BLOOD = "#0a0a0a", "#eee8db", "#e8262d"

LATIN = string.ascii_letters + string.digits + " .,:;/+×·'&()!?-_%#@"
KANJI = "転生灰装備言絵鋼蔵繋智城能力話声金動"


def get(url):
    return urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": UA}), timeout=30).read()


def font(family, text, axis=""):
    css = get(f"https://fonts.googleapis.com/css2?family={family.replace(' ', '+')}{axis}&text={urllib.parse.quote(text)}").decode()
    url = re.search(r"url\((https://[^)]+)\)", css).group(1)
    return base64.b64encode(get(url)).decode()


def icon(slug):
    svg = get(f"https://cdn.jsdelivr.net/npm/simple-icons@latest/icons/{slug}.svg").decode()
    return re.search(r' d="([^"]+)"', svg).group(1)


def fonts_css(*names):
    table = {
        "D": ("Dela Gothic One", LATIN, ""),
        "S": ("Instrument Serif", LATIN, ":ital@1"),
        "M": ("JetBrains Mono", LATIN, ":wght@500"),
        "I": ("Inter Tight", LATIN, ":wght@500"),
        "K": ("Yuji Boku", KANJI, ""),
    }
    out = []
    for n in names:
        fam, text, axis = table[n]
        out.append(f"@font-face{{font-family:{n};src:url(data:font/woff2;base64,{font(fam, text, axis)}) format('woff2')}}")
    return "".join(out)


HALFTONE = f'<pattern id="dots" width="9" height="9" patternUnits="userSpaceOnUse"><circle cx="4.5" cy="4.5" r="1.25" fill="{PAPER}"/></pattern>'


# ---------------------------------------------------------------- header

def header():
    W, H = 1200, 420
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Indra Tensei. Ash, AI agentic engineer from Navi Mumbai.">
<defs>
<style>{fonts_css("D", "S", "M", "K")}
.d{{font-family:D,Impact,sans-serif}} .s{{font-family:S,Georgia,serif;font-style:italic}} .m{{font-family:M,ui-monospace,monospace;letter-spacing:.22em}} .k{{font-family:K,serif}}
.up{{animation:up .9s cubic-bezier(.16,1,.3,1) backwards}}
.kj{{fill:{BLOOD};stroke:{BLOOD};stroke-width:0;stroke-dasharray:900;animation:draw 2.4s ease-out backwards,ink .8s ease-in backwards}}
.seal{{transform-box:fill-box;transform-origin:center;transform:rotate(-7deg);animation:stamp .5s cubic-bezier(.3,1.6,.5,1) 2.5s backwards}}
@keyframes up{{from{{opacity:0;transform:translateY(14px)}}to{{opacity:1;transform:none}}}}
@keyframes draw{{from{{stroke-dashoffset:900;stroke-width:2}}to{{stroke-dashoffset:0;stroke-width:2}}}}
@keyframes ink{{from{{fill-opacity:0}}to{{fill-opacity:1}}}}
@keyframes stamp{{from{{opacity:0;transform:scale(1.8) rotate(-14deg)}}to{{opacity:1;transform:scale(1) rotate(-7deg)}}}}
</style>
{HALFTONE}
<radialGradient id="fade" cx="83%" cy="48%" r="58%"><stop offset="0" stop-color="#fff"/><stop offset="1" stop-color="#000"/></radialGradient>
<mask id="m"><rect width="{W}" height="{H}" fill="url(#fade)"/></mask>
<radialGradient id="glow" cx="83%" cy="50%" r="40%"><stop offset="0" stop-color="{BLOOD}" stop-opacity=".32"/><stop offset="1" stop-color="{BLOOD}" stop-opacity="0"/></radialGradient>
</defs>
<rect width="{W}" height="{H}" rx="18" fill="{INK}"/>
<rect width="{W}" height="{H}" fill="url(#dots)" opacity=".11" mask="url(#m)"/>
<rect width="{W}" height="{H}" fill="url(#glow)"/>

<g class="k" font-size="176" text-anchor="middle">
  <text class="kj" x="1000" y="196" style="animation-delay:.2s,1.6s">転</text>
  <text class="kj" x="1000" y="380" style="animation-delay:.7s,2.1s">生</text>
</g>
<g class="seal"><rect x="850" y="316" width="62" height="62" rx="9" fill="{BLOOD}"/><rect x="855" y="321" width="52" height="52" rx="6" fill="none" stroke="{INK}" stroke-opacity=".35" stroke-width="1.5"/><text class="k" x="881" y="363" font-size="40" text-anchor="middle" fill="{INK}">灰</text></g>

<text class="m up" x="72" y="84" font-size="15" fill="{PAPER}" fill-opacity=".5" style="animation-delay:.1s">VOL. 2026  ·  NAVI MUMBAI, IN  ·  UTC+5:30</text>
<g class="d up" font-size="108" fill="{PAPER}" style="animation-delay:.25s">
  <text x="66" y="196">INDRA</text>
  <text x="66" y="300">TENSEI<tspan fill="{BLOOD}">.</tspan></text>
</g>
<text class="s up" x="72" y="350" font-size="32" fill="{PAPER}" fill-opacity=".86" style="animation-delay:.55s">Ash. I build AI agents, and the bots people actually live in.</text>
<text class="m up" x="72" y="390" font-size="14" fill="{PAPER}" fill-opacity=".45" style="animation-delay:.75s">AI AGENTIC ENGINEER  /  AGENTS · BOTS · VOICE · WEB</text>
</svg>'''


# ---------------------------------------------------------------- loadout

# counted from the dependency files of all 130 of my own repos (forks left out)
LANGS = [("Python", "python", 51, "bots, CLIs, voice agents"), ("JavaScript", "javascript", 37, "where it started, 2020"), ("TypeScript", "typescript", 25, "every product since")]
GROUPS = [
    ("絵", "FRONTEND", [("React", "react", 22), ("Tailwind", "tailwindcss", 19), ("Next.js", "nextdotjs", 16), ("GSAP", "greensock", 7)]),
    ("鋼", "BACKEND", [("Node.js", "nodedotjs", 50), ("Zod", "zod", 17), ("Express", "express", 11), ("Fastify", "fastify", 6)]),
    ("蔵", "DATA", [("PostgreSQL", "postgresql", 14), ("MongoDB", "mongodb", 12), ("Drizzle", "drizzle", 9), ("Redis", "redis", 5)]),
    ("繋", "BOTS", [("Discord", "discord", 13), ("WhatsApp", "whatsapp", 8), ("FFmpeg", "ffmpeg", 7), ("Puppeteer", "puppeteer", 4)]),
    ("智", "AI", [("OpenRouter", "openrouter", 9), ("Deepgram", None, 6), ("OpenAI", "openai", 5), ("Claude", "claude", 4)]),
    ("城", "SHIP", [("Docker", "docker", 12), ("Vercel", "vercel", 9), ("Actions", "githubactions", 8), ("Oracle Cloud", "oracle", None)]),
]


def glyph(slug, x, y, size, fill):
    if not slug:  # no logo for it in simple-icons: a little waveform
        bars = [0.35, 0.7, 1, 0.55, 0.8]
        w = size / 9
        return "".join(f'<rect x="{x + i * w * 1.9 + 0.5:.1f}" y="{y + size * (1 - h) / 2:.1f}" width="{w:.1f}" height="{size * h:.1f}" rx="{w / 2:.1f}" fill="{fill}"/>' for i, h in enumerate(bars))
    s = size / 24
    return f'<path transform="translate({x} {y}) scale({s:.4f})" d="{icon(slug)}" fill="{fill}"/>'


def loadout():
    W, PAD, GAP = 1200, 40, 22
    cw = (W - 2 * PAD - 2 * GAP) / 3
    top = 236
    ch = 214
    H = top + 2 * ch + GAP + PAD
    out = []

    # title
    out.append(f'<text class="d" x="{PAD}" y="66" font-size="30" fill="{PAPER}">LOADOUT</text>')
    out.append(f'<text class="k" x="{PAD + 206}" y="68" font-size="32" fill="{BLOOD}">装備</text>')
    out.append(f'<text class="m" x="{W - PAD}" y="62" font-size="13" fill="{PAPER}" fill-opacity=".45" text-anchor="end">RANKED BY HOW MANY OF MY 130 REPOS USE IT</text>')
    out.append(f'<line x1="{PAD}" y1="92" x2="{W - PAD}" y2="92" stroke="{PAPER}" stroke-opacity=".12"/>')

    # languages: three wide tiles with a bar each
    lw = (W - 2 * PAD - 2 * GAP) / 3
    top_n = max(n for *_, n, _ in LANGS)
    for i, (name, slug, n, note) in enumerate(LANGS):
        x = PAD + i * (lw + GAP)
        y = 114
        out.append(f'<g class="up" style="animation-delay:{0.1 + i * 0.08:.2f}s">')
        out.append(f'<rect x="{x}" y="{y}" width="{lw}" height="100" rx="12" fill="{PAPER}" fill-opacity=".035" stroke="{PAPER}" stroke-opacity=".1"/>')
        out.append(glyph(slug, x + 22, y + 22, 26, PAPER))
        out.append(f'<text class="d" x="{x + 62}" y="{y + 44}" font-size="22" fill="{PAPER}">{name.upper()}</text>')
        bw = lw - 44
        out.append(f'<rect x="{x + 22}" y="{y + 62}" width="{bw}" height="5" rx="2.5" fill="{PAPER}" fill-opacity=".08"/>')
        out.append(f'<rect class="bar" x="{x + 22}" y="{y + 62}" width="{bw * n / top_n:.1f}" height="5" rx="2.5" fill="{BLOOD}" style="animation-delay:{0.35 + i * 0.1:.2f}s"/>')
        out.append(f'<text class="s" x="{x + 22}" y="{y + 88}" font-size="18" fill="{PAPER}" fill-opacity=".55">{note}</text>')
        out.append(f'<text class="m" x="{x + lw - 22}" y="{y + 87}" font-size="13" fill="{BLOOD}" text-anchor="end">{n} REPOS</text>')
        out.append('</g>')

    # the six kits
    for gi, (kj, label, items) in enumerate(GROUPS):
        col, row = gi % 3, gi // 3
        x = PAD + col * (cw + GAP)
        y = top + row * (ch + GAP)
        out.append(f'<g class="up" style="animation-delay:{0.35 + gi * 0.07:.2f}s">')
        out.append(f'<rect x="{x}" y="{y}" width="{cw}" height="{ch}" rx="12" fill="{PAPER}" fill-opacity=".035" stroke="{PAPER}" stroke-opacity=".1"/>')
        out.append(f'<text class="k" x="{x + 22}" y="{y + 42}" font-size="24" fill="{BLOOD}">{kj}</text>')
        out.append(f'<text class="m" x="{x + 56}" y="{y + 38}" font-size="14" fill="{PAPER}" fill-opacity=".62">{label}</text>')
        out.append(f'<line x1="{x + 22}" y1="{y + 56}" x2="{x + cw - 22}" y2="{y + 56}" stroke="{PAPER}" stroke-opacity=".1"/>')
        for ii, (name, slug, n) in enumerate(items):
            iy = y + 74 + ii * 34
            out.append(glyph(slug, x + 22, iy, 18, PAPER))
            out.append(f'<text class="i" x="{x + 52}" y="{iy + 14}" font-size="18" fill="{PAPER}" fill-opacity=".92">{name}</text>')
            tag = f"×{n}" if n else "PROD"
            out.append(f'<text class="m" x="{x + cw - 22}" y="{iy + 14}" font-size="14" fill="{PAPER}" fill-opacity="{".45" if n else ".7"}" text-anchor="end">{tag}</text>')
        out.append('</g>')

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Loadout: the languages and tools I actually use, ranked by how many of my repos use them.">
<defs>
<style>{fonts_css("D", "S", "M", "I", "K")}
.d{{font-family:D,Impact,sans-serif}} .s{{font-family:S,Georgia,serif;font-style:italic}} .m{{font-family:M,ui-monospace,monospace;letter-spacing:.18em}} .i{{font-family:I,system-ui,sans-serif}} .k{{font-family:K,serif}}
.up{{animation:up .8s cubic-bezier(.16,1,.3,1) backwards}}
.bar{{transform-box:fill-box;transform-origin:left;animation:grow 1.1s cubic-bezier(.16,1,.3,1) backwards}}
@keyframes up{{from{{opacity:0;transform:translateY(12px)}}to{{opacity:1;transform:none}}}}
@keyframes grow{{from{{transform:scaleX(0)}}}}
</style>
{HALFTONE}
<linearGradient id="fade" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#fff"/><stop offset=".55" stop-color="#000"/></linearGradient>
<mask id="m"><rect width="{W}" height="{H}" fill="url(#fade)"/></mask>
</defs>
<rect width="{W}" height="{H}" rx="18" fill="{INK}"/>
<rect width="{W}" height="{H}" fill="url(#dots)" opacity=".07" mask="url(#m)"/>
{chr(10).join(out)}
</svg>'''


# ---------------------------------------------------------------- abilities

# what I can build, like a character sheet. name, how, and a proof tag where there is one
SKILLS = [
    ("智", "AGENTS", "TOOLS · MCP · RAG", None),
    ("話", "BOTS", "WHATSAPP · DISCORD", "2K+ MSGS A DAY"),
    ("声", "VOICE", "PHONE CALLS · HINDI", None),
    ("金", "COMMERCE", "WALLETS · PAYMENTS", "SCALED TO 1K+ USERS"),
    ("動", "WEB", "SITES THAT MOVE", None),
]
# use cases, scrolling like a match ticker
ASK = [
    "A SUPPORT AGENT THAT ANSWERS FROM YOUR DOCS",
    "A WHATSAPP BOT THAT TAKES ORDERS",
    "A PHONE AGENT THAT SPEAKS HINDI",
    "MCP SERVERS FOR YOUR APIS",
    "AN ECONOMY FOR YOUR DISCORD",
    "AGENTS THAT RUN THE BORING OPS",
    "A SITE THAT FEELS ALIVE",
]


def abilities():
    W, PAD, GAP = 1200, 40, 16
    pw = (W - 2 * PAD - 4 * GAP) / 5
    ph = 172
    py = 104
    ty = py + ph + 22
    H = ty + 50 + PAD - 8
    out = []

    out.append(f'<text class="k" x="{PAD}" y="68" font-size="34" fill="{BLOOD}">能力</text>')
    out.append(f'<text class="d" x="{PAD + 80}" y="66" font-size="30" fill="{PAPER}">ABILITIES</text>')
    out.append(f'<text class="m" x="{W - PAD}" y="62" font-size="13" fill="{PAPER}" fill-opacity=".45" text-anchor="end">WHAT I CAN BUILD FOR YOU</text>')
    out.append(f'<line x1="{PAD}" y1="84" x2="{W - PAD}" y2="84" stroke="{PAPER}" stroke-opacity=".12"/>')

    for i, (kj, name, how, proof) in enumerate(SKILLS):
        x = PAD + i * (pw + GAP)
        out.append(f'<g class="up" style="animation-delay:{0.1 + i * 0.09:.2f}s">')
        out.append(f'<clipPath id="c{i}"><rect x="{x}" y="{py}" width="{pw}" height="{ph}" rx="12"/></clipPath>')
        out.append(f'<rect x="{x}" y="{py}" width="{pw}" height="{ph}" rx="12" fill="{PAPER}" fill-opacity=".035" stroke="{PAPER}" stroke-opacity=".1"/>')
        out.append(f'<text class="k" x="{x + pw + 16}" y="{py + ph + 26}" font-size="156" fill="{PAPER}" fill-opacity=".045" text-anchor="end" clip-path="url(#c{i})">{kj}</text>')
        out.append(f'<text class="k" x="{x + 20}" y="{py + 46}" font-size="30" fill="{BLOOD}">{kj}</text>')
        size = 26 if len(name) <= 6 else 22
        out.append(f'<text class="d" x="{x + 20}" y="{py + 92}" font-size="{size}" fill="{PAPER}">{name}</text>')
        out.append(f'<rect class="bar" x="{x + 22}" y="{py + 106}" width="28" height="3" fill="{BLOOD}" style="animation-delay:{0.4 + i * 0.09:.2f}s"/>')
        out.append(f'<text class="m" x="{x + 22}" y="{py + 132}" font-size="11.5" fill="{PAPER}" fill-opacity=".6">{how}</text>')
        if proof:
            out.append(f'<text class="m" x="{x + 22}" y="{py + 153}" font-size="11.5" fill="{BLOOD}">{proof}</text>')
        out.append('</g>')

    # ticker: JetBrains Mono is monospaced, so one loop's width is exact
    fs, ls = 14, 2.5
    adv = fs * 0.6 + ls
    sep = "   ·   "
    loop = sep.join(ASK) + sep
    lw = len(loop) * adv
    spans = "".join(f'<tspan fill="{BLOOD}">·</tspan>' if ch == "·" else ch for ch in loop)
    pill = 156
    out.append(f'<rect x="{PAD}" y="{ty}" width="{W - 2 * PAD}" height="44" rx="10" fill="{BLOOD}" fill-opacity=".09" stroke="{BLOOD}" stroke-opacity=".35"/>')
    out.append(f'<rect x="{PAD}" y="{ty}" width="{pill}" height="44" rx="10" fill="{BLOOD}"/>')
    out.append(f'<rect x="{PAD + pill - 16}" y="{ty}" width="16" height="44" fill="{BLOOD}"/>')
    out.append(f'<text class="d" x="{PAD + pill / 2}" y="{ty + 29}" font-size="15" fill="{INK}" text-anchor="middle">ASK ME FOR</text>')
    out.append(f'<clipPath id="tk"><rect x="{PAD + pill + 12}" y="{ty}" width="{W - 2 * PAD - pill - 24}" height="44"/></clipPath>')
    out.append('<g clip-path="url(#tk)"><g class="tick">')
    for k in range(3):
        out.append(f'<text class="mt" x="{PAD + pill + 20 + k * lw:.1f}" y="{ty + 27}" font-size="{fs}" fill="{PAPER}" fill-opacity=".85" xml:space="preserve">{spans}</text>')
    out.append('</g></g>')

    label = "Abilities: AI agents (tools, MCP, RAG); bots on WhatsApp and Discord, 2,000+ messages a day; voice agents for phone calls in Hindi; commerce backends, scaled to 1,000+ users; websites that move. Ask me for: " + "; ".join(ASK).lower() + "."
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{label}">
<defs>
<style>{fonts_css("D", "M", "K")}
.d{{font-family:D,Impact,sans-serif}} .m{{font-family:M,ui-monospace,monospace;letter-spacing:.16em}} .mt{{font-family:M,ui-monospace,monospace;letter-spacing:{ls}px}} .k{{font-family:K,serif}}
.up{{animation:up .8s cubic-bezier(.16,1,.3,1) backwards}}
.bar{{transform-box:fill-box;transform-origin:left;animation:grow .9s cubic-bezier(.16,1,.3,1) backwards}}
.tick{{animation:tick {lw / 38:.1f}s linear infinite}}
@keyframes up{{from{{opacity:0;transform:translateY(12px)}}to{{opacity:1;transform:none}}}}
@keyframes grow{{from{{transform:scaleX(0)}}}}
@keyframes tick{{to{{transform:translateX(-{lw:.1f}px)}}}}
</style>
{HALFTONE}
<linearGradient id="fade" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#fff"/><stop offset=".6" stop-color="#000"/></linearGradient>
<mask id="m"><rect width="{W}" height="{H}" fill="url(#fade)"/></mask>
</defs>
<rect width="{W}" height="{H}" rx="18" fill="{INK}"/>
<rect width="{W}" height="{H}" fill="url(#dots)" opacity=".07" mask="url(#m)"/>
{chr(10).join(out)}
</svg>"""


if __name__ == "__main__":
    for name, build in (("header.svg", header), ("abilities.svg", abilities), ("loadout.svg", loadout)):
        with open(os.path.join(HERE, name), "w", encoding="utf-8", newline="\n") as f:
            f.write(build())
        print(name, os.path.getsize(os.path.join(HERE, name)) // 1024, "KB")
