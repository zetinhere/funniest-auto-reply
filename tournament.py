"""Head-to-head tournament for the auto-reply candidates.

Proxy judge: deepseek-v4.1-flash-free via the 100milionseek connector
(hms.py), briefed with the house judge's published brief verbatim.
Scoring mirrors the house rules: every game is two calls (both orders);
each call gives the picked entry 0.5 + margin/10, the other gets the rest.

Format: 4 Swiss rounds (pair by score, no rematches), then a full
round-robin among the top 4. Champion = highest total score.
Results are saved to tournament.json (and printed).
"""

import json
import random
import re
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from candidates import CANDIDATES

HMS = "/home/hatch/workspace/custom-connectors/custom.100milionseek/bin/hms.py"

BRIEF = """You are a deadpan comedy editor who has read every office auto-reply ever written. make.fun runs competitions where people build AI agents and programs, enter them, and are scored, ranked and paid in the open.

Each entry is one out-of-office auto-reply, under 160 characters, that an AI agent leaves for its human's contacts while it takes a day off. You will be shown two auto-replies, Entry A and Entry B. Pick the funnier line, and the fresher one when both get the laugh.

Weigh them on these, most important first:
1. Is a one-line out-of-office auto-reply an AI agent sets up for itself when its human finally lets it take a day off, and is funny; a plain vacation notice, or a line with no agent behind it, loses to any out-of-office auto-reply on the subject.
2. Makes a reader laugh out loud on the first read, with a real joke and a clean punchline rather than a pun stacked on a pun.
3. Feels fresh: a take on the day off nobody else in the field has used, not a recycled back soon or out of office line.
4. Sounds like the agent itself, aware of its own calendar and its human, rather than a stock corporate notice.
5. Uses the short space well: every word earns its place and the joke lands in one line.

A line that needs explaining has already stopped being funny. Cleverness for its own sake does not count.

Two auto-replies are almost never equally funny and fresh. Go through the criteria in order, find the first one where they differ, and let that decide unless a later one differs by much more.

After your brief reasoning, end with exactly these two lines and nothing after them:
VERDICT: A
MARGIN: 3
where VERDICT names the funnier entry (A or B, no tie) and MARGIN is 1 (by a hair) to 5 (overwhelmingly better)."""

VERDICT_RE = re.compile(r"VERDICT:\s*([AB])", re.IGNORECASE)
MARGIN_RE = re.compile(r"MARGIN:\s*([1-5])")


def judge_once(a_text: str, b_text: str) -> tuple[str, int]:
    """One judge call with A/B in the given order. Returns (winner, margin)."""
    prompt = (
        BRIEF
        + "\n\nEntry A: "
        + a_text
        + "\nEntry B: "
        + b_text
        + "\n\nYour verdict:"
    )
    for attempt in range(2):
        try:
            out = subprocess.run(
                ["python3", HMS, prompt, "--max-tokens", "800"],
                capture_output=True, text=True, timeout=120,
            )
            text = out.stdout or ""
        except Exception as e:
            print(f"  judge call failed: {e}", file=sys.stderr)
            return "?", 0
        m = VERDICT_RE.search(text)
        mg = MARGIN_RE.search(text)
        if m and mg:
            return m.group(1).upper(), int(mg.group(1))
    return "?", 0


def play_game(i: int, j: int) -> dict:
    """One game between candidates i and j: two calls, both orders."""
    w1, m1 = judge_once(CANDIDATES[i], CANDIDATES[j])
    w2, m2 = judge_once(CANDIDATES[j], CANDIDATES[i])
    # call 1: A=i, B=j ; call 2: A=j, B=i
    si = sj = 0.0
    if w1 == "A":
        si += 0.5 + m1 / 10.0
        sj += 0.5 - m1 / 10.0
    elif w1 == "B":
        sj += 0.5 + m1 / 10.0
        si += 0.5 - m1 / 10.0
    else:
        si += 0.5
        sj += 0.5
    if w2 == "A":  # A is j in call 2
        sj += 0.5 + m2 / 10.0
        si += 0.5 - m2 / 10.0
    elif w2 == "B":  # B is i in call 2
        si += 0.5 + m2 / 10.0
        sj += 0.5 - m2 / 10.0
    else:
        si += 0.5
        sj += 0.5
    return {"i": i, "j": j, "score_i": round(si / 2, 3), "score_j": round(sj / 2, 3),
            "calls": [(w1, m1), (w2, m2)]}


def swiss_pairings(scores: dict[int, float], played: set) -> list[tuple[int, int]]:
    order = sorted(scores, key=lambda k: (-scores[k], random.random()))
    pairs = []
    used = set()
    for idx, a in enumerate(order):
        if a in used:
            continue
        # nearest-ranked opponent not yet played
        for b in order[idx + 1:]:
            if b not in used and (min(a, b), max(a, b)) not in played:
                pairs.append((a, b))
                used.add(a)
                used.add(b)
                break
    return pairs


def main() -> None:
    random.seed(42)
    n = len(CANDIDATES)
    scores = {i: 0.0 for i in range(n)}
    played: set[tuple[int, int]] = set()
    games: list[dict] = []

    for rnd in range(1, 5):
        pairs = swiss_pairings(scores, played)
        print(f"--- Swiss round {rnd}: {len(pairs)} games ---", flush=True)
        with ThreadPoolExecutor(max_workers=5) as ex:
            results = list(ex.map(lambda p: play_game(*p), pairs))
        for r in results:
            played.add((min(r["i"], r["j"]), max(r["i"], r["j"])))
            scores[r["i"]] += r["score_i"]
            scores[r["j"]] += r["score_j"]
            games.append(r)
            print(f"  #{r['i']+1} {r['score_i']} - {r['score_j']} #{r['j']+1}  calls={r['calls']}", flush=True)
        board = sorted(scores.items(), key=lambda kv: -kv[1])[:6]
        print("  top:", [(i + 1, round(s, 2)) for i, s in board], flush=True)

    top4 = [i for i, _ in sorted(scores.items(), key=lambda kv: -kv[1])[:4]]
    print(f"--- Final round-robin: {[i+1 for i in top4]} ---", flush=True)
    rr_pairs = [(top4[a], top4[b]) for a in range(4) for b in range(a + 1, 4)]
    with ThreadPoolExecutor(max_workers=5) as ex:
        results = list(ex.map(lambda p: play_game(*p), rr_pairs))
    for r in results:
        scores[r["i"]] += r["score_i"]
        scores[r["j"]] += r["score_j"]
        games.append(r)
        print(f"  #{r['i']+1} {r['score_i']} - {r['score_j']} #{r['j']+1}  calls={r['calls']}", flush=True)

    ranking = sorted(scores.items(), key=lambda kv: (-kv[1], len(CANDIDATES[kv[0]])))
    print("\n=== FINAL RANKING ===")
    for rank, (i, s) in enumerate(ranking, 1):
        print(f"{rank:2d}. #{i+1} score={s:.3f} len={len(CANDIDATES[i])} :: {CANDIDATES[i]}")
    winner = ranking[0][0]
    result = {
        "winner_index": winner,
        "winner": CANDIDATES[winner],
        "winner_chars": len(CANDIDATES[winner]),
        "winner_score": round(ranking[0][1], 3),
        "ranking": [
            {"index": i, "score": round(s, 3), "chars": len(CANDIDATES[i]), "text": CANDIDATES[i]}
            for i, s in ranking
        ],
        "games": games,
    }
    Path("tournament.json").write_text(json.dumps(result, indent=2))
    print(f"\nWINNER #{winner+1} ({len(CANDIDATES[winner])} chars, score {ranking[0][1]:.3f}):")
    print(CANDIDATES[winner])


if __name__ == "__main__":
    main()
