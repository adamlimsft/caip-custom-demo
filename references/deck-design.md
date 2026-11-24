# Deck design: explain the custom demo in 5 slides

The deck tells the customer what the demo is, how it is built, what they will see and what they
get. It is built on the Microsoft Learn template in `assets/ms-learn-template.pptx` (cover with
Microsoft logo and 3D artwork, "Blank_with Head" content slide, Microsoft copyright footer).

## The 5 slides (fixed order, never more than 5)

| # | Slide        | What it shows                                                        |
| - | ------------ | -------------------------------------------------------------------- |
| 0 | Cover        | "<Customer>: a custom <Product> demo" + a short subtitle             |
| 1 | Story        | The challenge (left) and a big illustrative $ tile + 3 proof points  |
| 2 | Architecture | Sources → 3-5 product stages → who uses it, with the control spine  |
| 3 | Moments      | 3-5 demo moments left to right, each with what it proves             |
| 4 | Takeaway     | What's in the kit (tiles), how to run it (3 steps), outcome band     |

Titles state the point in one line (48 characters max), e.g. "Which asset fails next, and what's
it worth?" rather than "Use case".

## Look and feel (already coded in scripts/build_deck.py)

- Palette: Microsoft Learn purple `702573`, tints `F5EDF5` / `E8D3E9`, stage ramp `EEEAE5` →
  `5A1D5C`, one accent orange `FE5B38` (pain markers, takeaway outline), ink `1F1F1F`, grey
  `595959`, neutral `F2F0ED`.
- Font: Segoe UI (the template's font). Body 14pt, captions 12pt, never below 12pt.
- Flat rectangles, chevrons (`homePlate`) for moments, grey arrows for flow. No charts, no
  invented bars: the only number is the illustrative dollar tile.
- The template's cover artwork, logo and copyright footer stay untouched.

## Product stage examples (architecture slide)

| Product            | Stages                                                        |
| ------------------ | ------------------------------------------------------------- |
| Fabric             | Landing → Bronze → Silver → Gold                              |
| Azure AI Foundry   | Documents → Index (AI Search) → Agent / prompt flow → Evaluate |
| Azure OpenAI + RAG | Ingest → Chunk + embed → Retrieve → Generate + ground         |
| Databricks         | Auto Loader → Bronze → Silver → Gold (Unity Catalog)          |
| Azure ML           | Data → Features → Train → Register → Deploy + monitor         |
| Power BI           | Sources → Dataflow → Semantic model → Report + Copilot        |
| AKS / App Service  | Code → Build (CI) → Deploy (CD) → Run + observe               |

The "spine" is the thing that makes it scale: control tables (Fabric), evaluation datasets and
safety filters (Foundry), Unity Catalog (Databricks), MLflow registry (Azure ML), IaC / GitOps
(AKS).

## Writing rules

- Same names, numbers and moments as the kit (both come from design.json).
- Few words: card text one or two short lines; the talk goes in `notes`.
- The demo organisation is fictional and the footnote says so; the dollar figure says
  "(illustrative)".
- Cover title ≤ 60 characters, subtitle ≤ 38, slide titles ≤ 48. The generator enforces these.

## Fixing a slide after QA

The generator's fit check is conservative, but a render can still show a wrap. Shorten the text in
the spec, regenerate, then on the live deck `delete_shape` that slide's shapes from index 2
upwards (0 = title, 1 = footer) and send only that slide's ops from the new content file
(skip its `set_text` on shape 0 if the title did not change). One fix round only.
