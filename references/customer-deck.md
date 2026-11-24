# Customer-facing solution deck

The second deck of every run. The trainer deck explains the demo kit (how to run it); this one is
for the customer: the target design the demo proves, in the same Microsoft Learn look. It is the
"architecture and CI/CD" style deck: visual, few words, one idea per slide.

Shape: cover + 4-7 content slides + the template's closing slide (Microsoft logo).
Generator: `scripts/build_customer_deck.py` (shares palette, fonts and fit checks with
`build_deck.py`). Example spec: `customer-deck-example.json`.

## Spec

```
{
  "title": "<Customer> on <Product>: the design",   <= 60 chars
  "subtitle": "Architecture behind the demo",        <= 38 chars
  "notes": {"cover": "..."},
  "closing_notes": "...",                            optional
  "slides": [ {"type": "...", "title": "...", ..., "notes": "..."} ]   4-7 slides
}
```

## Slide types

| type           | Use it for                                  | Fields                                                     |
| -------------- | ------------------------------------------- | ---------------------------------------------------------- |
| `architecture` | Target architecture, end to end             | same as the trainer deck: sources, stages, consumers, spine |
| `table`        | Design decisions, source-by-source patterns | `rows` (header + 1-7 rows, 2-5 cols), `widths`, `band`     |
| `process`      | Onboarding a source, request flow, agent loop | `steps` [3-6] {name, desc, lines}, `band`               |
| `lanes`        | CI/CD Dev → Test → Prod, workspaces, zones  | `lanes` [2-4] {name, sub, items}, `arrows`, `band` {name, desc} |
| `cards`        | Quality / security / governance pillars     | `cards` [2-4] {name, sub, items, lift}, `band`            |
| `timeline`     | Migration or adoption roadmap               | `phases` [3-5] {when, name, lines, now}, `band`           |
| `value`        | Business value and next step                | `measure` {value, label}, `outcomes` [2-4], `next`        |

## Default slide sets by product

| Product          | Slides (in order)                                                                     |
| ---------------- | ------------------------------------------------------------------------------------- |
| Fabric           | architecture, table (design decisions), process (new source), cards (quality, security, governance), lanes (CI/CD), timeline (migration), value |
| Azure AI Foundry | architecture (docs → index → agent → evaluate), process (agent request flow), cards (safety, evaluation, responsible AI), table (model / tool choices), lanes (dev → eval → prod with gates), timeline (pilot → scale), value |
| Azure ML         | architecture, process (train → register → deploy), cards (MLOps, monitoring, governance), lanes (CI/CD), value |
| Databricks       | architecture, table (decisions), cards (Unity Catalog governance), lanes (CI/CD with bundles), timeline, value |
| Power BI         | architecture, table (Import / DirectQuery / Direct Lake), cards (security, governance, Copilot), lanes (dev → test → prod), value |
| AKS / App Service | architecture, process (request path), cards (security, scale, observability), lanes (CI/CD), value |

Trim to what the customer asked about in the discovery call; never pad to 7.

## Rules

- Customer-facing language: their problems and outcomes, not kit file names or notebook numbers.
- The real customer may appear on the cover and in titles; the demo organisation and every figure
  stay fictional, and the value slide says "(illustrative)".
- Titles state the point (≤ 48 characters): "Ship changes safely with CI/CD", not "CI/CD".
- Card bullets 3 per card, a few words each; the talk goes in `notes`.
- Timings on a timeline are illustrative; say so in the notes.
- Same names and numbers as the kit and the trainer deck (all three come from design.json).
