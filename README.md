# Job Connect — App Discovery

A free, bilingual (English/Arabic), static discovery and SEO site for **Job Connect** by **DevImpact**.

- Google Play: https://play.google.com/store/apps/details?id=com.jobsearch.jobconnect.work.jobs.devimpact
- Android application ID: com.jobsearch.jobconnect.work.jobs.devimpact
- Website (after GitHub Pages is enabled): https://shelternewlife.github.io/tobemotif-app-discovery/

## What this repository provides

- Pre-rendered HTML pages in /en/ and /ar/, readable without JavaScript.
- About, features, and FAQ pages in both languages.
- Canonical URLs, hreflang, Open Graph metadata, and Schema.org JSON-LD.
- Generated sitemap.xml, robots.txt, and llms.txt.
- Python standard-library build, validation, and automated tests.
- GitHub Actions build, test, and GitHub Pages deployment.

## Verified product scope

The public Google Play listing describes job listing search, job alerts, and saving jobs. Content is intentionally limited to those store-described capabilities and general career discovery wording. No previous-app features or unverified Android compatibility claims are carried over.

## Build and test locally

```bash
python -m unittest discover -s tests -v
python scripts/build.py
python scripts/validate.py
```

The generated site is written to dist/ and is not committed.

## GitHub Pages setup

In repository Settings → Pages → Build and deployment, select **GitHub Actions** as the source. The workflow deploys the generated dist/ artifact on pushes to main and on manual dispatch.

## Free-tier architecture and limitations

This project uses GitHub Pages, GitHub Actions, static JSON content, and Python's standard library. It has no database, server-side API, user accounts, Firebase, Cloudflare, or paid runtime dependency. GitHub plan limits and product terms may change. Search engines and AI crawlers decide independently whether and when to crawl or index pages; sitemap publication does not guarantee indexing. GitHub Pages does not provide comprehensive crawler logs.

## Content maintenance

Edit content/app.json, content/features.json, and content/faq.json, then commit changes to main. Keep descriptions aligned with the live Google Play listing. Review store links, privacy policy, and support details periodically.
