---
name: to-testmo
description: Export manual-tcs.md test cases to Testmo — field mapping, issue link, configs, state. Use on "export to Testmo", /to-testmo.
---

# To Testmo — Export Test Cases

**Done when:** every TC in `tasks/{KEY}/gen/manual-tcs.md` exists exactly once in Testmo under the confirmed folder, linked to `{KEY}`, configs set, and state Pending Review.

## Contract

- **Args:** `{KEY}` [, Testmo folder URL, Module folder name, or `folder_id`]
- **Reads:** `tasks/{KEY}/gen/manual-tcs.md`; the id sections of `.claude/steering/testmo.md`
- **Writes:** nothing

Every id comes from `testmo.md`:

```bash
awk '/^## /{p = /Testmo Projects|Configurations by Project|Case Field IDs|Jira Issue Connections|Deep-Link URL Formats/} p' .claude/steering/testmo.md
```

A ticket prefix not found in `testmo.md` → confirm the project and connection once before creating anything.

## Field Mapping

Rich text uses `<br />`, never `\n`. Omit any field whose source value is empty.

| manual-tcs.md | `testmo_create_cases` param | Transform |
|---|---|---|
| Name | `name` | as-is |
| Test Scenario | `customFields.custom_description` | `<p>…</p>` |
| Pre-requisites | `customFields.custom_prerequisite` | split on `; `, strip trailing `;` from each item, prefix each with `- `, join with `<br />`, wrapped `<p>…</p>` |
| Steps + ER | `customFields.custom_steps` | see below |
| Test Data | `customFields.custom_test_data` | plain text |
| Priority | `customFields.custom_priority` | id per `testmo.md` § Case Field IDs |
| Pre-requisites + Login Method | `customFields.custom_prerequisite` | split Pre-requisites on `; `, strip trailing `;` from each item, prefix each with `- `, join with `<br />`; Login Method appended as the final line — present only when the template writes it inline (a TC spanning multiple platforms), wrapped `<p>…</p>` |

Fixed on every case: `projectId`, `folder_id` (confirmed), `state_id`, `issues: [{ display_id: "{KEY}", integration_id: 1, connection_project_id: <from § Jira Issue Connections, matched by {KEY}'s prefix> }]`.

`Test Case Type` is not exported — no Testmo field holds it.

**`custom_steps`** — one object per step; that step's `[N]`-keyed ER checkpoints join with `<br />` into `text3` as a **numbered list** (`1. … 2. …`), which is `null` when the step has no checkpoint:

```json
[{ "text1": "1. Step action text", "text2": null, "text3": "1. Checkpoint A.<br />2. Checkpoint B.", "text4": null }]
```

## Procedure

1. **Folder** — if a Testmo URL is given (e.g. `…/repositories/2?group_id=4686`), extract `project_id` from the path segment and `folder_id` from the `group_id` query param — no lookup needed. Otherwise: use a bare `folder_id` directly; a Module name → resolve with `testmo_list_folders`; neither → ask "Which Module folder?"

2. **Parse** `tasks/{KEY}/gen/manual-tcs.md` into the params above, one payload per TC.

   **Configuration** comes from the file header line `**Configuration:** <names>`; a `**Configuration:**` line inside a TC block overrides it for that TC (the multi-platform exception noted in `generate-tcs/TEMPLATE.md`). Split on `;`. Every name must match `testmo.md` § Configurations by Project exactly.

3. **Duplicate guard** — `testmo_find_cases_by_issue` for `{KEY}`. Cases already linked → present the overlap by Name and ask: create only the missing | create all anyway | abort. Skip only on an exact Name match.

4. **Create** — `testmo_create_cases`, max 100 payloads per call.

5. **Configs** — no `**Configuration:**` line anywhere → omit this step and report `configs none`. Otherwise, per created case id, call `testmo_set_case_configs` with the ids for that TC's configuration names.

6. **Report:**
```
Testmo export — {KEY}
  {n} cases in folder {folder_id} | configs {list or "none"} | state Pending Review
  {n} skipped as already linked
  {case deep-link, in the format read in the Contract's id lookup}
```
Name every failed TC with its error.

## Rules

- A missing or unmatched id — config, priority, folder, connection — stops the export. Ask; never substitute a plausible number.
