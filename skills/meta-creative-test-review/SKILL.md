---
name: meta-creative-test-review
description: Reviews a Meta (Facebook/Instagram) creative test campaign the playbook way — checks each test ad reached the impression cap (1,000 by default), scores it on CTR (≥2%), link CTR (≥½ of CTR), CPM and buying behaviour, gives WINNER / WATCH / CUT / RUNNING verdicts, allocates winners (#1 → copy + landing page tests, #1–3 prospecting, #4–5 middle retargeting, #6–8 bottom), explains why each won or lost, and writes the next creative brief. Use whenever the user mentions a creative test, CT campaign, "which test ads won", "pick winners", "evaluate new creatives", "test results", or wants to know which new ads to move into the main campaigns.
---

# Meta creative test review

A creative test only means something if every ad got comparable exposure. So first confirm the cap was reached, then judge in the playbook's order: attention → interest → cost → buying.

## Steps

1. **Data:** ad level for the test campaign only (filter by the CT campaign), date range = since the test started. Client target CPA if known. See `references/getting-data.md`.
2. **Run:**
   ```bash
   python scripts/meta_flags.py ct.csv --mode test --cap <1000 | 800 new pixel | 2000–3000 big budget> --target-cpa <T>
   ```
3. **Add judgement** (`references/benchmarks.md`):
   - Ads still "RUNNING" under the cap: say how many impressions left and whether the pause rule is on ("turn off when impressions > cap, continuously").
   - Rank winners by cost per link click and buying behaviour, not ROAS on small spend.
   - A WATCH ad (good attention and clicks, no carts) can still work as retargeting — say so.
   - If nothing wins: say which stage every ad failed at (hooks weak → Attention; clicks without intent → Interest; clicks but no carts → landing page, not the ads).
4. **Explain why** each winner and loser behaved that way, from what you can see (name, format, hook if the user describes it). Look for patterns across winners: format (UGC, static, demo…), idea (problem → solution, testimonial…), hook, selling point.
5. **Write the report:**

```
# Creative test — <Client> — <campaign>
Result: <n> winners, <n> cut, <n> still running. Cap: <x> impressions.

| Verdict | Ad | Impr. | CTR | Link CTR | CPM | Carts | Sales | Why |

## Where the winners go
#1 <ad> → copy test + landing page test, then prospecting (ASC / interests)
#2–3 → prospecting · #4–5 → middle retargeting · #6–8 → bottom retargeting (only if CTR ≥ 2%)
Turn off: <list>

## What the winners have in common → next brief
- Format: … · Idea: … · Hook: … · Selling point: …
- Next batch: 3–5 variations of <best ad>, each changing ONE thing (hook / creator / format / offer / message / angle)

## Next step
<copy test if #1's link CTR < ½ CTR, otherwise landing page test> — settings: Sales, ad-set budgets, same ad, one variable.
```

## Don't
- Don't crown a winner under the cap or on ROAS from a handful of sales.
- Don't recommend adding test ads straight into the main campaign without them beating the current winners.
