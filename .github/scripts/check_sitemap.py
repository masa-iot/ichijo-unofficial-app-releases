#!/usr/bin/env python3
"""docs/ の HTML ページと sitemap.xml を突き合わせる。

- noindex でないページは、すべて sitemap に載っていること
- sitemap の URL は、すべて noindex でない実在のページを指していること
- 各ページの canonical / og:url が、そのページ自身の URL であること

URL の基準は docs/CNAME のドメイン。
docs/index.html → /、docs/foo.html → /foo.html、docs/guide/x/index.html → /guide/x/
"""
import sys
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pathlib import Path

DOCS = Path(__file__).resolve().parents[2] / "docs"
SITEMAP_NS = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}


class HeadParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.noindex = False
        self.canonical = None
        self.og_url = None

    def handle_starttag(self, tag, attrs):
        a = {k: (v or "") for k, v in attrs}
        if tag == "meta":
            if a.get("name", "").lower() == "robots" and "noindex" in a.get("content", "").lower():
                self.noindex = True
            if a.get("property", "") == "og:url":
                self.og_url = a.get("content")
        elif tag == "link" and "canonical" in a.get("rel", "").lower().split():
            self.canonical = a.get("href")


def page_url(base, path):
    rel = path.relative_to(DOCS).as_posix()
    if rel == "index.html":
        return base + "/"
    if rel.endswith("/index.html"):
        return base + "/" + rel[: -len("index.html")]
    return base + "/" + rel


def main():
    base = "https://" + (DOCS / "CNAME").read_text(encoding="utf-8").strip()
    errors = []

    pages = {}
    for path in sorted(DOCS.rglob("*.html")):
        parser = HeadParser()
        parser.feed(path.read_text(encoding="utf-8"))
        url = page_url(base, path)
        rel = path.relative_to(DOCS).as_posix()
        pages[url] = (rel, parser.noindex)
        if parser.noindex:
            continue
        if parser.canonical != url:
            errors.append(f"{rel}: canonical が {parser.canonical!r}（正しくは {url!r}）")
        if parser.og_url is not None and parser.og_url != url:
            errors.append(f"{rel}: og:url が {parser.og_url!r}（正しくは {url!r}）")

    tree = ET.parse(DOCS / "sitemap.xml")
    locs = [el.text.strip() for el in tree.getroot().findall("sm:url/sm:loc", SITEMAP_NS)]
    for loc in sorted({l for l in locs if locs.count(l) > 1}):
        errors.append(f"sitemap.xml: {loc} が重複しています")
    locs = set(locs)

    for url, (rel, noindex) in sorted(pages.items()):
        if not noindex and url not in locs:
            errors.append(f"{rel}: sitemap.xml に {url} がありません")
    for loc in sorted(locs):
        if loc not in pages:
            errors.append(f"sitemap.xml: {loc} に対応するページが docs/ にありません")
        elif pages[loc][1]:
            errors.append(f"sitemap.xml: {loc} は noindex のページです")

    if errors:
        print("\n".join(errors))
        return 1
    print(f"OK: {len(locs)} ページ（noindex {sum(1 for _, n in pages.values() if n)} ページ）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
