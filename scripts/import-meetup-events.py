#!/usr/bin/env python3
"""One-off import: parse a saved Meetup group-events DOM export into
src/content/events/*.yaml + public/uploads/events/*.jpg.

Not part of the app build — run manually with `python3 scripts/import-meetup-events.py`
whenever there's a fresh Meetup export to (re)import.
"""
import html
import re
import ssl
import sys
import urllib.request
from datetime import datetime
from pathlib import Path

import certifi
import yaml

SSL_CONTEXT = ssl.create_default_context(cafile=certifi.where())

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "data" / "meetupevents.html"
EVENTS_DIR = ROOT / "src" / "content" / "events"
IMAGES_DIR = ROOT / "public" / "uploads" / "events"

DESC_OPEN = re.compile(
    r'<span class="ds2-r14 mt-ds2-4 line-clamp-3 w-full text-ds2-text-fill-tertiary-enabled" '
    r'style="font-family: NeuSans, Inter, system-ui, sans-serif;">'
)


def slugify(text: str) -> str:
    text = html.unescape(text).lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-")


def extract_description(card: str) -> str:
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
        if tm.group() == "</span>":
            depth -= 1
        else:
            depth += 1
        pos = tm.end()
        if depth == 0:
            inner = card[m.end():tm.start()]
            break
    text = re.sub(r"<br\s*/?>", "\n", inner)
    text = re.sub(r"<[^>]+>", "", text)
    text = html.unescape(text)
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def classify_tag(title: str) -> str:
    t = title.lower()

    def has(*phrases):
        return any(p in t for p in phrases)

    if has("sharepoint", "spfx", "onedrive", "outlook", "viva", "teams", "m365", "syntex", "microsoft 365"):
        return "M365"
    if has(".net conf", ".net ", "blazor", "maui", "playwright", "vs code"):
        return ".NET"
    if has(
        "power platform", "power apps", "power automate", "power bi", "power pages",
        "power fx", "dataverse", "connector", "connectors", "low code", "low-code",
    ):
        return "Power Platform"
    if has("azure", "aks", "devops", "kubernetes", "vpn", "pim", "cosmos db", "active directory"):
        return "Azure"
    if has(
        " ai ", "ai/", "/ai", " ai,", "ai:", "ai)", "ai-", " ai#", "copilot", "openai",
        "chatgpt", "nlp", "machine learning", " ml ", "generative", "agent",
    ) or t.startswith("ai ") or t.endswith(" ai") or t.endswith(" ai?"):
        return "AI"
    return "Community"


def literal_str_representer(dumper, data):
    style = "|" if "\n" in data else None
    return dumper.represent_scalar("tag:yaml.org,2002:str", data, style=style)


yaml.add_representer(str, literal_str_representer)


def main():
    content = SOURCE.read_text(encoding="utf-8")
    parts = re.split(r'(?=data-eventref="\d+")', content)
    cards = [p for p in parts if p.startswith('data-eventref="')]
    print(f"Found {len(cards)} event cards")

    EVENTS_DIR.mkdir(parents=True, exist_ok=True)
    IMAGES_DIR.mkdir(parents=True, exist_ok=True)

    seen_slugs = set()
    written = 0
    for card in cards:
        m_id = re.search(r'data-eventref="(\d+)"', card)
        m_href = re.search(r'href="(https://www\.meetup\.com/pune-tech-community/events/\d+)[^"]*"', card)
        m_title = re.search(r'<h3[^>]*title="([^"]*)"', card)
        m_time = re.search(r'<time[^>]*datetime="([^"]*)"', card)
        m_loc = re.search(r'<span class="truncate">([^<]*)</span>', card)
        m_img = re.search(r'src="(https://secure\.meetupstatic\.com[^"]*)"', card)

        if not (m_id and m_href and m_title and m_time):
            print("  skipping card, missing required field", file=sys.stderr)
            continue

        event_id = m_id.group(1)
        meetup_url = m_href.group(1) + "/"
        title = html.unescape(m_title.group(1))
        location = html.unescape(m_loc.group(1)).strip() if m_loc else "TBD"
        description = extract_description(card) or title

        dt_raw = m_time.group(1)
        dt_clean = re.sub(r"\[[^\]]*\]$", "", dt_raw)  # strip trailing [Asia/Kolkata]
        dt = datetime.fromisoformat(dt_clean)

        date_str = dt.strftime("%Y-%m-%d")
        time_str = dt.strftime("%-I:%M %p IST")
        tag = classify_tag(title)
        fmt = "Virtual" if location.lower() == "online" else "In-person"

        slug = slugify(title)
        filename = f"{slug}-{event_id}"
        seen_slugs.add(filename)

        image_field = None
        if m_img:
            image_url = m_img.group(1)
            image_path = IMAGES_DIR / f"{event_id}.jpg"
            try:
                with urllib.request.urlopen(image_url, context=SSL_CONTEXT) as resp, image_path.open("wb") as f:
                    f.write(resp.read())
                image_field = f"/uploads/events/{event_id}.jpg"
            except Exception as exc:
                print(f"  warning: failed to download image for {event_id}: {exc}", file=sys.stderr)

        data = {
            "title": title,
            "date": date_str,
            "time": time_str,
            "tag": tag,
            "format": fmt,
            "location": location,
            "description": description,
            "meetupUrl": meetup_url,
        }
        if image_field:
            data["image"] = image_field

        out_path = EVENTS_DIR / f"{filename}.yaml"
        with out_path.open("w", encoding="utf-8") as f:
            yaml.dump(data, f, allow_unicode=True, sort_keys=False, default_flow_style=False, width=1000)
        written += 1

    print(f"Wrote {written} event files to {EVENTS_DIR}")


if __name__ == "__main__":
    main()
