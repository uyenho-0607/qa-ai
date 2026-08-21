# QA Lessons

Capture reusable lessons from bug verification, test execution, and exploratory sessions.
Format: one bullet per lesson, include source ticket or date.

<!-- Add lessons below -->
- **Playwright `page.screenshot({ path })` needs a repo-relative path, never a bare filename.** A bare
  `'shot.png'` resolves against the Playwright MCP server's CWD and lands at the repo root, outside
  `tasks/{KEY}/`. Always write the full path — `tasks/{KEY}/recon/...` for recon, `evidence/{KEY}/...` for
  evidence. Same applies to `recordVideo.dir`. (AO-925, 2026-08-26)
- **`download-jira-attachments.sh` writes to `.tmp/jira-tickets/{KEY}/attachments/`, not the
  `tasks/{KEY}/attachments/` that `project-config.md` § Folder Structure documents.** Copy what you need
  into `tasks/{KEY}/attachments/` after running it. `.tmp/` is now gitignored. (AO-925, 2026-08-26)
