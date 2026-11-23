"""deck-engine kit: the FIXED rendering engine. Do not rewrite it per deck.

Everything brand-specific comes from a theme (themes/*.json): colors, fonts, wordmark, steps.
The kit holds the page chrome (frame, wordmark, optional step strip), the primitives
(column, accent phrase, chips, cards, icons, icon discs, halftone "growth" symbols,
quote card with photo or initials), the CSS, and build().

A deck is ONE slides file:
    import kit, components as c
    theme = kit.load_theme("themes/neutral.json")
    slides = [c.cover(...), c.step_map(...), ...]
    kit.build(slides, "build/", theme, title="My deck", config="deck.json")
then:  node engine/render.js build/   and   python3 engine/check.py build/
"""
import glob
import json
import math
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))

# ---------------------------------------------------------------- theme
# C is mutated in place by set_theme(), so `from kit import C` always sees the active theme.
DEFAULT_THEME = {
    "name": "neutral",
    "wordmark": "deck",
    "steps": None,
    "colors": {
        "bg": "#f6f6f5", "frame": "#e6e6e4", "card": "#ffffff",
        "ink": "#1c1e21", "gray": "#4a4d52", "muted": "#7a7d82", "line": "#e1e2e3",
        "subtle": "#eceded", "track": "#f2f3f3",
        "accent": "#2f56c8", "accent_edge": "#1f3f9e", "accent_soft": "#dfe6fa",
        "accent_tint": "#f2f5fd", "accent_on_dark": "#86a2f0",
        "dark": "#1c1e21", "dark_text": "#c9cbce", "done": "#2f9e5b",
        "wordmark": None,
    },
    "fonts": {
        "sans": "Geist",
        "sans_files": {"400": "Geist-400.ttf", "500": "Geist-500.ttf", "600": "Geist-600.ttf", "700": "Geist-700.ttf"},
        "serif": "Instrument Serif",
        "serif_file": "InstrumentSerif-Italic.ttf",
        "font_dir": None,
    },
}

THEME = json.loads(json.dumps(DEFAULT_THEME))
C = dict(THEME["colors"])
STEPS = []


def set_theme(theme):
    """Activate a theme dict (merged over the defaults). Call before composing slides."""
    global THEME
    t = json.loads(json.dumps(DEFAULT_THEME))
    for k, v in (theme or {}).items():
        if isinstance(v, dict) and isinstance(t.get(k), dict):
            t[k].update(v)
        else:
            t[k] = v
    if not t["colors"].get("wordmark"):
        t["colors"]["wordmark"] = t["colors"]["accent"]
    THEME = t
    C.clear()
    C.update(t["colors"])
    set_steps(t.get("steps"))
    return t


def load_theme(path):
    """Read a theme JSON file and activate it. Relative font_dir resolves against the JSON file."""
    with open(path) as f:
        t = json.load(f)
    fd = t.get("fonts", {}).get("font_dir")
    if fd and not os.path.isabs(fd):
        t["fonts"]["font_dir"] = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(path)), fd))
    return set_theme(t)


def set_steps(names):
    """Step names for the strip at the top of step pages, e.g. ["Need", "Shortlist", "Trial"]. None = no strip."""
    STEPS[:] = list(names or [])


set_theme(DEFAULT_THEME)

# Card shadow drawn as stacked ZERO-BLUR layers. A blurred CSS shadow becomes an /SMask image
# in the PDF, which some viewers draw as a gray box. Never add a blur radius.
SHADOW = ("0 2px 0 0 rgba(26,26,26,.03), 0 4px 0 1px rgba(26,26,26,.022), "
          "0 6px 0 3px rgba(26,26,26,.016), 0 9px 0 5px rgba(26,26,26,.012), "
          "0 12px 0 8px rgba(26,26,26,.008), 0 15px 0 11px rgba(26,26,26,.005)")

# ---------------------------------------------------------------- people + quotes
_PHOTOS = {}  # basename -> absolute source path, copied into build_dir/photos/


def _initials(name):
    parts = [p for p in name.replace(".", " ").split() if p[:1].isalpha()]
    return ((parts[0][0] + (parts[-1][0] if len(parts) > 1 else "")) if parts else "?").upper()


def photo(person, size):
    """Round photo for person = {"name", "title", "photo": path or None}. No photo -> initials in a circle.
    Photos must be JPEGs with no transparency (check.py fails on any other image type)."""
    p = person.get("photo")
    if p:
        src = os.path.abspath(p)
        base = os.path.basename(src)
        _PHOTOS[base] = src
        return (f'<div class="ph" style="width:{size}px;height:{size}px">'
                f'<img src="photos/{base}" alt="{person["name"]}"></div>')
    return (f'<div class="ph ini" style="width:{size}px;height:{size}px;font-size:{round(size * 0.38)}px">'
            f'{_initials(person["name"])}</div>')


def attribution(person, inline=False):
    t = person.get("title", "")
    sep = ", " if inline else "<br>"
    return f'<div class="attr"><b>{person["name"]}</b>{sep + t if t else ""}</div>'


def quote_card(person, text, size=46, qsize=20):
    """Column quote card (bottom of the spoken column): accent left border, serif quote, photo + attribution."""
    return (f'<div class="card qcard"><div class="qt" style="font-size:{qsize}px">“{text}”</div>'
            f'<div class="who">{photo(person, size)}{attribution(person)}</div></div>')


# ---------------------------------------------------------------- icons (simple line icons, 24px grid)
ICONS = {
    "building": '<path d="M4 21V5.5L12 3v18"/><path d="M12 8.5h8V21"/><path d="M2.5 21h19"/><path d="M7 8h2M7 12h2M7 16h2M15 12h2M15 16h2"/>',
    "investor": '<circle cx="9" cy="7.5" r="3.3"/><path d="M3 20c.7-3.7 3.1-5.6 6-5.6s5.3 1.9 6 5.6"/><circle cx="18" cy="11" r="3.2"/><path d="M18 9.4v3.2"/>',
    "key": '<circle cx="7.5" cy="12" r="4"/><path d="M11.5 12H21M17.5 12v3.5M20.5 12v2.5"/>',
    "person": '<circle cx="12" cy="7.5" r="3.6"/><path d="M4.5 20.5c.9-4.2 3.8-6.3 7.5-6.3s6.6 2.1 7.5 6.3"/>',
    "team": '<circle cx="6" cy="7" r="2.3"/><circle cx="12" cy="5.8" r="2.3"/><circle cx="18" cy="7" r="2.3"/><path d="M2.5 14.5h19M5 14.5V20M19 14.5V20"/><path d="M3.5 12.5c.5-1.7 1.4-2.6 2.5-2.6M20.5 12.5c-.5-1.7-1.4-2.6-2.5-2.6M9 12.5c.5-2 1.6-3 3-3s2.5 1 3 3"/>',
    "bug": '<rect x="7.5" y="7.5" width="9" height="12" rx="4.5"/><path d="M12 11v8.5M7.5 12H3.5M20.5 12h-4M7.5 16.5l-3.5 2M16.5 16.5l3.5 2M8.5 8.5 6 5.5M15.5 8.5 18 5.5"/>',
    "laptop": '<rect x="4.5" y="5" width="15" height="10.5" rx="1.2"/><path d="M2 19h20"/>',
    "lock": '<rect x="5" y="10.5" width="14" height="10" rx="1.6"/><path d="M8 10.5V7.5a4 4 0 0 1 8 0v3"/><path d="M12 14.5v2.5"/>',
    "chip": '<rect x="6.5" y="6.5" width="11" height="11" rx="1.4"/><rect x="9.5" y="9.5" width="5" height="5"/><path d="M9.5 3v3.5M14.5 3v3.5M9.5 17.5V21M14.5 17.5V21M3 9.5h3.5M3 14.5h3.5M17.5 9.5H21M17.5 14.5H21"/>',
    "shield": '<path d="M12 3 19.5 6v5.5c0 4.6-3.1 8-7.5 9.5-4.4-1.5-7.5-4.9-7.5-9.5V6z"/><path d="m8.8 12 2.3 2.3 4.3-4.6"/>',
    "clock": '<circle cx="12" cy="12" r="8.5"/><path d="M12 7.5V12l3 2"/>',
    "doc": '<path d="M6 3h8.5L19 7.5V21H6z"/><path d="M14 3v5h5M9 12h7M9 15.5h7M9 18.5h4"/>',
    "search": '<circle cx="10.5" cy="10.5" r="6"/><path d="m15 15 5.5 5.5"/>',
    "flag": '<path d="M5.5 21V3.5"/><path d="M5.5 4h12l-2.5 4 2.5 4h-12"/>',
    "chat": '<path d="M4 5h16v11H9l-5 4z"/><path d="M8 9.5h8M8 12.5h5"/>',
    "calendar": '<rect x="3.5" y="5" width="17" height="15.5" rx="1.6"/><path d="M3.5 10h17M8 3v4M16 3v4"/>',
    "board": '<rect x="3" y="4" width="18" height="16" rx="1.6"/><path d="M9 4v16M15 4v16"/><path d="M5 8h2M11 8h2M11 11h2M17 8h2"/>',
    "money": '<rect x="2.5" y="6" width="19" height="12" rx="1.6"/><circle cx="12" cy="12" r="2.8"/><path d="M6 9v6M18 9v6"/>',
    "link": '<path d="M10 14a4 4 0 0 0 5.7 0l3-3a4 4 0 0 0-5.7-5.7l-1 1"/><path d="M14 10a4 4 0 0 0-5.7 0l-3 3a4 4 0 0 0 5.7 5.7l1-1"/>',
    "star": '<path d="m12 3.5 2.6 5.4 5.9.8-4.3 4.1 1 5.8L12 16.8l-5.2 2.8 1-5.8-4.3-4.1 5.9-.8z"/>',
    "check": '<circle cx="12" cy="12" r="8.5"/><path d="m8.3 12.2 2.5 2.5 4.9-5.2"/>',
}


def icon(name, size=22, color=None, sw=1.7):
    color = color or C["ink"]
    return (f'<svg class="ic" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" '
            f'stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round">{ICONS[name]}</svg>')


def icon_disc(name, d=44, bg=None, color=None, isz=None):
    bg, color = bg or C["accent_soft"], color or C["accent_edge"]
    isz = isz or int(d * 0.5)
    return f'<div class="disc" style="width:{d}px;height:{d}px;background:{bg}">{icon(name, isz, color)}</div>'


def arrow_right(w=18, color=None):
    color = color or C["muted"]
    return (f'<svg width="{w}" height="12" viewBox="0 0 {w} 12"><path d="M0 6h{w - 4}M{w - 8} 1.5 {w - 3} 6l-5 4.5" fill="none" '
            f'stroke="{color}" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg>')


CHECK_SVG = ('<svg width="11" height="11" viewBox="0 0 12 12"><path d="M2.5 6.3 5 8.7 9.6 3.6" fill="none" '
             'stroke="#fff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>')

# ---------------------------------------------------------------- halftone "growth" symbols (SVG dots)
# seed = start / small, branch = growing, tree = grown. Use them for stages, sizes or maturity levels.


def _ell(x, y, cx, cy, rx, ry, ang):
    a = math.radians(ang)
    dx, dy = x - cx, y - cy
    u = dx * math.cos(a) + dy * math.sin(a)
    v = -dx * math.sin(a) + dy * math.cos(a)
    return (u / rx) ** 2 + (v / ry) ** 2


def _seg(x, y, x1, y1, x2, y2):
    px, py = x2 - x1, y2 - y1
    t = max(0, min(1, ((x - x1) * px + (y - y1) * py) / (px * px + py * py)))
    return math.hypot(x - (x1 + t * px), y - (y1 + t * py))


def field_seed(x, y):
    shade = 0.45 + 0.55 * min(1, math.hypot(x - 0.36, y - 0.42) / 0.5)
    d = _ell(x, y, 0.5, 0.62, 0.27, 0.33, -18)
    if d < 1:
        return shade * (0.75 + 0.25 * d)
    for (cx, cy, rx, ry, ang) in ((0.40, 0.17, 0.12, 0.05, -35), (0.62, 0.15, 0.13, 0.05, 30)):
        if _ell(x, y, cx, cy, rx, ry, ang) < 1:
            return 0.8
    if _seg(x, y, 0.53, 0.30, 0.51, 0.20) < 0.014:
        return 0.9
    return 0


def field_branch(x, y):
    x1, y1, x2, y2 = 0.10, 0.94, 0.88, 0.10
    if _seg(x, y, x1, y1, x2, y2) < 0.016:
        return 0.95
    best = 0
    for i, t in enumerate((0.20, 0.34, 0.48, 0.62, 0.76)):
        px, py = x1 + t * (x2 - x1), y1 + t * (y2 - y1)
        ang = 20 if i % 2 == 0 else 250
        a = math.radians(ang)
        cx, cy = px + 0.14 * math.cos(a), py + 0.14 * math.sin(a)
        if _ell(x, y, cx, cy, 0.145, 0.07, ang) < 1:
            best = max(best, 0.5 + 0.45 * min(1, math.hypot(x - 0.2, y - 0.9) / 0.9))
    if _ell(x, y, 0.93, 0.06, 0.07, 0.035, -45) < 1:
        best = max(best, 0.9)
    return best


def field_tree(x, y):
    if 0.455 < x < 0.545 and 0.58 < y < 0.95:
        return 0.95
    if _seg(x, y, 0.5, 0.70, 0.36, 0.56) < 0.02 or _seg(x, y, 0.5, 0.66, 0.65, 0.53) < 0.02:
        return 0.9
    best = 0
    for (cx, cy, r) in ((0.5, 0.33, 0.25), (0.30, 0.45, 0.17), (0.70, 0.45, 0.17), (0.5, 0.50, 0.16)):
        d = math.hypot(x - cx, y - cy) / r
        if d < 1:
            best = max(best, 0.4 + 0.55 * min(1, math.hypot(x - 0.35, y - 0.2) / 0.55))
    return best




def field_sprout(x, y):
    """Pre-seed & Seed symbol: a seed lying on its side with a stem and two open leaves (reads as a sprout)."""
    d = _ell(x, y * 1.3, 0.50, 0.75 * 1.3, 0.33, 0.17, -14)
    if d < 1:
        return 0.5 + 0.5 * min(1, math.hypot(x - 0.36, y - 0.70) / 0.3)
    for i in range(12):
        def p(t): return (0.50 + 0.035 * math.sin(t * 2 * math.pi * 0.75), 0.66 - 0.40 * t)
        (x1, y1), (x2, y2) = p(i / 12), p((i + 1) / 12)
        if _seg(x, y, x1, y1, x2, y2) < 0.024:
            return 0.95
    if _ell(x, y, 0.33, 0.22, 0.17, 0.075, 25) < 1:
        return 0.85
    if _ell(x, y, 0.68, 0.17, 0.185, 0.08, -30) < 1:
        return 0.85
    return 0


def field_branch2(x, y):
    """Series A symbol: straight stem, paired leaves at even spacing, shrinking toward the tip."""
    x1, y1, x2, y2 = 0.12, 0.92, 0.84, 0.14
    L = math.hypot(x2 - x1, y2 - y1)
    ux, uy = (x2 - x1) / L, (y2 - y1) / L
    if _seg(x, y, x1, y1, x2, y2) < 0.017:
        return 0.95
    base = math.degrees(math.atan2(uy, ux))
    best = 0
    for i, t in enumerate((0.24, 0.42, 0.60, 0.78)):
        px, py = x1 + t * (x2 - x1), y1 + t * (y2 - y1)
        k = 1 - 0.14 * i
        rx, ry = 0.13 * k, 0.062 * k
        for side in (1, -1):
            ang = base + side * 58
            a = math.radians(ang)
            cx, cy = px + rx * math.cos(a), py + rx * math.sin(a)
            if _ell(x, y, cx, cy, rx, ry, ang) < 1:
                best = max(best, 0.6 + 0.35 * (1 - t))
    a = math.radians(base)
    if _ell(x, y, x2 + 0.05 * math.cos(a), y2 + 0.05 * math.sin(a), 0.07, 0.038, base) < 1:
        best = max(best, 0.8)
    return best


FIELDS = {"seed": field_sprout, "branch": field_branch2, "tree": field_tree,
          "seed-round": field_seed, "branch-curved": field_branch}


def halftone(field, w, h, step=8.0, rmax=3.6, color=None):
    """Draw a field (function or "seed"/"branch"/"tree") as a halftone of SVG dots (vector, no images)."""
    field = FIELDS.get(field, field) if isinstance(field, str) else field
    color = color or C["accent"]
    dots, row, y = [], 0, step / 2
    while y < h:
        x = step / 2 + (step / 2 if row % 2 else 0)
        while x < w:
            v = field(x / w, y / h)
            if v > 0.04:
                dots.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{rmax * math.sqrt(min(1, v)):.2f}"/>')
            x += step
        y += step * 0.866
        row += 1
    return f'<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}" fill="{color}">' + "".join(dots) + "</svg>"


# ---------------------------------------------------------------- page chrome + text primitives

def frame():
    wm = THEME.get("wordmark")
    return ('<div class="fr" style="left:64px;top:0;width:1px;height:720px"></div>'
            '<div class="fr" style="left:1216px;top:0;width:1px;height:720px"></div>'
            '<div class="fr" style="left:0;top:72px;width:1280px;height:1px"></div>'
            '<div class="fr" style="left:0;top:664px;width:1280px;height:1px"></div>'
            + (f'<div class="wm">{wm}</div>' if wm else ""))


def strip(cur):
    """Step strip: finished steps get a check, the current one is an accent pill, later ones are gray."""
    if not STEPS:
        return ""
    out = ['<div class="strip">']
    for i, name in enumerate(STEPS, 1):
        if i < cur:
            out.append(f'<div class="st done"><span class="ck">{CHECK_SVG}</span>Step {i} {name}</div>')
        elif i == cur:
            out.append(f'<div class="st cur">Step {i} {name}</div>')
        else:
            out.append(f'<div class="st">Step {i} {name}</div>')
    out.append("</div>")
    return "".join(out)


def section(body, step=None, cls=""):
    """One 1280x720 page. step=N shows the step strip with step N current."""
    return f'<section class="{cls}">{frame()}{strip(step) if step else ""}{body}</section>'


def column(lead, sup=None, quote=None):
    """The spoken column on the right (~290px): lead line 30px, supporting line 21px, optional quote card at the bottom."""
    s = f'<div class="col"><p class="lead">{lead}</p>'
    if sup:
        s += f'<p class="sup">{sup}</p>'
    if quote:
        s += quote
    return s + "</div>"


def ac(t):
    """Accent phrase: serif italic in the accent color. One per lead line."""
    return f'<em class="ac">{t}</em>'


def chip(t, cls=""):
    return f'<span class="chip {cls}">{t}</span>'


def chips(items, cls=""):
    return "".join(chip(t, cls) for t in items)


def card(body, cls="", style=""):
    return f'<div class="card {cls}" style="{style}">{body}</div>'


def lbl(t, style=""):
    return f'<div class="lbl" style="{style}">{t}</div>'


# ---------------------------------------------------------------- CSS
CSS = """
@page{size:1280px 720px;margin:0}
*{box-sizing:border-box}
html,body{margin:0;padding:0;background:var(--bg)}
section{width:1280px;height:720px;position:relative;overflow:hidden;background:var(--bg);break-after:page;
  font-family:var(--sans),sans-serif;color:var(--ink);-webkit-font-smoothing:antialiased}
section:last-child{break-after:auto}
.fr{position:absolute;background:var(--frame)}
.wm{position:absolute;left:84px;top:20px;font:700 27px/1 var(--sans);color:var(--wordmark);letter-spacing:-.055em}
.strip{position:absolute;right:84px;top:22px;display:flex;gap:8px}
.st{height:28px;padding:0 13px;border-radius:14px;font:500 13px/28px var(--sans);color:var(--muted);background:var(--subtle);display:flex;align-items:center;gap:7px;white-space:nowrap}
.st.cur{background:var(--accent);color:#fff}
.st.done{background:var(--card);color:var(--ink);padding-left:6px;box-shadow:inset 0 0 0 1px var(--line)}
.ck{width:18px;height:18px;border-radius:5px;background:var(--done);display:flex;align-items:center;justify-content:center}
.vis{position:absolute;left:84px;top:96px;width:776px;height:548px}
.col{position:absolute;left:906px;top:96px;width:290px;height:548px}
.lead{font:500 30px/1.18 var(--sans);letter-spacing:-.025em;margin:0;color:var(--ink)}
.ac{font-family:var(--serif),serif;font-style:italic;font-weight:400;color:var(--accent);font-size:1.12em;letter-spacing:0;line-height:1}
.sup{font:400 21px/1.4 var(--sans);color:var(--gray);margin:18px 0 0;letter-spacing:-.01em}
.card{background:var(--card);border-radius:10px;box-shadow:SHADOW}
.chip{display:inline-block;background:var(--accent-soft);color:var(--accent-edge);font:600 14px/1 var(--sans);padding:7px 10px;border-radius:6px;white-space:nowrap}
.chip.lg{font-size:16px;padding:9px 13px}
.chip.gr{background:var(--subtle);color:var(--muted);font-size:13px;padding:6px 8px}
.lbl{font:600 11px/1.2 var(--sans);letter-spacing:.1em;text-transform:uppercase;color:var(--muted)}
.ph{border-radius:50%;overflow:hidden;flex:none;background:var(--subtle)}
.ph img{width:100%;height:100%;display:block;object-fit:cover}
.ph.ini{display:flex;align-items:center;justify-content:center;background:var(--accent-soft);color:var(--accent-edge);font-family:var(--sans);font-weight:600;letter-spacing:-.02em}
.attr{font:400 12px/1.35 var(--sans);color:var(--muted)}
.attr b{font-weight:600;color:var(--gray)}
.disc{border-radius:50%;display:flex;align-items:center;justify-content:center;flex:none}
.ic{display:block;flex:none}
.qcard{position:absolute;left:0;right:0;bottom:0;border-left:4px solid var(--accent);padding:18px 18px 16px 18px}
.qt{font-family:var(--serif),serif;font-style:italic;line-height:1.22;color:var(--ink)}
.who{display:flex;align-items:center;gap:11px;margin-top:14px}
.btn{display:inline-block;background:var(--accent);color:#fff;font:600 16px/1 var(--sans);padding:14px 20px;border-radius:8px;box-shadow:0 4px 0 0 var(--accent-edge)}
/* cover */
.cover-h{font:500 58px/1.08 var(--sans);letter-spacing:-.035em;margin:0;color:var(--ink)}
.cover-h .ac{font-size:1.1em}
.ctags{display:flex;gap:8px;margin-top:30px;flex-wrap:wrap}
.rev{display:flex;align-items:center;gap:14px;margin-top:40px;padding:14px 20px 14px 14px;font:400 16px/1.35 var(--sans);color:var(--gray);width:fit-content;max-width:640px}
.rev-dot{width:44px;height:44px;border-radius:50%;background:var(--subtle);display:flex;align-items:center;justify-content:center;flex:none}
/* step map */
.mline{position:absolute;left:21px;top:40px;bottom:40px;width:2px;background:var(--accent-soft)}
.mrow{position:relative;display:flex;align-items:center;gap:22px;margin-bottom:12px}
.mrow:last-child{margin-bottom:0}
.mnode{width:44px;height:44px;border-radius:50%;background:var(--accent);color:#fff;font:600 18px/44px var(--sans);text-align:center;flex:none;position:relative;z-index:1;box-shadow:0 4px 0 0 var(--accent-edge)}
.mnode.end{background:var(--dark);box-shadow:0 4px 0 0 #000;display:flex;align-items:center;justify-content:center}
.mcard{flex:1;height:100%;padding:16px 24px;display:flex;flex-direction:column;justify-content:center;position:relative}
.mcard.dark{background:var(--dark);border-radius:10px}
.mname{font:600 21px/1.2 var(--sans);letter-spacing:-.015em;display:flex;align-items:baseline;gap:12px}
.mq{font:400 16px/1.35 var(--sans);color:var(--gray);margin-top:6px;max-width:440px}
.tease{position:absolute;right:20px;top:50%;transform:translateY(-50%);display:flex;align-items:center;gap:8px;background:var(--accent-soft);color:var(--accent-edge);font:600 14px/1.25 var(--sans);padding:10px 14px;border-radius:8px;max-width:190px}
/* quote row */
.rgrid{display:flex;flex-direction:column;gap:16px}
.rcard{flex:1;display:flex;align-items:center;gap:28px;padding:20px 30px 20px 26px;border-left:4px solid var(--accent)}
.rq{font-family:var(--serif),serif;font-style:italic;font-size:31px;line-height:1.16;color:var(--ink);margin-bottom:10px}
.rcard .attr{font-size:13px}
/* outcome rows */
.ogrid{display:flex;flex-direction:column;gap:11px}
.orow{flex:1;display:flex;align-items:center;padding:0 20px 0 18px;gap:20px}
.oleft{width:290px;display:flex;align-items:center;gap:14px;flex:none}
.otitle{font:600 17px/1.25 var(--sans);letter-spacing:-.01em}
.osub{font:400 13px/1.3 var(--sans);color:var(--muted);margin-top:3px}
.oev{flex:1;border-left:1px solid var(--line);padding-left:20px;min-height:64px;display:flex;align-items:center}
.oq{display:flex;align-items:center;gap:14px}
.oqt{font-family:var(--serif),serif;font-style:italic;font-size:18px;line-height:1.18;color:var(--ink);margin-bottom:4px}
.ostat{display:flex;align-items:center;gap:16px}
.ostat.two{gap:34px}
.big{font:600 34px/1 var(--sans);letter-spacing:-.03em;color:var(--accent);white-space:nowrap}
.mid{font:600 24px/1 var(--sans);letter-spacing:-.02em;color:var(--ink);margin-bottom:5px}
.otx{font:400 15px/1.3 var(--sans);color:var(--gray)}
.dots{display:flex;gap:5px;margin-bottom:7px}
.dot{width:11px;height:11px;border-radius:50%;background:var(--accent)}
.dot.off{background:var(--subtle)}
/* converge + decide */
.askrow{display:flex;gap:20px}
.asker{flex:1;height:178px;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;padding:0 22px}
.aname{font:600 20px/1.2 var(--sans);margin-top:14px}
.asub{font:400 15px/1.3 var(--sans);color:var(--gray);margin-top:6px}
.fl{display:block}
.decide{width:400px;margin:0 auto;height:66px;display:flex;align-items:center;justify-content:center;text-align:center;font:600 20px/1.2 var(--sans);border:2px solid var(--ink);padding:0 16px}
.forks{display:flex;justify-content:space-between;padding:0 48px}
.fork{width:304px;height:132px;border-radius:10px;display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center}
.fork.yes{background:var(--accent);color:#fff;box-shadow:0 4px 0 0 var(--accent-edge)}
.fork.no{background:var(--card);box-shadow:SHADOW}
.flab{font:600 11px/1 var(--sans);letter-spacing:.1em;text-transform:uppercase;opacity:.85;margin-bottom:10px}
.fork.no .flab{color:var(--muted)}
.ftxt{font:600 22px/1.25 var(--sans);letter-spacing:-.015em;padding:0 20px}
/* yes-adds flow */
.frow{display:flex;align-items:center;height:94px}
.fq{width:440px;height:94px;display:flex;align-items:center;gap:14px;padding:0 20px;font:500 17px/1.3 var(--sans)}
.yes-arrow{width:96px;position:relative;display:flex;justify-content:center;font:600 13px/1 var(--sans);color:var(--accent)}
.yes-arrow span{position:absolute;top:-19px;left:0;right:0;text-align:center}
.fchips{display:flex;flex-wrap:wrap;gap:8px;align-items:center;width:240px}
.fnote{width:100%;font:400 14px/1.3 var(--sans);color:var(--muted);margin-top:2px}
.no-arrow{height:28px;display:flex;align-items:center;gap:8px;padding-left:214px;font:600 13px/1 var(--sans);color:var(--muted)}
.flist{margin-top:4px;height:52px;border-radius:10px;background:var(--dark);color:#fff;font:500 16px/1.3 var(--sans);display:flex;align-items:center;padding:0 22px;width:776px}
/* feature cards */
.pgrid{display:grid;grid-template-columns:1fr 1fr;grid-auto-rows:1fr;gap:16px}
.pcard{padding:22px 24px;display:flex;flex-direction:column}
.ptop{display:flex;justify-content:space-between;align-items:center}
.ppays{font:600 19px/1.3 var(--sans);letter-spacing:-.012em;margin-top:16px;margin-bottom:14px}
.pex{margin-top:auto;background:var(--bg);border-radius:8px;padding:12px 14px}
.pex.alt{background:var(--accent-tint)}
.pext{font:400 15px/1.38 var(--sans);color:var(--gray);margin-top:6px}
/* bar chart + timeline */
.lvis{display:flex;flex-direction:column;gap:20px}
.lcard{padding:28px 30px 24px;flex:1;display:flex;flex-direction:column;justify-content:center}
.lrow{display:flex;align-items:center;gap:18px;margin-bottom:20px}
.lname{width:170px;font:600 17px/1.2 var(--sans);flex:none}
.ltrack{flex:1;height:44px;background:var(--track);border-radius:8px;display:flex;gap:4px;overflow:hidden}
.lbar{height:44px;background:var(--accent);border-radius:8px;display:flex;align-items:center;padding-left:14px;flex:none}
.lbar.b2{background:var(--accent-on-dark)}
.lbar span{font:600 13px/1 var(--sans);color:#fff;white-space:nowrap}
.lval{width:72px;font:600 22px/1 var(--sans);letter-spacing:-.02em;text-align:right;flex:none}
.laxis{display:flex;justify-content:space-between;margin-left:188px;margin-right:90px;font:500 13px/1 var(--sans);color:var(--muted)}
.ccard{padding:26px 30px 20px;flex:1;display:flex;flex-direction:column;justify-content:center}
.cline{font:500 18px/1.35 var(--sans);margin-top:10px}
.svt{font:500 14px var(--sans)}
.svn{font:600 15px var(--sans);fill:var(--ink)}
.svs{font:500 13px var(--sans);fill:var(--gray)}
/* module grid */
.mgrid{display:grid;grid-template-columns:1fr 1fr;gap:10px 14px}
.mod{height:94px;display:flex;align-items:center;gap:16px;padding:0 20px}
.mn{font:600 17px/1.2 var(--sans);letter-spacing:-.01em}
.mp{font:400 15px/1.3 var(--sans);color:var(--gray);margin-top:3px}
/* check table */
.chead{display:flex;padding:0 0 0 20px;height:24px;margin-bottom:6px}
.chead .h1{width:226px}.chead .h2{width:232px;padding-left:18px}.chead .h3{padding-left:20px}
.crow{display:flex;align-items:center;height:94px;margin-bottom:10px;padding:0 0 0 20px;overflow:hidden}
.crow:last-child{margin-bottom:0}
.c1{width:226px;display:flex;align-items:center;gap:12px;font:600 16px/1.25 var(--sans);flex:none}
.c2{width:232px;font:400 15px/1.35 var(--sans);color:var(--gray);padding:0 18px;flex:none}
.c3{flex:1;font:500 15px/1.35 var(--sans);color:var(--ink);padding:0 20px;align-self:stretch;display:flex;align-items:center;background:var(--accent-tint)}
/* two-path compare */
.bgrid{display:flex;gap:16px}
.bcol{flex:1;padding:26px 24px;display:flex;flex-direction:column}
.bcol.hl{box-shadow:inset 0 0 0 2px var(--accent), SHADOW}
.bt{font:600 24px/1.1 var(--sans);letter-spacing:-.02em}
.bd{font:400 16px/1.35 var(--sans);color:var(--gray);margin-top:6px}
.bsvg{flex:1;display:flex;align-items:center;justify-content:center}
.bpick{font:600 18px/1.2 var(--sans);padding-top:18px;border-top:1px solid var(--line)}
ul.bul{list-style:none;padding:0;margin:12px 0 0}
ul.bul li{position:relative;padding-left:20px;font:400 16px/1.38 var(--sans);color:var(--gray);margin-bottom:10px}
ul.bul li:before{content:'';position:absolute;left:2px;top:8px;width:8px;height:8px;border-radius:50%;background:var(--accent)}
/* number hero */
.pvis{display:flex;flex-direction:column;gap:18px}
.prc{padding:30px 34px 28px;flex:1;display:flex;flex-direction:column;justify-content:center}
.pbig{white-space:nowrap;font:600 104px/1 var(--sans);letter-spacing:-.05em;color:var(--ink);margin:18px 0 22px}
.pbig .dash{color:var(--accent);margin:0 4px}
.prow{display:flex;gap:10px;flex-wrap:wrap}
.pdo{display:flex;align-items:center;gap:12px;margin-top:22px;padding-top:20px;border-top:1px dashed var(--line);font:400 17px/1.35 var(--sans);color:var(--gray)}
.pdo b{color:var(--ink);font-weight:600}
.pmove{padding:26px 34px 28px}
.mvrow{display:flex;gap:10px;margin-top:14px;flex-wrap:wrap}
.mvrow span{font:500 15px/1 var(--sans);padding:10px 13px;border-radius:8px;background:var(--track);color:var(--ink)}
/* process + sample document */
.bflow{display:flex;align-items:flex-start;height:150px}
.bnode{flex:1;display:flex;flex-direction:column;align-items:flex-start;min-width:0}
.bn{font:600 18px/1.2 var(--sans);margin-top:12px}
.bx{font:400 15px/1.35 var(--sans);color:var(--gray);margin-top:5px;padding-right:6px}
.barr{width:32px;padding-top:16px;display:flex;justify-content:center;flex:none}
.coi{margin-top:10px;padding:22px 30px 16px;border-top:6px solid var(--accent);height:388px;overflow:hidden}
.coih{display:flex;justify-content:space-between;align-items:flex-start;padding-bottom:14px;border-bottom:1px solid var(--line)}
.coit{font:600 24px/1.1 var(--sans);letter-spacing:-.02em}
.coisub{display:inline-block;margin-top:8px;font:600 11px/1 var(--sans);letter-spacing:.1em;text-transform:uppercase;color:var(--accent-edge);background:var(--accent-soft);padding:5px 8px;border-radius:4px}
.wm2{font:700 22px/1 var(--sans);color:var(--wordmark);letter-spacing:-.055em}
.coigrid{display:grid;grid-template-columns:1fr 1fr 1.5fr;gap:16px;margin:16px 0 18px}
.cv{font:500 15px/1.3 var(--sans);margin-top:6px}
.coitab{width:100%;border-collapse:collapse}
.coitab th{text-align:left;padding:8px 0;border-bottom:1px solid var(--line)}
.coitab td{font:400 15px/1.2 var(--sans);padding:12px 0;border-bottom:1px solid var(--track)}
.coitab td:last-child{font-weight:500}
/* question cards */
.cqgrid{display:flex;flex-direction:column;gap:16px}
.cq{flex:1;display:flex;align-items:center;gap:24px;padding:0 32px 0 26px}
.cqq{font:500 23px/1.25 var(--sans);letter-spacing:-.018em}
.cqw{font:400 16px/1.35 var(--sans);color:var(--muted);margin-top:8px}
/* stage cards */
.sgrid{display:flex;align-items:stretch}
.stg{flex:1;padding:22px 22px;display:flex;flex-direction:column;min-width:0}
.stg.cur{box-shadow:inset 0 0 0 2px var(--accent), SHADOW}
.ssym{height:120px;display:flex;align-items:flex-end;justify-content:center;margin-bottom:14px}
.sname{font:600 21px/1.15 var(--sans);letter-spacing:-.015em}
.swhen{font:600 11px/1 var(--sans);letter-spacing:.1em;text-transform:uppercase;color:var(--muted);margin-top:8px}
.stg.cur .swhen{color:var(--accent)}
.sintro{font:400 15px/1.3 var(--sans);color:var(--gray);margin:16px 0 8px;padding-top:14px;border-top:1px solid var(--line)}
.schip{margin-bottom:8px}
.sprior{display:flex;flex-wrap:wrap;gap:6px}
.splus{font:400 15px/1.3 var(--sans);color:var(--gray);margin:14px 0 8px}
.sx{display:block;font:400 14px/1.3 var(--sans);color:var(--muted);margin-top:4px}
.sprice{margin-top:auto;padding-top:14px;border-top:1px solid var(--line)}
.spv{font:600 22px/1 var(--sans);letter-spacing:-.03em;white-space:nowrap}
.spn{font:400 13px/1.35 var(--sans);color:var(--muted);margin-top:6px}
.schev{width:34px;display:flex;align-items:center;justify-content:center;flex:none}
/* sources */
.srch{font:500 30px/1.1 var(--sans);letter-spacing:-.025em;margin:0 0 22px}
.scols{column-count:2;column-gap:44px}
.srow{display:flex;gap:12px;break-inside:avoid;margin-bottom:11px}
.sp{width:26px;flex:none;font:600 13px/1.4 var(--sans);color:var(--accent)}
.stx{font:400 13px/1.42 var(--sans);color:var(--gray)}
.edu{margin-top:14px;padding-top:14px;border-top:1px solid var(--line);font:500 15px/1.3 var(--sans);color:var(--ink)}
""".replace("SHADOW", SHADOW)


def theme_css(theme=None):
    """@font-face rules + :root color variables for a theme."""
    t = theme or THEME
    f, c = t["fonts"], t["colors"]
    out = []
    for w, file in sorted(f.get("sans_files", {}).items()):
        out.append(f"@font-face{{font-family:'{f['sans']}';src:url(fonts/{file}) format('truetype');font-weight:{w};font-style:normal}}")
    if f.get("serif_file"):
        out.append(f"@font-face{{font-family:'{f['serif']}';src:url(fonts/{f['serif_file']}) format('truetype');font-weight:400;font-style:italic}}")
    v = {k.replace("_", "-"): val for k, val in c.items() if val}
    v["sans"] = f"'{f['sans']}'"
    v["serif"] = f"'{f['serif']}'"
    out.append(":root{" + ";".join(f"--{k}:{val}" for k, val in v.items()) + "}")
    return "\n".join(out) + "\n"


def build(slides, out_dir, theme=None, title="Deck", extra_css="", config=None):
    """Write out_dir/deck.html with fonts/ and photos/ beside it (and deck.json if config is given).
    Then run:  node engine/render.js out_dir   and   python3 engine/check.py out_dir"""
    if theme is not None and theme is not THEME:
        set_theme(theme)
    os.makedirs(out_dir, exist_ok=True)
    fdir = os.path.join(out_dir, "fonts")
    os.makedirs(fdir, exist_ok=True)
    for src in [os.path.join(HERE, "fonts"), THEME["fonts"].get("font_dir")]:
        if src and os.path.isdir(src):
            for fp in glob.glob(os.path.join(src, "*.ttf")) + glob.glob(os.path.join(src, "*.otf")):
                shutil.copy(fp, fdir)
    if _PHOTOS:
        os.makedirs(os.path.join(out_dir, "photos"), exist_ok=True)
        for base, src in _PHOTOS.items():
            shutil.copy(src, os.path.join(out_dir, "photos", base))
    if config:
        shutil.copy(config, os.path.join(out_dir, "deck.json"))
    html = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<title>{title}</title>
<style>{theme_css()}{CSS}{extra_css}</style></head>
<body>
{''.join(slides)}
</body></html>
"""
    p = os.path.join(out_dir, "deck.html")
    with open(p, "w") as f:
        f.write(html)
    print(f"wrote {p}: {len(slides)} slides")
    return p
