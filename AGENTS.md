# Repository Guidelines

## What this is

A single-target reverse-engineering archive: what Netron (the Electron model
viewer) actually does, and which of its design decisions are worth carrying
into `ai-model-viewer` (the Rust reimplementation next door).

Not a software project — no build, no tests, no CI, no package manifest. It is
one article plus the evidence behind it.

## Layout

```
reports/netron-architecture.md    the article — start here
evidence/netron-*.json            raw REA output, 60MB, tracked on purpose
scripts/analyze.sh                re-runs the analysis against a target app
scripts/summarize.py              condenses the 60MB JSON into readable output
```

## Commands

```bash
python3 scripts/summarize.py                 # read the evidence, ~1s
./scripts/analyze.sh                         # re-run REA, ~70s, overwrites evidence/
./scripts/analyze.sh /abs/path/to/Other.app  # analyze a different target
```

Requirements: Node.js >=22.19 (or 24.x >=24.11, or 26+) and npm. REA is invoked
via `npx -y rea-agents@latest`; no global install, no lockfile.

## Evidence discipline

This is the part that matters.

- **Every number in the article traces to a count in the source or the evidence
  JSON.** If you add a figure, say where it came from — a file and line in the
  extracted `app.asar/source/*.js`, or a path in the evidence JSON.
- **Counts are reproducible; designs are inferred.** Line counts, byte counts,
  registry sizes, channel names are checkable. "This exists so that X" is a
  reading of the code, not a statement by the author. Keep those two apart in
  the prose.
- **The binary's sha256 identifies the analysis.** `subject.digest.sha256` in the
  evidence must match the app being discussed. A different Netron build
  invalidates every figure in the article.
- **Re-running does not reproduce byte-identical JSON.** REA output embeds
  absolute paths and per-run sequencing. Do not treat a diff as a regression;
  compare `subject.digest.sha256`.
- **Netron auto-updates.** It updated 9.3.1 → 9.3.2 mid-analysis. When the
  installed version moves, re-derive the figures or state the version the
  article is pinned to. `scripts/analyze.sh` names its output after the
  installed version for this reason.
- **Static only.** No runtime observation was performed. Claims like "the
  renderer never sends model data over IPC" are static observations about the
  code, not observations about a running app.

## Adding a second target

Don't. This repo is scoped to Netron. A second target belongs in its own
repository so its sha256 provenance stays unambiguous.

## Style

- Chinese prose, English technical terms (Electron, IPC, protobuf, source map).
  Match `reports/netron-architecture.md`.
- Compare across categories in tables, not in prose sentences.
- Every section ends with a **抄 / 不抄** judgement. That is the article's
  actual deliverable — a reader must be able to act on it.
- The reader is assumed to be building a model viewer, not a general reader.
  Skip explaining what protobuf is.
