const pluginRss = require("@11ty/eleventy-plugin-rss");

module.exports = function (eleventyConfig) {
  eleventyConfig.addPlugin(pluginRss);

  // Static assets
  eleventyConfig.addPassthroughCopy({ "src/images": "images" });
  eleventyConfig.addPassthroughCopy({ "src/css": "css" });
  // CNAME for the custom domain (created at deploy time; copied if present)
  eleventyConfig.addPassthroughCopy({ "src/CNAME": "CNAME" });

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
