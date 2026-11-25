import { defineConfig } from "astro/config";
import { unified } from "@astrojs/markdown-remark";
import remarkMath from "remark-math";
import rehypeKatex from "rehype-katex";

export default defineConfig({
  site: "https://quyenpham.com",
  markdown: {
    // LaTeX maths in Markdown, always between double dollar signs:
    //   inline:  $$x^2$$ inside a sentence     display: $$ ... $$ on their own lines
    // A single $ stays a normal dollar sign, so prices like $100 are never turned into maths.
    processor: unified({
      remarkPlugins: [[remarkMath, { singleDollarTextMath: false }]],
      rehypePlugins: [rehypeKatex],
    }),
    // Code highlighting with a light and a dark colour set;
    // global.css picks the right one for the current theme.
    // These two were chosen because every colour passes WCAG AA (4.5:1) on the site's backgrounds.
    shikiConfig: {
      themes: { light: "github-light-high-contrast", dark: "github-dark-default" },
      defaultColor: false,
    },
  },
});
