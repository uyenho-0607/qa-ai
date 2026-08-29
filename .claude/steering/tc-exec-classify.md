## Agent-Executable

- Setup, actions, and expected result must all be deterministic and objectively verifiable.
- Verify expected result using DOM state, text content, network response, or toast message.
- Evidence must objectively confirm the expected result.
- Treat DOM attributes as objective facts.
- Evaluate step complexity for multi-session TCs, not session count.
- Restore state after any state-changing TC; document the restore step before executing.
- Evaluate expected results against the requirement, not the TC assertion.

## Human-Executable

- Expected result requires subjective visual or UX judgment.
- Success criteria require human business interpretation.
- TC depends on a physical device, hardware token, or out-of-band system.
- Executing the steps would not validate the actual business intent.

## Blocked

- Ask first, then classify. Never silently downgrade to human-executable.
- When a required test account does not exist, ask before classifying.
- When a TC prerequisite is ambiguous, ask before classifying.
- When feature behavior remains unconfirmed after UI exploration, ask before classifying.
- When a TC covers a scenario absent from the requirement, confirm scope before classifying.

## Priority

- Requirement beats test case on all conflicts.
- Live app beats domain file on all UI facts.
