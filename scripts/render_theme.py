#!/usr/bin/env python3
"""
Preview generator: animated "Glass / Aurora" theme for the GitHub profile README.

Two colour variants (dark + light). Everything is pure SVG + SMIL animation:
  - no JavaScript  (GitHub renders README images in a no-script context)
  - no external service / CDN
  - animations are written INSIDE each .svg file, so they still play through <img src="...">
    exactly like GitHub renders them.

Outputs
  preview/assets/tech/<slug>.svg           dark tile, icon only (64x64)
  preview/assets/tech/<slug>-light.svg     light tile, icon only (64x64)
  preview/assets/stack-strip-{dark,light}.svg   glass card rows with animated logos + labels
  preview/assets/banner-{dark,light}.svg   hero
  preview/assets/divider-{dark,light}.svg  animated rule
  preview/assets/footer-{dark,light}.svg   outro
"""

import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "assets")            # shipped theme assets (referenced by README.md)
LAB = os.path.join(ROOT, "preview", "assets")  # same files, so preview/index.html can render them
TECH = os.path.join(LAB, "tech")               # per-logo tiles: building blocks for the preview lab

SANS = "Inter, 'Segoe UI', system-ui, -apple-system, 'Helvetica Neue', sans-serif"
MONO = "ui-monospace, SFMono-Regular, Menlo, Consolas, monospace"

DARK = dict(
    key="dark",
    canvas="#070C16", card="#0E1729", card_hi="#16233B",
    stroke="#1E2E4A", text="#EAF2FF", dim="#8FA3BF", faint="#5B6F8E",
    accent="#4D9BFF", accent2="#34E2C5", accent3="#A78BFA",
    mono_on_dark=True,
)
LIGHT = dict(
    key="light",
    canvas="#F5F7FC", card="#FFFFFF", card_hi="#EEF2FA",
    stroke="#DDE4F0", text="#101828", dim="#5A6B85", faint="#8494AC",
    accent="#1D6FE0", accent2="#0E9E86", accent3="#7C4DDB",
    mono_on_dark=False,
)


def blob(t, uid):
    """Shared defs for aurora blobs + soft blur."""
    return f"""
  <defs>
    <filter id="blur{uid}" x="-45%" y="-45%" width="190%" height="190%">
      <feGaussianBlur stdDeviation="34"/>
    </filter>
    <linearGradient id="edge{uid}" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="{t['accent']}"/>
      <stop offset="55%" stop-color="{t['accent2']}"/>
      <stop offset="100%" stop-color="{t['accent3']}"/>
    </linearGradient>
  </defs>"""


def aurora(t, uid, w, h, alpha=0.55):
    """Three drifting blurred blobs, each on its own slow loop -> living background."""
    return f"""
  <g filter="url(#blur{uid})" opacity="{alpha}">
    <ellipse cx="{w*0.16:.0f}" cy="{h*0.22:.0f}" rx="150" ry="96" fill="{t['accent']}" opacity="0.55">
      <animate attributeName="cx" values="{w*0.16:.0f};{w*0.24:.0f};{w*0.13:.0f};{w*0.16:.0f}" dur="19s" repeatCount="indefinite"/>
      <animate attributeName="cy" values="{h*0.22:.0f};{h*0.34:.0f};{h*0.16:.0f};{h*0.22:.0f}" dur="23s" repeatCount="indefinite"/>
    </ellipse>
    <ellipse cx="{w*0.82:.0f}" cy="{h*0.7:.0f}" rx="168" ry="98" fill="{t['accent2']}" opacity="0.34">
      <animate attributeName="cx" values="{w*0.82:.0f};{w*0.74:.0f};{w*0.86:.0f};{w*0.82:.0f}" dur="25s" repeatCount="indefinite"/>
      <animate attributeName="cy" values="{h*0.7:.0f};{h*0.58:.0f};{h*0.76:.0f};{h*0.7:.0f}" dur="21s" repeatCount="indefinite"/>
    </ellipse>
    <ellipse cx="{w*0.56:.0f}" cy="{h*0.92:.0f}" rx="120" ry="72" fill="{t['accent3']}" opacity="0.28">
      <animate attributeName="opacity" values="0.18;0.34;0.18" dur="13s" repeatCount="indefinite"/>
    </ellipse>
  </g>"""


def anim(dur, values, attr="transform", ease=None, begin=None, repeat="indefinite"):
    """An <animateTransform>/<animate>. keyTimes are derived from `values` so the
    list lengths always match (a mismatch silently disables the animation)."""
    tag = "animateTransform" if attr == "transform" else "animate"
    n = values.count(";") + 1
    parts = []
    if ease:
        times = ";".join(f"{i/(n-1):g}" for i in range(n))
        spl = ";".join([ease] * (n - 1))
        parts.append(f' calcMode="spline" keyTimes="{times}" keySplines="{spl}"')
    if begin:
        parts.append(f' begin="{begin}"')
    if attr == "transform":
        parts.append(' additive="sum"')
    parts.append(f' repeatCount="{repeat}"')
    return f'<{tag} attributeName="{attr}" values="{values}" dur="{dur}"{"".join(parts)}/>'


# ----------------------------------------------------------------------------------
# Animated logos. Each icon is drawn in a 48x48 box, pure SMIL, no scripts.
# ----------------------------------------------------------------------------------

def ic_react(t):
    ell = 'fill="none" stroke="#61DAFB" stroke-width="2.6"'
    return f"""
  <g>
    {anim("7s", "0 24 24;360 24 24", )}
    <ellipse cx="24" cy="24" rx="20" ry="7.6" {ell}/>
    <ellipse cx="24" cy="24" rx="20" ry="7.6" {ell} transform="rotate(60 24 24)"/>
    <ellipse cx="24" cy="24" rx="20" ry="7.6" {ell} transform="rotate(120 24 24)"/>
    <circle cx="24" cy="24" r="3.4" fill="#61DAFB">
      <animate attributeName="r" values="3.4;4.4;3.4" dur="2.2s" repeatCount="indefinite"/>
    </circle>
  </g>"""


def ic_js(t):
    return f"""
  <g>
    {anim("4.2s", "-6 24 24;6 24 24;-6 24 24", ease="0.4 0 0.6 1")}
    <rect x="6" y="6" width="36" height="36" rx="6" fill="#F7DF1E"/>
    <text x="36" y="37" text-anchor="end" font-family="{SANS}" font-size="17" font-weight="800" font-style="italic" fill="#1B1B1B">JS</text>
  </g>
  <g clip-path="url(#jsclip)" opacity="0.75">
    <rect x="-14" y="0" width="10" height="48" fill="#FFFFFF" opacity="0.6" transform="skewX(-18)">
      <animate attributeName="x" values="-16;54" dur="3.4s" begin="0.6s" repeatCount="indefinite"/>
    </rect>
  </g>
  <defs><clipPath id="jsclip"><rect x="6" y="6" width="36" height="36" rx="6"/></clipPath></defs>"""


def _shield(color, glyph, invert=False):
    a, b = (-5, 5)
    if invert:
        a, b = b, a
    return f"""
  <g>
    {anim("4.6s", f"{a} 24 24;{b} 24 24;{a} 24 24", ease="0.4 0 0.6 1")}
    <path d="M7 5 H41 L38 41 L24 45 L10 41 Z" fill="{color}"/>
    <path d="M24 8.6 H37.4 L35 38.6 L24 41.9 Z" fill="{color}" opacity="0.55"/>
    <text x="24" y="33" text-anchor="middle" font-family="{SANS}" font-size="17" font-weight="800" fill="#FFFFFF">{glyph}</text>
  </g>"""


def ic_html5(t):
    return _shield("#E34F26", "5")


def ic_css3(t):
    return _shield("#1572B6", "3", invert=True)


def ic_php(t):
    letters = "php"
    out = []
    for i, ch in enumerate(letters):
        out.append(
            f'<text x="{11.5 + i * 10}" y="29" font-family="{SANS}" font-size="14" font-weight="800" '
            f'font-style="italic" fill="#FFFFFF" opacity="0.25">'
            f'<animate attributeName="opacity" values="0.25;1;1;0.25;0.25" keyTimes="0;0.12;0.55;0.7;1" '
            f'dur="2.8s" begin="{i * 0.28:.2f}s" repeatCount="indefinite"/>{ch}</text>'
        )
    return f"""
  <ellipse cx="24" cy="24" rx="22" ry="11.5" fill="#777BB4"/>
  <ellipse cx="24" cy="24" rx="22" ry="11.5" fill="none" stroke="#FFFFFF" stroke-opacity="0.35"/>
  <g>{''.join(out)}</g>"""


def ic_laravel(t):
    bars = [("14", 0), ("21", 0.28), ("28", 0.56)]
    g = ['<rect x="8" y="8" width="5" height="32" rx="2.5" fill="#FF2D20"/>']
    for i, (w, d) in enumerate(bars):
        y = 8 + i * 11
        g.append(
            f'<rect x="15" y="{y}" width="{w}" height="5" rx="2.5" fill="#FF2D20">'
            f'<animate attributeName="width" values="0;{w};{w};0" keyTimes="0;0.28;0.78;1" '
            f'dur="3.4s" begin="{d:.2f}s" repeatCount="indefinite"/></rect>'
        )
    return "".join(g)


def ic_flutter(t):
    shapes = [
        ("#47C5FB", "M24 3 L45 24 L34 35 L13 14 Z", 0.00),
        ("#54C5F8", "M13 14 L34 35 L24 45 L3 24 Z", 0.34),
        ("#0553B1", "M24 24 L24 45 L13.5 34.5 Z", 0.68),
    ]
    out = []
    for fill, d, delay in shapes:
        out.append(
            f'<path d="{d}" fill="{fill}" opacity="0">'
            f'<animate attributeName="opacity" values="0;1;1;0" keyTimes="0;0.12;0.82;1" '
            f'dur="3.6s" begin="{delay}s" repeatCount="indefinite"/>'
            f'<animateTransform attributeName="transform" type="translate" values="-5 5;0 0;0 0;-5 5" '
            f'keyTimes="0;0.12;0.82;1" dur="3.6s" begin="{delay}s" repeatCount="indefinite"/></path>'
        )
    return "".join(out)


def ic_dart(t):
    return f"""
  <g transform="translate(2,2)">
    <path d="M18 2 L42 22 L18 42 L2 42 L22 22 L2 2 Z" fill="#0175C2"/>
    <path d="M2 2 L22 22 L2 42 Z" fill="#00A8E1">
      <animateTransform attributeName="transform" type="translate" values="0 0;-4 0;0 0" dur="3.4s"
        calcMode="spline" keySplines="0.3 0 0.7 1;0.3 0 0.7 1" keyTimes="0;0.5;1" repeatCount="indefinite"/>
    </path>
  </g>"""


def ic_kotlin(t):
    return f"""
  <defs>
    <linearGradient id="ktg" x1="0" y1="1" x2="1" y2="0">
      <stop offset="0%" stop-color="#1C92FB"/><stop offset="50%" stop-color="#7F52FF"/><stop offset="100%" stop-color="#E448F6"/>
    </linearGradient>
    <clipPath id="ktc"><rect x="6" y="6" width="36" height="36"/></clipPath>
  </defs>
  <g clip-path="url(#ktc)">
    <path d="M6 6 H42 L24 24 Z" fill="url(#ktg)"/>
    <path d="M6 6 L24 24 L6 42 Z" fill="url(#ktg)" opacity="0.7"/>
    <rect x="6" y="6" width="0" height="36" fill="#FFFFFF" opacity="0.55">
      <animate attributeName="width" values="0;0;40;40" keyTimes="0;0.45;0.75;1" dur="3s" repeatCount="indefinite"/>
      <animate attributeName="opacity" values="0;0.5;0" keyTimes="0;0.6;1" dur="3s" repeatCount="indefinite"/>
    </rect>
  </g>"""


def ic_mysql(t):
    return f"""
  <g>
    <circle cx="24" cy="24" r="10" fill="none" stroke="{t['accent2']}" stroke-width="1.6" opacity="0">
      <animate attributeName="r" values="14;26" dur="2.6s" repeatCount="indefinite"/>
      <animate attributeName="opacity" values="0.5;0" dur="2.6s" repeatCount="indefinite"/>
    </circle>
    <path d="M9 13 V35 C9 39 39 39 39 35 V13" fill="#0A5B6B" opacity="0.9"/>
    <ellipse cx="24" cy="13" rx="15" ry="5.6" fill="#007589"/>
    <ellipse cx="24" cy="13" rx="15" ry="5.6" fill="none" stroke="#F29111" stroke-width="1.4" opacity="0.8"/>
    <path d="M9 24 C9 28 39 28 39 24" fill="none" stroke="#F29111" stroke-width="1.8" opacity="0.95">
      <animate attributeName="d" values="M9 20 C9 24 39 24 39 20;M9 30 C9 34 39 34 39 30;M9 20 C9 24 39 24 39 20" dur="3.4s" repeatCount="indefinite"/>
    </path>
    <path d="M9 27 C9 31 39 31 39 27" fill="none" stroke="#8FE3D8" stroke-width="1.4" opacity="0.6">
      <animate attributeName="d" values="M9 23 C9 27 39 27 39 23;M9 33 C9 37 39 37 39 33;M9 23 C9 27 39 27 39 23" dur="3.4s" repeatCount="indefinite"/>
    </path>
  </g>"""


def ic_sqlite(t):
    rows = []
    for i, y in enumerate((16, 23, 30, 37)):
        rows.append(
            f'<rect x="10" y="{y}" width="28" height="4" rx="2" fill="{t["accent"]}" opacity="0.25">'
            f'<animate attributeName="opacity" values="0.25;1;0.25" dur="2.8s" begin="{i*0.45:.2f}s" repeatCount="indefinite"/>'
            f'<animate attributeName="width" values="28;18;28" dur="2.8s" begin="{i*0.45:.2f}s" repeatCount="indefinite"/></rect>'
        )
    return f"""
  <path d="M8 10 H40 V40 H8 Z" fill="none" stroke="{t['stroke']}" stroke-width="1.6" rx="3"/>
  <path d="M8 10 H40 V16 H8 Z" fill="{t['accent']}" opacity="0.5"/>
  {''.join(rows)}"""


def ic_git(t):
    return f"""
  <rect x="5" y="5" width="38" height="38" rx="10" fill="#F05032"/>
  <g stroke="#FFFFFF" stroke-width="2.6" fill="none" stroke-linecap="round">
    <path d="M24 13 V35" stroke-dasharray="22" stroke-dashoffset="22">
      <animate attributeName="stroke-dashoffset" values="22;0;0;22" keyTimes="0;0.35;0.8;1" dur="3.6s" repeatCount="indefinite"/>
    </path>
    <path d="M24 24 C24 30 28 32 33 32" stroke-dasharray="16" stroke-dashoffset="16">
      <animate attributeName="stroke-dashoffset" values="16;16;0;0;16" keyTimes="0;0.25;0.55;0.82;1" dur="3.6s" repeatCount="indefinite"/>
    </path>
  </g>
  <g fill="#FFFFFF">
    <circle cx="24" cy="12.5" r="3.1"/><circle cx="24" cy="35.5" r="3.1"/>
    <circle cx="34" cy="32" r="3.1" opacity="0.4">
      <animate attributeName="opacity" values="0.4;1;0.4" dur="3.6s" begin="1.4s" repeatCount="indefinite"/>
    </circle>
  </g>"""


def ic_docker(t):
    boxes = []
    cells = [(11, 22), (16.5, 22), (22, 22), (27.5, 22), (33, 22),
             (16.5, 16.5), (22, 16.5), (27.5, 16.5), (22, 11)]
    for i, (x, y) in enumerate(cells):
        boxes.append(
            f'<rect x="{x}" y="{y}" width="4.6" height="4.6" rx="1" fill="#2496ED" opacity="0.35">'
            f'<animate attributeName="opacity" values="0.35;1;0.35" dur="2.4s" begin="{i*0.16:.2f}s" repeatCount="indefinite"/></rect>'
        )
    return f"""
  <g>
    {anim("4.4s", "-2 24 24;2 24 24;-2 24 24", ease="0.4 0 0.6 1")}
    {''.join(boxes)}
    <path d="M6 28 H42 C41 36 34 39 24 39 C14 39 7 36 6 28 Z" fill="#2496ED"/>
  </g>
  <path d="M2 42 q6 -3 12 0 t12 0 t12 0 t8 0" fill="none" stroke="{t['accent2']}" stroke-width="1.6" opacity="0.55">
    <animateTransform attributeName="transform" type="translate" values="0 0;-12 0;0 0" dur="6s" repeatCount="indefinite"/>
  </path>"""


def ic_tailwind(t):
    lobe = "M2 18 C8 6 18 6 24 18 C18 30 8 30 2 18 Z"
    lobe2 = "M24 30 C30 18 40 18 46 30 C40 42 30 42 24 30 Z"
    return f"""
  <g fill="#06B6D4">
    <path d="{lobe}">
      <animateTransform attributeName="transform" type="translate" values="0 0;4 -2;0 0" dur="4.2s"
        calcMode="spline" keySplines="0.4 0 0.6 1;0.4 0 0.6 1" keyTimes="0;0.5;1" repeatCount="indefinite"/>
    </path>
    <path d="{lobe2}">
      <animateTransform attributeName="transform" type="translate" values="0 0;-4 2;0 0" dur="4.2s"
        calcMode="spline" keySplines="0.4 0 0.6 1;0.4 0 0.6 1" keyTimes="0;0.5;1" repeatCount="indefinite"/>
    </path>
    <path d="{lobe}" opacity="0.22" transform="translate(22 12)">
      <animate attributeName="opacity" values="0.08;0.3;0.08" dur="4.2s" repeatCount="indefinite"/>
    </path>
  </g>"""


def ic_figma(t):
    shapes = [
        ("#F24E1E", "M24 4 V18 H17 A7 7 0 0 1 17 4 Z", 0.00),
        ("#FF7262", "M31 4 A7 7 0 1 1 31 18 A7 7 0 1 1 31 4 Z", 0.14),
        ("#A259FF", "M24 18 V32 H17 A7 7 0 0 1 17 18 Z", 0.28),
        ("#1ABCFE", "M31 18 A7 7 0 1 1 31 32 A7 7 0 1 1 31 18 Z", 0.42),
        ("#0ACF83", "M24 32 V46 H17 A7 7 0 0 1 10 39 V32 Z", 0.56),
    ]
    out = []
    for fill, d, delay in shapes:
        out.append(
            f'<path d="{d}" fill="{fill}">'
            f'<animateTransform attributeName="transform" type="translate" values="0 0;0 -3.5;0 1.5;0 0;0 0" '
            f'keyTimes="0;0.16;0.32;0.48;1" dur="3.2s" begin="{delay}s" repeatCount="indefinite"/></path>'
        )
    return "".join(out)


def ic_vercel(t):
    tri = "#FFFFFF" if t["key"] == "dark" else "#0F172A"
    return f"""
  <g>
    <animateTransform attributeName="transform" type="translate" values="-8 0;0 0;0 0;-8 0"
      keyTimes="0;0.18;0.85;1" dur="3.8s" calcMode="spline"
      keySplines="0.2 0.9 0.2 1;0 0 1 1;0.6 0 1 1" repeatCount="indefinite"/>
    <path d="M24 11 L41 40 H7 Z" fill="{tri}"/>
  </g>"""


def ic_bootstrap(t):
    return f"""
  <g transform="translate(24,24)">
    <animateTransform attributeName="transform" type="scale" values="1 1;-1 1;1 1" keyTimes="0;0.5;1"
      dur="4s" calcMode="spline" keySplines="0.4 0 0.6 1;0.4 0 0.6 1" additive="sum" repeatCount="indefinite"/>
    <rect x="-18" y="-18" width="36" height="36" rx="8" fill="#7952B6"/>
    <text x="0" y="8" text-anchor="middle" font-family="Georgia, 'Times New Roman', serif" font-size="26" font-weight="700" fill="#FFFFFF">B</text>
  </g>"""


def ic_alpinejs(t):
    return f"""
  <defs>
    <linearGradient id="alpg" x1="0" y1="1" x2="1" y2="0">
      <stop offset="0%" stop-color="#4EA8DE"/><stop offset="100%" stop-color="#8CC9E8"/>
    </linearGradient>
  </defs>
  <path d="M24 7 L43 41 H5 Z" fill="url(#alpg)">
    <animateTransform attributeName="transform" type="skewX" values="0;-7;0;7;0" dur="5s" repeatCount="indefinite"
      additive="sum"/>
  </path>
  <path d="M24 19 L34 38 H14 Z" fill="{t['card']}" opacity="0.85"/>"""


def ic_postman(t):
    return f"""
  <circle cx="24" cy="24" r="17" fill="#FF6C37" opacity="0.16"/>
  <circle cx="24" cy="24" r="17" fill="none" stroke="#FF6C37" stroke-width="2"/>
  <g>
    <animateTransform attributeName="transform" type="rotate" values="0 24 24;360 24 24" dur="6s"
      calcMode="spline" keySplines="0.5 0 0.5 1;0.5 0 0.5 1" repeatCount="indefinite"/>
    <path d="M16 30 L31 15 a5 5 0 0 1 7 7 L23 37 L14 38 Z" fill="#FF6C37"/>
  </g>"""


def ic_vscode(t):
    body = "#007ACC" if t["key"] == "light" else "#2A8CD9"
    return f"""
  <path d="M33 6 L43 11 V37 L33 42 L17 27 L7 36 L5 34 V14 L7 12 L17 21 Z" fill="{body}"/>
  <path d="M33 15 V33 L22 24 Z" fill="{t['card']}" opacity="0.9">
    <animate attributeName="opacity" values="0.9;0.25;0.9" dur="2.6s" repeatCount="indefinite"/>
  </path>
  <path d="M7 12 L28 36" stroke="#FFFFFF" stroke-width="1.6" opacity="0.5"/>"""


ICONS = {
    "react": ("React", ic_react),
    "javascript": ("JavaScript", ic_js),
    "html5": ("HTML5", ic_html5),
    "css3": ("CSS3", ic_css3),
    "php": ("PHP", ic_php),
    "laravel": ("Laravel", ic_laravel),
    "flutter": ("Flutter", ic_flutter),
    "dart": ("Dart", ic_dart),
    "kotlin": ("Kotlin", ic_kotlin),
    "mysql": ("MySQL", ic_mysql),
    "sqlite": ("SQLite", ic_sqlite),
    "git": ("Git", ic_git),
    "docker": ("Docker", ic_docker),
    "tailwind": ("Tailwind", ic_tailwind),
    "figma": ("Figma", ic_figma),
    "vercel": ("Vercel", ic_vercel),
    "bootstrap": ("Bootstrap", ic_bootstrap),
    "alpinejs": ("Alpine.js", ic_alpinejs),
    "postman": ("Postman", ic_postman),
    "vscode": ("VS Code", ic_vscode),
}

ORDER = list(ICONS.keys())


def icon_svg(slug, theme):
    label, fn = ICONS[slug]
    name = f"{label} animated icon"
    uid = f"{slug}{theme['key']}"
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="64" height="64" viewBox="0 0 48 48" role="img" aria-label="{name}">
  <title>{name}</title>{fn(theme)}
</svg>"""


# ----------------------------------------------------------------------------------
# Glass strip: a row of tiles (glass card + animated logo + label)
# ----------------------------------------------------------------------------------

CARD_W, CARD_H, GAP, PAD = 104, 108, 14, 22


def glass_strip_svg(slugs, theme, uid, title):
    n = len(slugs)
    w = PAD * 2 + n * CARD_W + (n - 1) * GAP
    h = PAD * 2 + CARD_H
    cards = []
    for i, slug in enumerate(slugs):
        label, fn = ICONS[slug]
        x = PAD + i * (CARD_W + GAP)
        y = PAD
        cx = x + CARD_W / 2
        icon = f'<g transform="translate({x + CARD_W/2 - 24:.0f} {y + 20})" >{fn(theme)}</g>'
        cards.append(f"""
    <g>
      <rect x="{x}" y="{y}" width="{CARD_W}" height="{CARD_H}" rx="20" fill="{theme['card']}" fill-opacity="0.72"/>
      <rect x="{x}" y="{y}" width="{CARD_W}" height="{CARD_H}" rx="20" fill="url(#sheen{uid})"/>
      <rect x="{x+0.6:.1f}" y="{y+0.6:.1f}" width="{CARD_W-1.2}" height="{CARD_H-1.2}" rx="19.4" fill="none" stroke="{theme['stroke']}" stroke-opacity="0.9"/>
      <rect x="{x}" y="{y}" width="{CARD_W}" height="1.4" rx="0.7" fill="url(#edge{uid})" opacity="0.75">
        <animate attributeName="opacity" values="0.25;0.9;0.25" dur="{4 + i*0.3:.1f}s" repeatCount="indefinite"/>
      </rect>
      {icon}
      <text x="{cx:.0f}" y="{y + CARD_H - 16}" text-anchor="middle" font-family="{SANS}" font-size="11.5" font-weight="600" fill="{theme['dim']}">{label}</text>
    </g>""")
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{title}">
  <title>{title}</title>
  <defs>
    <linearGradient id="edge{uid}" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="{theme['accent']}"/><stop offset="50%" stop-color="{theme['accent2']}"/><stop offset="100%" stop-color="{theme['accent3']}"/>
    </linearGradient>
    <linearGradient id="sheen{uid}" x1="0" y1="0" x2="0.6" y2="1">
      <stop offset="0%" stop-color="{ '#FFFFFF' if theme['key']=='dark' else theme['accent'] }" stop-opacity="{0.10 if theme['key']=='dark' else 0.09}"/>
      <stop offset="100%" stop-color="{ '#FFFFFF' if theme['key']=='dark' else theme['accent2'] }" stop-opacity="0"/>
    </linearGradient>
  </defs>{''.join(cards)}
</svg>"""


# ----------------------------------------------------------------------------------
# Banner / hero
# ----------------------------------------------------------------------------------

def banner_svg(theme):
    t, uid = theme, theme["key"]
    w, h = 900, 300
    name_color = "#F2F7FF" if t["key"] == "dark" else "#0B1220"
    sub = t["dim"]
    role_line = "Full-Stack Developer  ·  UI/UX Designer"
    role_line2 = "AI-Assisted Builder  ·  SMK RPL · Grade XI"
    # small animated logos in the corner: keep the hero speaking the same language as the stack strip
    mini = [
        ("react", 700, 66),
        ("mysql", 756, 66),
        ("laravel", 812, 66),
    ]
    minis = []
    for slug, mx, my in mini:
        _, fn = ICONS[slug]
        minis.append(f'<g transform="translate({mx} {my}) scale(0.62)">{fn(theme)}</g>')

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="David Yehuda Surbakti - Full-Stack Developer">
  <title>David Yehuda Surbakti — Full-Stack Developer</title>{blob(t, uid)}
  <rect width="{w}" height="{h}" fill="{t['canvas']}"/>
  <rect width="{w}" height="{h}" fill="#FFFFFF" opacity="{0 if t['key']=='dark' else 0.42}"/>
  {aurora(t, uid, w, h, 0.62 if t == DARK else 0.5)}
  <rect width="{w}" height="{h}" fill="url(#edge{uid})" opacity="{0.05 if t['key']=='dark' else 0.04}"/>

  <!-- status pill -->
  <g transform="translate(56,54)">
    <rect x="0" y="0" width="176" height="30" rx="15" fill="{t['card']}" fill-opacity="0.8" stroke="{t['stroke']}"/>
    <circle cx="18" cy="15" r="4" fill="{t['accent2']}">
      <animate attributeName="opacity" values="1;0.3;1" dur="2.4s" repeatCount="indefinite"/>
    </circle>
    <text x="32" y="19.5" font-family="{SANS}" font-size="11.5" font-weight="600" letter-spacing="1.4" fill="{t['dim']}">OPEN TO COLLABORATE</text>
  </g>

  <!-- name -->
  <text x="56" y="164" font-family="{SANS}" font-size="46" font-weight="800" letter-spacing="-1.2" fill="{name_color}">David Yehuda Surbakti</text>
  <!-- underline draws itself, once -->
  <path d="M58 182 H470" stroke="url(#edge{uid})" stroke-width="4" stroke-linecap="round" fill="none" stroke-dasharray="412" stroke-dashoffset="412">
    <animate attributeName="stroke-dashoffset" values="412;0" dur="1.1s" begin="0.25s" fill="freeze"/>
  </path>
  <text x="56" y="212" font-family="{SANS}" font-size="14.5" font-weight="600" fill="{t['accent']}">{role_line}</text>
  <text x="56" y="234" font-family="{SANS}" font-size="13" fill="{sub}">{role_line2}</text>
  <text x="56" y="266" font-family="{SANS}" font-size="12.5" fill="{t['faint']}">Semarang, Indonesia  ·  building clean interfaces &amp; the logic behind them</text>

  {''.join(minis)}

  <!-- soft specular sweep across the whole card -->
  <g clip-path="url(#clip{uid})">
    <rect x="-320" y="-40" width="200" height="380" fill="#FFFFFF" opacity="{0.09 if t['key']=='dark' else 0.5}" transform="skewX(-14)">
      <animate attributeName="x" values="-340;1080" dur="7s" begin="1.6s" repeatCount="indefinite"/>
    </rect>
  </g>
  <rect x="0.6" y="0.6" width="{w-1.2}" height="{h-1.2}" rx="22" fill="none" stroke="{t['stroke']}" stroke-width="1.2"/>
  <defs>
    <clipPath id="clip{uid}"><rect x="1" y="1" width="{w-2}" height="{h-2}" rx="22"/></clipPath>
  </defs>
</svg>"""


def divider_svg(theme):
    t, w = theme, 900
    uid = "d" + theme["key"]
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="40" viewBox="0 0 {w} 40" role="img" aria-label="divider">
  <title>divider</title>
  <defs>
    <linearGradient id="dg{uid}" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="{t['stroke']}" stop-opacity="0"/>
      <stop offset="35%" stop-color="{t['accent']}" stop-opacity="0.7"/>
      <stop offset="65%" stop-color="{t['accent2']}" stop-opacity="0.7"/>
      <stop offset="100%" stop-color="{t['stroke']}" stop-opacity="0"/>
    </linearGradient>
  </defs>
  <rect x="0" y="19" width="{w}" height="1.6" fill="url(#dg{uid})"/>
  <g>
    <animateTransform attributeName="transform" type="translate" values="120 0;780 0;120 0" dur="16s"
      calcMode="spline" keySplines="0.45 0 0.55 1;0.45 0 0.55 1" keyTimes="0;0.5;1" repeatCount="indefinite"/>
    <circle cx="0" cy="20" r="3" fill="{t['accent2']}"/>
    <circle cx="0" cy="20" r="9" fill="none" stroke="{t['accent2']}" stroke-opacity="0.35"/>
  </g>
</svg>"""


def footer_svg(theme):
    t, uid = theme, theme["key"]
    w, h = 900, 150
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="footer">
  <title>footer</title>
  <defs>
    <linearGradient id="fe{uid}" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="{t['accent']}"/><stop offset="50%" stop-color="{t['accent2']}"/><stop offset="100%" stop-color="{t['accent3']}"/>
    </linearGradient>
  </defs>
  <rect width="{w}" height="{h}" rx="22" fill="{t['card']}" fill-opacity="{0.7 if t['key']=='dark' else 1}" stroke="{t['stroke']}"/>
  <path id="wv{uid}" d="M0 96 C150 62 300 122 450 92 C600 62 750 120 900 88" fill="none" stroke="url(#fe{uid})" stroke-width="2.4" stroke-opacity="0.7"/>
  <circle r="4.5" fill="{t['accent2']}">
    <animateMotion dur="11s" repeatCount="indefinite" rotate="auto" path="M0 96 C150 62 300 122 450 92 C600 62 750 120 900 88"/>
  </circle>
  <text x="450" y="128" text-anchor="middle" font-family="{SANS}" font-size="12.5" letter-spacing="1.6" fill="{t['faint']}">THANKS FOR SCROLLING  ·  LET'S BUILD SOMETHING TOGETHER</text>
</svg>"""


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def write(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.rstrip() + "\n")


def main():
    for theme in (DARK, LIGHT):
        suffix = theme["key"]
        for slug in ORDER:
            name = slug if suffix == "dark" else f"{slug}-light"
            write(os.path.join(TECH, f"{name}.svg"), icon_svg(slug, theme))

        chunks = [ORDER[0:7], ORDER[7:14], ORDER[14:20]]
        for i, ch in enumerate(chunks, start=1):
            write(os.path.join(OUT, f"stack-{i}-{suffix}.svg"),
                  glass_strip_svg(ch, theme, f"{i}{suffix}", "Tech stack"))

        write(os.path.join(OUT, f"banner-{suffix}.svg"), banner_svg(theme))
        write(os.path.join(OUT, f"divider-{suffix}.svg"), divider_svg(theme))
        write(os.path.join(OUT, f"footer-{suffix}.svg"), footer_svg(theme))

    import shutil
    import xml.etree.ElementTree as ET
    os.makedirs(LAB, exist_ok=True)
    for fn in sorted(os.listdir(OUT)):
        if fn.endswith(".svg"):
            shutil.copy2(os.path.join(OUT, fn), os.path.join(LAB, fn))

    n = 0
    for base in (OUT, TECH):
        for root, _, files in os.walk(base):
            for fn in files:
                if fn.endswith(".svg"):
                    ET.parse(os.path.join(root, fn))
                    n += 1
    print(f"OK: {n} svg files written + XML-valid  ({OUT} + {TECH})")


if __name__ == "__main__":
    main()
