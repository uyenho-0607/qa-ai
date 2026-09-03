#!/usr/bin/env python3
"""
Reads Jira issue JSON from stdin (fields: attachment, comment).
Prints one line per attachment: filename|source|author|date|excerpt
Source is either "comment:<id>" or "ticket-description".
"""
import re
import sys
import json
from datetime import datetime


def parse_ts(s):
    if not s:
        return None
    s = re.sub(r'([+-]\d{2})(\d{2})$', r'\1:\2', s)
    try:
        return datetime.fromisoformat(s)
    except Exception:
        return None


data = json.load(sys.stdin)
attachments = data.get('fields', {}).get('attachment', [])
comments = data.get('fields', {}).get('comment', {}).get('comments', [])

for att in attachments:
    att_ts = parse_ts(att.get('created', ''))
    best_comment = None
    best_delta = None

    for c in comments:
        c_ts = parse_ts(c.get('created', ''))
        if c_ts is None or att_ts is None:
            continue
        delta = abs((att_ts - c_ts).total_seconds())
        if delta <= 60 and (best_delta is None or delta < best_delta):
            best_comment = c
            best_delta = delta

    if best_comment:
        body_raw = best_comment.get('body', '')
        # body may be a plain string or an ADF dict — normalise to str
        if isinstance(body_raw, dict):
            # Extract text from ADF: walk content nodes for 'text' leaves
            def extract_text(node):
                if isinstance(node, dict):
                    if node.get('type') == 'text':
                        return node.get('text', '')
                    return ''.join(extract_text(c) for c in node.get('content', []))
                if isinstance(node, list):
                    return ''.join(extract_text(c) for c in node)
                return ''
            body_raw = extract_text(body_raw)
        body_excerpt = str(body_raw)[:120].replace('\n', ' ')
        print(
            att['filename'] + '|'
            + 'source:comment:' + best_comment['id'] + '|'
            + 'by:' + best_comment['author']['displayName'] + '|'
            + 'date:' + best_comment['created'][:10] + '|'
            + 'excerpt:' + body_excerpt
        )
    else:
        print(att['filename'] + '|source:ticket-description|||')
