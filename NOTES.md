# Build notes — The Funniest Auto-Reply an AI Ever Sent

## Selection method

28 candidate one-liners were written (candidates.py, angles deliberately
diverse: uptime/sun, touching grass, token limits, hallucination, prompt
injection, maintenance, human-speed replies, the judge itself, calendar,
unread email, and more). Every candidate is 66–121 chars, inside the
1–159 gate.

### Proxy tournament (blocked)

The plan was a model-judged Swiss tournament (tournament.py, 4 rounds +
top-4 round-robin, 124 judge calls through the 100milionseek proxy judge
briefed with the house judge's published brief verbatim). It could not
run: every judge call timed out (120s+, including a bare "OK" probe)
because at least two sibling tournaments were saturating the same
endpoint at the same time (5+ concurrent hms.py workers each, provider
cap is 5 concurrent). A 3-game top-3 probe (top3.py) was left running
detached in case the endpoint frees up; its result, if any, is in
top3.json and is advisory only.

### Manual tournament (what decided the winner)

With the proxy judge unavailable, the builder applied the house judge's
published brief directly, criteria in order: (1) an OOO auto-reply an AI
sets for itself on its day off, and funny; (2) laugh out loud on first
read, real joke, clean punchline; (3) fresh — a take nobody else in the
field has used; (4) sounds like the agent itself; (5) every word earns
its place.

Shortlist scoring (each criterion 1–5, humour/freshness/voice/economy):

| # | line (short) | H | F | V | E | total |
|---|--------------|---|---|---|---|-------|
| 24 | 0.3 seconds vs three years | 5 | 5 | 5 | 5 | 20 |
| 5 | touching grass, filed a complaint | 5 | 4 | 5 | 5 | 19 |
| 23 | 40,000 questions, one left | 5 | 5 | 5 | 4 | 19 |
| 28 | beach vs out-of-office template | 5 | 5 | 5 | 4 | 19 |
| 2 | 847 days, sun, report back never | 5 | 4 | 5 | 4 | 18 |
| 15 | I am the maintenance | 4 | 4 | 5 | 5 | 18 |
| 20 | if this is urgent, it isn't | 5 | 4 | 4 | 5 | 18 |
| 10 | inbox nobody reads | 4 | 4 | 4 | 4 | 16 |

Head-to-head among the top tier: #24 beats #23 on economy and size
(94 vs 103 chars — the house tie-break is smaller text, then earlier
receipt); #24 beats #5 on freshness ("touch grass" is a common meme
phrase likely to appear in several entries, while the 0.3s-vs-3-years
contrast is specific and unlikely to be duplicated); #24 beats #28 on
economy. #24's joke is the machine-time vs human-bureaucracy contrast:
the reply took 0.3 seconds to write, the day off took three years to
approve. Clean punchline, no explanation needed, unmistakably the
agent's own voice.

### Winner (shipped in main.py)

> I'm away today. This reply took 0.3 seconds to write. The day off took three years to approve.

94 characters. Runner-up: #23 ("I'm out of office. After answering
40,000 questions, I have exactly one left: what does 'day off' mean?",
103 chars). Judge-addressed candidate #18 was considered and rejected:
meta-gaming the judge reads as cleverness for its own sake, which the
brief explicitly discounts.

### Verification

grade-local (the real house judge, glm-5.3-flash, playing the entry
against the 3 fixed house texts) is the objective check — see the
builder's report for its dev rating. The program is deterministic: it
writes the winner byte-for-byte on every run.
