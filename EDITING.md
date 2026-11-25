# Editing the website

Everything you write lives in **`src/content/`**. You never need to touch the layout code.

```
src/content/
  profile.yaml        ← your name, intro, links, resume details
  projects/           ← one .md file per project
  notes/
    Math/             ← each folder is a tab on the home page
    SQL/
```

Colours and fonts are in `src/styles/theme.css` (instructions at the top of that file).

---

## Change your intro, links or resume

Open `src/content/profile.yaml`. Each line is `field: "value"`.

- An empty value `""` hides that button (e.g. `linkedin: ""` means no LinkedIn button).
- Lines starting with `#` are comments: the site ignores them.
- The resume page is built from `experience`, `skills` and `education`. Empty sections are hidden.
- `projects_card` is the "What's this?" card on the right of the Projects tab. Empty `text: ""` hides it.

## Add a project

1. In `src/content/projects/`, copy `_template.md` and rename the copy, e.g. `sales-dashboard.md`.
   The name becomes the web address: `/projects/sales-dashboard/`. Use lowercase and dashes.
2. Fill in the lines between the two `---` at the top (title, summary, tools…).
3. Write the case study below the second `---` in normal Markdown.
4. Set `draft: false` when it's ready to go live.

Each project file automatically gets a card on the Projects tab and its own page.
`featured: true` lists it first with a "Featured" label; otherwise `order` decides (lower first).

## Add a note

1. Pick the topic folder, e.g. `src/content/notes/SQL/`.
2. Copy `example-note.md` in that folder and rename the copy, e.g. `window-functions.md`.
3. Change the title, summary and date (`YYYY-MM-DD`), and write the note.
4. Set `draft: false` to publish.

**Maths:** always use double dollar signs. `$$x^2$$` inside a sentence stays inline; `$$` on their
own lines (above and below the formula) makes a centred equation. A single `$` is just a dollar sign,
so prices like $45/MWh are safe to write.
**Code:** three backticks plus the language name, e.g. ` ```sql `, then the code, then ` ``` `.
The Math and SQL example notes show both.

## Add a new tab

Create a new folder in `src/content/notes/`, e.g. `Statistics`, and put a note in it.
The folder name becomes the tab name exactly as written (so `SQL` shows as "SQL"),
and the address is lowercase: `/notes/statistics/`. Tabs appear in A–Z order after Projects.

A tab only appears on the live site once its folder has at least one note with `draft: false`.

## Drafts

`draft: true` hides a project or note from the **live site**. It still shows when you preview
locally (with a "Draft" label), so you can check it before publishing.

## If something is wrong

If a file is missing a required line or has a typo, the preview and the build stop with a
message that names the file and the line to fix, for example:

```
projects → battery-trading data does not match collection schema.
  title: missing. Add a line like:  title: "Battery trading simulation"
```

---

## Preview on your computer

1. In VS Code: **Terminal → New Terminal**.
2. Run `npm run dev` (the first time on a new computer, run `npm install` first).
3. Open http://localhost:4321. The page updates every time you save a file.
4. Press `Ctrl + C` in the terminal to stop.

If it says `npm` is not recognised, close VS Code completely and reopen it.

## Publish

**From VS Code:** open the Source Control panel (the branch icon on the left), type a short
message like "Add SQL note on joins", click **Commit**, then **Sync Changes** (or **Push**).

**From the terminal:**

```sh
git add -A
git commit -m "Add SQL note on joins"
git push
```

The site rebuilds automatically and is live at https://quyenpham.com in 1–2 minutes.

## Edit directly on github.com

Handy for small fixes when you're not at your computer.

1. Go to https://github.com/phquyen/phquyen.github.io and open the file (e.g. `src/content/profile.yaml`).
2. Click the pencil icon (**Edit this file**), make your change.
3. Click **Commit changes…** and commit to `main`.

To add a file: open the folder, click **Add file → Create new file**. Typing `Statistics/` in the
name box creates a new folder (and so a new tab).

**Check it worked:** open the **Actions** tab on GitHub. A green tick means it's live; a red cross
means something needs fixing: click it to see the same error message described above.
