# Evidence Strategy

Executed at Phase 4. Tier-1 TCs verified at recon require no further planning.

---

## File Naming (Stem)

The plan defines the **stem**. The execution run appends `_{platform_id}.{ext}`. The length limit lives in `capture-mechanics.md` § File name.

- **Group / Video stem**: `TC_{ids}_{slug}`
- **Frame stem**: `TC_{ids}_c{N}[_c{M}...]_{slug}`
- **`{ids}`**: The case ids carried in the TC subtitles of `tc.md` — whatever the TC source named in `project-config.md` § Producers issues — joined by `_` (e.g. `161963`, or `161976_161977` for a merged pair). **NEVER use plan sequential IDs (e.g., `TC-1`)**.
- **`c{N}`**: Numbers from the TC **Expected** list covered by the frame (e.g., `c1`, `c1_c2`).
- **`{slug}`**: 2–4 `snake_case` words describing the assertion.

---

## `normal` Mode

Populates `## Evidence` → `### Groups`.

### Type Selection (SCREENSHOT Default, VIDEO Last Resort)

- **SCREENSHOT**: Assign by default if a still frame (or sequence of stills) proves the assertion.
- **VIDEO**: Assign **ONLY** if ALL criteria are met:
  1. Assertion depends on continuous timing/sequence with no resting state (e.g., transient toast clearing in 1 step).
  2. Sequential screenshots cannot substitute.
  3. Assertion is *not* a negative/absence check (proven by backend check + still frame).

### Grouping Rules

- **Group TCs into 1 row** if ALL hold: Same platform, same precondition/starting screen, sequential execution without teardown, distinct capture moments, failure in one TC does not obscure another.
- **Split TCs into separate rows** if ANY hold: Different preconditions, teardown required between TCs, or potential failure corruption.
- **Cross-Platform Exception**: A paired TC is the **only case where a platform change does NOT trigger a group split**. Do not split into two platform groups; keep as 1 paired group capturing once per side into files distinguished by platform suffix (`_{platform_id}`).
- **Solo TCs**: A TC that does not group still gets a 1-TC row in the Groups table.

---

## `screenshot` Mode

Populates `## Evidence` → `### Frames`. Omit the Groups table entirely.

### Frame Sharing Rules
One frame may prove multiple expected results (within or across TCs) ONLY if ALL hold:
- Every covered entry is visible simultaneously without scrolling.
- All entries hold at the same instant on the same screen.
- Failure in one assertion does not make another ambiguous.

### Frame Limitations (`Video needed for`)
- Screenshots cannot prove transient elements, disappearances, strict ordering, or negative states.
- List any such expected result entry in the `Video needed for` column and assign a VIDEO for that specific assertion.