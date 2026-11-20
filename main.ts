// Entry point for the news-image-20261119 competition.
//
// The artwork itself lives in entry.png, rendered ahead of time by draw.py.
// At run time there is no network and nothing to compute: this program just
// delivers the committed PNG to the output folder, byte for byte, so every
// run produces exactly the same file.
//
//   node main.ts                                  -> writes /output/entry.png
//   MAKEFUN_OUTPUT_DIR=out node main.ts           -> writes out/entry.png
//
// Node 22, standard library only.

import { copyFileSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

// Resolve the folder this file sits in, then locate the image beside it.
const here = dirname(fileURLToPath(import.meta.url));
const sourceImage = join(here, "entry.png");

// The grader mounts its output folder at /output; locally the caller can
// redirect it with the MAKEFUN_OUTPUT_DIR environment variable.
const outputDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
mkdirSync(outputDir, { recursive: true });

// A straight copy keeps the bytes identical on every run (deterministic).
copyFileSync(sourceImage, join(outputDir, "entry.png"));
