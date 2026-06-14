# Staying Afloat

A personal blog (migrated from [timtianchen.wordpress.com](https://timtianchen.wordpress.com/)),
built with [Eleventy](https://www.11ty.dev/) and deployed to GitHub Pages.

## Develop

```sh
npm install
npm run serve     # local dev server at http://localhost:8080
npm run build     # build to _site/
```

## Content

Posts live in `src/posts/*.md` as Markdown with YAML front matter. Images are in
`src/images/posts/<slug>/`.

### Re-importing from WordPress

The raw WordPress posts are cached in `cache/wp/*.json`. To regenerate the
Markdown (e.g. after pulling new posts), run:

```sh
python3 tools/import_wordpress.py          # all cached posts
python3 tools/import_wordpress.py 478 95   # specific post IDs
```

The importer converts post HTML to clean Markdown (via pandoc), downloads every
image locally, and writes one file per post. Requires `pandoc` and Python
`beautifulsoup4` + `lxml`.

To refresh the cache from the live site, re-fetch from the WordPress.com REST API:
`https://public-api.wordpress.com/rest/v1.1/sites/timtianchen.wordpress.com/posts/`

## Deploy

Pushing to `main` triggers `.github/workflows/deploy.yml`, which builds and
publishes to GitHub Pages.

### Before going live — set these

- `src/_data/site.json` → `url`: the canonical site URL (used by the RSS feed).
- `src/CNAME`: a one-line file with the custom domain (e.g. `example.com`). It is
  copied to the site root on build. (Not yet created — add it when the domain is set.)
- Repo **Settings → Pages → Source: GitHub Actions**, then add the custom domain
  and enable **Enforce HTTPS**.
- DNS at Squarespace per `PLAN.md` (apex A records + `www` CNAME).
