// Reads the content files for the pages. You shouldn't need to edit this.
import { getCollection, getEntry, type CollectionEntry } from "astro:content";

export type Project = CollectionEntry<"projects">;
export type Note = CollectionEntry<"notes">;
export type Profile = CollectionEntry<"profile">["data"];
export type Topic = { name: string; slug: string; notes: Note[] };

/** Drafts show up in `npm run dev` (labelled "Draft") but never on the live site. */
const showDrafts = import.meta.env.DEV;

export async function getProfile(): Promise<Profile> {
  const entry = await getEntry("profile", "profile");
  if (!entry) {
    throw new Error(
      "src/content/profile.yaml could not be read. Check the first error message above: it names the line to fix.",
    );
  }
  return entry.data;
}

/** Projects: featured first, then by `order`, then by title. */
export async function getProjects(): Promise<Project[]> {
  const all = await getCollection("projects", (p) => showDrafts || !p.data.draft);
  return all.sort(
    (a, b) =>
      Number(b.data.featured) - Number(a.data.featured) ||
      a.data.order - b.data.order ||
      a.data.title.localeCompare(b.data.title),
  );
}

/** "Machine Learning" -> "machine-learning" */
export const slugify = (s: string) =>
  s.toLowerCase().trim().replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "");

/** The folder a note is in, e.g. "SQL" for src/content/notes/SQL/joins.md */
function topicOf(note: Note): string {
  const parts = (note.filePath ?? "").split(/[\\/]/);
  return parts[parts.lastIndexOf("notes") + 1] ?? "Notes";
}

/** The web address of a note, e.g. /notes/sql/joins/ */
export function notePath(note: Note): string {
  const file = (note.filePath ?? note.id).split(/[\\/]/).pop()!.replace(/\.md$/, "");
  return `/notes/${slugify(topicOf(note))}/${slugify(file)}/`;
}

/** One topic per notes folder (A–Z), each with its notes newest first. */
export async function getTopics(): Promise<Topic[]> {
  const notes = await getCollection("notes", (n) => showDrafts || !n.data.draft);
  const byTopic = new Map<string, Note[]>();
  for (const note of notes) {
    const name = topicOf(note);
    byTopic.set(name, [...(byTopic.get(name) ?? []), note]);
  }
  return [...byTopic.entries()]
    .sort(([a], [b]) => a.localeCompare(b))
    .map(([name, list]) => ({
      name,
      slug: slugify(name),
      notes: list.sort((a, b) => b.data.date.getTime() - a.data.date.getTime()),
    }));
}

/** e.g. "25 Nov 2026" */
export function formatDate(date: Date): string {
  return date.toLocaleDateString("en-AU", { day: "numeric", month: "short", year: "numeric", timeZone: "UTC" });
}

/** Whether the SQL tab and its pages exist: `show_sql: true` in profile.yaml, or always in `npm run dev`. */
export async function sqlTabShown(): Promise<boolean> {
  return showDrafts || (await getProfile()).show_sql;
}
