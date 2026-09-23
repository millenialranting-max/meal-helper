# Getting the ad-level data

The analysis script needs one row per ad with these columns (names can be Ads Manager's own):
Campaign name, Ad set name, Ad name, Amount spent, Impressions, Frequency, Clicks (all), Link clicks,
Landing page views (or Content views), Adds to cart, Checkouts initiated, Purchases, Purchases conversion value.

## Route A — Meta Ads connector (preferred when the Meta_Ads tools are available)
1. `ads_get_ad_accounts` → pick the client's account (match by name; ask if several match). Skip accounts where `is_queryable` is false and tell the user why.
2. `ads_get_field_context` at level `ad` to confirm the canonical names for: ad name, campaign name, ad set name, spend/amount spent, impressions, frequency, clicks (all), link clicks, landing page views, adds to cart, checkouts initiated, purchases, purchase value. Use only names it returns.
3. `ads_get_ad_entities` with `level: "ad"`, the verified `fields`, the date range the skill asks for (`date_preset`, e.g. `yesterday`, `last_3d`, `last_7d`), and a filter for ads with delivery/spend in the period if supported. Follow any `next_actions` the tool returns before continuing. Page with `cursor` until done.
4. Write the rows to a CSV in the scratchpad (one row per ad, header = the column names above) and run the script on it.
5. For a comparison period (weekly skill), repeat step 3 with the prior range (`time_range` JSON) into a second CSV and pass it as `--prev`.

If the connector errors, lacks a field, or returns nothing for conversions, say so in one line and switch to Route B for the missing part rather than guessing numbers.

## Route B — Ads Manager export (always works)
Ask the user to export from Ads Manager: Ads tab → date range → Columns: their saved preset (or the list above) → Reports → Export table data → CSV. Then run the script on the file they share.

## Client numbers
The script needs `--target-cpa`, and ideally `--breakeven-cpa` and `--aov`. Look for them in this conversation, in the client's Client ID / onboarding doc, or in project memory. If they are missing, ask once in a single line ("What's the target CPA and break-even CPA for <client>? AOV if you know it") and continue with whatever you have — the script still flags funnel leaks without them, it just can't judge profit.
