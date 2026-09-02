# Semantic Compiler Frontend

The Semantic Compiler separates **what Spec Coding means** from **how a target Coding Agent implements it**.

```text
Canonical Workflow / Rules / Exception / Meta Protocol
        ↓
Source Resolution
        ↓
Per-document Worklist
        ↓
Atomic Extraction + Fresh Review (Agent)
        ↓
Semantic Integration (Agent)
        ↓
IR Verification
        ↓
Semantic IR
```

It intentionally has **no Target, Adoption Baseline, Runtime, model, tool, Subagent, workspace, or Harness output dependency**. Those belong to the later Harness backend.

## Commands

```bash
python -m tools.semantic_compiler resolve \
  --spec-root . \
  --output .semantic-state/source-manifest.json

python -m tools.semantic_compiler prepare \
  --source-manifest .semantic-state/source-manifest.json \
  --output .semantic-state/worklist.json

python -m tools.semantic_compiler validate \
  --source-manifest .semantic-state/source-manifest.json \
  --ir semantic/pilot/clauses.json \
  --output .semantic-state/validate.json

# release scope additionally supplies a separately produced review receipt:
#   --review-receipt .semantic-state/review-receipt.json
```

`prepare` creates exactly one extraction + fresh-review work item per Canonical document. It is short-lived execution state, not a new Source of Truth; its purpose is to prevent the Agent from silently choosing only the mainline documents.

## Extraction contract

Extraction is semantic work and is intentionally not faked by the deterministic tool.

For each worklist document, a fresh Extractor should:

1. classify content as `NORMATIVE`, `GUIDANCE`, `EXAMPLE`, `RATIONALE`, or `NAVIGATION`;
2. turn every independent normative behavior into one or more Atomic Clauses;
3. preserve trigger/condition, strength, prohibition, state transition, authority, artifact, and failure-routing semantics;
4. keep precise source bindings using document path + stable heading anchor;
5. leave Runtime strategy out of the Clause.

One source span may yield multiple Clauses, and one Clause may cite multiple sources. Markdown headings are audit/navigation boundaries only; they do not define semantic cardinality.

### Clause kinds

- `invariant`: must continue to hold.
- `trigger`: a condition activates behavior.
- `gate`: a condition blocks or permits progression.
- `transition`: an authoritative state change.
- `authority`: who may decide or mutate semantics.
- `artifact`: persistent or handoff fact requirements.
- `routing`: correction, escalation, or exception routing.

### Semantic relations

Stable execution semantics may be expressed with `requires`, `before`, `triggers`, `blocks`, `specializes`, and `isolated_from`.

Do **not** encode Runtime strategy such as a concrete Subagent, model, thinking level, worktree count, parallelism, or vendor-specific file. Encode the stable requirement (for example `fresh + read-oriented + isolated_from implementation`); the Harness backend may later realize it with a fresh Reviewer Subagent when the Runtime supports that mechanism.

## Integration and review

Each document must complete extraction and Fresh Review before global integration. Integration may deduplicate equivalent meaning and recover dependencies, specialization, hard ordering, triggers, and isolation requirements, but must not summarize away independent obligations.

The deterministic validator checks source/version binding, scope, Clause shape, unique IDs, relation targets, and hard-order cycles. A `release` scope additionally requires a separately produced Review Receipt binding the same source fingerprint, with per-document review, global review, and semantic mutation review. The deterministic validator checks the receipt contract but does not pretend to create reviewer independence itself.

Markdown Canonical documents remain the Source of Truth. Semantic IR is a derived, version-bound release artifact and must be regenerated rather than manually patched when source semantics change.
