"""Demo deck: How to choose a project management tool.
Every name, quote, price and score here is made up to show the engine. No real product or person.

Build:   python3 examples/demo/slides.py            (writes examples/demo/build/)
Render:  node engine/render.js examples/demo/build
Check:   python3 engine/check.py examples/demo/build
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "engine"))
import kit
from kit import ac
import components as c

theme = kit.load_theme(os.path.join(ROOT, "themes", sys.argv[2] if len(sys.argv) > 2 else "neutral.json"))
kit.set_steps(["Need", "Shortlist", "Trial"])

# Example person: no photo, so the quote card draws initials in a circle.
sam = {"name": "Sam Ortiz", "title": "Example quote, team lead", "photo": None}

slides = []

# 1 COVER
# Q: What is this, and is it for me?
# A: A short guide for team leads picking their first project tool.
# Outcome: a smart, informed decision.
slides.append(c.cover(
    f"Pick a project tool your team will {ac('still use')} in six months.",
    symbol="seed",
    tags=["For team leads", "Teams of 5 to 30", "Choosing a first tool"],
    byline="A 5-minute guide. Every name and number in it is an example."))

# 2 MAP
# Q: What will this take me through?
# A: Three steps, from "do we need this?" to a tool the team uses every day.
# Outcome: save time; control.
slides.append(c.step_map(
    [("Need", "Do you need a tool yet, and which features?", None),
     ("Shortlist", "How to judge any tool, and what a year costs.", None),
     ("Trial", "How to test two tools on real work.", "Step 3 ends with a sample scorecard")],
    ("A tool your team uses every day", "Picked together, tested on real work, priced for a year.", "check"),
    f"Three steps take you from {ac('“do we need this?”')} to a tool your team uses.",
    "Each step answers the next question you'll have."))

# 3 STEP 1: DO WE NEED ONE YET?
# Q: Do we need a tool yet?
# A: Yes, when your team loses track of work more than once a month.
# Outcome: save money (don't buy too early); save time.
slides.append(c.converge_decide(
    [("chat", "Tasks get lost in chat", "Someone asks, and nobody owns it."),
     ("person", "Nobody knows who owns what", "Two people do the same task."),
     ("calendar", "Status meetings run long", "You spend the hour asking for updates.")],
    "Did one of these happen twice this month?",
    "Pick a tool now.", "Check again next month.",
    f"You need a tool when your team {ac('loses track')} of work.", None,
    quote=kit.quote_card(sam, "We found out a task was late when the client asked about it."),
    step=1))

# 4 STEP 1: WHICH FEATURES?
# Q: Which features do we need?
# A: Answer four yes/no questions; every yes adds a feature to your list.
# Outcome: save money; a smart, informed decision.
slides.append(c.yes_adds_flow(
    [("board", "Do you plan work in one- or two-week cycles?", ["Boards", "Sprints"], None),
     ("person", "Do clients need to see your progress?", ["Guest access"], None),
     ("clock", "Do you bill clients by the hour?", ["Time tracking"], None),
     ("lock", "Do some projects need to stay private?", ["Permissions"], "Check this for each project.")],
    "Your list: every feature you said yes to. A tool that misses one is out.",
    f"{ac('Every yes')} adds a feature to your list.",
    "Features you said no to don't count when you compare tools.",
    step=1))

# 5 STEP 2: HOW DO WE JUDGE A TOOL?
# Q: How do we know a tool is good?
# A: Run five checks on each tool, in an afternoon.
# Outcome: control; a fair comparison.
slides.append(c.check_table(
    ("Ask any tool", "How to check", "Good sign"),
    [("person", "Can a new person use it on day one?", "Invite one teammate. Watch them add a task.", "They add it in under 5 minutes, with no help."),
     ("link", "Does it connect to your apps?", "Look for your chat and calendar apps in its list.", "Both are listed and take a few clicks to set up."),
     ("laptop", "Does it work on a phone?", "Install the app. Update a task from it.", "The phone app can do what the desktop does."),
     ("lock", "Who can see what?", "Make a private project. Log in as a guest.", "The guest sees only what you shared."),
     ("doc", "Can you take your data with you?", "Look for export in the settings.", "All tasks export to a spreadsheet file.")],
    f"Five checks you can run on {ac('any tool')} in an afternoon.",
    "Run the same five on each tool, so the comparison is fair.",
    step=2))

# 6 STEP 2: WHAT WILL IT COST?
# Q: What will a year cost us?
# A: People times monthly price times 12; in this example, $1,152.
# Outcome: save money; no surprises.
slides.append(c.number_hero(
    "Example &middot; price per year, 12 people", "$1,152",
    f"Do the math {ac('per year,')} not per month.",
    "People times price times 12. Here, $8 a month for each person becomes $1,152 a year.",
    chips_row=["12 people", "$8 per person per month", "12 months"],
    note="<b>Guests:</b> ask if they count as paid users.", note_icon="person",
    drivers_label="Your price depends on",
    drivers=["Team size", "Monthly or yearly billing", "The plan you pick", "Guest users", "Add-ons"],
    step=2))

# 7 STEP 3: HOW DO WE TEST IT?
# Q: How do we run the trial?
# A: Move one real project into two tools for two weeks, then score both together.
# Outcome: a smart decision the team agrees with.
slides.append(c.process_doc(
    [("search", "Pick two", "The two tools that passed the most checks."),
     ("board", "Move one project", "A real project, not a test one."),
     ("clock", "Run two weeks", "Everyone uses only the new tools."),
     ("team", "Decide together", "Score both. Pick the higher score.")],
    {"title": "Trial scorecard", "tag": "Sample", "mark": "",
     "fields": [("Team", "Your team"), ("Trial", "Two weeks, one real project"), ("Tools", "Tool A and Tool B")],
     "headers": ("Check", "Tool A / Tool B"),
     "rows": [("New person on day one", "Yes / No"), ("Connects to your apps", "Yes / Yes"),
              ("Works on a phone", "Yes / Yes"), ("Price per year, 12 people", "$1,152 / $1,440")]},
    f"Test two tools on {ac('real work')} for two weeks.",
    "Then score both with your team and pick the higher score.",
    step=3))

# 8 SOURCES
# Q: Where does each fact come from?
# A: In this demo, every fact is an example.
# Outcome: honesty.
slides.append(c.sources_page(
    [("1", "Written for this demo. Not advice about any real product."),
     ("3", "Sam Ortiz is a made-up person. The quote is an example."),
     ("6", "$8 per person per month is an example price, not the price of a real product."),
     ("7", "Tool A and Tool B are placeholders. Their scores and prices are examples.")],
    closing="Demo deck: every name, quote and number in it is an example."))

if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "build")
    kit.build(slides, out, theme, title="Choosing a project tool", config=os.path.join(HERE, "deck.json"))
