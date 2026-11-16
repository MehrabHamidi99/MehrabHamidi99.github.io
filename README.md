# Mehrab Hamidi — personal website

Live site: https://mehrabhamidi99.github.io/

A static research portfolio for GitHub Pages. Edit the files in `content/`; GitHub Actions builds and publishes the site when changes reach `main`. You do not need to edit HTML for routine updates.

## Edit directly on GitHub

1. Open this repository and navigate to the relevant file in `content/`.
2. Click the pencil (Edit). For a new blog post, choose **Add file → Create new file**.
3. Edit, then commit to `main` (or use a branch and merge a pull request).
4. Watch **Actions → Deploy site**. The build checks local links and publishes to the existing `gh-pages` branch. GitHub Pages then serves the update; allow a few minutes.

Keep **Settings → Pages → Deploy from a branch → gh-pages / (root)**, as used by this repository. No new hosting service or custom domain is needed.

## Add news

Add an entry to `content/news.yml`. Keep indentation and quote dates. The newest entries appear first automatically; the homepage shows the latest three.

```yaml
- date: '2026-11-16'
  category: Research
  title: A short headline
  text: One or two sentences about the update.
  url: https://example.com/your-announcement
```

`url` is optional. Use a real link before publishing. Future-dated entries remain hidden until a build on or after that date. The site is not rebuilt daily automatically; run **Actions → Deploy site → Run workflow** to publish a scheduled entry.

## Add a blog post

Copy `content/blog/_template.md` to a new file such as `content/blog/2026-11-16-my-new-post.md`. Files starting with `_` are templates and never publish.

```markdown
---
title: My new research note
summary: A one-sentence preview for the blog and homepage.
date: '2026-11-16'
category: Research notes
slug: my-new-post
draft: false
---
Write your opening paragraph here.

## A section heading

Use **bold**, *italics*, and [links](https://example.com).

- First point
- Second point
```

The URL is `/blog/my-new-post/`. Keep the slug stable after publishing so shared links continue to work. Set `draft: true` to keep work private from the built website. **The repository itself is public, so committed drafts are still publicly readable on GitHub.** Future-dated posts wait for a subsequent build. Markdown supports fenced code blocks, headings, lists, images, and tables. Put new public images in `portfolio/static/` and reference `/assets/portfolio/filename.jpg`.

## Add a publication

Copy an entry in `content/publications.yml`. Use a unique lowercase `id`, a numeric `year`, and one of `Conference`, `Workshop`, `Journal`, `Preprint`, or `Thesis` for `type`. Set `selected: true` for a homepage feature. Keep the homepage selection focused (the current design features three papers). Publication links accept `https://…` or a local `/…` path. Titles containing a colon should be quoted.

The build preserves author order and highlights Mehrab's name. It sorts by year, keeping file order within the same year. Distinguish preprints from accepted publications and workshops from main conferences.

## Update bio, skills, CV, and contact

Edit `content/profile.yml` for the homepage and on-page CV details. The single **View CV (PDF)** button on `/cv/` opens `assets/pdf/cv_june2026.pdf`, the supplied June 2026 CV. To update that PDF later, replace this file while keeping its filename; the next deployment publishes it automatically. The old PDF URL is preserved for existing external links, but is no longer linked from the CV page. The thesis remains at its existing URL.

Use the sun/moon button in the header to switch between light and dark themes. Your choice is remembered across pages and visits; first-time visitors follow their system theme.

The two initial blog notes summarize public coauthored work. They can be revised or unpublished by setting `draft: true`.

## Preview locally

Python 3.11 or newer:

```sh
python3 -m venv .venv
.venv/bin/pip install -r requirements-site.txt
.venv/bin/python scripts/build_site.py
.venv/bin/python scripts/check_site.py
.venv/bin/python -m http.server 8000 --directory _site
```

Open http://localhost:8000. Re-run the build after content or template changes, then refresh the browser. Stop the server with Ctrl+C. `_site/` is generated; do not edit or commit it.

## Structure

- `content/`: editable profile, publications, news, and Markdown posts.
- `portfolio/templates/`: page layouts and shared components.
- `portfolio/static/`: stylesheet, small progressive-enhancement script, and portrait.
- `scripts/build_site.py`: validates content and generates pages, RSS, sitemap, and selected assets.
- `scripts/check_site.py`: checks generated pages and local links before deployment.
- `requirements-site.txt`: pinned build dependencies.
- `.github/workflows/deploy.yml`: builds, checks, and publishes.

The previous al-folio/Jekyll files are retained as historical source, but are **not used or copied into the deployed site**. Old template-specific automation is retained in `legacy-workflows/`, outside GitHub Actions. CodeQL is preserved. You no longer need Ruby, Jekyll, Node, Docker, or the old `Gemfile` to build this portfolio.

## Content provenance

Recent additions were checked on 16 November 2026:

- [Navigating Potholes](https://arxiv.org/abs/2605.16134): arXiv preprint, submitted 15 May 2026.
- [T-GRAB](https://doi.org/10.1145/3770854.3785699): KDD 2026 publication, also listed on [Mila](https://mila.quebec/en/directory/mehrab-hamidi). The [earlier arXiv version](https://arxiv.org/abs/2507.10183) records the KDD 2025 workshop oral.
- [VPT interpretability](https://arxiv.org/abs/2407.12161): Mechanistic Interpretability Workshop at ICML 2024.
- Thesis title and year follow the title page of the existing `assets/pdf/Thesis.pdf` (December 2024).
- Education, experience, scholarship, and tools follow the existing site/CV. No hiring outcomes, citation counts, or unpublished publications are claimed.
