---
name: exec-workflow
description: End-to-end manual SIT execution workflow — fetch Jira, collect TCs, design exec plan, run tests, paste evidence into a doc, and report. Use when user says "run full workflow", "exec workflow", /exec-workflow.
---

# Exec Workflow

## Contract

- **Args:** `{KEY}` — Jira ticket key (required)
- **Delegates:** `manual-exec-design`, `manual-exec-run`
- **Reads:** `tasks/{KEY}/exec/report.md`; `tasks/{KEY}/exec/.upload/ledger-*.md` (only to chase a flagged capture)
- **Writes:** nothing directly — every artifact belongs to a delegate
- **Guardrails:** Execute all phases strictly in sequence. Configuration is collected once in Phase 1 and passed through unchanged.

---

## Phase 1 — Setup

Prompt user in **one message**. Wait for all answers before proceeding:

> 1. **Gates**: [off (default) | on] — Pause for approval at the design summary gate.
> 2. **Evidence mode**: [normal (default) | screenshot] — `normal` captures video evidence; `screenshot` captures screenshots only.
> 3. **Evidence destination** — the options depend on the mode, because video cannot be inlined in a Doc:
>    - `normal` → [new-drive (default) | drive:{url}]
>    - `screenshot` → [new-doc (default) | user-doc:{url}]
> 4. **Annotations**: [no (default) | yes] — Label captures with TC ID and checkpoint.
> 5. **Platforms**: [all enabled (default) | {ids}] — Scope the run to specific platform ids from `project-config.md` § Platforms.

Reject a destination that does not match the mode — re-ask with only the valid options.

Done when: All five configuration values are recorded.

---

## Phase 2 — Exec Plan Design

If `tasks/{KEY}/exec/exec.md` is missing: invoke `/manual-exec-design {KEY}`, `evidence={evidence_mode}`, `annotations={annotations}` [, `platforms={ids}`] [, `no-gate` if `gates = off`]. The design skill fetches its own missing inputs (`jira.md`, `tc.md`).

Done when: `tasks/{KEY}/exec/exec.md` exists and design gate is passed.

---

## Phase 3 — Execution

Invoke `/manual-exec-run {KEY}`. A `new-drive`/`new-doc` destination is the callee's own default — omit the arg. A `drive:{url}` or `user-doc:{url}` destination passes as `evidence_dest={the bare url}`.

Done when: Every result line in `exec.md` is resolved (no `⏳ PENDING`) and `tasks/{KEY}/exec/report.md` exists.

---

## Phase 4 — Evidence Verification

Read the `Missing` and `Anomalies` lines out of `tasks/{KEY}/exec/report.md` § Evidence Audit — Phase 3 already ran the `evidence-auditor` agent and wrote its output there. Act on them: a capture that needs re-taking needs the live session, so it comes back to you here.

The per-wave upload ledgers sit in `tasks/{KEY}/exec/.upload/ledger-*.md` — read one only to chase a capture the auditor flagged.

`report.md` carries no auditor output → dispatch the `evidence-auditor` agent for `{KEY}` with the destination now. No Agent tool in context → dispatch nothing — cross-reference `tasks/{KEY}/exec/evidence/` against the destination yourself and follow `evidence-auditor.md` § Run step 5.

Done when: All executed TC evidence is present in the destination. Present evidence destination URL to user.
