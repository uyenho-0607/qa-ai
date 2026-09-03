# TC Execution Classification

## Agent-Executable

- Setup, actions, and expected result must all be deterministic and objectively verifiable.
- Expected result must be checkable against an observable in the TC's platform pack § Observables.

## Human-Executable

- Expected result requires subjective visual or UX judgment.
- Success criteria require human business interpretation.
- TC depends on a physical device, hardware token, or out-of-band system.
- Executing the steps would not validate the actual business intent.
- Biometric authentication (fingerprint, face).

## Ask before classifying

- Ask first, then classify.
- Ask before classifying when: a required test account does not exist · a TC prerequisite is ambiguous · feature behavior remains unconfirmed after UI exploration · a TC covers a scenario absent from the requirement (confirm scope).

## Precedence

- Requirement beats test case on all conflicts.
