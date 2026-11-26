// Defines what each content file must contain. If something is missing or
// wrong, `npm run dev` / `npm run build` stops and tells you the file and field.
// You shouldn't need to edit this file unless you want to add a new field.
import { defineCollection } from "astro:content";
import { glob, file } from "astro/loaders";
import { z } from "astro/zod";
import { parse as parseYaml } from "yaml";

/** Friendly messages: says whether the field is missing or just wrongly written. */
const hint = (field: string, example: string) => ({
  error: (issue: { input?: unknown }) =>
    issue.input === undefined
      ? `missing. Add a line like:  ${field}: ${example}`
      : `not valid. It should look like:  ${field}: ${example}`,
});
const text = (field: string, example: string) =>
  z.string(hint(field, example)).trim().min(1, `is empty. Write something, e.g.  ${field}: ${example}`);
const optionalUrl = (field: string, example: string) =>
  z.union([z.literal(""), z.url(hint(field, example))], hint(field, example)).default("");

// ---------- src/content/profile.yaml ----------
const profile = defineCollection({
  loader: file("src/content/profile.yaml", {
    parser: (raw) => [{ id: "profile", ...(parseYaml(raw) ?? {}) }],
  }),
  schema: z.object({
    name: text("name", '"Quyen Pham (Quinn)"'),
    headline: text("headline", `"*Data scientist* by day"`), // big text at the top of the home page
    bio: text("bio", '"Based in Adelaide. ..."'),
    email: z
      .union([z.literal(""), z.email(hint("email", '"you@example.com"'))], hint("email", '"you@example.com"'))
      .default(""),
    github: optionalUrl("github", '"https://github.com/your-name"'),
    linkedin: optionalUrl("linkedin", '"https://www.linkedin.com/in/your-name"'),
    resume: z.string(hint("resume", '"/resume/"')).default("/resume/"),
    // SQL tab: false hides it (and its pages) on the live site; it still shows in `npm run dev`.
    show_sql: z.boolean(hint("show_sql", "true")).default(false),
    // "Open to work" badge in the top right corner of every page.
    open_to_work: z.boolean(hint("open_to_work", "true")).default(false),
    // The card on the right of the Projects tab. Empty text = no card.
    projects_card: z
      .object({
        title: z.string().default("What's this?"),
        text: z.string().default(""),
      })
      .default({ title: "What's this?", text: "" }),
    experience: z
      .array(
        z.object({
          role: text("role", '"Data Analyst"'),
          organisation: text("organisation", '"Company name"'),
          location: z.string().optional(),
          start: text("start", '"Mar 2023"'),
          end: text("end", '"Present"'),
          points: z.array(z.string()).default([]),
        }),
      )
      .default([]),
    // Resume extras: a line under your name and a short paragraph at the top.
    location: z.string().default(""),
    summary: z.string().default(""),
    // Either a plain list ["Python", "SQL"] or groups: [{ group: "Data & BI", items: ["SQL"] }]
    skills: z
      .array(
        z.union(
          [
            z.string(),
            z.object({
              group: text("group", '"Data & BI"'),
              items: z.array(z.string(), hint("items", '["SQL", "Power BI"]')),
            }),
          ],
          hint("skills", '[{ group: "Data & BI", items: ["SQL", "Power BI"] }]'),
        ),
      )
      .default([]),
    education: z
      .array(
        z.object({
          qualification: text("qualification", '"Bachelor of ..."'),
          institution: text("institution", '"University name"'),
          location: z.string().optional(),
          year: z.union([z.string(), z.number()]).optional(),
          note: z.string().optional(),
        }),
      )
      .default([]),
  }),
});

// ---------- src/content/projects/*.md ----------
const projects = defineCollection({
  // Files starting with "_" (like _template.md) are ignored.
  loader: glob({ base: "./src/content/projects", pattern: "[^_]*.md" }),
  schema: ({ image }) =>
    z.object({
      title: text("title", '"Battery trading simulation"'),
      summary: text("summary", '"One or two sentences for the card."'),
      tools: z.array(z.string(), hint("tools", '["Python", "pandas"]')).default([]),
      github: z.url(hint("github", '"https://github.com/phquyen/repo"')).optional(),
      demo: z.url(hint("demo", '"https://example.com"')).optional(),
      // Optional picture for the card and the top of the page (path relative to the .md file).
      cover: image().optional(),
      cover_alt: z.string().default(""),
      // Optional key numbers (up to 4), shown as big tiles on the card and the page.
      highlights: z
        .array(
          z.object({
            value: text("value", '"+47.5%"'),
            label: text("label", '"profit vs a simple rule"'),
          }),
          hint("highlights", '[{ value: "+47.5%", label: "profit vs a simple rule" }]'),
        )
        .max(4, "has more than 4 items. Keep the 4 most important numbers.")
        .default([]),
      featured: z.boolean(hint("featured", "true")).default(false),
      order: z.number(hint("order", "10")).default(100),
      draft: z.boolean(hint("draft", "false")).default(false),
    }),
});

// ---------- src/content/notes/<Topic>/*.md ----------
const notes = defineCollection({
  // Only files inside a topic folder count; each folder becomes a tab.
  loader: glob({ base: "./src/content/notes", pattern: "*/[^_]*.md" }),
  schema: z.object({
    title: text("title", '"Limits, explained simply"'),
    summary: text("summary", '"One sentence for the list."'),
    date: z.coerce.date(hint("date", "2026-11-25")),
    draft: z.boolean(hint("draft", "false")).default(false),
  }),
});

// ---------- src/content/sql/*.md ----------
// A short question in Markdown plus exactly one ```sql block (checked in src/lib/sql.ts).
const sql = defineCollection({
  loader: glob({ base: "./src/content/sql", pattern: "[^_]*.md" }),
  schema: z.object({
    title: text("title", '"Busiest day of the week"'),
    date: z.coerce.date(hint("date", "2026-11-25")),
    difficulty: z.enum(["easy", "medium", "hard"], hint("difficulty", '"easy" (or "medium" / "hard")')),
    skills: z.array(z.string(), hint("skills", '["GROUP BY", "JOIN"]')).default([]),
    draft: z.boolean(hint("draft", "false")).default(false),
  }),
});

export const collections = { profile, projects, notes, sql };
