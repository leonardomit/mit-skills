#!/usr/bin/env python3
"""Dump full messages for one session (rebuild incomplete cron from tool outputs)."""
import sqlite3
import sys
from pathlib import Path

DB = Path.home() / ".hermes" / "state.db"


def main() -> None:
    if len(sys.argv) < 3:
        print("usage: dump_session_full.py <session_id> <out_path>")
        sys.exit(2)
    sid = sys.argv[1]
    out_path = Path(sys.argv[2])
    db = sqlite3.connect(str(DB))
    db.row_factory = sqlite3.Row
    rows = db.execute(
        """
SELECT id, role, content, tool_name, tool_calls, finish_reason
FROM messages WHERE session_id=? ORDER BY id
""",
        (sid,),
    ).fetchall()
    parts: list[str] = []
    for r in rows:
        parts.append(
            f"===== id={r['id']} role={r['role']} tool={r['tool_name']} fr={r['finish_reason']} ====="
        )
        if r["tool_calls"]:
            parts.append("TOOL_CALLS:")
            parts.append(r["tool_calls"][:8000])
        if r["content"]:
            parts.append(r["content"])
        parts.append("")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("\n".join(parts), encoding="utf-8")
    print(f"msgs={len(rows)} bytes={out_path.stat().st_size}")


if __name__ == "__main__":
    main()
