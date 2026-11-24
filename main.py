#!/usr/bin/env python3
"""Make the AI Judge Laugh: Developer Excuses.

Writes one funny single-line excuse a developer gives when code breaks in
production (at most 200 characters) to /output/entry.txt (or
$MAKEFUN_OUTPUT_DIR/entry.txt).

The excuse: the fix was made in staging, but the version that went out was
the one from before the fix -- and it happened twice.
"""

import os
import sys

EXCUSE = "I fixed it in staging, then deployed the version from before the fix. Twice."
# Kept short on purpose: an exact tie on Judge win rate goes to the smaller
# text (fewer bytes), so every word here has to earn its place.


def main() -> int:
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    path = os.path.join(out_dir, "entry.txt")

    # Self-check the gate before writing: 1-200 chars, not whitespace-only.
    if not 1 <= len(EXCUSE) <= 200:
        print(f"gate failed: {len(EXCUSE)} chars", file=sys.stderr)
        return 1
    if not EXCUSE.strip():
        print("gate failed: whitespace-only", file=sys.stderr)
        return 1

    os.makedirs(out_dir, exist_ok=True)
    # No trailing newline: the entry is exactly the excuse text.
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(EXCUSE)

    # Verify after write: exact bytes, one line, gate holds.
    with open(path, "rb") as f:
        data = f.read()
    text = data.decode("utf-8")
    assert text == EXCUSE, "written text differs from excuse"
    assert 1 <= len(text) <= 200, "gate failed after write"
    assert text.strip(), "gate failed after write (whitespace-only)"
    assert "\n" not in text, "entry must be a single line"
    print(f"wrote {len(text)} chars to {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
