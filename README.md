# phquyen.github.io
Personal portfolio website, built with [Astro](https://astro.build) and TypeScript.

## Editing the site

All the text lives in **`src/content.ts`**. Edit it, commit, and push to `main`; GitHub Actions rebuilds and deploys the site automatically.

| What | Where |
| --- | --- |
| Name, intro, about, projects, links | `src/content.ts` |
| Page structure | `src/pages/index.astro` |
| Colours and styling | `src/styles.css` |

## Running locally

```sh
npm install      # first time only
npm run dev      # live preview at http://localhost:4321
npm run build    # type-check and build into dist/
```
