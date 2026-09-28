#!/usr/bin/env python3
"""Extract last substantial assistant finals from sessions in the last 24h."""
import sqlite3
from datetime import datetime
from pathlib import Path

DB = Path.home() / ".hermes" / "state.db"
OUT = Path.home() / ".hermes" / "cache" / "journal-day-extract.txt"


def main() -> None:
    db = sqlite3.connect(str(DB))
    db.row_factory = sqlite3.Row
    sessions = db.execute(
        """
SELECT id, source, started_at, title
FROM sessions
WHERE started_at > (strftime('%s','now') - 86400)
ORDER BY started_at ASC
"""
    ).fetchall()
    parts: list[str] = []
    for s in sessions:
        sid = s["id"]
        started = datetime.fromtimestamp(s["started_at"]).strftime("%Y-%m-%d %H:%M")
        parts.append("=" * 80)
        parts.append(f"SESSION {sid} | {s['source']} | {started} | {s['title'] or ''}")
        parts.append("=" * 80)
        rows = db.execute(
            """
SELECT id, role, content, tool_calls
FROM messages WHERE session_id = ? ORDER BY id ASC
""",
            (sid,),
        ).fetchall()
        finals: list[str] = []
        for r in rows:
            content = (r["content"] or "").strip()
            tc = r["tool_calls"]
            has_tools = bool(tc and tc not in ("null", "[]", ""))
            if r["role"] == "assistant" and content and not has_tools:
                finals.append(content)
            elif r["role"] == "assistant" and content and len(content) > 200:
                finals.append(content)
        if not finals:
            for r in rows:
                if r["role"] == "assistant" and (r["content"] or "").strip():
                    finals.append((r["content"] or "").strip())
        if finals:
            text = finals[-1]
            if len(text) > 6000:
                parts.append(text[:6000])
                parts.append(f"\n...[truncated total={len(text)}]")
            else:
                parts.append(text)
        else:
            parts.append("(no assistant text)")
            parts.append(f"msg count={len(rows)}")
        parts.append("")
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("\n".join(parts), encoding="utf-8")
    print(f"wrote {OUT} sessions={len(sessions)} bytes={OUT.stat().st_size}")


if __name__ == "__main__":
    main()
