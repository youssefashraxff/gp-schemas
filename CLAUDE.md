# gp-schemas: notes for Claude

The shared JSON Schemas for the Concept Development GP. They are the **single source of
truth** for every piece of data that crosses the API, the WebSocket or a saved phase result.
gp-backend generates Pydantic models from them and gp-frontend generates TypeScript types;
both pin this repo as a git submodule.

## Read before any task

The SDLC documents in gp-backend (`docs/sdlc/<phase>/spec.md`, section 5.2) say which schema
changes a phase needs. Change exactly those, and put the plan task ID in the PR title.

## Rules

- **Each schema file is self-contained:** shared pieces (like `Evidence` and `Fact`) are copied
  into the file's own `$defs`, not referenced across files. If you change a shared piece, change
  every copy in the same PR.
- **No estimated facts:** `Evidence.fact_type` is only `computable`, `retrieved` or `expert`.
  Never add `estimate`, `assumption` or a confidence score; a missing source means the agent
  escalates.
- **Progress names say their level:** `progress_phase`, `progress_status`, `progress_step`,
  `progress_percent`, `progress_agent`.
- **Keep the compact style** of the existing files (one property per line).
- Renaming or removing a field breaks both consumers. Say so in the PR, and list what
  gp-backend and gp-frontend must change when they bump the submodule.

## Check

```bash
check-jsonschema --check-metaschema schemas/*.schema.json
```

## Git and PRs

- Branch from `develop`; one change per PR, into `develop`. Only the project lead merges.
- Explain **what** changed, **why**, and what each consumer must do, in plain language.

## Hooks in this repo (`.claude/settings.json`)

| Hook | What it does |
|---|---|
| Before a shell command | Blocks pushing to `main`/`develop`, force pushes, and committing while on `main`/`develop` |
| After an edit | Validates an edited `*.schema.json` (valid JSON and valid JSON Schema); problems come back to Claude |
