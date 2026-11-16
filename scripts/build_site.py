#!/usr/bin/env python3
"""Build the portfolio from content/*.yml and Markdown, without legacy theme output."""
from datetime import date, datetime, timezone
from email.utils import format_datetime
from pathlib import Path
import json
import re
import shutil
import xml.etree.ElementTree as ET

import markdown
import yaml
from jinja2 import Environment, FileSystemLoader, StrictUndefined, select_autoescape
from markupsafe import Markup, escape

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / '_site'
TODAY = datetime.now(timezone.utc).date()


def read_yaml(name):
    return yaml.safe_load((ROOT / 'content' / name).read_text())


def date_value(value):
    return date.fromisoformat(str(value))


def required(item, keys, context):
    for key in keys:
        if key not in item or item[key] in (None, ''):
            raise ValueError(f'{context}: missing {key}')


def check_link(url):
    if not isinstance(url, str) or not re.match(r'^(https://|/(?!/))', url):
        raise ValueError(f'Use an https:// or root-relative link: {url!r}')


def main():
    profile = read_yaml('profile.yml')
    required(profile, ['name', 'email', 'url', 'headline', 'intro'], 'Profile')
    publications = read_yaml('publications.yml') or []
    ids = set()
    for paper in publications:
        required(paper, ['id', 'title', 'authors', 'year', 'venue', 'type', 'topic', 'summary', 'links'], 'Publication')
        if paper['id'] in ids or not re.fullmatch(r'[a-z0-9-]+', paper['id']):
            raise ValueError(f'Duplicate or invalid publication id: {paper["id"]}')
        ids.add(paper['id'])
        if paper['type'] not in ['Preprint', 'Conference', 'Workshop', 'Journal', 'Thesis']:
            raise ValueError(f'Unknown publication type: {paper["type"]}')
        if not isinstance(paper['year'], int) or paper['year'] > TODAY.year:
            raise ValueError(f'Invalid publication year: {paper["year"]}')
        paper.setdefault('selected', False)
        paper.setdefault('note', '')
        for link in paper['links']:
            required(link, ['label', 'url'], paper['title'])
            check_link(link['url'])
    publications.sort(key=lambda p: p['year'], reverse=True)
    news = read_yaml('news.yml') or []
    for item in news:
        required(item, ['date', 'category', 'title', 'text'], 'News')
        item['date'] = date_value(item['date']).isoformat()
        item.setdefault('url', '')
        if item['url']:
            check_link(item['url'])
    news = sorted((item for item in news if date_value(item['date']) <= TODAY), key=lambda item: item['date'], reverse=True)
    posts, slugs = [], set()
    for path in sorted((ROOT / 'content/blog').glob('*.md')):
        if path.name.startswith('_'):
            continue
        text = path.read_text()
        if not text.startswith('---\n') or '\n---\n' not in text[4:]:
            raise ValueError(f'{path.name}: expected YAML front matter between --- lines')
        frontmatter, body = text[4:].split('\n---\n', 1)
        post = yaml.safe_load(frontmatter)
        required(post, ['title', 'summary', 'date', 'category', 'slug', 'draft'], path.name)
        if not isinstance(post['draft'], bool):
            raise ValueError(f'{path.name}: draft must be true or false')
        if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', post['slug']) or post['slug'] in slugs:
            raise ValueError(f'{path.name}: invalid or duplicate slug')
        slugs.add(post['slug'])
        post['date'] = date_value(post['date']).isoformat()
        if post['draft'] or date_value(post['date']) > TODAY:
            continue
        post['body'] = Markup(markdown.markdown(body, extensions=['fenced_code', 'tables', 'toc']))
        post['reading_time'] = max(1, (len(body.split()) + 199) // 200)
        post['url'] = f'/blog/{post["slug"]}/'
        posts.append(post)
    posts.sort(key=lambda p: p['date'], reverse=True)
    env = Environment(loader=FileSystemLoader(ROOT / 'portfolio/templates'), autoescape=select_autoescape(['html']), undefined=StrictUndefined)
    env.filters['date_label'] = lambda value: date_value(value).strftime('%b %d, %Y')
    env.filters['author_highlight'] = lambda value: Markup('<strong>Mehrab Hamidi</strong>').join(escape(part) for part in value.split('Mehrab Hamidi'))
    schema = {'@context': 'https://schema.org', '@type': 'Person', 'name': profile['name'], 'url': profile['url'], 'jobTitle': 'Machine Learning Researcher', 'image': profile['url'] + '/assets/portfolio/portrait.jpg', 'sameAs': [item['url'] for item in profile['links']]}
    context = dict(profile=profile, publications=publications, news=news, posts=posts, year=TODAY.year, schema=schema, post=None)
    # Only this generated directory is replaced; authored content and legacy assets stay intact.
    if OUT.is_symlink():
        raise ValueError('_site must not be a symlink')
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir()
    shutil.copytree(ROOT / 'portfolio/static', OUT / 'assets/portfolio')
    (OUT / 'assets/pdf').mkdir(parents=True)
    for filename in ['Thesis.pdf', 'cv_2024_i.pdf', 'ICML2025_Template.pdf']:
        shutil.copy2(ROOT / 'assets/pdf' / filename, OUT / 'assets/pdf' / filename)
    routes = []

    def render(template, route, title, description, active, **extra):
        destination = OUT / (route.lstrip('/') + 'index.html' if route.endswith('/') else route.lstrip('/'))
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(env.get_template(template).render(context | dict(path=route, title=title, description=description, active=active) | extra))
        if route != '/404.html':
            routes.append(route)

    render('home.html', '/', profile['name'], profile['intro'], 'home')
    render('publications.html', '/publications/', 'Publications', 'Papers and preprints by Mehrab Hamidi on deep learning, optimization, and interpretability.', 'publications')
    render('news.html', '/news/', 'News', 'Research news and milestones from Mehrab Hamidi.', 'news')
    render('blog.html', '/blog/', 'Research notes', 'Notes on neural networks, interpretability, and temporal graph learning.', 'blog')
    render('cv.html', '/cv/', 'Curriculum vitae', 'Education, research experience, and selected publications of Mehrab Hamidi.', 'cv')
    render('404.html', '/404.html', 'Page not found', 'Find publications, research notes, and contact details for Mehrab Hamidi.', '')
    for post in posts:
        render('post.html', post['url'], post['title'], post['summary'], 'blog', post=post)
    ET.register_namespace('', 'http://www.sitemaps.org/schemas/sitemap/0.9')
    sitemap = ET.Element('urlset', xmlns='http://www.sitemaps.org/schemas/sitemap/0.9')
    for route in routes:
        element = ET.SubElement(sitemap, 'url')
        ET.SubElement(element, 'loc').text = profile['url'] + route
    ET.ElementTree(sitemap).write(OUT / 'sitemap.xml', encoding='utf-8', xml_declaration=True)
    rss = ET.Element('rss', version='2.0')
    channel = ET.SubElement(rss, 'channel')
    for key, value in {'title': 'Mehrab Hamidi · Research notes', 'link': profile['url'] + '/blog/', 'description': 'Notes on machine learning research.', 'language': 'en'}.items():
        ET.SubElement(channel, key).text = value
    for post in posts:
        item = ET.SubElement(channel, 'item')
        for key, value in {'title': post['title'], 'link': profile['url'] + post['url'], 'guid': profile['url'] + post['url'], 'description': post['summary'], 'pubDate': format_datetime(datetime.combine(date_value(post['date']), datetime.min.time(), tzinfo=timezone.utc))}.items():
            ET.SubElement(item, key).text = value
    ET.ElementTree(rss).write(OUT / 'feed.xml', encoding='utf-8', xml_declaration=True)
    (OUT / 'robots.txt').write_text('User-agent: *\nAllow: /\nSitemap: ' + profile['url'] + '/sitemap.xml\n')
    (OUT / '.nojekyll').touch()
    print(f'Built {len(routes) + 1} pages, {len(publications)} publications, {len(news)} updates, {len(posts)} posts into {OUT}')


if __name__ == '__main__':
    main()
