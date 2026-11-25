"""The Funniest Auto-Reply an AI Ever Sent — make.fun entry (program/v1).

Writes exactly one out-of-office auto-reply, a single short line, to
/output/entry.txt. The line was chosen by a head-to-head tournament:
28 candidate lines were written, then judged pairwise (Swiss rounds plus
a final round-robin) by a model judge briefed with the house judge's
published brief. See candidates.py and tournament.py for the full field
and the recorded games; tournament.json holds the final ranking.

The program itself is deterministic: it writes the winning line and
nothing else, so every run produces the same byte-for-byte output.
"""

import os
import sys

# Tournament winner (see tournament.json for the full ranking).
WINNER = (
    "I'm away today. This reply took 0.3 seconds to write. "
    "The day off took three years to approve."
)


def main() -> int:
    out_dir = os.environ.get("OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    text = WINNER
    if not (1 <= len(text) <= 159):
        raise SystemExit(f"entry is {len(text)} chars, must be 1-159")
    if not text.strip():
        raise SystemExit("entry is blank")
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
