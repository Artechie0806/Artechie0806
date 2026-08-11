#!/usr/bin/env python3
"""A comic page for a GitHub profile README.

Direction
---------
Newsprint, two inks: black line art and one spot red on warm paper. Everything
is hand-inked rather than drafted -- every rect, balloon and circle is a
polyline with a seeded jitter, so nothing has the CAD-perfect edge that makes
generated art read as generated.

The strips aren't decoration. Aryan's own project write-ups are already built as
Problem -> Twist -> Result, so each strip dramatises a true story from his work:
the day job (27B model, one box, quantize, ~150 tok/s) and the asteroid target
leakage he found and published instead of burying.

No webfonts survive inside a GitHub-embedded SVG, so lettering leans on system
faces: Impact for sound effects and logo, Trebuchet caps for balloons.
"""

import math, os, random

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "assets")
os.makedirs(OUT, exist_ok=True)

PAPER = "#F4F0E4"
INK = "#15120F"
RED = "#DE3226"
DISPLAY = "Impact, Haettenschweiler, 'Arial Narrow Bold', 'Franklin Gothic Heavy', sans-serif"
LETTER = "'Trebuchet MS', 'Segoe UI', Tahoma, Verdana, sans-serif"
CODE = "ui-monospace, SFMono-Regular, Menlo, Consolas, monospace"


# ---------------------------------------------------------------- primitives
def esc(s):
    s = s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    return "".join(c if ord(c) < 128 else f"&#{ord(c)};" for c in s)


def wob_rect(x, y, w, h, rng, amp=1.6, step=22):
    pts = []

    def edge(x1, y1, x2, y2):
        d = math.hypot(x2 - x1, y2 - y1)
        n = max(2, int(d / step))
        for i in range(n):
            t = i / n
            pts.append((x1 + (x2 - x1) * t, y1 + (y2 - y1) * t))

    edge(x, y, x + w, y); edge(x + w, y, x + w, y + h)
    edge(x + w, y + h, x, y + h); edge(x, y + h, x, y)
    j = [(px + rng.uniform(-amp, amp), py + rng.uniform(-amp, amp)) for px, py in pts]
    return "M " + " L ".join(f"{a:.1f} {b:.1f}" for a, b in j) + " Z"


def wob_ellipse(cx, cy, rx, ry, rng, amp=2.2, n=34):
    pts = []
    for i in range(n):
        a = 2 * math.pi * i / n
        r = 1 + rng.uniform(-amp, amp) / max(rx, ry)
        pts.append((cx + math.cos(a) * rx * r, cy + math.sin(a) * ry * r))
    return "M " + " L ".join(f"{a:.1f} {b:.1f}" for a, b in pts) + " Z"


def star(cx, cy, r1, r2, spikes, rng, amp=3):
    pts = []
    for i in range(spikes * 2):
        a = math.pi * i / spikes - math.pi / 2
        r = (r1 if i % 2 == 0 else r2) + rng.uniform(-amp, amp)
        pts.append((cx + math.cos(a) * r, cy + math.sin(a) * r))
    return "M " + " L ".join(f"{a:.1f} {b:.1f}" for a, b in pts) + " Z"


PREVIEW = False


def txt(x, y, s, size=13, fam=LETTER, fill=INK, anchor="start", maxw=None,
        weight="bold", ls=0.4, cls="", style="", extra="", force=False):
    est = len(s) * size * 0.58 + max(0, len(s) - 1) * ls
    tl = ""
    if maxw and (force or est > maxw):
        adj = "spacingAndGlyphs" if force or est > maxw * 1.12 else "spacing"
        tl = f' textLength="{maxw:.0f}" lengthAdjust="{adj}"'
        if PREVIEW:            # cairo ignores textLength; approximate the clamp
            size = min(size, maxw / max(1, len(s) * 0.62))
    c = f' class="{cls}"' if cls else ""
    st = f' style="{style}"' if style else ""
    return (f'<text x="{x:.1f}" y="{y:.1f}" font-family="{fam}" font-size="{size}" '
            f'font-weight="{weight}" letter-spacing="{ls}" fill="{fill}" '
            f'text-anchor="{anchor}"{tl}{c}{st} {extra}>{esc(s)}</text>')


def anchored(cx, cy, cls, delay, body):
    """Scale/rotate around (cx,cy) without relying on transform-box."""
    d = f' style="animation-delay:{delay:.2f}s"' if delay else ""
    return (f'<g transform="translate({cx:.1f},{cy:.1f})"><g class="{cls}"{d}>'
            f'<g transform="translate({-cx:.1f},{-cy:.1f})">{body}</g></g></g>')


def balloon(cx, cy, rx, ry, tip, rng, lines, size=13, delay=0.0, fam=LETTER):
    ax, ay = cx + (rx * 0.35 if tip[0] > cx else -rx * 0.35), cy + ry * 0.72
    tail = (f'<path d="M {ax - 13:.1f} {ay:.1f} L {tip[0]:.1f} {tip[1]:.1f} '
            f'L {ax + 13:.1f} {ay:.1f} Z" fill="{PAPER}" stroke="{INK}" '
            f'stroke-width="2.4" stroke-linejoin="round"/>')
    body = (f'<path d="{wob_ellipse(cx, cy, rx, ry, rng)}" fill="{PAPER}" stroke="{INK}" '
            f'stroke-width="2.6" stroke-linejoin="round"/>')
    n = len(lines)
    tx = "".join(txt(cx, cy - (n - 1) * (size * 0.62) + i * size * 1.24 + size * 0.34,
                     l, size=size, anchor="middle", maxw=rx * 1.72, fam=fam) for i, l in enumerate(lines))
    return anchored(cx, cy, "pop", delay, tail + body + tx)


def burst(cx, cy, r1, r2, tip, rng, lines, size=26, delay=0.0, fill=RED):
    """A shout balloon: spiky outline, display type."""
    tail = (f'<path d="M {cx - 15:.0f} {cy + r2 * 0.6:.0f} L {tip[0]:.0f} {tip[1]:.0f} '
            f'L {cx + 15:.0f} {cy + r2 * 0.6:.0f} Z" fill="{PAPER}" stroke="{INK}" '
            f'stroke-width="2.6" stroke-linejoin="round"/>')
    body = (f'<path d="{star(cx, cy, r1, r2, 15, rng, amp=2.4)}" fill="{PAPER}" stroke="{INK}" '
            f'stroke-width="2.8" stroke-linejoin="round"/>')
    n = len(lines)
    tx = "".join(txt(cx, cy - (n - 1) * (size * 0.6) + i * size * 1.1 + size * 0.34, l,
                     size=size, fam=DISPLAY, anchor="middle", fill=fill,
                     maxw=r2 * 1.5, force=True) for i, l in enumerate(lines))
    return anchored(cx, cy, "slam", delay, tail + body + tx)


def receipt(x, y, w, h, rng, teeth=10):
    """Paper receipt with a torn zigzag bottom edge."""
    pts = []
    n = max(2, int(w / 20))
    for i in range(n + 1):
        pts.append((x + w * i / n + rng.uniform(-1.2, 1.2), y + rng.uniform(-1.2, 1.2)))
    pts.append((x + w + rng.uniform(-1, 1), y + h - 10))
    for i in range(teeth * 2 + 1):
        t = 1 - i / (teeth * 2)
        pts.append((x + w * t, y + h - (10 if i % 2 else 0) + rng.uniform(-1, 1)))
    pts.append((x + rng.uniform(-1, 1), y + h - 10))
    return "M " + " L ".join(f"{a:.1f} {b:.1f}" for a, b in pts) + " Z"


def eye(cx, cy, r, rng):
    lid = (f'<path d="M {cx - r} {cy} Q {cx} {cy - r * 0.82} {cx + r} {cy} '
           f'Q {cx} {cy + r * 0.82} {cx - r} {cy} Z" fill="{PAPER}" stroke="{INK}" '
           f'stroke-width="2.6" stroke-linejoin="round"/>')
    pup = f'<circle cx="{cx}" cy="{cy}" r="{r * 0.30:.1f}" fill="{INK}"/>'
    cut = (f'<line x1="{cx - r * 0.95:.0f}" y1="{cy + r * 0.75:.0f}" x2="{cx + r * 0.95:.0f}" '
           f'y2="{cy - r * 0.75:.0f}" stroke="{RED}" stroke-width="3.4" stroke-linecap="round" '
           f'pathLength="1" class="draw" style="animation-delay:1.3s"/>')
    return lid + pup + cut


def caption(x, y, w, lines, rng, size=11.5, delay=0.0, fill=PAPER, ink=INK):
    h = 12 + len(lines) * size * 1.42
    box = (f'<path d="{wob_rect(x, y, w, h, rng, amp=1.2, step=26)}" fill="{fill}" '
           f'stroke="{ink}" stroke-width="2.2" stroke-linejoin="round"/>')
    tx = "".join(txt(x + 9, y + size * 1.32 + i * size * 1.42, l, size=size,
                     fill=ink, maxw=w - 18) for i, l in enumerate(lines))
    cls = f' class="fade" style="animation-delay:{delay:.2f}s"' if delay else ' class="fade"'
    return f'<g{cls}>{box}{tx}</g>', h


def rays(cx, cy, r0, r1, n, rng, stroke=INK, w=2.2, cls="draw", delay=0.0):
    out = []
    for i in range(n):
        a = 2 * math.pi * i / n + rng.uniform(-0.05, 0.05)
        j = rng.uniform(0.82, 1.18)
        out.append(f'<line x1="{cx + math.cos(a) * r0:.1f}" y1="{cy + math.sin(a) * r0:.1f}" '
                   f'x2="{cx + math.cos(a) * r1 * j:.1f}" y2="{cy + math.sin(a) * r1 * j:.1f}" '
                   f'stroke="{stroke}" stroke-width="{w}" stroke-linecap="round" '
                   f'pathLength="1" class="{cls}" style="animation-delay:{delay + i * 0.018:.2f}s"/>')
    return "".join(out)


def sfx(cx, cy, word, rng, size=44, rot=-7, delay=0.0, fill=RED, maxw=None):
    """Sound effect: red fill, heavy ink outline, punched in."""
    f = bool(maxw)
    t = (txt(cx, cy, word, size=size, fam=DISPLAY, anchor="middle", ls=1, maxw=maxw, force=f,
             fill="none", extra=f'stroke="{INK}" stroke-width="7" stroke-linejoin="round"')
         + txt(cx, cy, word, size=size, fam=DISPLAY, anchor="middle", ls=1, fill=fill,
               maxw=maxw, force=f))
    return anchored(cx, cy, "slam", delay,
                    f'<g transform="rotate({rot} {cx} {cy})">{t}</g>')


def css(animated=True):
    if not animated:                      # static bake, for previewing composition
        return """
    .fade,.pop,.slam,.wipe,.rise { opacity: 1; }
    .draw { stroke-dashoffset: 0; }
  """
    return f"""
    .fade {{ opacity: 0; animation: fade .55s ease-out both; }}
    .rise {{ opacity: 0; animation: rise .6s cubic-bezier(.2,.9,.3,1) both; }}
    .pop  {{ opacity: 0; animation: pop .5s cubic-bezier(.24,1.6,.4,1) both; }}
    .slam {{ opacity: 0; animation: slam .42s cubic-bezier(.3,1.4,.5,1) both; }}
    .draw {{ stroke-dasharray: 1; stroke-dashoffset: 1;
             animation: draw .7s cubic-bezier(.2,.8,.3,1) both; }}
    .spin {{ animation: spin 3.4s linear infinite; }}
    .beat {{ animation: beat 2.6s ease-in-out infinite; }}
    .drift{{ animation: drift 3.2s ease-in-out infinite; }}
    .nudgeR{{ animation: nudgeR 2.4s ease-in-out infinite; }}
    .nudgeL{{ animation: nudgeL 2.4s ease-in-out infinite; }}

    @keyframes fade {{ to {{ opacity: 1; }} }}
    @keyframes rise {{ from {{ transform: translateY(10px); }} to {{ opacity: 1; transform: none; }} }}
    @keyframes pop  {{ from {{ transform: scale(.72); }} to {{ opacity: 1; transform: scale(1); }} }}
    @keyframes slam {{ from {{ transform: scale(2.1) rotate(-9deg); }}
                       to   {{ opacity: 1; transform: scale(1) rotate(0); }} }}
    @keyframes draw {{ to {{ stroke-dashoffset: 0; }} }}
    @keyframes spin {{ to {{ transform: rotate(360deg); }} }}
    @keyframes beat {{ 0%,100% {{ transform: scale(1); }} 50% {{ transform: scale(1.035); }} }}
    @keyframes drift{{ 0%,100% {{ transform: translateY(0); }} 50% {{ transform: translateY(-4px); }} }}
    @keyframes nudgeR{{ 0%,100% {{ transform: translateX(0); }} 50% {{ transform: translateX(7px); }} }}
    @keyframes nudgeL{{ 0%,100% {{ transform: translateX(0); }} 50% {{ transform: translateX(-7px); }} }}

    @media (prefers-reduced-motion: reduce) {{
      .fade,.pop,.slam,.rise {{ opacity: 1; animation: none; transform: none; }}
      .draw {{ stroke-dashoffset: 0; animation: none; }}
      .spin,.beat,.drift,.nudgeR,.nudgeL {{ animation: none; }}
    }}
  """


def page(w, h, body, animated=True, label="", defs=""):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}"
     role="img" aria-label="{esc(label)}">
  <defs>
    <pattern id="tone" width="7" height="7" patternUnits="userSpaceOnUse" patternTransform="rotate(30)">
      <circle cx="2" cy="2" r="1.5" fill="{RED}" fill-opacity="0.30"/>
    </pattern>
    <pattern id="tone2" width="6" height="6" patternUnits="userSpaceOnUse" patternTransform="rotate(15)">
      <circle cx="2" cy="2" r="1.15" fill="{INK}" fill-opacity="0.30"/>
    </pattern>
{defs}
  </defs>
  <style>{css(animated)}</style>
{body}
</svg>
'''


# --------------------------------------------------------------------- cover
def build_cover(animated=True):
    rng = random.Random(11)
    W, H = 1000, 300
    b = [f'<rect width="{W}" height="{H}" fill="{PAPER}"/>']

    # halftone wash + speed lines behind the logo
    b.append(f'<g class="fade"><circle cx="866" cy="204" r="98" fill="url(#tone)"/></g>')
    for i in range(13):
        y = 62 + i * 10.5 + rng.uniform(-2, 2)
        x2 = 640 + rng.uniform(0, 120)
        b.append(f'<line x1="{962 - rng.uniform(0,30):.0f}" y1="{y:.0f}" x2="{x2:.0f}" y2="{y:.0f}" '
                 f'stroke="{INK}" stroke-width="{rng.uniform(1.4,3.0):.1f}" stroke-linecap="round" '
                 f'opacity="0.22" pathLength="1" class="draw" style="animation-delay:{i*0.03:.2f}s"/>')

    # frame
    b.append(f'<path d="{wob_rect(9, 9, W-18, H-18, rng, amp=1.9, step=34)}" fill="none" '
             f'stroke="{INK}" stroke-width="4" stroke-linejoin="round" pathLength="1" class="draw"/>')

    # top strapline
    b.append(f'<g class="fade" style="animation-delay:.5s">'
             + txt(30, 42, "THE ONGOING ADVENTURES OF AN AGENT WRANGLER", size=11.5,
                   fill=INK, ls=1.6, maxw=400, force=True) + '</g>')
    b.append(f'<g class="fade" style="animation-delay:.5s">'
             + txt(W-30, 42, "NO. 01  \u00b7  NAVI MUMBAI", size=11.5, anchor="end", ls=1.6, maxw=190, force=True) + '</g>')

    # corner box (portfolio monogram)
    cb = (f'<path d="{wob_rect(30, 62, 92, 92, rng, amp=1.4, step=24)}" fill="{PAPER}" '
          f'stroke="{INK}" stroke-width="3" stroke-linejoin="round"/>'
          + txt(76, 120, "AR.", size=44, fam=DISPLAY, anchor="middle", fill=INK, maxw=58, force=True)
          + f'<line x1="40" y1="130" x2="112" y2="130" stroke="{RED}" stroke-width="3"/>'
          + txt(76, 146, "AI / ML", size=11, anchor="middle", ls=1.4, maxw=76))
    b.append(anchored(76, 108, "pop", 0.25, cb))

    # logo: red offset + solid ink
    logo = (txt(153, 157, "ARYAN RANE", size=76, fam=DISPLAY, fill=RED, ls=1, maxw=452, force=True)
            + txt(148, 152, "ARYAN RANE", size=76, fam=DISPLAY, fill=INK, ls=1, maxw=452, force=True))
    b.append(anchored(148, 130, "pop", 0.12, logo))

    # banner
    ban = (f'<path d="M 142 176 L 700 170 L 704 214 L 146 220 Z" fill="{INK}"/>'
           + txt(166, 205, "AGENTIC LLM SYSTEMS  \u00b7  INFERENCE INFRA", size=23, fam=DISPLAY,
                 fill=PAPER, ls=1.6, maxw=516, force=True))
    b.append(f'<g class="rise" style="animation-delay:.35s">{ban}</g>')

    b.append(f'<g class="fade" style="animation-delay:.6s">'
             + txt(150, 250, "B.TECH CS (AIML)  \u00b7  AI ENGINEER AT INNOVITI  \u00b7  MULTI-AGENT PIPELINES",
                   size=12.5, fill=INK, ls=0.8, maxw=560, force=True) + '</g>')

    # starburst
    st = (f'<path d="{star(858, 214, 78, 52, 13, rng)}" fill="{RED}" stroke="{INK}" '
          f'stroke-width="3" stroke-linejoin="round"/>'
          + txt(858, 202, "OPEN TO", size=18, fam=DISPLAY, anchor="middle", fill=PAPER, ls=1, maxw=74, force=True)
          + txt(858, 230, "AI-ML ROLES!", size=22, fam=DISPLAY, anchor="middle", fill=PAPER, ls=1, maxw=116, force=True))
    b.append(anchored(858, 214, "pop", 0.55,
                      f'<g class="beat" style="transform-origin:858px 214px">{st}</g>'
                      if animated else st))

    # barcode, because every cover has one
    bars = []
    bx = 30
    while bx < 118:
        bw = rng.choice([1.4, 1.4, 2.4, 3.4])
        bars.append(f'<rect x="{bx:.1f}" y="196" width="{bw:.1f}" height="42" fill="{INK}"/>')
        bx += bw + rng.choice([1.6, 2.4, 3.2])
    b.append(f'<g class="fade" style="animation-delay:.7s">' + "".join(bars)
             + txt(30, 254, "ARTECHIE0806", size=10, ls=1.6) + '</g>')

    return page(W, H, "\n".join("  " + x for x in b), animated,
                "Comic cover: Aryan Rane, AI engineer, agentic LLM systems and inference infrastructure, open to roles")


# ------------------------------------------------------------ strip: day job
def build_dayjob(animated=True):
    rng = random.Random(24)
    W, H = 1000, 272
    M, G = 10, 16
    PW = (W - 2 * M - 2 * G) // 3
    PH = H - 2 * M
    b = [f'<rect width="{W}" height="{H}" fill="{PAPER}"/>']
    defs = "".join(f'<clipPath id="p{i}"><rect x="{M + i*(PW+G)+2}" y="{M+2}" '
                   f'width="{PW-4}" height="{PH-4}"/></clipPath>' for i in range(3))

    def frame(i, delay):
        x = M + i * (PW + G)
        return (f'<g class="fade" style="animation-delay:{delay:.2f}s">'
                f'<path d="{wob_rect(x, M, PW, PH, rng, amp=1.7, step=30)}" fill="{PAPER}" '
                f'stroke="{INK}" stroke-width="3.4" stroke-linejoin="round"/></g>'), x

    # -- panel 1: the machine
    f1, x1 = frame(0, 0)
    b.append(f1)
    cap, ch = caption(x1 + 14, M + 14, PW - 28, ["ONE BOX. 96 GB.", "A 27-BILLION-PARAMETER MODEL."], rng, delay=0.1)
    b.append(cap)
    gx, gy = x1 + 40, M + 132
    card = (f'<path d="{wob_rect(gx, gy, 182, 78, rng, amp=1.3, step=24)}" fill="url(#tone2)" '
            f'stroke="{INK}" stroke-width="3" stroke-linejoin="round"/>')
    for k in range(4):
        card += (f'<line x1="{gx + 16 + k * 15}" y1="{gy + 14}" x2="{gx + 16 + k * 15}" '
                 f'y2="{gy + 64}" stroke="{INK}" stroke-width="2.4" stroke-linecap="round"/>')
    card += txt(gx + 104, gy + 50, "27B", size=22, fam=DISPLAY, anchor="middle", fill=INK, maxw=48, force=True)
    fan = (f'<circle cx="0" cy="0" r="19" fill="{PAPER}" stroke="{INK}" stroke-width="2.6"/>'
           + "".join(f'<path d="M 0 0 Q {math.cos(a)*15:.1f} {math.sin(a)*15:.1f} '
                     f'{math.cos(a+0.7)*18:.1f} {math.sin(a+0.7)*18:.1f}" fill="none" '
                     f'stroke="{INK}" stroke-width="2.2" stroke-linecap="round"/>'
                     for a in (0.4, 2.5, 4.6)))
    b.append(card)
    b.append(f'<g transform="translate({gx + 152},{gy + 39})"><g class="spin">{fan}</g></g>')
    for k in range(3):                              # heat
        hx = gx + 26 + k * 40
        b.append(f'<g class="drift" style="animation-delay:{k*0.4:.1f}s">'
                 f'<path d="M {hx} {gy-10} q 8 -12 0 -22 q -8 -12 0 -22" fill="none" stroke="{RED}" '
                 f'stroke-width="2.6" stroke-linecap="round" pathLength="1" class="draw" '
                 f'style="animation-delay:{0.5+k*0.1:.2f}s"/></g>')
    b.append(balloon(x1 + 226, M + 92, 60, 29, (x1 + 200, M + 128), rng,
                     ["IT FITS...", "BARELY."], size=13, delay=0.55))

    # -- panel 2: quantize
    f2, x2 = frame(1, 0.18)
    b.append(f2)
    cx, cy = x2 + PW / 2, M + 142
    b.append(f'<g class="fade" style="animation-delay:.5s"><path d="{wob_rect(cx-72, cy-58, 144, 116, rng, amp=1.4, step=26)}" '
             f'fill="none" stroke="{INK}" stroke-width="2.2" stroke-dasharray="7 6" opacity="0.55"/></g>')
    inner = (f'<path d="{wob_rect(cx-42, cy-34, 84, 68, rng, amp=1.2, step=20)}" fill="url(#tone)" '
             f'stroke="{INK}" stroke-width="3" stroke-linejoin="round"/>'
             + txt(cx, cy + 8, "8-BIT", size=22, fam=DISPLAY, anchor="middle", fill=INK))
    b.append(anchored(cx, cy, "pop", 0.62, inner))
    b.append(f'<g class="fade" style="animation-delay:.55s">'
             + txt(cx - 68, cy - 64, "16-BIT", size=12, fill="#7A7266", ls=1, maxw=56, force=True) + '</g>')
    for dx, dy, rot, nud in ((-96, 0, 0, "nudgeR"), (96, 0, 180, "nudgeR")):
        ax, ay = cx + dx, cy + dy
        arrow = (f'<path d="M -22 0 L 6 0 M -6 -9 L 7 0 L -6 9" fill="none" stroke="{INK}" '
                 f'stroke-width="3.4" stroke-linecap="round" stroke-linejoin="round"/>')
        b.append(f'<g transform="translate({ax:.0f},{ay:.0f}) rotate({rot})">'
                 f'<g class="{nud}" style="animation-delay:.9s">{arrow}</g></g>')
    b.append(sfx(x2 + PW / 2, M + 54, "QUANTIZE!", rng, size=42, rot=-8, delay=0.75, maxw=246))
    cap2, _ = caption(x2 + 14, M + PH - 52, PW - 28,
                      ["THEN MEASURE AGAIN.", "AND AGAIN."], rng, delay=0.9)
    b.append(cap2)

    # -- panel 3: the number
    f3, x3 = frame(2, 0.36)
    b.append(f3)
    ncx, ncy = x3 + PW / 2, M + 118
    b.append(f'<g clip-path="url(#p2)">{rays(ncx, ncy, 66, 118, 18, rng, stroke=INK, w=2.4, delay=0.85)}</g>')
    b.append(anchored(ncx, ncy, "slam", 1.0,
                      txt(ncx, ncy + 6, "~150", size=74, fam=DISPLAY, anchor="middle", fill="none",
                          maxw=186, force=True,
                          extra=f'stroke="{INK}" stroke-width="8" stroke-linejoin="round"')
                      + txt(ncx, ncy + 6, "~150", size=74, fam=DISPLAY, anchor="middle", fill=RED,
                            maxw=186, force=True)))
    b.append(f'<g class="fade" style="animation-delay:1.15s">'
             + txt(ncx, ncy + 42, "TOKENS / SECOND", size=18, fam=DISPLAY, anchor="middle",
                   fill=INK, ls=1.4, maxw=196, force=True) + '</g>')
    cap3, _ = caption(x3 + 14, M + PH - 66, PW - 28,
                      ["\u221260% COST PER TOKEN.", "AND FULL CONTROL", "OF THE INFRASTRUCTURE."],
                      rng, delay=1.25, fill=INK, ink=PAPER)
    b.append(cap3)

    return page(W, H, "\n".join("  " + x for x in b), animated, defs=defs, label=
                "Three panel comic strip: a 27B model on one 96GB box, quantized to 8-bit, reaching ~150 tokens per second")


# ------------------------------------------------------------ strip: leakage
def build_leakage(animated=True):
    rng = random.Random(37)
    W, H = 1000, 272
    M, G = 10, 16
    PW = (W - 2 * M - 2 * G) // 3
    PH = H - 2 * M
    b = [f'<rect width="{W}" height="{H}" fill="{PAPER}"/>']
    defs = "".join(f'<clipPath id="q{i}"><rect x="{M + i*(PW+G)+2}" y="{M+2}" '
                   f'width="{PW-4}" height="{PH-4}"/></clipPath>' for i in range(3))

    def frame(i, delay):
        x = M + i * (PW + G)
        return (f'<g class="fade" style="animation-delay:{delay:.2f}s">'
                f'<path d="{wob_rect(x, M, PW, PH, rng, amp=1.7, step=30)}" fill="{PAPER}" '
                f'stroke="{INK}" stroke-width="3.4" stroke-linejoin="round"/></g>'), x

    # -- panel 1: the too-good score
    f1, x1 = frame(0, 0)
    b.append(f1)
    cap, _ = caption(x1 + 14, M + 14, 178,
                     ["RANDOM FOREST.", "NASA JPL SMALL-BODY DATA."], rng, delay=0.1)
    b.append(cap)
    sx, sy = x1 + 40, M + 96
    b.append(f'<g class="fade" style="animation-delay:.35s"><path d="{wob_rect(sx, sy, 150, 92, rng, amp=1.3)}" '
             f'fill="{PAPER}" stroke="{INK}" stroke-width="3" stroke-linejoin="round"/></g>')
    b.append(f'<path d="M {sx+14} {sy+76} L {sx+52} {sy+58} L {sx+92} {sy+34} L {sx+134} {sy+16}" '
             f'fill="none" stroke="{RED}" stroke-width="3.6" stroke-linecap="round" '
             f'pathLength="1" class="draw" style="animation-delay:.6s"/>')
    b.append(f'<g class="fade" style="animation-delay:.8s">'
             + txt(sx + 75, sy + 120, "99.99%  \u00b7  AUC 1.00", size=17, fam=DISPLAY,
                   anchor="middle", fill=INK, ls=1, maxw=182, force=True) + '</g>')
    b.append(balloon(x1 + 238, M + 62, 54, 25, (x1 + 210, M + 96), rng, ["NAILED IT."], delay=0.95))

    # -- panel 2: the definition
    f2, x2 = frame(1, 0.18)
    b.append(f2)
    cap2, ch2 = caption(x2 + 14, M + 14, PW - 28,
                        ["A HAZARDOUS ASTEROID IS", "DEFINED AS MOID \u2264 0.05 AU", "AND H \u2264 22."],
                        rng, delay=0.35)
    b.append(cap2)
    fy = M + 14 + ch2 + 26
    feats = [("moid_ld", True), ("h", True), ("diameter", False), ("albedo", False), ("e", False)]
    for i, (name, hot) in enumerate(feats):
        yy = fy + i * 25
        b.append(f'<g class="fade" style="animation-delay:{0.55 + i*0.07:.2f}s">'
                 + txt(x2 + 42, yy, name, size=15, fam=CODE, weight="600",
                       fill=INK if hot else "#6C665C") + '</g>')
    b.append(f'<path d="{wob_ellipse(x2 + 82, fy + 7, 72, 30, rng, amp=3.0, n=30)}" fill="none" '
             f'stroke="{RED}" stroke-width="3.2" stroke-linecap="round" pathLength="1" '
             f'class="draw" style="animation-delay:1.05s"/>')
    b.append(sfx(x2 + PW - 78, M + PH - 44, "...WAIT.", rng, size=30, rot=-6, delay=1.5,
                 fill=PAPER, maxw=118))

    # -- panel 3: the stamp
    f3, x3 = frame(2, 0.36)
    b.append(f3)
    scx, scy = x3 + PW / 2, M + 140
    b.append(f'<g clip-path="url(#q2)">{rays(scx, scy, 74, 104, 12, rng, stroke=INK, w=2.6, delay=1.5)}</g>')
    cap3, ch3 = caption(x3 + 14, M + 14, PW - 28,
                        ["TWO OF THE FIVE FEATURES", "WERE MOID AND H."], rng, delay=0.5)
    b.append(cap3)
    stamp = (f'<path d="{wob_rect(scx-104, scy-31, 208, 62, rng, amp=2.4, step=24)}" fill="none" '
             f'stroke="{RED}" stroke-width="5" stroke-linejoin="round"/>'
             f'<path d="{wob_rect(scx-96, scy-24, 192, 48, rng, amp=2.0, step=22)}" fill="none" '
             f'stroke="{RED}" stroke-width="2" stroke-linejoin="round"/>'
             + txt(scx, scy + 11, "TARGET LEAKAGE", size=30, fam=DISPLAY, anchor="middle",
                   fill=RED, ls=1, maxw=172, force=True))
    b.append(anchored(scx, scy, "slam", 1.6,
                      f'<g transform="rotate(-7 {scx:.0f} {scy:.0f})">{stamp}</g>'))
    cap4, _ = caption(x3 + 14, M + PH - 52, PW - 28,
                      ["SHIPPED THE FINDING,", "NOT THE NUMBER."], rng, delay=1.95, fill=INK, ink=PAPER)
    b.append(cap4)

    return page(W, H, "\n".join("  " + x for x in b), animated, defs=defs, label=
                "Three panel comic strip: a 99.99% accurate asteroid model turns out to be target leakage, published as a finding")


# --------------------------------------------------- strip: the SQL critic
def build_critic(animated=True):
    rng = random.Random(51)
    W, H = 1000, 272
    M, G = 10, 16
    PW = (W - 2 * M - 2 * G) // 3
    PH = H - 2 * M
    b = [f'<rect width="{W}" height="{H}" fill="{PAPER}"/>']
    defs = "".join(f'<clipPath id="c{i}"><rect x="{M + i*(PW+G)+2}" y="{M+2}" '
                   f'width="{PW-4}" height="{PH-4}"/></clipPath>' for i in range(3))

    def frame(i, delay):
        x = M + i * (PW + G)
        return (f'<g class="fade" style="animation-delay:{delay:.2f}s">'
                f'<path d="{wob_rect(x, M, PW, PH, rng, amp=1.7, step=30)}" fill="{PAPER}" '
                f'stroke="{INK}" stroke-width="3.4" stroke-linejoin="round"/></g>'), x

    # -- panel 1: the ask
    f1, x1 = frame(0, 0)
    b.append(f1)
    cap, _ = caption(x1 + 14, M + 14, 186, ["UPLOAD A FILE.", "ASK IN PLAIN ENGLISH."], rng, delay=0.1)
    b.append(cap)
    fx, fy = x1 + 26, M + 116
    doc = (f'<path d="{wob_rect(fx, fy, 78, 96, rng, amp=1.2, step=22)}" fill="{PAPER}" '
           f'stroke="{INK}" stroke-width="3" stroke-linejoin="round"/>')
    for k in range(4):
        doc += (f'<line x1="{fx + 13}" y1="{fy + 22 + k * 16}" x2="{fx + 65}" y2="{fy + 22 + k * 16}" '
                f'stroke="{INK}" stroke-width="2.2" stroke-linecap="round" opacity="0.75"/>')
    b.append(f'<g class="fade" style="animation-delay:.4s">{doc}'
             + txt(fx + 39, fy + 116, "sales.csv", size=12, fam=CODE, anchor="middle",
                   weight="600", maxw=74) + '</g>')
    b.append(balloon(x1 + 216, M + 124, 76, 42, (x1 + 148, M + 166), rng,
                     ["WHICH REGION", "LOST MONEY", "IN Q3?"], size=13, delay=0.6))

    # -- panel 2: the argument
    f2, x2 = frame(1, 0.18)
    b.append(f2)
    for bx, label, delay in ((x2 + 24, "SQL AUTHOR", 0.5), (x2 + 194, "CRITIC", 0.55)):
        box = (f'<path d="{wob_rect(bx, M + 130, 98, 50, rng, amp=1.3, step=22)}" fill="url(#tone2)" '
               f'stroke="{INK}" stroke-width="3" stroke-linejoin="round"/>'
               + txt(bx + 49, M + 161, label, size=13, anchor="middle", fill=INK, maxw=84, force=True))
        b.append(f'<g class="fade" style="animation-delay:{delay:.2f}s">{box}</g>')
    b.append(balloon(x2 + 74, M + 58, 58, 27, (x2 + 74, M + 126), rng,
                     ["SELECT * FROM", "orders ..."], size=11.5, delay=0.75, fam=CODE))
    b.append(f'<line x1="{x2 + 20}" y1="{M + 76}" x2="{x2 + 128}" y2="{M + 42}" stroke="{RED}" '
             f'stroke-width="3.6" stroke-linecap="round" pathLength="1" class="draw" '
             f'style="animation-delay:1.25s"/>')
    b.append(burst(x2 + 242, M + 62, 50, 37, (x2 + 242, M + 126), rng, ["NO."], size=27, delay=1.05))
    cap2, _ = caption(x2 + 14, M + PH - 52, PW - 28,
                      ["READ-ONLY. ONE STATEMENT.", "ROW CAP. TIMEOUT."], rng, delay=1.35)
    b.append(cap2)

    # -- panel 3: the receipt
    f3, x3 = frame(2, 0.36)
    b.append(f3)
    cap3, _ = caption(x3 + 14, M + 14, PW - 28,
                      ["EVERY ANSWER SHIPS WITH", "THE SQL THAT MADE IT."], rng, delay=0.55)
    b.append(cap3)
    rx0, ry0 = x3 + 54, M + 82
    rec = (f'<path d="{receipt(rx0, ry0, 208, 122, rng)}" fill="{PAPER}" stroke="{INK}" '
           f'stroke-width="2.8" stroke-linejoin="round"/>')
    for k, line in enumerate(["SELECT region,", "SUM(revenue)", "FROM orders", "GROUP BY 1;"]):
        rec += txt(rx0 + 16, ry0 + 24 + k * 19, line, size=12.5, fam=CODE, weight="600",
                   fill=INK, maxw=172)
    rec += f'<line x1="{rx0 + 14}" y1="{ry0 + 92}" x2="{rx0 + 194}" y2="{ry0 + 92}" stroke="{INK}" stroke-width="1.6" opacity="0.5"/>'
    rec += txt(rx0 + 16, ry0 + 106, "12 ROWS \u00b7 READ-ONLY", size=11.5, fill=RED, maxw=172)
    b.append(anchored(rx0 + 104, ry0 + 61, "pop", 0.9, rec))
    cap4, _ = caption(x3 + 14, M + PH - 40, PW - 28, ["NOTHING TAKEN ON FAITH."],
                      rng, delay=1.3, fill=INK, ink=PAPER)
    b.append(cap4)

    return page(W, H, "\n".join("  " + x for x in b), animated, defs=defs, label=
                "Three panel comic strip: a question in plain English, a critic agent rejecting the SQL author, and an answer shipped with its SQL")


# ---------------------------------------------------- strip: the verifier
def build_verifier(animated=True):
    rng = random.Random(63)
    W, H = 1000, 272
    M, G = 10, 16
    PW = (W - 2 * M - 2 * G) // 3
    PH = H - 2 * M
    b = [f'<rect width="{W}" height="{H}" fill="{PAPER}"/>']
    defs = "".join(f'<clipPath id="v{i}"><rect x="{M + i*(PW+G)+2}" y="{M+2}" '
                   f'width="{PW-4}" height="{PH-4}"/></clipPath>' for i in range(3))

    def frame(i, delay):
        x = M + i * (PW + G)
        return (f'<g class="fade" style="animation-delay:{delay:.2f}s">'
                f'<path d="{wob_rect(x, M, PW, PH, rng, amp=1.7, step=30)}" fill="{PAPER}" '
                f'stroke="{INK}" stroke-width="3.4" stroke-linejoin="round"/></g>'), x

    # -- panel 1: fluent, confident, unchecked
    f1, x1 = frame(0, 0)
    b.append(f1)
    cap, _ = caption(x1 + 14, M + 14, PW - 28,
                     ["THE AGENT THAT WRITES", "NEVER GRADES ITS OWN WORK."], rng, delay=0.1)
    b.append(cap)
    bx = x1 + 96
    box = (f'<path d="{wob_rect(bx, M + 178, 124, 50, rng, amp=1.3, step=22)}" fill="url(#tone2)" '
           f'stroke="{INK}" stroke-width="3" stroke-linejoin="round"/>'
           + txt(bx + 62, M + 209, "RESEARCHER", size=13, anchor="middle", maxw=104, force=True))
    b.append(f'<g class="fade" style="animation-delay:.45s">{box}</g>')
    b.append(balloon(x1 + 158, M + 118, 88, 36, (x1 + 158, M + 174), rng,
                     ["THE MARKET GREW", "40% IN 2024."], size=13, delay=0.7))

    # -- panel 2: the sealed room
    f2, x2 = frame(1, 0.18)
    b.append(f2)
    cap2, _ = caption(x2 + 14, M + 14, PW - 28,
                      ["THE VERIFIER SEES ONE CLAIM", "AND ITS CITED TEXT."], rng, delay=0.35)
    b.append(cap2)
    vx, vy = x2 + 56, M + 92
    room = (f'<path d="{wob_rect(vx, vy, 204, 104, rng, amp=1.6, step=26)}" fill="{PAPER}" '
            f'stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>'
            f'<path d="{wob_rect(vx + 11, vy + 11, 182, 82, rng, amp=1.2, step=24)}" fill="none" '
            f'stroke="{INK}" stroke-width="1.8" stroke-linejoin="round" opacity="0.55"/>')
    b.append(f'<g class="fade" style="animation-delay:.6s">{room}</g>')
    for k, (lab, col) in enumerate((("CLAIM", RED), ("SOURCE", INK))):
        cxx = vx + 26 + k * 92
        chip = (f'<path d="{wob_rect(cxx, vy + 28, 78, 34, rng, amp=1.1, step=18)}" fill="{PAPER}" '
                f'stroke="{col}" stroke-width="2.8" stroke-linejoin="round"/>'
                + txt(cxx + 39, vy + 50, lab, size=12.5, anchor="middle", fill=col, maxw=64, force=True))
        b.append(anchored(cxx + 39, vy + 45, "pop", 0.85 + k * 0.12, chip))
    b.append(f'<g class="fade" style="animation-delay:1.1s">'
             + txt(vx + 102, vy + 84, "16K TOKEN BUDGET", size=11, anchor="middle",
                   fill="#7A7266", ls=1, maxw=150, force=True) + '</g>')
    b.append(f'<g class="fade" style="animation-delay:1.25s">{eye(x2 + 250, M + 222, 22, rng)}</g>')
    b.append(f'<g class="fade" style="animation-delay:1.3s">'
             + txt(x2 + 22, M + 228, "NO DRAFT. NO CONTEXT.", size=12, fill=INK, maxw=180, force=True) + '</g>')

    # -- panel 3: the verdict
    f3, x3 = frame(2, 0.36)
    b.append(f3)
    scx, scy = x3 + PW / 2, M + 140
    b.append(f'<g clip-path="url(#v2)">{rays(scx, scy, 76, 106, 12, rng, stroke=INK, w=2.6, delay=1.5)}</g>')
    cap3, _ = caption(x3 + 14, M + 14, PW - 28,
                      ["THE QUOTE MUST APPEAR", "IN THE SOURCE, VERBATIM."], rng, delay=0.5)
    b.append(cap3)
    stamp = (f'<path d="{wob_rect(scx-106, scy-31, 212, 62, rng, amp=2.4, step=24)}" fill="none" '
             f'stroke="{RED}" stroke-width="5" stroke-linejoin="round"/>'
             f'<path d="{wob_rect(scx-98, scy-24, 196, 48, rng, amp=2.0, step=22)}" fill="none" '
             f'stroke="{RED}" stroke-width="2" stroke-linejoin="round"/>'
             + txt(scx, scy + 11, "UNSUPPORTED", size=30, fam=DISPLAY, anchor="middle",
                   fill=RED, ls=1, maxw=174, force=True))
    b.append(anchored(scx, scy, "slam", 1.6, f'<g transform="rotate(-7 {scx:.0f} {scy:.0f})">{stamp}</g>'))
    cap4, _ = caption(x3 + 14, M + PH - 52, PW - 28,
                      ["NO QUOTE, NO CLAIM.", "THE VERDICT DOWNGRADES ITSELF."],
                      rng, delay=1.95, fill=INK, ink=PAPER)
    b.append(cap4)

    return page(W, H, "\n".join("  " + x for x in b), animated, defs=defs, label=
                "Three panel comic strip: a fluent claim, an isolated verifier that sees only the claim and its source, and an unsupported verdict")


# ------------------------------------------------------------------- outputs
# strip-leakage.svg is still available -- add ("strip-leakage.svg", build_leakage) to rebuild it
BUILDS = [("cover.svg", build_cover), ("strip-critic.svg", build_critic),
          ("strip-verifier.svg", build_verifier), ("strip-dayjob.svg", build_dayjob)]

for name, fn in BUILDS:
    p = os.path.join(OUT, name)
    with open(p, "w", encoding="utf-8") as f:
        f.write(fn(True))
    print(f"{name:20s} {os.path.getsize(p):>7,} bytes")

import cairosvg
globals()["PREVIEW"] = True
for name, fn in BUILDS:
    cairosvg.svg2png(bytestring=fn(False).encode(), output_width=1000,
                     write_to=os.path.join(HERE, "pv_" + name.replace(".svg", ".png")),
                     background_color="#FFFFFF")
print("previews rendered")
