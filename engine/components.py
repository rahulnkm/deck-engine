"""deck-engine component bank: one function per layout pattern. Each returns one finished page (a <section>).

All words and data are arguments. Layout, sizes and colors are fixed here and in kit.py.
Every teaching component takes:
  lead  - the spoken lead line (30px). Wrap one phrase in kit.ac("...") for the accent.
  sup   - optional supporting line (21px).
  quote - optional kit.quote_card(person, text) shown at the bottom of the spoken column.
  step  - optional step number; shows the step strip (kit.set_steps or theme "steps").
See components/README.md for when to use each one.
"""
from kit import (C, section, column, ac, icon, icon_disc, chip, chips, photo, attribution, halftone,
                 arrow_right, lbl)

__all__ = ["cover", "step_map", "quote_row", "outcome_rows", "ev_quote", "ev_stat", "ev_stats",
           "converge_decide", "yes_adds_flow", "feature_cards", "bar_chart", "module_grid", "check_table",
           "two_path_compare", "fan_diagram", "direct_diagram", "number_hero", "process_doc",
           "question_cards", "stage_cards", "sources_page"]


def _page(vis, lead, sup=None, quote=None, step=None, vis_cls=""):
    return section(f'<div class="vis {vis_cls}">{vis}</div>{column(lead, sup, quote)}', step=step)


# ------------------------------------------------------------------ 1 cover
def cover(headline, symbol="seed", tags=None, byline=None, byline_icon="person"):
    """Opening page. headline: one sentence (use ac() once). symbol: "seed"/"branch"/"tree", raw SVG, or None.
    tags: who it's for, e.g. ["Team leads", "5-30 people"] (likeness). byline: optional small card line."""
    sym = ""
    if symbol:
        svg = halftone(symbol, 330, 430, step=8.5, rmax=3.9) if symbol in ("seed", "branch", "tree") else symbol
        sym = f'<div style="position:absolute;left:836px;top:150px">{svg}</div>'
    tg = f'<div class="ctags">{chips(tags, "lg")}</div>' if tags else ""
    by = (f'<div class="card rev"><div class="rev-dot">{icon(byline_icon, 22, C["muted"])}</div><div>{byline}</div></div>'
          if byline else "")
    return section(f'''<div style="position:absolute;left:84px;top:176px;width:700px">
  <h1 class="cover-h">{headline}</h1>{tg}{by}</div>{sym}''')


# ------------------------------------------------------------------ 2 step map
def step_map(steps, end, lead, sup=None, step=None):
    """The whole journey up front. steps: [(name, what it answers, tease or None)], 2-5 of them.
    end: (title, description, icon) - the outcome the reader holds at the end."""
    n = len(steps) + 1
    h = int((548 - 12 * (n - 1)) / n)
    rows = []
    for i, (name, q, tease) in enumerate(steps, 1):
        t = f'<div class="tease">{icon("star", 16, C["accent_edge"])}{tease}</div>' if tease else ""
        rows.append(f'''<div class="mrow" style="height:{h}px"><div class="mnode">{i}</div>
      <div class="card mcard"><div class="mname"><span class="lbl">Step {i}</span>{name}</div>
      <div class="mq">{q}</div>{t}</div></div>''')
    et, ed, ei = end
    rows.append(f'''<div class="mrow" style="height:{h}px"><div class="mnode end">{icon(ei, 22, "#fff")}</div>
    <div class="mcard dark"><div class="mname" style="color:#fff">{et}</div>
    <div class="mq" style="color:{C["dark_text"]}">{ed}</div></div></div>''')
    return _page(f'<div class="mline"></div>{"".join(rows)}', lead, sup, step=step)


# ------------------------------------------------------------------ 3 quote row
def quote_row(quotes, lead, sup=None, step=None, photo_size=92):
    """Recognition: "others feel this too". quotes: [(person, text)], 2-3. Real, sourced quotes only."""
    cards = "".join(f'<div class="card rcard">{photo(p, photo_size)}<div><div class="rq">“{t}”</div>{attribution(p)}</div></div>'
                    for p, t in quotes)
    return _page(cards, lead, sup, step=step, vis_cls="rgrid")


# ------------------------------------------------------------------ 4 outcome rows
def ev_quote(person, text, size=50):
    return (f'<div class="oq">{photo(person, size)}<div><div class="oqt">“{text}”</div>'
            f'{attribution(person, inline=True)}</div></div>')


def ev_stat(big, text, dots=None):
    """Evidence: one big number + a line. dots=(lit, total) draws a dot row above the line."""
    d = ""
    if dots:
        lit, total = dots
        d = '<div class="dots">' + "".join(f'<span class="dot{"" if i < lit else " off"}"></span>' for i in range(total)) + "</div>"
    return f'<div class="ostat"><div class="big">{big}</div><div>{d}<div class="otx">{text}</div></div></div>'


def ev_stats(pairs):
    """Evidence: two or three medium numbers side by side. pairs: [(number, line)]."""
    return '<div class="ostat two">' + "".join(f'<div><div class="mid">{n}</div><div class="otx">{t}</div></div>' for n, t in pairs) + "</div>"


def outcome_rows(rows, lead, sup=None, step=None):
    """What you get, backed by evidence. rows: [(icon, result, sub or None, evidence_html)], 3-5.
    Build evidence with ev_quote / ev_stat / ev_stats."""
    out = []
    for ic, title, sub, ev in rows:
        s = f'<div class="osub">{sub}</div>' if sub else ""
        out.append(f'<div class="card orow"><div class="oleft">{icon_disc(ic, 40)}<div><div class="otitle">{title}</div>{s}</div></div>'
                   f'<div class="oev">{ev}</div></div>')
    return _page("".join(out), lead, sup, step=step, vis_cls="ogrid")


# ------------------------------------------------------------------ 5 converge + decide
def converge_decide(sources, question, yes, no, lead, sup=None, quote=None, step=None,
                    yes_label="Yes", no_label="Not yet"):
    """Several triggers flow into one yes/no question. sources: [(icon, name, sub)], exactly 3."""
    m = C["muted"]
    ask = "".join(f'<div class="card asker">{icon_disc(ic, 52)}<div class="aname">{nm}</div><div class="asub">{sb}</div></div>'
                  for ic, nm, sb in sources)
    vis = f'''<div class="askrow">{ask}</div>
  <svg class="fl" width="776" height="90" viewBox="0 0 776 90" fill="none" stroke="{m}" stroke-width="1.5">
    <path d="M124 0v30h264M388 0v74M652 0v30H388"/><path d="m382 68 6 8 6-8" stroke-linejoin="round"/></svg>
  <div class="card decide">{question}</div>
  <svg class="fl" width="776" height="64" viewBox="0 0 776 64" fill="none" stroke="{m}" stroke-width="1.5">
    <path d="M388 0v18H200v38M388 18h188v38"/><path d="m194 50 6 8 6-8M570 50l6 8 6-8" stroke-linejoin="round"/></svg>
  <div class="forks">
    <div class="fork yes"><div class="flab">{yes_label}</div><div class="ftxt">{yes}</div></div>
    <div class="fork no"><div class="flab">{no_label}</div><div class="ftxt">{no}</div></div>
  </div>'''
    return _page(vis, lead, sup, quote, step)


# ------------------------------------------------------------------ 6 yes-adds flow
def yes_adds_flow(questions, summary, lead, sup=None, step=None):
    """If/else flow where every yes adds chips to a list. questions: [(icon, question, [chips], note or None)], 3-4.
    summary: the dark bar at the bottom."""
    a, m = C["accent"], C["muted"]
    fl = []
    for ic, q, chs, note in questions:
        nt = f'<div class="fnote">{note}</div>' if note else ""
        fl.append(f'''<div class="frow"><div class="card fq">{icon(ic, 22)}<span>{q}</span></div>
      <div class="yes-arrow"><span>Yes</span><svg width="64" height="12" viewBox="0 0 64 12"><path d="M0 6h58M53 1.5 59 6l-6 4.5" fill="none" stroke="{a}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg></div>
      <div class="fchips">{chips(chs)}{nt}</div></div>''')
        fl.append(f'<div class="no-arrow"><svg width="12" height="26" viewBox="0 0 12 26"><path d="M6 0v20M1.5 15.5 6 21l4.5-5.5" fill="none" stroke="{m}" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg><span>No</span></div>')
    return _page(f'{"".join(fl)}<div class="flist">{summary}</div>', lead, sup, step=step)


# ------------------------------------------------------------------ 7 feature cards
def feature_cards(cards, lead, sup=None, step=None):
    """What each option does, with a concrete example. cards: up to 4 dicts:
    {"name": chip text, "icon": name, "does": one line, "example": text or None,
     "example_label": "Example", "alt": True to tint the example box (e.g. "When to add it")}."""
    out = []
    for c in cards:
        ex = c.get("example")
        exh = (f'<div class="pex{" alt" if c.get("alt") else ""}"><div class="lbl">{c.get("example_label", "Example")}</div>'
               f'<div class="pext">{ex}</div></div>') if ex else ""
        out.append(f'<div class="card pcard"><div class="ptop">{chip(c["name"])}{icon(c["icon"], 24, C["muted"])}</div>'
                   f'<div class="ppays">{c["does"]}</div>{exh}</div>')
    return _page("".join(out), lead, sup, step=step, vis_cls="pgrid")


# ------------------------------------------------------------------ 8 bar chart (+ optional timeline)
def bar_chart(title, rows, axis, lead, sup=None, quote=None, step=None, timeline=None):
    """Horizontal bars. rows: [(label, [(pct_of_track, segment_label)], value_text)]. axis: tick labels, e.g. ["0", "5", "10"].
    timeline (optional): {"label", "line", "span": text over the active span, "inside": text, "outside": text}."""
    rh = []
    for label, segs, val in rows:
        bars = "".join(f'<div class="lbar{" b2" if j % 2 else ""}" style="width:calc({p}% - {4 if j else 0}px)"><span>{sl}</span></div>'
                       for j, (p, sl) in enumerate(segs))
        rh.append(f'<div class="lrow"><div class="lname">{label}</div><div class="ltrack">{bars}</div><div class="lval">{val}</div></div>')
    ax = "".join(f"<span>{t}</span>" for t in axis)
    vis = f'<div class="card lcard">{lbl(title, "margin-bottom:22px")}{"".join(rh)}<div class="laxis">{ax}</div></div>'
    if timeline:
        t = timeline
        vis += f'''<div class="card ccard">{lbl(t["label"])}<div class="cline">{t["line"]}</div>
    <svg width="704" height="104" viewBox="0 0 704 104" style="margin-top:14px">
      <line x1="0" y1="47" x2="704" y2="47" stroke="{C["line"]}" stroke-width="2"/>
      <rect x="40" y="38" width="400" height="18" rx="9" fill="{C["accent_soft"]}"/>
      <text x="240" y="28" text-anchor="middle" class="svt" fill="{C["accent_edge"]}">{t["span"]}</text>
      <circle cx="300" cy="47" r="9" fill="{C["accent"]}"/>
      <text x="300" y="86" text-anchor="middle" class="svt" fill="{C["ink"]}">{t["inside"]}</text>
      <circle cx="580" cy="47" r="9" fill="#fff" stroke="{C["muted"]}" stroke-width="2"/>
      <text x="580" y="86" text-anchor="middle" class="svt" fill="{C["muted"]}">{t["outside"]}</text>
    </svg></div>'''
    return _page(vis, lead, sup, quote, step, vis_cls="lvis")


# ------------------------------------------------------------------ 9 module grid
def module_grid(items, lead, sup=None, step=None, label=None):
    """Icon grid of options, 2 columns, up to 10. items: [(icon, name, one plain line)]."""
    mc = "".join(f'<div class="card mod">{icon_disc(ic, 40)}<div><div class="mn">{n}</div><div class="mp">{p}</div></div></div>'
                 for ic, n, p in items)
    top = lbl(label, "margin-bottom:12px") if label else ""
    return _page(f'{top}<div class="mgrid">{mc}</div>', lead, sup, step=step)


# ------------------------------------------------------------------ 10 check table
def check_table(headers, rows, lead, sup=None, step=None):
    """Checks the reader can run themselves. headers: (ask, how to check, answer). rows: [(icon, ask, how, answer)], up to 5."""
    h1, h2, h3 = headers
    rh = "".join(f'<div class="card crow"><div class="c1">{icon_disc(ic, 36)}<span>{q}</span></div>'
                 f'<div class="c2">{how}</div><div class="c3">{ans}</div></div>' for ic, q, how, ans in rows)
    head = (f'<div class="chead"><div class="h1 lbl">{h1}</div><div class="h2 lbl">{h2}</div>'
            f'<div class="h3 lbl" style="color:{C["accent"]}">{h3}</div></div>')
    return _page(head + rh, lead, sup, step=step)


# ------------------------------------------------------------------ 11 two-path compare
def fan_diagram(start, middle, ends):
    """You -> middle -> three ends (e.g. You -> Agency -> 3 vendors)."""
    m, ink = C["muted"], C["ink"]
    e = "".join(f'<rect x="264" y="{y}" width="66" height="34" rx="8" fill="{C["subtle"]}"/>'
                f'<text x="297" y="{y + 22}" text-anchor="middle" class="svs">{t}</text>' for y, t in zip((6, 58, 110), ends))
    return f'''<svg width="330" height="150" viewBox="0 0 330 150" fill="none">
  <g stroke="{m}" stroke-width="1.5"><path d="M74 75h52M206 75c30 0 30-52 58-52M206 75h58M206 75c30 0 30 52 58 52"/></g>
  <rect x="0" y="56" width="74" height="38" rx="19" fill="{C["subtle"]}"/><text x="37" y="80" text-anchor="middle" class="svn">{start}</text>
  <rect x="126" y="56" width="80" height="38" rx="8" fill="{ink}"/><text x="166" y="80" text-anchor="middle" class="svn" style="fill:#fff">{middle}</text>
  {e}</svg>'''


def direct_diagram(start, target, sub=""):
    """You -> one target, direct."""
    return f'''<svg width="330" height="150" viewBox="0 0 330 150" fill="none">
  <path d="M74 75h90" stroke="{C["muted"]}" stroke-width="1.5"/>
  <rect x="0" y="56" width="74" height="38" rx="19" fill="{C["subtle"]}"/><text x="37" y="80" text-anchor="middle" class="svn">{start}</text>
  <rect x="164" y="48" width="140" height="54" rx="10" fill="{C["accent"]}"/><text x="234" y="{73 if sub else 80}" text-anchor="middle" class="svn" style="fill:#fff">{target}</text>
  <text x="234" y="91" text-anchor="middle" class="svs" style="fill:#fff">{sub}</text></svg>'''


def two_path_compare(left, right, lead, sup=None, step=None):
    """Two options side by side with an honest "Pick X if...". Each side: {"title", "desc", "diagram" (svg or ""),
    "pick", "items": [2-3 lines], "hl": True for the highlighted side}."""
    def col(d):
        li = "".join(f"<li>{t}</li>" for t in d["items"])
        return (f'<div class="card bcol{" hl" if d.get("hl") else ""}"><div class="bt">{d["title"]}</div><div class="bd">{d["desc"]}</div>'
                f'<div class="bsvg">{d.get("diagram", "")}</div><div class="bpick">{d["pick"]}</div><ul class="bul">{li}</ul></div>')
    return _page(col(left) + col(right), lead, sup, step=step, vis_cls="bgrid")


# ------------------------------------------------------------------ 12 number hero
def number_hero(label, number, lead, sup=None, chips_row=None, note=None, note_icon="doc",
                drivers_label=None, drivers=None, step=None):
    """One big number (price, time, count) + what drives it. number may contain <span class="dash">&ndash;</span>.
    chips_row: what the number includes. note: one line under a dashed rule. drivers: what moves the number."""
    pr = f'<div class="prow">{chips(chips_row, "lg")}</div>' if chips_row else ""
    nt = f'<div class="pdo">{icon(note_icon, 22, C["muted"])}<span>{note}</span></div>' if note else ""
    vis = f'<div class="card prc">{lbl(label)}<div class="pbig">{number}</div>{pr}{nt}</div>'
    if drivers:
        vis += (f'<div class="card pmove">{lbl(drivers_label or "Depends on")}<div class="mvrow">'
                + "".join(f"<span>{d}</span>" for d in drivers) + "</div></div>")
    return _page(vis, lead, sup, step=step, vis_cls="pvis")


# ------------------------------------------------------------------ 13 process + sample document
def process_doc(steps, doc, lead, sup=None, quote=None, step=None):
    """A short process row (3-4 actions, no step numbers) above a sample of the document the reader ends up with.
    steps: [(icon, name, one line)]; the last one is filled with the accent.
    doc: {"title", "tag": e.g. "Sample", "mark": small wordmark text or "", "fields": [(label, value)] x3,
          "headers": (col1, col2), "rows": [(a, b)]}."""
    fh = []
    for i, (ic, n, t) in enumerate(steps):
        last = i == len(steps) - 1
        fh.append(f'<div class="bnode">{icon_disc(ic, 44, C["accent"] if last else None, "#fff" if last else None)}'
                  f'<div class="bn">{n}</div><div class="bx">{t}</div></div>')
        if not last:
            fh.append(f'<div class="barr">{arrow_right()}</div>')
    fields = "".join(f'<div>{lbl(l)}<div class="cv">{v}</div></div>' for l, v in doc["fields"])
    h1, h2 = doc["headers"]
    rows = "".join(f"<tr><td>{a}</td><td>{b}</td></tr>" for a, b in doc["rows"])
    vis = f'''<div class="bflow">{"".join(fh)}</div>
  <div class="card coi">
    <div class="coih"><div><div class="coit">{doc["title"]}</div><div class="coisub">{doc.get("tag", "Sample")}</div></div><div class="wm2">{doc.get("mark", "")}</div></div>
    <div class="coigrid">{fields}</div>
    <table class="coitab"><tr><th class="lbl">{h1}</th><th class="lbl">{h2}</th></tr>{rows}</table>
  </div>'''
    return _page(vis, lead, sup, quote, step)


# ------------------------------------------------------------------ 14 question cards
def question_cards(questions, lead, sup=None, step=None):
    """Questions for the reader to bring (to a call, a vendor, a meeting). questions: [(icon, question, why)], 3."""
    cq = "".join(f'<div class="card cq">{icon_disc(ic, 56, None, None, 28)}<div><div class="cqq">{q}</div><div class="cqw">{w}</div></div></div>'
                 for ic, q, w in questions)
    return _page(cq, lead, sup, step=step, vis_cls="cqgrid")


# ------------------------------------------------------------------ 15 stage cards / timeline
def stage_cards(stages, lead, sup=None, step=None):
    """What changes over time or size. stages: 2-3 dicts:
    {"symbol": "seed"/"branch"/"tree"/svg, "name", "when", "intro", "prior": [gray chips carried over],
     "chips": [(chip, small note or "")], "value": e.g. a price or None, "value_note", "cur": True for "you are here"}."""
    sizes = {"seed": (110, 130, 5.5, 2.4), "branch": (124, 124, 5.0, 2.2), "tree": (120, 130, 5.5, 2.4)}
    chev = (f'<div class="schev"><svg width="14" height="22" viewBox="0 0 14 22"><path d="m3 3 8 8-8 8" fill="none" '
            f'stroke="{C["muted"]}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg></div>')
    out = []
    for s in stages:
        sym = s.get("symbol", "")
        if sym in sizes:
            w, h, st, r = sizes[sym]
            sym = halftone(sym, w, h, step=st, rmax=r)
        pri = "".join(f'<span class="chip gr">{c}</span>' for c in s.get("prior", ()))
        pri = f'<div class="sprior">{pri}</div><div class="splus">Plus:</div>' if pri else ""
        chs = "".join(f'<div class="schip">{chip(c)}{("<span class=sx>" + x + "</span>") if x else ""}</div>' for c, x in s.get("chips", ()))
        pr = (f'<div class="sprice"><div class="spv">{s["value"]}</div><div class="spn">{s.get("value_note", "")}</div></div>'
              if s.get("value") else "")
        out.append(f'<div class="card stg{" cur" if s.get("cur") else ""}"><div class="ssym">{sym}</div>'
                   f'<div class="sname">{s["name"]}</div><div class="swhen">{s["when"]}</div>'
                   f'<div class="sintro">{s["intro"]}</div>{pri}{chs}{pr}</div>')
    return _page(chev.join(out), lead, sup, step=step, vis_cls="sgrid")


# ------------------------------------------------------------------ 16 sources page
def sources_page(rows, title="Sources, by page", closing=None):
    """Last page: every fact's source, by page number. rows: [(page, text)]. closing: one line under a rule."""
    sl = "".join(f'<div class="srow"><div class="sp">{p}</div><div class="stx">{t}</div></div>' for p, t in rows)
    cl = f'<div class="edu">{closing}</div>' if closing else ""
    return section(f'''<div style="position:absolute;left:84px;top:96px;width:1112px">
  <h2 class="srch">{title}</h2><div class="scols">{sl}</div>{cl}</div>''')
