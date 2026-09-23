---
name: meta-weekly-review
description: Weekly Meta (Facebook/Instagram) ads diagnosis for an existing client account, based on the Meta Ads Playbook. Compares last 7 days with the previous 7 at ad level, walks the funnel (CTR → link CTR → CPM → page views → add to cart → checkout → purchase) to find the account's FIRST leak and each ad's first leak, flags failing and fatiguing ads with where and what to check, builds keep / cut / fix / scale lists, checks structure (ads live vs budget, prospecting vs retargeting split, tests mixed into main campaigns) and ends with a next-week plan. Use whenever the user says "weekly review", "weekly check", "audit the Meta account", "what's wrong with the ads", "why did ROAS drop", "which ads should I cut", "troubleshoot the funnel", or "plan next week for [client]".
---

# Meta weekly review

The weekly job is diagnosis and decisions: which ads earn their keep, where the funnel leaks, and what to change next week. It follows the playbook's rule: **find the first failing stage and fix only that** — changing five things at once teaches nothing.

## Steps

1. **Client numbers:** target CPA, break-even CPA, AOV, daily budget, goal (profit-first / growth-first). See `references/getting-data.md`.
2. **Data:** ad level for `last_7d` → `this_week.csv`; the 7 days before → `prev_week.csv`. Include campaign and ad set names (needed for structure checks).
3. **Run:**
   ```bash
   python scripts/meta_flags.py this_week.csv --mode weekly --target-cpa <T> --breakeven-cpa <B> --aov <A> --prev prev_week.csv --json flags.json
   ```
4. **Add the checks the script can't do** (use `references/benchmarks.md`):
   - **Structure:** count active ads vs daily budget (~$30 → 1–3; $100–700 → 2–5 winners). Share of spend on the top 3 ads. Are test ads sitting inside main campaigns? Prospecting vs retargeting spend (target 80–90 / 10–20). Middle vs bottom retargeting separated with exclusions?
   - **Economics:** account ROAS vs break-even and scale zone (≈1.5× break-even). Would an AOV lever (bundle, quantity break, shipping threshold) help more than ad changes?
   - **Fatigue:** winners with CTR down ≥25%, CPM up ≥30% or frequency > 3 vs last week.
   - **Context:** new ads under 1,000 impressions or < 3 days old are "too early", not failures. Middle-funnel retargeting is judged on clicks.
5. **Decide** one main focus for next week = the account's first leak (or scaling, if everything passes). Map it to a playbook action:
   - Attention/Interest → creative test with new hooks, or copy test on the #1 ad
   - Page load/Buying intent → landing page test, product page fixes
   - Cart/Checkout → site fixes (shipping visibility, cart clutter, payment), bottom retargeting
   - Result only (funnel fine, CPA high) → AOV lever or cheaper-attention creatives
   - All healthy + above scale zone → +$10–20/day, new interest ad set, or side creative test
6. **Write the report** (markdown in chat; if the user wants a file, make it a PDF/HTML with the same sections):

```
# Weekly review — <Client> — <date range>
**Verdict:** <one sentence: state of the account + the one focus for next week>

## Scorecard (this week vs last)
| Metric | This week | Last week | Benchmark | Status |   ← spend, purchases, CPA, ROAS, CTR, link CTR, CPM, ATC rate, cart→checkout, checkout→purchase

## Where the funnel leaks
First leak: <stage> — <evidence with numbers> — <what to check>

## Ads
### 🔴 Cut or fix now
| Ad | Campaign | Spend | CPA | Fails at | What to check / do |
### 🟡 Watch / fatigue
### 🟢 Keep (winners)  → note which could take more budget
### ⚪ Too early

## Structure check
- Ads live vs budget · top-3 spend share · prospecting/retargeting split · tests isolated? — ✅/⚠️ each

## Next week (max 5 actions, in order)
1. …
```

Keep every flagged ad to one line: the stage where it fails and the concrete thing to check. Quote real numbers.

## Don't
- Don't recommend more than one new test per stage per week, or several variables in one test.
- Don't call an ad a winner or loser without enough exposure; don't pause on ROAS alone.
- Don't invent benchmarks; the ones in `references/benchmarks.md` are the standard (two are labelled assumptions — say so if you rely on them).
