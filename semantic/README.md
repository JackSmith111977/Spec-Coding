# Semantic IR

This directory holds version-bound **derived** Semantic IR for Spec Coding.

- Canonical Markdown under `docs/` remains the Source of Truth.
- `pilot/` is an experimental corpus used to validate the V3 Semantic Compiler model and is **not** a complete release IR.
- A future full `release` scope must cover every Canonical Workflow, Rule, Exception Workflow, and Meta Protocol registered by `docs/manifest.yaml` and pass independent semantic + mutation review.

Do not manually patch released IR to change Spec Coding semantics. Change the earliest Canonical source, then recompile.
