---
name: ad-versions
description: Ad copy + creative version writer for Filip Kostic. Asks what it needs about the brand, then researches the gaps itself (website, reviews, Reddit, competitors, Meta Ad Library), turns one real customer problem into a one-sentence angle, and writes 3 distinct paste-ready copy versions with matching creative descriptions (hook, solution, show it, visual proof, one change per variation) plus a fair test plan. Use EVERY TIME Filip wants ad variations or new ads for a brand, or says "3 versions of ad copy", "ad variations for [brand]", "new creatives for [client]", "copy for angle X", "write the ads for these angles", "Google and Meta copy", "copy + creative for [angle]". Covers Meta, Google Search RSA and Display. Full RSA builds → rsa-writer; production briefs → creative-brief; iterating a proven winner → winner-variations.
---

# Ad Versions — research → angle → 3× copy + creative per concept

## Purpose
Produce test-ready ads that start from **evidence about the customer**, not from a format. One real problem → one clear angle → three genuinely different versions, each with a matched creative that *shows* the value, plus a plan to test them fairly. Method details and examples: `references/creative-method.md` (read it the first time you use this skill in a conversation).

## Step 1 — Intake: ask, don't guess
Read the Client ID doc first (voice, never-claims, cheat sheet are hard constraints; never invent client facts). Then ask Filip **only what's missing**, in one short message (skip anything already known):
1. Brand + product/offer to advertise, and the landing page URL
2. Who buys it (persona), and the main use case
3. What customers want, what stops them, what they've tried before (any reviews/comments/objections he can paste?)
4. Proof available: reviews count/rating, numbers, guarantees, before/afters, press
5. Main competitors (names/URLs)
6. Platform + placement, daily test budget, and any angle already chosen
7. Assets that exist (UGC, product video, photos) or production limits

If he says "don't know", "you find it", or doesn't answer a point → go to Step 2 for that point. Don't block on answers you can research.

## Step 2 — Research what's missing (web)
Use web search/fetch; keep notes with source links. Cover, in order of value:
- **Brand site**: product page, homepage, FAQ, about, shipping/returns, pricing, bundles — what's promised and what's missing.
- **Customer voice**: on-site reviews, Trustpilot/Google/Amazon reviews, Reddit and forum threads, YouTube/TikTok comments. Copy exact phrases — the customer's words become hooks.
- **Competitors** (2–4; find them via search if not given): their product pages, price points, offers, and especially their **negative reviews** (gaps you can attack) and positive reviews (what the category values).
- **Competitor ads**: Meta Ad Library (facebook.com/ads/library) for the brand and competitors — which formats, hooks and offers they run, and which ads have run longest (a sign they work). If the Meta Ads connector is available, `ads_library_search` does this directly.
Label every researched fact with its source; anything unverified is *[TO CONFIRM]*. Never state a client claim (price, rating, result, guarantee) you didn't find or get told.

## Step 3 — Customer insight → angles
Summarise the research as a short table: **Want · Blocker · Already tried · Exact customer phrase · Source**. Then:
- Pick **one problem per angle**; write each angle as **one sentence** ("Get more steps while you work without a giant treadmill taking precious space").
- One product usually has several reasons to buy (e.g. blackout blinds → nursery, RV, truck cab, studio). List them as separate angles; recommend testing the strongest first, others later with side budget.
- If Filip already chose angles, still sanity-check them against the evidence and say so in one line if one looks weak.

## Step 4 — Pick the format for the message
Format is how the message is delivered, chosen *after* the angle:
- **Static** when the value is obvious at a glance.
- **Video/UGC/demo** when people must see it work (folding, fitting, routine, before/after, real use).
- **Product-on-white + text** only for high-intent/retargeting audiences — cold traffic needs the picture painted.

## Step 5 — The 3×3 structure (9 ads per concept)
Two levels, don't collapse them:
1. **Pick 3 persuasion approaches** for the concept. Default trio: Direct/benefit · Story/emotive · Proof/objection — swap freely when the angle demands it (identity, seasonality, risk-reversal, social proof, curiosity…). The 3 approaches must be genuinely different persuasion logics.
2. **Write 3 executions per approach** (E1/E2/E3) sharing the approach's logic but differing in **one** thing — hook, scene, creator, or format — named explicitly (e.g. "E2 = same script, carousel instead of UGC"). Not synonym swaps: if two executions could run under the same visual unchanged, rewrite one.
Name ads [Angle]-[Approach]-[E#] so results map back to structure: approach-level results show WHY something works, execution-level show HOW to say it.

**Every execution is built on the build card:**
- **Hook** — direct and qualifying; lead with the customer's problem in their words ("If you work from home and finish the day with 800 steps when your goal was 10,000, keep listening"). The strongest line goes first; assume nobody reads line two unless line one earns it.
- **Solution** — plain words, one promise (the angle).
- **Show it** — the scene sequence that demonstrates the promise.
- **Proof** — for every claim ask "how can I show this?"; use real numbers only if the brand has them. Don't write "life-changing" — show why.
- Clear beats clever: aim for "this solves my exact problem", not an ad for everyone. Warranty/returns/spec lists belong on the landing page, not in the ad.
- Check that the landing page continues the ad's promise; if it doesn't, flag it (the ad only buys the click).

## Per-platform output spec (char-count everything before delivering)
**Meta (feed/reels):** Primary text (first 125 chars must work standalone), Headline ≤ 40 chars (aim ~27), Description ≤ 30 chars, CTA button (inquiry funnels: Learn More / Get Quote / Contact Us — "Book Now" only where booking is instant).
**Google Search (RSA):** 5 headlines ≤ 30 chars + 2 descriptions ≤ 90 chars, keyword-conscious, no two headlines saying the same thing. (Full 15/4 builds → rsa-writer.)
**Google Display:** Short headline ≤ 30, Long headline ≤ 90, Description ≤ 90.

## Creative descriptions (one per execution)
2–3 sentences: what the image/video literally shows (scene by scene for video: hook shot → demonstration → proof), style/format (static, carousel, UGC, POV, demo), any text overlay, and the one variable that differs from its siblings. Concrete enough that a designer or AI tool can start immediately. Full production specs → creative-brief.

## Step 6 — Test plan (always include, short)
- Match volume to budget: at ~$30–100/day test a focused batch (e.g. the 3 E1s, or one approach's 3 executions) rather than all 9 at once.
- Run them apples-to-apples in a separate creative-test campaign with an impression cap per ad (1,000; 800 on a new pixel with $50–70 CPMs; 2–3k if budget allows). Estimate days = ads × CPM × cap/1000 ÷ daily budget.
- Read results along the journey: CTR (did they stop?) → link CTR drop (did they click? big drop = attention without intent) → carts/checkout/CVR after the click (if clicks don't buy, check the landing page before blaming the ad) → does it hold at more budget?
- A winner is not "the ad Meta spent the most on". Hand results to testing-plan / meta-creative-test-review.

## Rules
- Language, tone, CTA verbs and never-claim list come from the Client ID cheat sheet — check every line against it. If there's no Client ID doc, say so and use the researched brand voice.
- Respect platform policy notes (health, finance, before/after claims) in the Client ID's restrictions section.
- Unverifiable specifics (prices, counts, results) either come from the doc, Filip, or a cited source — otherwise *[TO CONFIRM]*, never shipped silently.

## Output format
1. **Research snapshot** (only when Step 2 ran): insight table + 3–6 competitor/ad-library observations, each with a source link.
2. **Angles**: one sentence each, the recommended first one marked.
3. Per concept: concept name + platform + format, then approaches → V/E blocks (copy fields + creative description + "differs by").
4. **Test plan** (4–5 lines) and **next brief rule**: whatever wins decides the next batch (angle won → more on that angle; hook won → same hook, 3 new bodies; demo beat UGC → more demos).
Deliver in chat for review; offer a .docx/.xlsx export when Filip approves or asks for handoff format.

## Document export (when Filip asks for "a document", "separate doc", "export this", or approves copy for handoff)
Produce a standalone .docx — the Copy Pack — one file per persona:
1. **Title**: [Client] — Ad Copy Pack: [Persona name] ([Platform]).
2. **Persona description**: who they are, why they buy, primary message — from the Client ID doc / research, with sources for researched facts.
3. **Per concept/angle**: angle sentence (emotional driver, core promise, proof point), then one real table per approach (rows: Primary text / Headline / Description / CTA / Creative description / Differs by; columns: E1 / E2 / E3).
4. **Test plan** section and any *[TO CONFIRM]* flags; char counts next to headlines/descriptions.
Real tables (never raw markdown pipes), proper headings, client-meeting quality.

## Hand-off
Winners → creative-brief (production briefs), testing-plan (queue the test), meta-creative-test-review (judge results), winner-variations (once something proves out).
