"""Rebuild the component gallery: one example page per bank component, then thumbs/ and gallery.png.

Usage (from the repo root):
    python3 components/build_gallery.py           # writes components/build/deck.html
    node engine/render.js components/build
    python3 engine/check.py components/build
    python3 components/build_gallery.py --thumbs  # writes components/thumbs/*.png and components/gallery.png
All content is generic example content. Every name, quote and number is made up.
"""
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, ".."))
sys.path.insert(0, os.path.join(ROOT, "engine"))
sys.path.insert(0, os.path.join(ROOT, "examples", "demo"))
import kit
from kit import ac
import components as c
import slides as demo  # the demo deck: reuses its pages for 8 of the 16 components

BUILD = os.path.join(HERE, "build")
D = demo.slides  # 0 cover, 1 map, 2 converge, 3 yes-flow, 4 check-table, 5 number, 6 process-doc, 7 sources

ana = {"name": "Ana Lee", "title": "Example quote, ops lead"}
ravi = {"name": "Ravi Mehta", "title": "Example quote, design lead"}
jo = {"name": "Jo Brandt", "title": "Example quote, agency owner"}

quote_row = c.quote_row(
    [(ana, "I spent Monday mornings asking who was doing what."),
     (ravi, "We tried three tools in a year. Nobody used any of them."),
     (jo, "Clients kept emailing to ask where their project was.")],
    f"Other team leads {ac('feel this too.')}",
    "These are example quotes. In a real deck, use real customers' words and photos.")

outcome_rows = c.outcome_rows(
    [("clock", "Status meetings get shorter", None, c.ev_stat("30 min", "saved each week, in this example")),
     ("person", "Every task has an owner", None, c.ev_quote(ana, "Now I open the board instead of asking around.")),
     ("money", "You know the cost for the year", "Priced before you buy.", c.ev_stats([("$1,152", "per year, example"), ("12", "people on the plan")])),
     ("link", "It works with the apps you use", None, c.ev_stat("2", "apps connected: chat and calendar", dots=(2, 2)))],
    f"Here's what a good tool {ac('gives you.')}",
    "Each result has a number or a person behind it.")

feature_cards = c.feature_cards(
    [{"name": "Boards", "icon": "board", "does": "Shows every task as a card you move from to-do to done.",
      "example": "You see at a glance that three tasks are stuck in review."},
     {"name": "Sprints", "icon": "calendar", "does": "Groups the work you plan to finish in one or two weeks.",
      "example": "On Monday the team picks 12 tasks. On Friday you see which ones are done."},
     {"name": "Guest access", "icon": "person", "does": "Lets a client see one project, and nothing else.",
      "example": "The client checks progress on their own, instead of emailing you."},
     {"name": "Time tracking", "icon": "clock", "does": "Records the hours spent on each task.",
      "example": "Add it if you bill clients by the hour.", "example_label": "When to add it", "alt": True}],
    f"Each feature solves a {ac('different problem.')}",
    "Boards show the work, sprints plan it, guests see it, and time tracking bills it.", step=1)

bar_chart = c.bar_chart(
    "Example &middot; days to set up", [
        ("Tool A", [(30, "Setup")], "3 days"),
        ("Tool B", [(30, "Setup"), (40, "Training")], "7 days")],
    ["0", "5 days", "10 days"],
    f"Setup time is {ac('part of the cost.')}",
    "Count the days your team spends getting started, not only the price.",
    timeline={"label": "Trial window: what counts", "line": "Score only what happens during the two-week trial.",
              "span": "Trial", "inside": "Problem during the trial: counts", "outside": "Problem after it: next review"},
    step=2)

module_grid = c.module_grid(
    [("board", "Boards", "Cards you move from to-do to done."),
     ("calendar", "Sprints", "Plan one or two weeks of work."),
     ("person", "Guest access", "Clients see one project."),
     ("clock", "Time tracking", "Hours spent on each task."),
     ("lock", "Permissions", "Choose who sees each project."),
     ("link", "App connections", "Chat and calendar in one place."),
     ("doc", "Docs", "Notes that live next to the tasks."),
     ("chat", "Comments", "Talk about a task on the task."),
     ("flag", "Goals", "Link tasks to what the team wants this quarter."),
     ("search", "Search", "Find any task in seconds.")],
    f"Here are {ac('10 common features.')} Pay only for the ones you need.",
    "Use your list from Step 1 to pick.", step=2, label="Example &middot; common features")

two_path = c.two_path_compare(
    {"title": "Consultant", "desc": "Sets up and compares several tools for you.",
     "diagram": c.fan_diagram("You", "Expert", ["Tool", "Tool", "Tool"]), "pick": "Pick a consultant if…",
     "items": ["You have no time to run a trial yourself.", "You need a tool set up for 50 or more people."]},
    {"title": "Do it yourself", "desc": "You test two tools with your own team.",
     "diagram": c.direct_diagram("You", "Your trial", "two tools"), "pick": "Do it yourself if…",
     "items": ["Your team has fewer than 30 people.", "You want the team to choose with you."], "hl": True},
    f"A consultant compares {ac('several tools')} for you. You can also do it yourself.",
    "If a consultant fits you better, use one.", step=2)

question_cards = c.question_cards(
    [("doc", "What happens to our data if we leave?", "So you can take your work with you."),
     ("person", "Do guests count as paid users?", "So the price per year has no surprises."),
     ("clock", "How long does setup take for a team our size?", "So you can plan the trial weeks.")],
    f"Ask every tool {ac('these three questions.')}",
    "Write down each answer, so you can compare them side by side.", step=2)

stage_cards = c.stage_cards(
    [{"symbol": "seed", "name": "5 to 15 people", "when": "Today", "intro": "You need:",
      "chips": [("Boards", ""), ("Comments", ""), ("App connections", "")],
      "value": "$480&ndash;1,440", "value_note": "per year, example prices", "cur": True},
     {"symbol": "branch", "name": "15 to 50 people", "when": "Next", "intro": "Everything before:",
      "prior": ["Boards", "Comments", "App connections"],
      "chips": [("Sprints", "plan work in cycles"), ("Permissions", "private projects")],
      "value": "$1,440&ndash;6,000", "value_note": "per year, example prices"},
     {"symbol": "tree", "name": "50+ people", "when": "Later", "intro": "Everything before:",
      "prior": ["Boards", "Comments", "App connections", "Sprints", "Permissions"],
      "chips": [("Goals", "link tasks to team goals")]}],
    f"As the team grows, you {ac('add features')} and seats.",
    "Pick a tool that has the next stage's features, so you don't have to switch.")

# (slug, title, page) in bank order
BANK = [
    ("01-cover", "Cover", D[0]),
    ("02-step-map", "Step map", D[1]),
    ("03-quote-row", "Quote row", quote_row),
    ("04-outcome-rows", "Outcome rows", outcome_rows),
    ("05-converge-decide", "Converge + decide", D[2]),
    ("06-yes-adds-flow", "Yes-adds flow", D[3]),
    ("07-feature-cards", "Feature cards", feature_cards),
    ("08-bar-chart", "Bar chart + timeline", bar_chart),
    ("09-module-grid", "Module grid", module_grid),
    ("10-check-table", "Check table", D[4]),
    ("11-two-path-compare", "Two-path compare", two_path),
    ("12-number-hero", "Number hero", D[5]),
    ("13-process-doc", "Process + sample document", D[6]),
    ("14-question-cards", "Question cards", question_cards),
    ("15-stage-cards", "Stage cards", stage_cards),
    ("16-sources-page", "Sources page", D[7]),
]


def thumbs():
    from PIL import Image, ImageDraw, ImageFont
    pdf = os.path.join(BUILD, "deck.pdf")
    tdir = os.path.join(HERE, "thumbs")
    os.makedirs(tdir, exist_ok=True)
    tmp = os.path.join(BUILD, "thumb")
    subprocess.run(["pdftoppm", "-png", "-scale-to", "640", pdf, tmp], check=True)
    files = sorted(f for f in os.listdir(BUILD) if f.startswith("thumb") and f.endswith(".png"))
    assert len(files) == len(BANK), (len(files), len(BANK))
    for f, (slug, _, _) in zip(files, BANK):
        os.replace(os.path.join(BUILD, f), os.path.join(tdir, slug + ".png"))
    # gallery: 4 columns, caption under each
    tw, th, gap, cap, cols = 420, 236, 24, 40, 4
    rows = (len(BANK) + cols - 1) // cols
    W, H = cols * tw + (cols + 1) * gap, rows * (th + cap) + (rows + 1) * gap
    g = Image.new("RGB", (W, H), "white")
    d = ImageDraw.Draw(g)
    font = ImageFont.truetype(os.path.join(ROOT, "engine", "fonts", "Geist-500.ttf"), 17)
    for i, (slug, title, _) in enumerate(BANK):
        x, y = gap + (i % cols) * (tw + gap), gap + (i // cols) * (th + cap + gap)
        im = Image.open(os.path.join(tdir, slug + ".png")).convert("RGB").resize((tw, th), Image.LANCZOS)
        g.paste(im, (x, y))
        d.rectangle([x, y, x + tw - 1, y + th - 1], outline="#e1e2e3")
        d.text((x, y + th + 10), f"{i + 1}. {title}", fill="#1c1e21", font=font)
    g.save(os.path.join(HERE, "gallery.png"), optimize=True)
    print("wrote", tdir, "and gallery.png")


if __name__ == "__main__":
    if "--thumbs" in sys.argv:
        thumbs()
    else:
        kit.build([p for _, _, p in BANK], BUILD, title="Component gallery",
                  config=os.path.join(ROOT, "examples", "demo", "deck.json"))
