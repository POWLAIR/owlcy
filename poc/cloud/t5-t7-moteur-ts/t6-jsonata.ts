// T6 — JSONata : les expressions ${…} de doc/feature/02-pipelines-factory.md sur un contexte de run réaliste
import jsonata from "jsonata";

const ctx = {
  params: { sources: ["https://a.dev/rss", "https://b.dev/rss"], topics: "agents IA", notion_db: "db_123" },
  item: "https://a.dev/rss",
  collect: { output: [
    [{ title: "A1", link: "https://a.dev/1" }, { title: "A2", link: "https://a.dev/2" }],
    [{ title: "B1", link: "https://b.dev/1" }],
  ] },
  filter: { output: [{ title: "A1", link: "https://a.dev/1" }, { title: "B1", link: "https://b.dev/1" }] },
  digest: { output: { points: ["p1", "p2", "p3"] } },
  previous: { output: { links: ["https://a.dev/1"] } },
};

const cases: { expr: string; expect: unknown; where: string }[] = [
  { where: "l.24 foreach", expr: "params.sources", expect: ctx.params.sources },
  { where: "l.26 with.url", expr: "item", expect: "https://a.dev/rss" },
  { where: "l.29 $flatten", expr: "$flatten(collect.output)", expect: null /* JSONata n'a pas $flatten natif : on teste */ },
  { where: "l.29 équivalent natif", expr: "collect.output.*", expect: 3 },
  { where: "l.35 when $count", expr: "$count(digest.output) > 0", expect: true },
  { where: "l.38 with.database", expr: "params.notion_db", expect: "db_123" },
  { where: "l.118 dédoublonnage (doc)", expr: "collect.output[link in $not(previous.output.links)]", expect: null },
  { where: "l.118 dédoublonnage (corrigé)", expr: "collect.output.*[$not(link in $$.previous.output.links)]", expect: 2 },
  { where: "l.121 retry.until", expr: "$count(digest.output.points) <= 5", expect: true },
  { where: "l.123 validate", expr: "$count(digest.output.points) > 0", expect: true },
];

const results = [];
for (const c of cases) {
  let value: unknown, error: string | undefined;
  try { value = await jsonata(c.expr).evaluate(ctx); } catch (e: any) { error = `${e.code ?? ""} ${e.message}`.trim(); }
  const shown = Array.isArray(value) && typeof c.expect === "number" ? value.length : value;
  const ok = error === undefined && (c.expect === null ? true : JSON.stringify(shown) === JSON.stringify(c.expect));
  results.push({ where: c.where, expr: c.expr, ok, value: shown, error });
}
// Perf : une expression compilée évaluée 10 000 fois
const e = jsonata("$count(collect.output.*[$not(link in $$.previous.output.links)])");
const t0 = performance.now();
for (let i = 0; i < 10_000; i++) await e.evaluate(ctx);
const perf_us = +(((performance.now() - t0) / 10_000) * 1000).toFixed(1);
console.log(JSON.stringify({ jsonata: "2.2.2", results, eval_us_per_call: perf_us }, null, 2));
