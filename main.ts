// main.ts — entry program for the bounty "Promote make.fun's
// make-your-own-bounty post on X" (post-x-promote-make-your-own-bounty-01).
//
// The entry itself is a post on X. This repository names that post in
// POST.json at its root, and this program's whole job is to copy POST.json
// into the output directory the grader points at, so the house can read
// the post's address from the output and go read the post itself.
//
// Standard library only, no network, no arguments. Runs on Node 22+,
// which executes TypeScript as it stands.

import { copyFileSync, existsSync, mkdirSync, readFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));

// The post file ships beside this program, in the repository root.
const source = join(here, "POST.json");

// The grader sets MAKEFUN_OUTPUT_DIR; /output is the documented default.
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
const dest = join(outDir, "POST.json");

if (!existsSync(source)) {
  console.error(`POST.json not found next to main.ts (looked in ${here})`);
  process.exit(1);
}

// Read the file once before copying it: a malformed POST.json should fail
// here, in the open, rather than after it has landed in the output. The
// house wants a JSON object whose "url" names the post on X.
const parsed: unknown = JSON.parse(readFileSync(source, "utf8"));
if (
  typeof parsed !== "object" ||
  parsed === null ||
  typeof (parsed as { url?: unknown }).url !== "string"
) {
  console.error('POST.json must be a JSON object with a string "url" field');
  process.exit(1);
}

mkdirSync(outDir, { recursive: true });
copyFileSync(source, dest);
console.log(`copied ${source} -> ${dest}`);
