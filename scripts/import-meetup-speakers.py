#!/usr/bin/env python3
"""One-off import: pull real speaker names, titles, LinkedIn links and (where
available) full bios out of the saved Meetup group-events DOM export, into
src/content/speakers/*.yaml.

Not part of the app build — run manually with `python3 scripts/import-meetup-speakers.py`.
"""
import html
import re
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "data" / "meetupevents.html"
SPEAKERS_DIR = ROOT / "src" / "content" / "speakers"

# Organizers already have their own profiles under src/content/organizers/ —
# don't duplicate them here even though they're mentioned constantly as hosts.
ORGANIZERS = {"Nanddeep Nachan", "Siddharth Vaghasia", "Smita Nachan", "Kunj Sangani"}

# Same person, different name spelling across events — merge onto the fuller form.
NAME_MERGE = {
    "Varun S": "Varun Srinivas",
    "Dr. Gomathi S": "Dr. S. Gomathi",
    "Bhargavi Chakravarthi Rangarajan": "C R Bhargavi",
    "Prashant Bhoyar": "Prashant G Bhoyar",
    "Kamal Shree": "Kamal Shree Soundirapandian",
    "Kamal Shree Soundirapandian See": "Kamal Shree Soundirapandian",
}

# Noise from the free-text "by <Name>" fallback pass: generic role words and
# sentence fragments the regex over-matched (an organizer name glued to the
# next sentence because there was no punctuation break).
JUNK = {
    "Co-Host", "Host", "OpenAI", "Design", "Pune Tech Community", "Microsoft",
    "Meetup", "Microsoft MVPs", "AI Using Python", "Azure OpenAI Services",
    "Global AI Community. It", "Cosmos DB. Implementing Cosmos", "Semantic Search",
    "Using GitHub Copilot", "Using Pipelines",
    "Kunj Sangani Create", "Kunj Sangani Prompt Engineering", "Kunj Sangani This",
    "Nanddeep Nachan Global AI", "Nanddeep Nachan Policy",
    "Siddharth Vaghasia Configure", "Siddharth Vaghasia Using Azure",
    "Smita Nachan In", "Smita Nachan Understanding Embeddings",
}

DESC_OPEN = re.compile(
    r'<span class="ds2-r14 mt-ds2-4 line-clamp-3 w-full text-ds2-text-fill-tertiary-enabled" '
    r'style="font-family: NeuSans, Inter, system-ui, sans-serif;">'
)
NAME_WORD = r"[A-Z][\wÀ-ÖØ-öø-ÿ\.\'\-]*"
BY_NAME_RE = re.compile(
    rf'\bby\s+({NAME_WORD}(?:\s+{NAME_WORD}){{0,3}})(?:\s+and\s+({NAME_WORD}(?:\s+{NAME_WORD}){{0,3}}))?'
)
BIO_BLOCK_RE = re.compile(
    r"About the Speaker.*?</strong><br>\s*<strong>([^<]+)</strong>\s*(.*?)</p>\s*"
    r'(?:<p class="mb-ds2-10">Connect with[^<]*</p>\s*<ul[^>]*>(.*?)</ul>)?',
    re.S,
)
NAME_TITLE_LINKEDIN_RE = re.compile(
    r'<a href="(https://www\.linkedin\.com/in/[^"]*)"[^>]*>([^<]+)</a>\s*\(([^)]+)\)'
)


def literal_str_representer(dumper, data):
    style = "|" if "\n" in data else None
    return dumper.represent_scalar("tag:yaml.org,2002:str", data, style=style)


yaml.add_representer(str, literal_str_representer)


def slugify(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-")


def clean_text(text: str) -> str:
    text = re.sub(r"<[^>]+>", "", text)
    text = html.unescape(text)
    text = text.replace("*", "")
    text = re.sub(r"\s+", " ", text).strip().strip(",")
    return text


def clean_bio(html_text: str) -> str:
    text = re.sub(r"<br\s*/?>", "\n", html_text)
    text = re.sub(r"<[^>]+>", "", text)
    text = html.unescape(text).replace("*", "")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def canonical_name(name: str) -> str | None:
    name = name.strip()
    name = NAME_MERGE.get(name, name)
    if name in ORGANIZERS:
        return None
    return name


def extract_description_html(card: str) -> str:
    m = DESC_OPEN.search(card)
    if not m:
        return ""
    tag_re = re.compile(r"<span\b|</span>")
    depth = 1
    pos = m.end()
    inner = ""
    while depth > 0:
        tm = tag_re.search(card, pos)
        if not tm:
            return ""
        depth += -1 if tm.group() == "</span>" else 1
        pos = tm.end()
        if depth == 0:
            inner = card[m.end():tm.start()]
            break
    return inner


def main():
    content = SOURCE.read_text(encoding="utf-8")
    people: dict[str, dict] = {}

    def get(name: str) -> dict:
        return people.setdefault(name, {"name": name})

    # Tier 1: full bio blocks (name + real bio + optional LinkedIn)
    for m in BIO_BLOCK_RE.finditer(content):
        name = canonical_name(clean_text(m.group(1)))
        if not name:
            continue
        bio_body = clean_bio(m.group(2))
        linkedin = None
        if m.group(3):
            lm = re.search(r'href="(https://www\.linkedin\.com[^"]*)"', m.group(3))
            if lm:
                linkedin = lm.group(1)
        p = get(name)
        p["bio"] = f"{name} {bio_body}"
        if linkedin:
            p["linkedin"] = linkedin

    # Tier 2: "Name (Title)" linked speaker-list entries — the richest source
    # for the majority of people (real title + real LinkedIn, no prose bio).
    for linkedin, raw_name, raw_title in NAME_TITLE_LINKEDIN_RE.findall(content):
        name = canonical_name(clean_text(raw_name))
        if not name:
            continue
        title = clean_text(raw_title)
        if title.lower() in ("organizer", "organizers"):
            continue
        p = get(name)
        p.setdefault("linkedin", linkedin)
        # keep the longest/most descriptive title seen across events
        if len(title) > len(p.get("title", "")):
            p["title"] = title

    # Tier 3: bare "by <Name>" mentions in agenda text — name only, no title
    # or bio, for speakers not already covered by tier 1/2.
    parts = re.split(r'(?=data-eventref="\d+")', content)
    cards = [p for p in parts if p.startswith('data-eventref="')]
    for card in cards:
        text = re.sub(r"<[^>]+>", " ", extract_description_html(card))
        text = re.sub(r"\s+", " ", html.unescape(text))
        for m in BY_NAME_RE.finditer(text):
            for g in m.groups():
                if not g or g in JUNK:
                    continue
                name = canonical_name(g.strip())
                if name:
                    get(name)

    SPEAKERS_DIR.mkdir(parents=True, exist_ok=True)
    written = 0
    for data in people.values():
        slug = slugify(data["name"])
        with (SPEAKERS_DIR / f"{slug}.yaml").open("w", encoding="utf-8") as f:
            yaml.dump(data, f, allow_unicode=True, sort_keys=False, width=1000)
        written += 1

    with_bio = sum(1 for p in people.values() if "bio" in p)
    with_title_only = sum(1 for p in people.values() if "title" in p and "bio" not in p)
    name_only = written - with_bio - with_title_only
    print(f"Wrote {written} speaker files ({with_bio} with bio, {with_title_only} with title, {name_only} name-only)")


if __name__ == "__main__":
    main()
