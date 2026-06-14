# Staying Afloat

A personal blog built with [Eleventy](https://www.11ty.dev/) and deployed to
GitHub Pages.

## Develop

```sh
npm install
npm run serve     # local dev server at http://localhost:8080
npm run build     # build to _site/
```

## Content

Posts live in `src/posts/*.md` as Markdown with YAML front matter. Images are in
`src/images/posts/<slug>/`. To add a post, create a new Markdown file in
`src/posts/` with `title`, `date`, `categories`, `summary`, and an optional
`hero` image in its front matter.

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
