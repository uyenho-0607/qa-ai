# QA Lessons

One bullet per lesson, with its source ticket and date.

A lesson a *rule file already owns* goes in that rule file instead — a capture mechanic in
`.claude/steering/capture-*.md`, a driver quirk in the driver rule. Only what no rule file owns lands here.

<!-- Add lessons below -->
- **`download-jira-attachments.sh` writes to `.tmp/jira-tickets/{KEY}/attachments/`, not the
  `tasks/{KEY}/attachments/` that `project-config.md` § Folder Structure documents.** Copy what you need
  into `tasks/{KEY}/attachments/` after running it. (AO-925, 2026-08-26)
- **A checkpoint asserting "the modal closed" can be sampled too early.** Polling that breaks as soon as a
  success toast appears catches the toast while the modal is still mounted. Poll for *both* conditions, or
  re-sample a few seconds later, before recording the result. (AO-925, 2026-08-28)
