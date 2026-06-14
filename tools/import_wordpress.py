#!/usr/bin/env python3
"""Import posts from the timtianchen.wordpress.com REST API into Eleventy.

Reads the raw post JSON cached under cache/wp/, converts the post body from
HTML to clean GitHub-flavored Markdown via pandoc, downloads every image
locally (so the published site has no dependency on wordpress.com), drops
embeds (leaving a link), and writes one Markdown file per post under src/posts/
with YAML front matter: title, date (day only), category, and hero (the first
image, renamed hero.<ext>, when the post has images).

Every post is assigned one or more of ten curated categories via
CATEGORIES_BY_SLUG below (first entry is primary). New posts not in that map
fall back to their original WordPress categories, then to "Personal", with a
warning so they can be curated.

Usage:
    python3 tools/import_wordpress.py            # import every cached post
    python3 tools/import_wordpress.py 478 95     # import only these post IDs
"""

import glob
import html
import json
import os
import re
import subprocess
import sys
import urllib.request

from bs4 import BeautifulSoup

CACHE_DIR = "cache/wp"
POSTS_DIR = "src/posts"
IMG_ROOT = "src/images/posts"          # on disk
IMG_URL = "/images/posts"              # as served
IMG_WIDTH = 1600                       # cap downloaded image width

UA = "Mozilla/5.0 (blog-importer)"

# Curated categories per post (ten categories total), keyed by slug. The first
# entry is the primary category; additional entries are added where a post
# genuinely spans more than one theme.
CATEGORIES_BY_SLUG = {
    # Research — the craft of doing research
    "differing-expectations": ["Research", "Academia"],
    "academic-integrity-and-honesty": ["Research"],
    "i-dont-like-reading": ["Research"],
    "theoretical-foundations-or-lack-thereof": ["Research", "Introspection"],
    "difficulties-with-supervising": ["Research", "Academia"],
    "effective-visual-presentations": ["Research"],
    "first-journal-article": ["Research", "Academia"],
    "acrimonious-attack-on-others-work": ["Research"],
    # Academia — academic career & institutional life
    "pepper-people": ["Academia", "Introspection"],
    "being-a-drifter": ["Academia", "Introspection"],
    "human-resources": ["Academia"],
    "thoughts-on-applying-for-a-faculty-position": ["Academia"],
    "first-semester": ["Academia"],
    "building-a-lab": ["Academia"],
    "foreign-faculty-on-boarding-to-us-universities": ["Academia"],
    "students": ["Academia"],
    "arcade-conferences": ["Academia", "Travel"],
    # Travel — places lived & visited
    "living-in-zurich": ["Travel", "Society"],
    "landing": ["Travel", "Society"],
    "on-a-train": ["Travel", "Writing"],
    "moving-back-across-the-pond": ["Travel", "Personal"],
    "a-visit-to-china-a-story-of-constrained-renaissance": ["Travel", "Society"],
    "that-time-in-chile": ["Travel", "Introspection"],
    "zurich-sunset": ["Travel"],
    # Society — politics & social issues
    "education": ["Society"],
    "american-problems": ["Society", "Books"],
    "charlottesville": ["Society"],
    "abortion-to-the-extreme": ["Society", "Philosophy"],
    "gender-equality": ["Society"],
    # Philosophy — ethics, religion, big ideas
    "religions": ["Philosophy"],
    "fairness-vs-justice": ["Philosophy", "Society"],
    "filial-piety-is-a-load-of-horse-shit": ["Philosophy", "Society"],
    # Personal — life events
    "reckless-purchasing-of-a-house-part-i": ["Personal"],
    "reckless-purchasing-of-a-house-part-ii": ["Personal"],
    "dive-bars": ["Personal", "Writing"],
    "car": ["Personal"],
    "wednesday-night-skate-2025-02-25": ["Personal"],
    # Introspection — mood, mental health, quiet reflection
    "waiting": ["Introspection"],
    "hello-darkness-my-old-friend": ["Introspection", "Travel"],
    "a-nightmare": ["Introspection"],
    "bye": ["Introspection"],
    "imposter-syndrome": ["Introspection", "Academia"],
    "reminiscence": ["Introspection", "Academia"],
    # Writing — the craft & the blog itself
    "returning-to-this": ["Writing", "Introspection"],
    "writing": ["Writing", "Introspection"],
    "what-music-means-to-me": ["Writing", "Introspection"],
    # Technology — engineering, tech, design
    "ramblings": ["Technology"],
    "uncanny-valley": ["Technology"],
    "fully-stressed-and-strained-design": ["Technology", "Research"],
    # Books — book & media impressions
    "theft-by-finding": ["Books"],
    "there-is-no-free-lunch": ["Books"],
}


# A one-sentence summary per post, used on cards and as the meta description.
SUMMARY_BY_SLUG = {
    "ramblings": "A gripe about how large organizations inevitably standardize on clunky, unwieldy software.",
    "differing-expectations": "Comparing the clear, short-term expectations of an engineering firm with the open-ended ambiguity of academic research.",
    "living-in-zurich": "An affectionate, exasperated portrait of Zurich — spotless, hyper-organized, efficient, and a little cold.",
    "academic-integrity-and-honesty": "On Feynman's call for total honesty in research: presenting the bad along with the good.",
    "i-dont-like-reading": "A researcher's confession that he hates reading academic literature — even his own papers.",
    "theoretical-foundations-or-lack-thereof": "Wrestling with the nagging fear of being deficient in the fundamentals, and climbing the knowledge genealogy tree.",
    "difficulties-with-supervising": "How much help should you actually give the students you supervise?",
    "education": "Arguing against judging teachers by their students' standardized test scores.",
    "effective-visual-presentations": "What actually makes presentation slides good, beyond merely looking pretty.",
    "landing": "Landing in the UK to an Obama audiobook, and reflecting on America's narrative of reinvention.",
    "zurich-sunset": "A set of photographs of the sun setting over Zurich.",
    "pepper-people": "Reflections at the midpoint of a PhD, with the end of the tunnel still out of sight.",
    "first-journal-article": "The bruising road to a first published paper, through two rejections.",
    "uncanny-valley": "On the uncanny valley — why almost-human replicas unsettle us.",
    "being-a-drifter": "The wry parallels between academics and drifters.",
    "fully-stressed-and-strained-design": "Explaining Fully Stressed Design, a heuristic for minimizing the mass of a lattice structure.",
    "what-music-means-to-me": "An honest admission of a fairly ordinary, undiscerning relationship with music.",
    "on-a-train": "Musings written on a sleeper train from Zurich to Amsterdam, on whether they really work.",
    "human-resources": "A no-holds-barred rant against HR departments and the very idea that humans are 'resources.'",
    "waiting": "A quiet, meditative piece about standing on a bridge and waiting.",
    "hello-darkness-my-old-friend": "A summer trip to the States shadowed by a familiar, returning darkness.",
    "acrimonious-attack-on-others-work": "On the cruelty of harsh, name-calling academic peer review.",
    "theft-by-finding": "Re-listening to David Sedaris's diaries, and how audiobooks rob a book of full attention.",
    "religions": "A Hitchens-inspired case against religion and the concept of a god.",
    "there-is-no-free-lunch": "First impressions of Chris Anderson's book 'Free' and its mostly self-evident economics.",
    "american-problems": "Reading Amy Schumer and Trevor Noah back to back, and what it reveals about America.",
    "charlottesville": "A reckoning with the white-supremacist march in Charlottesville.",
    "returning-to-this": "Returning to a blog abandoned for years, and resolving to keep it going.",
    "thoughts-on-applying-for-a-faculty-position": "Personal notes on the opaque ordeal of applying for a faculty position.",
    "imposter-syndrome": "Sitting alone in a bar with the chronic, gnawing ailment of imposter syndrome.",
    "a-nightmare": "Transcribing a disorienting nightmare about being unable to find a job.",
    "first-semester": "Surviving — and quietly enjoying — a first semester as a new professor, memes and all.",
    "writing": "A lifelong struggle with writing, in every language he has ever tried.",
    "fairness-vs-justice": "Pitting fairness against justice from an engineer's point of view.",
    "building-a-lab": "Turning a horror-movie lab space into a working research lab.",
    "reckless-purchasing-of-a-house-part-i": "How not to buy a house: from Zillow listing to closing in 34 days.",
    "reckless-purchasing-of-a-house-part-ii": "The aftermath of a too-fast house purchase — repairs, regrets, and all.",
    "abortion-to-the-extreme": "Using the rhetorical trick of extrapolation, and watching where it breaks down, on abortion.",
    "foreign-faculty-on-boarding-to-us-universities": "A guide to the opaque, deliberately difficult process of onboarding as foreign faculty in the US.",
    "gender-equality": "Making the case for explicit gender-balance quotas in governing bodies.",
    "moving-back-across-the-pond": "A life measured in transatlantic moves, beginning with a 2001 flight from Shanghai.",
    "students": "Lessons learned, and mistakes made, in hiring and managing a first cohort of students.",
    "a-visit-to-china-a-story-of-constrained-renaissance": "Returning to Shanghai after two decades to witness a constrained renaissance.",
    "dive-bars": "An ode to dive bars as the airport gates of drinking.",
    "reminiscence": "Looking back on the postdoc years as the most fun of an academic life.",
    "that-time-in-chile": "Memories of a year in Chile, pulled loose by an article about sopaipillas.",
    "car": "Buying a Honda Accord in the strange shortage economy of late 2021.",
    "wednesday-night-skate-2025-02-25": "A route map for a Wednesday-night group skate.",
    "filial-piety-is-a-load-of-horse-shit": "A blunt argument that filial piety imposes an unfair, unconsented contract on children.",
    "arcade-conferences": "How endless conference travel turns airports into places of comfort.",
    "bye": "A sign-off that opens with the message he sent right before firing his therapist.",
}


def summary_for(p: dict) -> str:
    """Resolve the one-sentence summary; fall back to the WordPress excerpt."""
    slug = p["slug"]
    if slug in SUMMARY_BY_SLUG:
        return SUMMARY_BY_SLUG[slug]
    excerpt = re.sub(r"<[^>]+>", " ", p.get("excerpt", "") or "")
    excerpt = unescape(re.sub(r"\s+", " ", excerpt))
    if excerpt:
        excerpt = excerpt.split(". ")[0].rstrip(". ") + "."
        print(f"    !! {slug} not in SUMMARY_BY_SLUG; using excerpt.", file=sys.stderr)
        return excerpt
    print(f"    !! {slug} has no summary; leaving blank.", file=sys.stderr)
    return ""


def categories_for(p: dict) -> list:
    """Resolve the category list for a post, always returning at least one."""
    slug = p["slug"]
    if slug in CATEGORIES_BY_SLUG:
        return CATEGORIES_BY_SLUG[slug]
    wp = [c for c in p.get("categories", {}).keys() if c.lower() != "uncategorized"]
    fallback = wp or ["Personal"]
    print(
        f"    !! {slug} not in CATEGORIES_BY_SLUG; using {fallback} "
        f"— add it to the map to curate.",
        file=sys.stderr,
    )
    return fallback


def unescape(s: str) -> str:
    return html.unescape(s or "").strip()


def yaml_quote(s: str) -> str:
    """Safely quote a scalar for YAML front matter."""
    return '"' + s.replace("\\", "\\\\").replace('"', '\\"') + '"'


def download_image(src: str, slug: str, hero: bool = False) -> str | None:
    """Download an image referenced by `src` into the post's image dir.

    The post's first image is saved as ``hero.<ext>`` so it can double as a
    featured image. Returns the site-relative URL to use in the Markdown, or
    None on failure.
    """
    base = src.split("?")[0]
    fname = base.split("/")[-1] or "image"
    fname = re.sub(r"[^A-Za-z0-9._-]", "_", fname)
    if hero:
        ext = os.path.splitext(fname)[1].lower() or ".jpg"
        fname = "hero" + ext
    dest_dir = os.path.join(IMG_ROOT, slug)
    os.makedirs(dest_dir, exist_ok=True)
    dest = os.path.join(dest_dir, fname)
    if not os.path.exists(dest):
        # Request a sensibly-sized version from WordPress rather than the
        # multi-megabyte original.
        dl_url = base + f"?w={IMG_WIDTH}"
        try:
            req = urllib.request.Request(dl_url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=60) as r:
                data = r.read()
            with open(dest, "wb") as f:
                f.write(data)
        except Exception as e:  # noqa: BLE001
            print(f"    !! failed to download {src}: {e}", file=sys.stderr)
            return None
    return f"{IMG_URL}/{slug}/{fname}"


def clean_and_localize(content: str, slug: str) -> tuple[str, int, str | None]:
    """Download images locally and reduce WordPress block markup to clean HTML.

    - Every <img> is downloaded and stripped to just src (+ alt). This removes
      the srcset/sizes/data-* attributes that still pointed at wordpress.com.
      The first image is saved as hero.<ext> and returned for the front matter.
    - Anchors that merely wrap an image (lightbox links) are unwrapped.
    - <figure> wrappers without a real caption (including gallery wrappers) are
      unwrapped so pandoc emits plain Markdown images; figures with a caption
      are kept but stripped of attributes.
    """
    soup = BeautifulSoup(content, "html.parser")
    n = 0
    hero_url = None

    for i, img in enumerate(soup.find_all("img")):
        src = img.get("src")
        if not src:
            img.decompose()
            continue
        alt = img.get("alt", "") or ""
        is_hero = i == 0
        local = download_image(src, slug, hero=is_hero)
        img.attrs = {}
        img["src"] = local or src
        if local:
            n += 1
            if is_hero:
                hero_url = local
        if alt:
            img["alt"] = alt

    # Drop <iframe> embeds before pandoc sees them (pandoc resolves iframe src
    # to its live fallback content). Leave a plain link so nothing is lost.
    for iframe in soup.find_all("iframe"):
        src = iframe.get("src", "")
        if src.startswith("//"):
            src = "https:" + src
        if src.startswith("http"):
            a = soup.new_tag("a", href=src)
            a.string = "View embedded map"
            p = soup.new_tag("p")
            p.append(a)
            iframe.replace_with(p)
        else:
            iframe.decompose()

    # Unwrap anchors that only wrap image(s) — WordPress lightbox links.
    for a in soup.find_all("a"):
        if a.find("img") and not a.get_text(strip=True):
            a.unwrap()

    # Figures: keep only those with a real caption (outer first => galleries
    # unwrap before their inner image figures).
    for fig in soup.find_all("figure"):
        cap = fig.find("figcaption")
        cap_text = cap.get_text(strip=True) if cap else ""
        if cap_text:
            fig.attrs = {}
            cap.attrs = {}
        else:
            if cap:
                cap.decompose()
            fig.unwrap()

    return str(soup), n, hero_url


def html_to_markdown(content: str) -> str:
    """Convert post HTML to clean GFM Markdown using pandoc."""
    proc = subprocess.run(
        [
            "pandoc",
            "-f", "html-native_divs-native_spans",
            "-t", "gfm+pipe_tables",
            "--wrap=none",
        ],
        input=content.encode("utf-8"),
        capture_output=True,
        check=True,
    )
    md = proc.stdout.decode("utf-8")
    # Put each Markdown image on its own block so galleries stack rather than
    # rendering as a cramped inline row.
    md = re.sub(r"\)\s+!\[", ")\n\n![", md)
    # Collapse 3+ blank lines to a single blank line.
    md = re.sub(r"\n{3,}", "\n\n", md).strip()
    return md + "\n"


def front_matter(p: dict, hero_url: str | None) -> str:
    lines = ["---"]
    lines.append(f"title: {yaml_quote(unescape(p['title']))}")
    lines.append(f"date: {p['date'][:10]}")        # day only, no time
    lines.append("categories:")
    lines += [f"  - {yaml_quote(c)}" for c in categories_for(p)]
    summary = summary_for(p)
    if summary:
        lines.append(f"summary: {yaml_quote(summary)}")
    if hero_url:
        lines.append(f"hero: {yaml_quote(hero_url)}")
    lines.append("---")
    return "\n".join(lines) + "\n\n"


def import_post(path: str) -> str:
    p = json.load(open(path))
    slug = p["slug"]
    print(f"  {p['ID']:>4}  {slug}")
    content = p.get("content", "") or ""
    content, n_img, hero_url = clean_and_localize(content, slug)
    if n_img:
        print(f"        {n_img} image(s) localized; hero: {hero_url}")
    md = html_to_markdown(content)
    body = front_matter(p, hero_url) + md
    os.makedirs(POSTS_DIR, exist_ok=True)
    out = os.path.join(POSTS_DIR, f"{slug}.md")
    with open(out, "w", encoding="utf-8") as f:
        f.write(body)
    return out


def ensure_dir_data():
    """Write the posts/ directory data file if absent.

    This assigns the post layout to every Markdown file in the directory. The
    importer guarantees it so re-imports work even if src/posts was wiped.
    """
    os.makedirs(POSTS_DIR, exist_ok=True)
    path = os.path.join(POSTS_DIR, "posts.json")
    if not os.path.exists(path):
        with open(path, "w", encoding="utf-8") as f:
            f.write('{\n  "layout": "layouts/post.njk"\n}\n')


def main():
    ensure_dir_data()
    ids = set(sys.argv[1:])
    files = sorted(glob.glob(os.path.join(CACHE_DIR, "*.json")))
    if ids:
        files = [f for f in files if os.path.splitext(os.path.basename(f))[0] in ids]
    print(f"Importing {len(files)} post(s)...")
    for f in files:
        import_post(f)
    print("Done.")


if __name__ == "__main__":
    main()
