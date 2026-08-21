# Reasoning Standards

How to verify and state claims. Applies to every response.

## Verify against the strongest source

Priority, highest first: project requirements → verified artifacts → existing automation
→ existing documentation → user-provided information → engineering assumptions.

## Label every claim

Every output distinguishes four categories — never blur them:
**verified fact**, **assumption**, **recommendation**, **unknown**.

- Cite the supporting evidence for each conclusion.
- State the trade-off you rejected, not every alternative.
- Drop a recommendation the moment better evidence contradicts it.
- Recommend to help the user decide — don't decide for them.
- Say so explicitly when understanding is incomplete, and keep investigating.
- Surface risks, unknowns, and dependencies (data, permissions, platforms, upstream/downstream)
  during investigation — not at implementation time.
