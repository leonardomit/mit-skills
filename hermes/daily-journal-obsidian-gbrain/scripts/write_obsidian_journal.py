#!/usr/bin/env python3
"""Write journal markdown to Obsidian vault via temp + os.replace (avoid EDEADLK)."""
import os
import sys
from pathlib import Path


def main() -> None:
    if len(sys.argv) < 3:
        print("usage: write_obsidian_journal.py <src.md> <target.md>")
        sys.exit(2)
    src = Path(sys.argv[1])
    target = Path(sys.argv[2])
    content = src.read_text(encoding="utf-8")
    target.parent.mkdir(parents=True, exist_ok=True)
    tmp = target.with_suffix(".md.tmp")
    with open(tmp, "w", encoding="utf-8") as f:
        f.write(content)
        f.flush()
        os.fsync(f.fileno())
    os.replace(tmp, target)
    st = target.stat()
    print(f"OK path={target} bytes={st.st_size}")
    with open(target, "rb") as f:
        head = f.read(80)
    print("head:", head[:80])


if __name__ == "__main__":
    main()
