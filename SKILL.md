---
name: caip-custom-demo
description: |
  CAIP Custom Demo: in one run, builds a customer-specific, industry-tailored demo kit for a Cloud
  & AI Platforms (CAIP) training (Microsoft Fabric, Azure AI Foundry, Azure OpenAI, Azure Machine
  Learning, Databricks, Power BI, AKS, App Service...)
  AND two Microsoft Learn decks: a 5-slide trainer deck that walks through the demo, and a
  customer-facing solution deck (architecture, design decisions, governance, CI/CD, roadmap,
  value). Delivers the zip (fictional messy data, configs, READMEs, AI guide) plus both decks. Use when a
  trainer asks to "create a custom demo", "build a demo kit for <customer>", "custom Fabric /
  Foundry demo", "demo and deck for <customer>", "customer demo zip" or "tailor the demo to
  <industry>". Do NOT use for a deck only with no demo (use pptx), class lookups/rosters (use
  mtt-class-lookup) or courseware bugs (use mtt-courseware-feedback). CAIP-focused, but also
  works for other Microsoft products (M365 Copilot, Copilot Studio, Dynamics 365, Power Platform,
  security) when a trainer asks.
metadata:
  title: CAIP Custom Demo
  version: "2.1.0"
  category: productivity
  icon: Box
---

# CAIP Custom Demo

Builds a reusable, customer-specific demo for a Microsoft trainer (MTT) teaching a Cloud & AI
Platforms course, and in the SAME run two decks: one the trainer uses to walk through the demo,
and one to show the customer the design the demo proves.
Everything it needs is in this folder (references, checks, deck generator and the Microsoft Learn
template), so it can move into a skills pack unchanged. Nothing is tied to one customer.

**Three deliverables, one run, always all three** (unless the trainer explicitly asks for less):

1. `<Customer>-<Product>-Demo-Kit.zip` – the technical demo kit.
2. `<Customer> <Product> Custom Demo.pptx` – trainer deck, 5 slides: the challenge, how the demo
   is built, the demo moments, what's in the kit and how to run it.
3. `<Customer> <Product> Solution Design.pptx` – customer-facing deck, cover + 4-7 slides +
   closing: target architecture, design decisions, how a new source goes live, quality /
   security / governance, CI/CD, migration roadmap, business value.

All three are built from ONE design (Step 2), so names, numbers and moments always match.

## When to Use

- "Create a custom Fabric demo for Contoso Energy"
- "Build a Foundry demo kit and deck for <customer>"
- "Demo for <customer> on Databricks" / "tailor the demo to healthcare"
- "Give me a customer demo zip and slides for DP-700 / AI-102 / DP-100"

## When NOT to Use

- A deck only, no demo assets: use the `pptx` skill
- Class details, rosters, lab codes: `mtt-class-lookup`; courseware bugs: `mtt-courseware-feedback`
- Running or deploying the kit in a real tenant: this skill builds files only

## Workflow

Track the run with `core-TaskCreate`: Intake, Design, Build kit, Build trainer deck, Build customer
deck, Validate and deliver.

### Step 1: Intake (ask before building)

1. Search M365 first and pre-fill what you find: `graph_deferred-GetMyRecentTranscripts` /
   `graph_deferred-ListMeetingTranscripts` for a pre-training call, `m365_search-SearchM365` and
   `ExecuteSql` (`messages WHERE MATCH('<customer>')`) for emails and chats about the customer.
2. Ask the remaining questions with **`core-AskUserQuestion`**, batched into one or two calls,
   never as plain-text questions. Skip anything already answered. Full list, options and defaults:
   [references/intake-questions.md](references/intake-questions.md) (customer, industry, CAIP
   product + course, use cases, sources, modules, audience + time, sharing).

### Step 2: Design once, for all three deliverables

Write `working/<kit>/design.json` with the fictional organisation, the use case per industry and
its illustrative dollar measure, sources, layers/stages, modules, demo moments and how to run it.
Show a short plan in chat (organisation, use case, measure, sources, modules, the slide titles
of both decks, zip tree). Self-check the use cases are common, high-value ones a sponsor would recognise. Proceed
unless the trainer changes something. The kit READMEs and the deck spec are both derived from this
one design: same names, same numbers, same moments.
Pick the customer deck's slides from the product's default set in
[references/customer-deck.md](references/customer-deck.md), trimmed to what the customer asked about.

### Step 3: Build the kit (offline in `working/<kit>/`)

Follow [references/build-rules.md](references/build-rules.md), the product designs in
[references/reference-design.md](references/reference-design.md) and the README voice in
[references/readme-style.md](references/readme-style.md). Key rules:
- Python stdlib / pandas / openpyxl only (pip is blocked).
- Fictional, deliberately messy data with planted day-by-day issues; the kit says it is fictional.
- Config-driven: adding a source or industry = adding config, not code. One config per industry.
- Generate data inside the product where possible; ~3 source systems; keep the zip small.
- Files at the zip ROOT, short names, no spaces, paths < 100 chars (target < 60).
- No contact/intro line and no help offer or personal sign-off in any README or AI guide.

### Step 4: Build the trainer deck (same run, on the Microsoft Learn template)

Load the `pptx` skill first (it owns the live-deck tools and rules), then follow
[references/deck-design.md](references/deck-design.md). In short:

1. Write `working/<kit>/deck_spec.json` from the design (format:
   [references/deck-spec.md](references/deck-spec.md), example:
   [references/deck-spec-example.json](references/deck-spec-example.json)).
2. `python scripts/build_deck.py working/<kit>/deck_spec.json --out working/<kit>/deck`.
   It fails on text that would overflow, wrap a title or go under 12pt; shorten the spec text and
   rerun until it prints `wrote ...`. It never writes a .pptx, only two patch files.
3. Seed the template: `cp <this skill>/assets/ms-learn-template.pptx working/<kit>/tpl.pptx`, then
   `host-CopyArtifact(surface="output", source="working/<kit>/tpl.pptx",
   destination="<Customer> <Product> Custom Demo.pptx")` → take the returned `file_N`.
4. `host-EditArtifact(surface="live", path=file_N, patches_file="working/<kit>/deck-1-structure.json")`
   (5 slides), then `host-GetArtifactModel(surface="live")` to confirm 5 slides, then
   `host-EditArtifact(... patches_file="working/<kit>/deck-2-content.json")`.
5. QA once: `host-GetArtifactModel(render=true)` → `core-RenderArtifact` on slides 0-4 → view
   every image. Fix overflow or overlap by shortening spec text: `delete_shape` the slide's added
   shapes (index 2 upwards) and re-send that slide's patches from a re-generated content file.
   One fix round at most.

### Step 5: Build the customer-facing deck (same run, same template)

Follow [references/customer-deck.md](references/customer-deck.md):

1. Write `working/<kit>/customer_deck_spec.json` (example:
   [references/customer-deck-example.json](references/customer-deck-example.json)).
2. `python scripts/build_customer_deck.py working/<kit>/customer_deck_spec.json --out working/<kit>/cust`
   until it prints `wrote ...`.
3. Seed a second copy of the template with `host-CopyArtifact` as
   `<Customer> <Product> Solution Design.pptx`, apply `cust-1-structure.json`, re-read the model
   (cover + N content + closing), then apply `cust-2-content.json`.
4. Same QA as the trainer deck: one render sweep of every slide, one fix round at most.

The kit and the two decks can be built in any order, but all three finish before Step 6.

### Step 6: Validate and deliver all three

1. `python scripts/check_kit.py working/<kit> --zip working/<Name>.zip` (never runs kit code):
   JSON/config loads, code compiles, path lengths, no spaces, README H1, table width, root-level
   zip, test unzip, no contact line or help offer. Also run generated SQL in `sqlite3` where the
   dialect allows. Fix every FAIL.
2. Publish the zip: `host-CopyArtifact(surface="output", source="working/<Name>.zip",
   destination="<Customer>-<Product>-Demo-Kit.zip")` (add `label="General"` when shared with the
   customer). Confirm `ok: true`.
3. Both decks are already the trainer's live files; cite each by its `[file_N]` handle.
4. Reply in chat (format below).

## Output

Short chat reply, no raw file dumps:

```
Your custom demo for <Customer> is ready:
- **<Customer>-<Product>-Demo-Kit.zip** – <n> files: README, Use_Case_Explanation.md, <modules>, AI guide.
- [file_N] – trainer deck, 5 slides: the challenge, how the demo is built, the demo moments,
  what's in the kit.
- [file_M] – customer deck, <n> slides: <slide titles>.
Checked: <checks that passed>. Not run in a tenant; do a dry run first.
Want: another industry, a customer-only cut, or a swapped use case?
```

## Guardrails

- Ask intake questions before building; never invent the customer's real systems or use cases.
- All organisations, people and identifiers are fictional; never real customer data or PII. The
  deck may name the real customer on the cover only; the demo organisation stays fictional.
- Dollar figures are labelled "illustrative" in the kit and the deck.
- A customer-shared kit contains only that customer's industry and gets the "General" label.
- Never claim anything was tested in a tenant. State exactly which local checks ran.
- Never build or edit the .pptx with python-pptx or scripts: the deck is built only with the
  artifact tools on `live`, seeded from `assets/ms-learn-template.pptx`. Trainer deck max 5 slides;
  customer deck max 7 content slides plus cover and closing.
- The customer deck uses customer language (problems, outcomes), never kit file names.
- Never write to the user's skills folder or other files; deliverables are the zip in `output/`
  and the two live decks.
- If a check fails and can't be fixed, deliver nothing for that part and say what failed.
