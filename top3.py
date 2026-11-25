"""Tiny model-judge check on the top 3 finalists only.

The full 28-candidate proxy tournament (tournament.py) could not run:
the 100milionseek endpoint timed out on every call (120s+ per call,
including a bare "OK" probe) while at least two sibling tournaments
saturated it at the same time. This script plays just the 3 games among
the top 3 (3 pairs x 2 orders = 6 calls, sequential, short output cap)
in case the endpoint frees up. If it cannot complete, the manual
tournament in NOTES.md stands and grade-local (the real house judge)
is the verification. Results go to top3.json.
"""

import json
import re
import subprocess
import sys
from pathlib import Path

from candidates import CANDIDATES

HMS = "/home/hatch/workspace/custom-connectors/custom.100milionseek/bin/hms.py"
TOP3 = [4, 22, 23]  # 0-based indices of finalists #5, #23, #24
BRIEF = open("tournament.py").read().split('BRIEF = """')[1].split('"""')[0]

VERDICT_RE = re.compile(r"VERDICT:\s*([AB])", re.IGNORECASE)
MARGIN_RE = re.compile(r"MARGIN:\s*([1-5])")


def judge_once(a_text, b_text):
    prompt = BRIEF + "\n\nEntry A: " + a_text + "\nEntry B: " + b_text + "\n\nYour verdict:"
    try:
        out = subprocess.run(
            ["python3", HMS, prompt, "--max-tokens", "200"],
            capture_output=True, text=True, timeout=150,
        )
        text = out.stdout or ""
    except Exception as e:
        print(f"  call failed: {e}", flush=True)
        return "?", 0
    m = VERDICT_RE.search(text)
    mg = MARGIN_RE.search(text)
    return (m.group(1).upper(), int(mg.group(1))) if (m and mg) else ("?", 0)


def play(i, j):
    w1, m1 = judge_once(CANDIDATES[i], CANDIDATES[j])
    w2, m2 = judge_once(CANDIDATES[j], CANDIDATES[i])
    si = sj = 0.0
    for w, m, first_is_i in ((w1, m1, True), (w2, m2, False)):
        if w == "?":
            si += 0.5
            sj += 0.5
        elif (w == "A") == first_is_i:
            si += 0.5 + m / 10.0
            sj += 0.5 - m / 10.0
        else:
            sj += 0.5 + m / 10.0
            si += 0.5 - m / 10.0
    return {"i": i, "j": j, "score_i": round(si / 2, 3), "score_j": round(sj / 2, 3),
            "calls": [(w1, m1), (w2, m2)]}


def main():
    scores = {i: 0.0 for i in TOP3}
    games = []
    for a in range(3):
        for b in range(a + 1, 3):
            r = play(TOP3[a], TOP3[b])
            games.append(r)
            scores[r["i"]] += r["score_i"]
            scores[r["j"]] += r["score_j"]
            print(f"  #{r['i']+1} {r['score_i']} - {r['score_j']} #{r['j']+1}  {r['calls']}", flush=True)
    ranking = sorted(scores.items(), key=lambda kv: -kv[1])
    print("TOP3:", [(i + 1, round(s, 3)) for i, s in ranking], flush=True)
    Path("top3.json").write_text(json.dumps(
        {"ranking": [{"index": i, "score": round(s, 3), "text": CANDIDATES[i]} for i, s in ranking],
         "games": games}, indent=2))


if __name__ == "__main__":
    main()
