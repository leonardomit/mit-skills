#!/usr/bin/env bun
// Put journal page without embed (avoid PGLite hang).
// MUST run from ~/gbrain (relative imports). Example:
//   cp this.js ~/gbrain/_put_journal_tmp.js
//   cd ~/gbrain && bun ./_put_journal_tmp.js 2026-07-31
import { loadConfig, toEngineConfig } from "./src/core/config.ts";
import { createEngine } from "./src/core/engine-factory.ts";
import { connectWithRetry } from "./src/core/db.ts";
import { configureGateway } from "./src/core/ai/gateway.ts";
import { readFileSync, existsSync, rmSync } from "fs";
import { createHash } from "crypto";
import { homedir } from "os";
import { join } from "path";

const day = process.argv[2] || new Date().toISOString().slice(0, 10);
const mdRel = `journal/${day}.md`;
const stage = join(homedir(), ".hermes/cache/gbrain-journal-stage", mdRel);
const lockDir = join(homedir(), ".gbrain/brain.pglite/.gbrain-lock");

if (!existsSync(stage)) {
  console.error("missing stage", stage);
  process.exit(1);
}

try {
  const lockFile = join(lockDir, "lock");
  if (existsSync(lockFile)) {
    const raw = readFileSync(lockFile, "utf8");
    let pid = null;
    try {
      pid = JSON.parse(raw).pid;
    } catch {
      const m = raw.match(/"pid"\s*:\s*(\d+)/);
      if (m) pid = Number(m[1]);
    }
    if (pid) {
      try {
        process.kill(pid, 0);
        console.log("lock held by live pid", pid);
      } catch {
        console.log("removing stale lock pid", pid);
        rmSync(lockDir, { recursive: true, force: true });
      }
    }
  }
} catch (e) {
  console.log("lock check:", e.message);
}

const content = readFileSync(stage, "utf8");
const slug = mdRel.replace(/\.md$/, "");
const config = loadConfig();
configureGateway({
  embedding_model: config.embedding_model,
  embedding_dimensions: 768,
  env: process.env,
});
const engCfg = toEngineConfig(config);
const engine = await createEngine(engCfg);
await connectWithRetry(engine, engCfg, { noRetry: true });

const body = content.replace(/^---[\s\S]*?---\n/, "");
const title = (content.match(/title:\s*"([^"]+)"/) || [, slug])[1];
const hash = createHash("sha256").update(body).digest("hex");

await engine.transaction(async (tx) => {
  await tx.putPage(slug, {
    type: "journal",
    title,
    compiled_truth: body.trim() + "\n",
    timeline: "",
    frontmatter: { type: "journal" },
    content_hash: hash,
    effective_date: new Date(day + "T00:00:00-03:00"),
    effective_date_source: "filename",
    import_filename: day,
    source_path: mdRel,
  });
  if (tx.replaceChunks) {
    await tx.replaceChunks(slug, [
      {
        chunk_index: 0,
        chunk_text: body.slice(0, 8000),
        chunk_source: "compiled_truth",
      },
    ]);
  }
});
const page = await engine.getPage(slug);
console.log("PAGE", page?.slug, page?.title);
await engine.disconnect();
setTimeout(() => process.exit(0), 400);
