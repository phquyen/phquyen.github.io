# phquyen.github.io

Personal portfolio website, live at https://quyenpham.com. Built with [Astro](https://astro.build) and TypeScript.

**To edit content, see [EDITING.md](EDITING.md).** All text lives in `src/content/`; colours and fonts in `src/styles/theme.css`.

Pushing to `main` rebuilds and deploys the site via GitHub Actions.

```sh
npm install      # first time only
npm run dev      # preview at http://localhost:4321
npm run build    # type-check, validate content, build into dist/
```

## Code layout (for reference)

| Folder | What it does |
| --- | --- |
| `src/content/` | All content: `profile.yaml`, `projects/`, `notes/<Topic>/` |
| `src/content.config.ts` | Required fields for each content file, and the error messages |
| `src/pages/` | One file per web address (`/`, `/projects/…`, `/notes/…`, `/resume/`) |
| `src/layouts/` | Shared page frame (`Base`) and the intro + tabs (`Tabs`) |
| `src/components/`, `src/lib/` | Project cards, icons, and helpers that read the content |
| `src/styles/` | `theme.css` (colours, fonts, sizes) and `global.css` (layout) |
