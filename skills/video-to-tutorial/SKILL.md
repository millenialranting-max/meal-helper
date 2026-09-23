---
name: video-to-tutorial
description: Turns one or more educational YouTube videos (or pasted transcripts) into a concise, colourful, step-by-step tutorial PDF — a roadmap strip, numbered steps in the order you'd actually do the work, exact settings cards, pass/fail checks, a troubleshooting tree, and next steps — built only from what the videos teach. Use whenever the user shares YouTube links (youtu.be / youtube.com) or transcripts and asks to "turn these into a tutorial", "make a step-by-step guide / playbook / SOP / how-to PDF", "summarise these videos into steps", "what do I actually do from these videos", or "make a document like the last tutorial" — even if they only say "summarise these videos" but clearly want something actionable.
---

# Video → tutorial PDF

The goal is a document someone can **follow**, not a summary of what was said. Readers should be able to open it next to the tool the videos teach and do each step without rewatching anything. So: process order, concrete values, decision rules, and fixes for when things go wrong — and nothing the videos don't support.

## 1. Get the transcripts

```bash
python scripts/fetch_transcripts.py <workdir>/transcripts <url1> <url2> ...
```
It tries yt-dlp with alternate player clients (this gets past YouTube's "confirm you're not a bot" block on server IPs), then youtube-transcript-api. For any video that still fails, ask the user to paste its transcript (YouTube: "…" → Show transcript). If *every* request fails with a network error, YouTube is probably blocked by the environment's network settings — tell the user rather than guessing content. Never write a tutorial from titles or search snippets alone.

Long transcripts (a 2-hour video ≈ 25k words): read them in chunks; don't skim — the useful numbers and settings are usually buried mid-video.

## 2. Analyse each video, then merge

For each video, note: its core claim, the steps/process it teaches, every concrete number (thresholds, budgets, durations, ratios), settings and exact UI choices, decision rules ("if X then Y"), common mistakes, and examples with results. Then merge across videos:
- **Order by the workflow**, not by video. Ask "what does a person do first, second, …?"
- **Deduplicate**: when videos repeat a point, keep the most specific version once.
- **Resolve conflicts** explicitly (one line: "Video A says X, B says Y — use X when…").
- Separate what the creator states from what you derive; label derived numbers as such in the source note.

## 3. Design the tutorial

Start from `assets/template.html` (component library: header, roadmap, step headings, two/three-box grids, checklists, recipe/settings cards, pass/fail gates, callouts, troubleshooting tree, system map, source note). `references/example-tutorial.html` is a finished 3-page example (a Meta ads client tutorial) — skim it to match tone and density.

Structure that works for most how-to topics:
1. **Header + roadmap strip** — one chip per step, 4–9 steps.
2. **Prerequisites / numbers to know** — what to define or set up before starting.
3. **Steps, in doing order** — each with the concrete action; branches as two boxes ("if you have X… / if starting fresh…").
4. **Settings cards** for anything the reader must build or configure — exact values, stop conditions, a worked example.
5. **Checks / gates** — how to tell good from bad, in the order to check, with thresholds.
6. **Troubleshooting tree** — top-down questions; fix only the first "no".
7. **What to do next / scaling / routine** + a short weekly or daily checklist if the topic has one.
8. **Source note** — videos, creator, date, which numbers are examples vs your derivation.

Writing rules: imperative verbs, numbers with units, one idea per bullet, no filler intros or recaps. Use the videos' own examples (real numbers) inside cards — they make rules concrete. Aim for 2–4 A4 pages; one page is fine for short topics. Don't pad to fill space.

## 4. Render and check

```bash
python scripts/render_pdf.py tutorial.html "<Topic>_Tutorial.pdf"
```
It prints the page count and saves PNG previews. **Look at every preview** before sending: fix near-empty pages (move a `pb` break or tighten), cut-off tables, overlapping text. Re-render until clean.

## 5. Deliver

Send the PDF (and offer the HTML if they want to edit it). In chat: one line per page on what's there, plus any assumptions or videos you couldn't read. Keep it short.
