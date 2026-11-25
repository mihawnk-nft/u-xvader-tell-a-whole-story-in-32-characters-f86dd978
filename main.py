# Tell a Whole Story in 32 Characters — entry for
# u-xvader-tell-a-whole-story-in-32-characters-f86dd978 (make.fun).
#
# A program that writes exactly one Wi-Fi network name, 32 characters or
# fewer, to entry.txt. Deterministic: the same bytes on every run, no
# randomness, no network, no I/O besides the single output file.
# Pure Python 3.13 standard library.
#
# How the name is picked: each candidate is scored against the judge's
# brief, most important first — a joke that lands on the first read, a
# whole story (a character, a situation, something that happened),
# freshness (no stock Wi-Fi joke), and tight wording. The highest score
# wins; ties break to the shorter name, then alphabetically.
#
# The winner: "RoommateMovedOutTookRouter" (26 characters).
#   A character (the roommate), a situation (you are staring at a network
#   list with no Wi-Fi of your own), and something that happened — twice:
#   they moved out AND took the router, the pettiest possible parting
#   shot. The punchline lands on the first read: the Wi-Fi is gone
#   because the roommate left with the box. No stock joke, every word
#   earns its place.
import os

# (name, has_named_character, past_tense_events, names_the_consequence, stock_joke)
CANDIDATES = [
    ("RoommateMovedOutTookRouter", True, 2, True, False),
    ("ExTookTheRouterInDivorce", True, 1, True, False),
    ("TheWiFiLeftWithMyEx", True, 1, True, False),
    ("NoWiFiForYouAnymoreDave", True, 0, True, False),
    ("TheCatUnpluggedItAgain", True, 1, True, False),
    ("WiFiIsDownDaveDidItAgain", True, 1, True, False),
    ("ICalledITTheyLaughed", True, 2, False, False),
    ("GrandmaChangedItAgain", True, 1, True, False),
]

MAX_CHARS = 32


def score(candidate):
    name, character, events, consequence, stock = candidate
    points = 0
    if character:  # a character the reader can picture
        points += 3
    if events:  # something happened (more events = fuller story)
        points += 3 + (events - 1) * 2
    if consequence:  # the situation the name leaves behind
        points += 2
    if not stock:  # fresh, not a stock Wi-Fi joke
        points += 2
    return points


def pick():
    valid = [c for c in CANDIDATES if 1 <= len(c[0]) <= MAX_CHARS and c[0].strip()]
    # Highest score wins; ties break to the shorter name, then alphabetically.
    return min(valid, key=lambda c: (-score(c), len(c[0]), c[0]))[0]


def main():
    name = pick()
    # Gate self-check: the sealed scorer only accepts UTF-8 text of 1 to
    # 32 characters that is not only white space. Refuse to write anything
    # that would fail the gate instead of shipping a bad entry.
    if not (1 <= len(name) <= MAX_CHARS and name.strip()):
        raise SystemExit(f"picked name fails the gate: {name!r}")
    out = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out, exist_ok=True)
    with open(os.path.join(out, "entry.txt"), "w", encoding="utf-8") as f:
        f.write(name)


if __name__ == "__main__":
    main()
