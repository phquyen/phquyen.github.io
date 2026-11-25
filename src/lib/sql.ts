// Reads the SQL query files and the fictional RideNest database at BUILD time.
// You shouldn't need to edit this.
import { readFile } from "node:fs/promises";
import { join } from "node:path";
import { getCollection, type CollectionEntry } from "astro:content";
import initSqlJs from "sql.js";

export type SqlEntry = CollectionEntry<"sql">;
export type SqlQuery = SqlEntry & { sql: string };
export type ResultSet = { columns: string[]; rows: (string | number | null)[][]; total: number; error?: string };
export type TablePreview = ResultSet & { name: string };

export const DB_URL = "/sql/rideshare.sqlite";
export const DOCS_URL = "https://github.com/phquyen/phquyen.github.io/blob/main/docs/sql-dataset.md";
export const PREVIEW_TABLES = ["trips", "riders", "drivers", "promos"];
export const MAX_ROWS = 500;

const showDrafts = import.meta.env.DEV;

/** The single ```sql block in a query file. Stops the build with a clear message otherwise. */
function extractSql(entry: SqlEntry): string {
  const blocks = [...(entry.body ?? "").matchAll(/```sql[^\n]*\n([\s\S]*?)```/g)];
  if (blocks.length !== 1) {
    throw new Error(
      `src/content/sql/${entry.id}.md must contain exactly one \`\`\`sql code block (found ${blocks.length}). ` +
        "Put the query between a line with ```sql and a line with ```.",
    );
  }
  return blocks[0][1].trim();
}

/** All query files (drafts only in `npm run dev`), newest first. */
export async function getQueries(): Promise<SqlQuery[]> {
  const entries = await getCollection("sql", (q) => showDrafts || !q.data.draft);
  return entries
    .map((entry) => ({ ...entry, sql: extractSql(entry) }))
    .sort((a, b) => b.data.date.getTime() - a.data.date.getTime() || a.data.title.localeCompare(b.data.title));
}

// The database is loaded once per build and shared by every page.
let dbBytes: Promise<Uint8Array> | undefined;
let engine: ReturnType<typeof initSqlJs> | undefined;

async function openDb() {
  // Builds always run from the project folder, so this path is stable.
  dbBytes ??= readFile(join(process.cwd(), "public", "sql", "rideshare.sqlite")).then((b) => new Uint8Array(b));
  engine ??= initSqlJs();
  const [SQL, bytes] = await Promise.all([engine, dbBytes]);
  return new SQL.Database(bytes);
}

/** Runs a query for real (at build time) and returns up to MAX_ROWS rows. */
export async function runQuery(sql: string): Promise<ResultSet> {
  const db = await openDb();
  try {
    const results = db.exec(sql);
    const last = results.at(-1);
    if (!last) return { columns: [], rows: [], total: 0 };
    return { columns: last.columns, rows: last.values.slice(0, MAX_ROWS) as ResultSet["rows"], total: last.values.length };
  } catch (err) {
    return { columns: [], rows: [], total: 0, error: err instanceof Error ? err.message : String(err) };
  } finally {
    db.close();
  }
}

/** First 5 rows and the row count of each table, for the preview tabs. */
export async function getTablePreviews(): Promise<TablePreview[]> {
  return Promise.all(
    PREVIEW_TABLES.map(async (name) => {
      const head = await runQuery(`SELECT * FROM ${name} LIMIT 5`);
      const count = await runQuery(`SELECT COUNT(*) FROM ${name}`);
      return { name, ...head, total: Number(count.rows[0]?.[0] ?? 0) };
    }),
  );
}

/** Queries per day (YYYY-MM-DD -> count), for the activity grid. */
export function countByDay(queries: SqlQuery[]): Map<string, number> {
  const counts = new Map<string, number>();
  for (const q of queries) {
    const day = q.data.date.toISOString().slice(0, 10);
    counts.set(day, (counts.get(day) ?? 0) + 1);
  }
  return counts;
}
