# Editing the website

Everything you write lives in **`src/content/`**. You never need to touch the layout code.

```
src/content/
  profile.yaml        ← your name, intro, links, resume details
  projects/           ← one .md file per project
  sql/                ← one .md file per SQL query (the SQL tab)
  notes/
    Math/             ← each notes folder is a tab on the home page
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
`featured: true` gives it the wide spotlight card at the top of the Projects tab;
otherwise `order` decides the position (lower first).

Two optional extras make a project stand out (examples are in `_template.md`):

- **`cover`**: a picture for the card and the top of the page. Put the image in
  `src/assets/projects/<name>/` and point to it, e.g. `cover: "../../assets/projects/my-project/screenshot.png"`.
  Add `cover_alt` describing what it shows. Images are compressed automatically.
- **`highlights`**: up to 4 key numbers, shown as big tiles. Only use real, checkable numbers.

Pages with 3 or more `##` headings get an "On this page" contents list beside the text on wide screens.

## Add a note

1. Pick the topic folder, e.g. `src/content/notes/Math/`.
2. Copy `example-note.md` in that folder and rename the copy, e.g. `limits.md`.
3. Change the title, summary and date (`YYYY-MM-DD`), and write the note.
4. Set `draft: false` to publish.

**Maths:** always use double dollar signs. `$$x^2$$` inside a sentence stays inline; `$$` on their
own lines (above and below the formula) makes a centred equation. A single `$` is just a dollar sign,
so prices like $45/MWh are safe to write.
**Code:** three backticks plus the language name, e.g. ` ```python `, then the code, then ` ``` `.
The Math example note shows maths.

## Add a SQL query

The SQL tab (`/sql/`) has a workbench where visitors can edit and run queries against
**RideNest**, a *fictional* ride-hailing dataset (tables `trips`, `riders`, `drivers`, `promos`).
Every column is described in `docs/sql-dataset.md`.

1. In `src/content/sql/`, copy `busiest-weekday.md` and rename the copy, e.g. `top-riders.md`.
   It gets its own page: `/sql/top-riders/`.
2. Fill in the lines at the top:
   - `title`: a short name for the question.
   - `date`: the day you wrote it (`YYYY-MM-DD`). It colours that day in the activity grid.
   - `difficulty`: `"easy"`, `"medium"` or `"hard"`.
   - `skills`: what it practises, e.g. `["JOIN", "Window functions"]`.
3. Below the second `---`, write the question in a sentence or two, then **exactly one** SQL block:

   ````md
   Who are the 10 riders with the most completed trips?

   ```sql
   SELECT rider_id, COUNT(*) AS trips
   FROM trips
   WHERE status = 'completed'
   GROUP BY rider_id
   ORDER BY trips DESC
   LIMIT 10;
   ```
   ````

4. Preview with `npm run dev`, press **Run** to check it, then set `draft: false` and publish.

The newest query opens first on `/sql/`; all published queries are listed in the query log,
newest first. If a file has no SQL block (or more than one), the build stops and names the file.

Use the SQLite dialect: e.g. `strftime('%w', requested_at)` for the weekday, `date(requested_at)` for the day.

**Changing the dataset:** edit `scripts/make_sql_dataset.py`, then run `py -3 scripts/make_sql_dataset.py`.
It rewrites `public/sql/rideshare.sqlite` and `docs/sql-dataset.md`. It always produces the same data.

## Add a new tab

Create a new folder in `src/content/notes/`, e.g. `Statistics`, and put a note in it.
The folder name becomes the tab name exactly as written (so `Math` shows as "Math"),
and the address is lowercase: `/notes/statistics/`. Notes tabs appear in A–Z order after Projects and SQL.
Don't name a notes folder `SQL`: that tab already exists.

A notes tab only appears on the live site once its folder has at least one note with `draft: false`.

## Drafts

`draft: true` hides a project, note or SQL query from the **live site**. It still shows when you preview
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
