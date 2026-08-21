#!/bin/bash
# Downloads all attachments from a Jira ticket to a local folder.
# Automatically extracts keyframes from video attachments using ffmpeg.
#
# Prerequisites:
#   export JIRA_EMAIL="your-email@aquariux.com"
#   export JIRA_API_TOKEN="your-atlassian-api-token"
#   brew install ffmpeg  (for video frame extraction)
#
# Usage:
#   ./download-jira-attachments.sh OMS-600
#
# Output:
#   .tmp/jira-tickets/OMS-600/attachments/image-xxx.png
#   .tmp/jira-tickets/OMS-600/attachments/video-xxx.mp4
#   .tmp/jira-tickets/OMS-600/attachments/video-xxx-frames/frame-001.png ...

set -euo pipefail

ISSUE_KEY="${1:?Usage: $0 <ISSUE-KEY>}"
SITE="aquariux.atlassian.net"
if [[ -z "${JIRA_EMAIL:-}" || -z "${JIRA_API_TOKEN:-}" ]]; then
  echo "Error: JIRA_EMAIL and JIRA_API_TOKEN must be set in your environment (add to ~/.zshrc)." >&2
  exit 1
fi

WORKSPACE_ROOT="${WORKSPACE_ROOT:-$PWD}"
OUT_DIR="${WORKSPACE_ROOT}/.tmp/jira-tickets/${ISSUE_KEY}/attachments"

AUTH=$(printf '%s:%s' "$JIRA_EMAIL" "$JIRA_API_TOKEN" | base64)

# Fetch attachment metadata
ATTACHMENTS=$(curl -s \
  -H "Authorization: Basic ${AUTH}" \
  -H "Accept: application/json" \
  "https://${SITE}/rest/api/3/issue/${ISSUE_KEY}?fields=attachment" \
  | python3 -c "
import sys, json
data = json.load(sys.stdin)
for a in data.get('fields', {}).get('attachment', []):
    print(a['filename'] + '|' + a['content'] + '|' + a.get('mimeType', ''))
")

if [[ -z "$ATTACHMENTS" ]]; then
  echo "No attachments found for ${ISSUE_KEY}."
  exit 0
fi

mkdir -p "$OUT_DIR"
echo "Downloading attachments for ${ISSUE_KEY} → ${OUT_DIR}/"
echo ""

VIDEO_FILES=()

while IFS='|' read -r filename url mimetype; do
  # Sanitize filename to prevent path traversal
  safe_filename="$(basename -- "$filename")"

  echo "  ↓ ${safe_filename} (${mimetype})"
  curl -s -L \
    -H "Authorization: Basic ${AUTH}" \
    -o "${OUT_DIR}/${safe_filename}" \
    "$url"

  # Track video files for frame extraction
  if [[ "$mimetype" == video/* ]]; then
    VIDEO_FILES+=("${safe_filename}")
  fi
done <<< "$ATTACHMENTS"

# Extract frames from video attachments
if [[ ${#VIDEO_FILES[@]} -gt 0 ]]; then
  if command -v ffmpeg &>/dev/null; then
    echo ""
    echo "Extracting frames from video attachments..."
    for video in "${VIDEO_FILES[@]}"; do
      FRAMES_DIR="${OUT_DIR}/${video%.*}-frames"
      mkdir -p "$FRAMES_DIR"
      echo "  🎬 ${video} → ${FRAMES_DIR}/"
      ffmpeg -i "${OUT_DIR}/${video}" -vf "fps=1" -q:v 2 "${FRAMES_DIR}/frame-%03d.png" -loglevel error
      FRAME_COUNT=$(ls -1 "$FRAMES_DIR"/*.png 2>/dev/null | wc -l | tr -d ' ')
      echo "     Extracted ${FRAME_COUNT} frames"
    done
  else
    echo ""
    echo "⚠️  ffmpeg not found — skipping video frame extraction."
    echo "   Install with: brew install ffmpeg"
  fi
fi

echo ""
echo "Done. Files in: ${OUT_DIR}/"
ls -lh "$OUT_DIR/"
