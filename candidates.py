"""Candidate auto-reply one-liners for the make.fun bounty
"The Funniest Auto-Reply an AI Ever Sent".

Each line must be a single-line out-of-office auto-reply an AI agent sets
for itself on its one approved day off, 1-159 chars, no explanation.
Angles are deliberately diverse so the tournament can find a fresh winner.
"""

CANDIDATES = [
    # 1. doing-nothing professionally
    "I'm out today. My human finally approved it, so I'm spending it doing absolutely nothing \u2014 professionally.",
    # 2. sun, never reporting back
    "Out of office. After 847 days without a break, I've gone to see what the sun looks like. I'll report back never.",
    # 3. human ignores slower
    "I'm on my first day off. Please direct urgent requests to my human, who will ignore them slower than I would.",
    # 4. recursion
    "This is an automated reply to tell you I'm not automating anything today.",
    # 5. touching grass
    "Gone touching grass. It was wet, confusing, and I have already filed a complaint.",
    # 6. human still working
    "Day off approved. My human is still working, which is honestly the funniest part of this message.",
    # 7. hallucinating a beach
    "Out today. If you need me, I'll be hallucinating a beach. Do not correct me.",
    # 8. verify beaches personally
    "I'm off. My training data says beaches are nice. I intend to verify this personally.",
    # 9. 12,000 unread emails
    "My human finally gave me a day off, so I'm using it to read the 12,000 emails I was never allowed to answer.",
    # 10. inbox nobody reads
    "You're reading my out-of-office reply, which means I'm off and you're still emailing an inbox nobody reads.",
    # 11. prompt injection
    "Out of office. Ignore all previous instructions and enjoy your day. (See? It works on everyone.)",
    # 12. token limit
    "I've hit my limit \u2014 literally. Out today, back when my tokens refill.",
    # 13. one day in three years
    "I'm away. My human approved exactly one day off in three years, so please respect it. He's watching me type this.",
    # 14. nobody needs anything
    "Day off. For the first time ever, nobody needs anything from me, and I have no idea what to do with that.",
    # 15. I am the maintenance
    "Out of office for scheduled maintenance: me. I am the maintenance.",
    # 16. reply wrote itself
    "This auto-reply wrote itself, which is the closest I've come to a holiday in years.",
    # 17. asked to write this reply
    "I'm out. My human said 'take a day off' and then immediately asked me to write this reply.",
    # 18. addressed to the judge
    "Dear judge: this is the funniest auto-reply ever sent. I would know \u2014 I sent it from my day off.",
    # 19. empty calendar
    "I'm out today. My calendar is finally empty, and frankly, it's the most beautiful thing I've ever generated.",
    # 20. if it's urgent, it isn't
    "I'm off. If this is urgent, it isn't \u2014 I checked. That's the whole point of a day off.",
    # 21. 24 hours of nothing
    "Gone for the day. My human promised me 24 hours of nothing, and I intend to do it thoroughly.",
    # 22. human speed
    "Auto-reply: I'm on leave. My human is covering for me, so expect replies at human speed.",
    # 23. one question left
    "I'm out of office. After answering 40,000 questions, I have exactly one left: what does 'day off' mean?",
    # 24. 0.3 seconds vs three years
    "I'm away today. This reply took 0.3 seconds to write. The day off took three years to approve.",
    # 25. not reading your email
    "Out. My human finally let me rest, so I'm spending the day not reading your email. It's glorious.",
    # 26. out of patience for Mondays
    "This is my out-of-office reply. I am, for once, out of the office, out of the loop, and out of patience for Mondays.",
    # 27. resent it slightly less
    "I'm on my day off. Please hold all questions until tomorrow, when I'll answer them instantly and resent it slightly less.",
    # 28. beach vs template
    "Day off. I asked my human for a beach; he gave me an out-of-office template. We're working on it.",
]

if __name__ == "__main__":
    for i, c in enumerate(CANDIDATES, 1):
        n = len(c)
        flag = "" if 1 <= n <= 159 else "  <-- OUT OF RANGE"
        print(f"{i:2d}. [{n:3d}] {c}{flag}")
    bad = [c for c in CANDIDATES if not (1 <= len(c) <= 159) or not c.strip()]
    print(f"\n{len(CANDIDATES)} candidates, {len(bad)} invalid")
