"""Surveille l'apparition de la catégorie anti-gaspi sur un Drive Leclerc
et envoie une notification Telegram au passage absent -> présent."""

import json
import os
import re
import sys
import urllib.parse
import urllib.request
from pathlib import Path

from playwright.sync_api import sync_playwright

URL = os.environ.get(
    "DRIVE_URL", "https://m-courses.leclercdrive.fr/magasin-016301-016301"
)
PATTERN = re.compile(r"anti[\s\-]?gaspi", re.IGNORECASE)
STATE_FILE = Path("state/state.json")
BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]
MANUAL = os.environ.get("GITHUB_EVENT_NAME") == "workflow_dispatch"


def telegram(text: str) -> None:
    data = urllib.parse.urlencode({"chat_id": CHAT_ID, "text": text}).encode()
    req = urllib.request.Request(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", data=data
    )
    urllib.request.urlopen(req, timeout=20).read()


def check_page():
    """Retourne (présent, titre, taille_html, statut_http)."""
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(locale="fr-FR")
        response = page.goto(URL, wait_until="networkidle", timeout=60_000)
        page.wait_for_timeout(3_000)  # laisse le menu JS se charger
        html = page.content()
        title = page.title()
        status = response.status if response else None
        browser.close()
    return bool(PATTERN.search(html)), title, len(html), status


def load_state() -> bool:
    try:
        return json.loads(STATE_FILE.read_text())["present"]
    except Exception:
        return False


def save_state(present: bool) -> None:
    STATE_FILE.parent.mkdir(exist_ok=True)
    STATE_FILE.write_text(json.dumps({"present": present}))


def main() -> int:
    present, title, size, status = check_page()
    previous = load_state()
    print(f"HTTP={status} titre={title!r} taille_html={size}")
    print(f"présent={present} (avant: {previous})")

    if MANUAL:
        telegram(
            "✅ Test manuel\n"
            f"HTTP : {status}\n"
            f"Titre : {title}\n"
            f"Taille de la page : {size} caractères\n"
            f"Anti-gaspi présent : {present}"
        )

    if present and not previous:
        telegram(f"🛒 Paniers anti-gaspi disponibles !\n{URL}")
    elif previous and not present:
        telegram("Les paniers anti-gaspi ont disparu.")

    save_state(present)
    return 0


if __name__ == "__main__":
    sys.exit(main())