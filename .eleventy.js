const pluginRss = require("@11ty/eleventy-plugin-rss");

module.exports = function (eleventyConfig) {
  eleventyConfig.addPlugin(pluginRss);

  // Static assets
  eleventyConfig.addPassthroughCopy({ "src/images": "images" });
  eleventyConfig.addPassthroughCopy({ "src/css": "css" });
  // CNAME for the custom domain (created at deploy time; copied if present)
  eleventyConfig.addPassthroughCopy({ "src/CNAME": "CNAME" });
  // Audio recordings (linked from transcript posts)
  eleventyConfig.addPassthroughCopy({ "src/recordings": "recordings" });

  // --- Filters ---
  eleventyConfig.addFilter("readableDate", (d) =>
    new Intl.DateTimeFormat("en-US", {
      dateStyle: "long",
      timeZone: "UTC",
    }).format(d)
  );
  eleventyConfig.addFilter("isoDate", (d) => d.toISOString());
  eleventyConfig.addFilter("year", (d) => d.getUTCFullYear());
  eleventyConfig.addFilter("head", (arr, n) => (n < 0 ? arr.slice(n) : arr.slice(0, n)));

  const slugify = (s) =>
    String(s)
      .toLowerCase()
      .replace(/[^a-z0-9]+/g, "-")
      .replace(/^-|-$/g, "");
  eleventyConfig.addFilter("categorySlug", slugify);

  // --- Collections ---
  const byDateDesc = (api) =>
    api.getFilteredByGlob("src/posts/*.md").sort((a, b) => b.date - a.date);

  eleventyConfig.addCollection("posts", byDateDesc);

  eleventyConfig.addCollection("postsByYear", (api) => {
    const groups = {};
    for (const p of byDateDesc(api)) {
      const y = p.date.getUTCFullYear();
      (groups[y] ||= []).push(p);
    }
    return Object.keys(groups)
      .sort((a, b) => b - a)
      .map((year) => ({ year, posts: groups[year] }));
  });

  eleventyConfig.addCollection("categoryList", (api) => {
    const groups = {};
    for (const p of byDateDesc(api)) {
      for (const c of p.data.categories || []) {
        (groups[c] ||= []).push(p);
      }
    }
    return Object.keys(groups)
      .sort()
      .map((name) => ({
        name,
        slug: slugify(name),
        posts: groups[name],
        count: groups[name].length,
      }));
  });

  // --- Transforms ---
  // Links to other sites open in a new tab. Internal links are left alone.
  eleventyConfig.addTransform("externalLinks", function (content) {
    const out = this.page && this.page.outputPath;
    if (!out || !out.endsWith(".html")) return content;
    return content.replace(
      /<a\s+([^>]*?)href="(https?:\/\/[^"]+)"([^>]*?)>/gi,
      (match, pre, href, post) => {
        if (/timtianchen\.com/i.test(href)) return match;   // own site
        let attrs = (pre + 'href="' + href + '"' + post).trim();
        if (/\btarget\s*=/i.test(attrs)) return match;      // already set by hand
        attrs += ' target="_blank"';
        if (!/\brel\s*=/i.test(attrs)) attrs += ' rel="noopener noreferrer"';
        return "<a " + attrs + ">";
      }
    );
  });

  return {
    dir: {
      input: "src",
      includes: "_includes",
      data: "_data",
      output: "_site",
    },
    markdownTemplateEngine: false, // keep imported post bodies verbatim
    htmlTemplateEngine: "njk",
    templateFormats: ["njk", "md", "11ty.js"],
  };
};
