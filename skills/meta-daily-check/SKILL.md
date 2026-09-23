---
name: meta-daily-check
description: Daily Meta (Facebook/Instagram) ads health check for an existing client account. Pulls yesterday and the last 3 days at ad level, flags every ad that is bleeding money or failing a funnel benchmark (CTR, link CTR, CPM, page views, add to cart, checkout, CPA vs target), says WHERE it fails and WHAT to check, and gives a short "do today" list. Use it whenever the user says "daily check", "check the Meta account", "anything on fire", "how are the ads doing today", "daily ads review", "check [client]'s ads", or asks which ads to pause today — even if they don't say "daily".
---

# Meta daily check

A 2-minute morning scan. The job is to catch money leaks and broken ads early, not to redesign the account. Big decisions (restructure, scaling plans, new campaigns) belong to the weekly review, so keep this short and action-first.

## Steps

1. **Identify the client and numbers.** Which ad account, target CPA, break-even CPA, AOV. See `references/getting-data.md` → "Client numbers".
2. **Get the data** (see `references/getting-data.md`): ad level, **last 3 days** (`last_3d`) — one day is too noisy to cut ads on. Also pull **yesterday** at account level for the spend/purchases line.
3. **Run the script:**
   ```bash
   python scripts/meta_flags.py last3d.csv --mode daily --target-cpa <T> --breakeven-cpa <B> --aov <A>
   ```
4. **Sanity-check the flags** with `references/benchmarks.md`. The script is deliberately mechanical; you add judgement:
   - A new ad (launched < 3 days, or in a test campaign under the impression cap) flagged for 0 purchases → downgrade to "too early", don't recommend pausing.
   - Middle-of-funnel retargeting ads are judged on clicks, not purchases — don't flag them for CPA.
   - If the *whole account* shares one leak (e.g. every ad has low add-to-cart), say it's a site problem, not an ad problem.
   - Big overnight changes across all ads at once usually mean tracking/pixel or delivery issues → say "check Events Manager / delivery first".
5. **Write the report** in this format (keep it under ~25 lines):

```
# Daily check — <Client> — <date>
Yesterday: $<spend> · <purchases> purchases · CPA $<x> (target $<t>) · ROAS <x>
Status: 🟢 on track / 🟡 watch / 🔴 action needed — <one line why>

## 🔴 Do today
- <Ad name> (<campaign>): <problem> → <exact action: pause / lower budget / check X>

## 🟡 Watch (re-check tomorrow)
- <Ad name>: <problem> — where: <stage> — check: <what>

## 🟢 Fine
<count> ads healthy. Best: <ad> (CPA $x).
```

Use the script's "Where" and "What to check" wording for each ad, trimmed to one line. Name the funnel stage explicitly (Attention, Interest, Page load, Buying intent, Cart, Checkout, Result) so the user knows where to look.

## Don't
- Don't recommend new campaigns, restructures or budget increases above $10–20/day here — point to the weekly review instead.
- Don't pause anything on a single day's data or under 1,000 impressions.
- Don't make up numbers if data is missing; say what's missing.
