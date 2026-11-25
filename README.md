# gp-schemas

Shared data contracts for the Concept Development GP. Single source of truth for the shapes that cross the frontend/backend boundary and the phase boundaries.

Included as a **git submodule** at `schemas/` in both `gp-backend` and `gp-frontend`. Each repo generates its own types from these files:

- Backend → Pydantic models (`datamodel-code-generator`)
- Frontend → TypeScript interfaces (`json-schema-to-typescript`)

## Schemas

| File | What it describes |
|---|---|
| `schemas/concept_input.schema.json` | What a client submits to start a concept |
| `schemas/phase_result.schema.json` | A saved, versioned phase output with field-level `built_from` references and content hashes |
| `schemas/concept.schema.json` | The stored concept returned by `POST /concepts` |
| `schemas/progress_event.schema.json` | The progress message sent over the WebSocket |
| `schemas/evidence.schema.json` | Where one fact came from (computable / retrieved / expert). Copied into other schemas' `$defs` |
| `schemas/escalation.schema.json` | A question an agent asks the expert mid-task, and its answer |
| `schemas/research_output.schema.json` | The output fields of Phase 1 (Research), every fact with evidence |

## Changing a schema

1. Branch from `develop`, edit the schema, open a PR (Youssef reviews).
2. After merge, bump the submodule in each consuming repo:
   ```bash
   cd schemas && git fetch && git checkout <new-commit> && cd ..
   # regenerate types (see that repo's README), commit both together
   ```
3. CI in each repo fails if generated types don't match the pinned schemas commit.

Keep schemas self-contained (shared pieces go in `$defs` inside the same file) so both generators handle them cleanly.
