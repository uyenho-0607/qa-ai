---
name: capture-evidence
description: Capture screenshot or video evidence on any supported target. Receives structured input, returns file paths. Use when capturing evidence, or when user says /capture-evidence or /capture-screenshot.
---

# Capture Evidence

## Contract

- **Args:** `targets={ids}`, `stem={caller stem}`, `dest={output dir}` [, `type={screenshot|video}`, case-insensitive, default `screenshot`] [, `element=`, `label=` — required together when `annotation=yes`] [, `annotation={yes|no}` — web targets only, default `no`]
- **Reads:** `project-config.md` § Platforms — extract, never whole: `awk '/^## /{p=/^## (Platforms)$/} p' .kiro/steering/project-config.md`; `capture-mechanics.md`; the resolved platform pack; the target's driver rule and capture mechanics file for its Group
- **Writes:** evidence files to caller-provided `dest`

---

## Pre-Flight

Read `.kiro/steering/capture-mechanics.md`. For each target in `targets`, resolve its pack from `project-config.md` § Platforms, load both the driver rule and the capture mechanics file for its Group per `capture-mechanics.md`, and read the pack's § Targets, § Label overlay, § Preflight, and § Stack quirks sections.

---

## Input / Output

**Input:**

    stem:             "{caller-defined stem}"         # e.g. TC_{case_id}_submit_form / {KEY}_bug_1
    dest:             "tasks/{KEY}/exec/evidence/"    # output directory
    element:          "{id= | desc= | text= of the asserted element}"
    label:            "{what is being verified}"

**Output:**

    file_paths: ["{dest}{stem}_{target}.{png|mp4}"]

---

## Flow

Per requested target, in order:

1. **Resolve the target** per its pack § Preflight. An unavailable target returns an unavailability status — never a substituted device or target.
2. **Reach the asserted state.** Navigate or launch, then bring the element into view.
3. **Confirm the element is there** per the target's driver rule — a fresh query immediately before action, never a coordinate. An unresolvable element is reported back to the caller with a capture of the screen it sits on.
4. **Capture**, per the target's mechanics file and `type`.
5. **Verify the capture** per `capture-mechanics.md` § Verify.
6. **Return the file paths** and what each capture shows — the caller records that, not a file. A target that could not run is reported, never skipped silently.

---

## Hard Rules

- **Annotation:** `annotation=yes` → apply the label overlay per `capture-web.md` § Element annotation, using `element` and `label` from the Input. `no` → inject zero labels, overlays, element borders, or checkpoint divs.
- **No Unscripted Exploration:** Never re-explore to find an element the caller already named — use what was passed.
- **File Retention:** Never auto-delete a file. Wait for confirmation.
