# QA Lessons

Reusable lessons from bug verification, test execution, and exploratory sessions. One bullet per lesson, with
its source ticket or date. `report-bug` and `verify-bug` read this at pre-flight.

A lesson that a *rule file already owns* goes in that rule file instead, where it fires for every skill that
loads it — a capture mechanic in `.kiro/steering/capture-*.md`, a driver quirk in the driver rule.

<!-- Add lessons below -->
- **`download-jira-attachments.sh` writes to `.tmp/jira-tickets/{KEY}/attachments/`, not the
  `tasks/{KEY}/attachments/` that `project-config.md` § Folder Structure documents.** Copy what you need
  into `tasks/{KEY}/attachments/` after running it. `.tmp/` is now gitignored. (AO-925, 2026-08-26)
