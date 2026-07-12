#!/usr/bin/env python3
"""Fetch the Google Scholar citation count and update index.html."""

from pathlib import Path
import re
import sys

import requests
from bs4 import BeautifulSoup


SCHOLAR_ID = "dNhzCu4AAAAJ"
SCHOLAR_URL = f"https://scholar.google.com/citations?user={SCHOLAR_ID}&hl=en"
ROOT = Path(__file__).resolve().parent.parent
INDEX_PATH = ROOT / "index.html"


def fetch_citations() -> str:
    response = requests.get(
        SCHOLAR_URL,
        headers={
            "User-Agent": (
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            )
        },
        timeout=20,
    )
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    stats = soup.select("td.gsc_rsb_std")
    if not stats:
        raise RuntimeError("Google Scholar citation statistics were not found")

    citations = stats[0].get_text(strip=True)
    if not citations.replace(",", "").isdigit():
        raise RuntimeError(f"Unexpected citation value: {citations!r}")
    return citations


def update_html(citations: str) -> None:
    html = INDEX_PATH.read_text(encoding="utf-8")
    pattern = r'(<span id="scholar-citations">)[^<]*(</span>)'
    updated, count = re.subn(pattern, rf"\g<1>{citations}\g<2>", html, count=1)
    if count != 1:
        raise RuntimeError("Could not find the Scholar citation placeholder in index.html")
    INDEX_PATH.write_text(updated, encoding="utf-8")


def main() -> int:
    try:
        citations = fetch_citations()
        update_html(citations)
    except Exception as error:
        print(
            f"Scholar update skipped; keeping the last verified count: {error}",
            file=sys.stderr,
        )
        return 0

    print(f"Google Scholar citations updated to {citations}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
