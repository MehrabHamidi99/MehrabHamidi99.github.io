#!/usr/bin/env python3
"""Check generated routes, metadata, assets, anchors, and public content before deploy."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote
import json
import sys
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1] / '_site'

class Page(HTMLParser):
    def __init__(self, source):
        super().__init__()
        self.links, self.ids, self.h1, self.title, self.description = [], set(), 0, False, False
        self.errors = []
        self.feed(source)
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'h1': self.h1 += 1
        if tag == 'title': self.title = True
        if tag == 'meta' and attrs.get('name') == 'description': self.description = bool(attrs.get('content'))
        if 'id' in attrs:
            if attrs['id'] in self.ids: self.errors.append('Duplicate id: ' + attrs['id'])
            self.ids.add(attrs['id'])
        if tag == 'img' and not attrs.get('alt'): self.errors.append('Image missing descriptive alt text')
        for attribute in ['href', 'src']:
            if attribute in attrs: self.links.append(attrs[attribute])


def main():
    pages = {p: Page(p.read_text()) for p in ROOT.rglob('*.html')}
    assert pages, 'Build the site first'
    failures = []
    for path, page in pages.items():
        label = str(path.relative_to(ROOT))
        if page.h1 != 1: failures.append(f'{label}: expected one h1, got {page.h1}')
        if not page.title or not page.description: failures.append(f'{label}: missing title or description')
        failures.extend(f'{label}: {error}' for error in page.errors)
        source = path.read_text()
        for forbidden in ['Albert Einstein', 'Nobel Prize', 'al-folio', 'example_pdf', 'Your post title']:
            if forbidden in source: failures.append(f'{label}: template content {forbidden!r}')
        for link in page.links:
            url = urlsplit(link)
            if url.scheme or url.netloc: continue
            target = ROOT / unquote(url.path).lstrip('/') if url.path else path
            if target.is_dir(): target = target / 'index.html'
            if not target.is_file(): failures.append(f'{label}: broken local link {link}')
            elif url.fragment and target in pages and unquote(url.fragment) not in pages[target].ids:
                failures.append(f'{label}: missing anchor {link}')
    for name in ['sitemap.xml', 'feed.xml']: ET.parse(ROOT / name)
    # Output is allowlisted by the builder: do not leak drafts, source, or the legacy demo tree.
    for excluded in ['content', '_posts', '_projects', 'README.md', 'portfolio', '.git']:
        if (ROOT / excluded).exists(): failures.append(f'Unexpected published source: {excluded}')
    if failures:
        print('\n'.join(failures)); sys.exit(1)
    print(f'PASS: {len(pages)} pages; local links, assets, anchors, metadata, RSS, sitemap, and demo exclusion.')

if __name__ == '__main__': main()
