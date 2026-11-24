# Build rules (lessons learned)

These came from building and refining real kits. Treat them as rules, not suggestions.

## Environment

- Build offline in `working/<kit>/`. Validate with Python using stdlib, pandas or openpyxl only;
  pip is blocked, so don't plan on other packages.
- Zip with Python `zipfile` (ZIP_DEFLATED) after the checks pass.

## Data

- Realistic, deliberately messy, fictional synthetic data.
- Plant data-quality issues across days so the demo has a story:
  - Day 1: bad values (nulls in keys, negative readings, invalid codes, bad dates)
  - Day 2: late-arriving rows and SCD2 changes (an asset moves site, a customer changes tier)
  - Day 3: schema drift (renamed or added column, changed type)
- Every organisation, person and identifier is fictional. Say so in the main README and in each
  sample data folder. Never use real customer names in the data, even for a customer kit.
- Generate data inside the product where possible (notebook generators with a fixed seed), so
  there is nothing large to upload. Ship only small seed samples (a few hundred rows).
- Default to about 3 source systems.

## Design

- Metadata-driven wherever the product supports it: control tables drive ingestion, DQ rules,
  PII treatment and Gold SQL. Adding a source or an industry means adding config, not code.
- One config file per industry (e.g. `config/energy.json`). Every module works for every pack.
- Each industry gets an illustrative dollar measure (outage cost at risk, expected loss, lost
  sales...). Label it "illustrative" wherever it appears.
- Use cases are common, high-value ones customers expect to see. Self-check before building:
  would a sponsor in that industry recognise it straight away? If not, swap it.

## Folder layout

```
README.md
Use_Case_Explanation.md
config/          one JSON per industry
data/            small seed samples + README
notebooks/       generators + transforms + README
pipelines/       pipeline JSON + README
sql/             warehouse / gold SQL + README
ai/              one guide per industry (e.g. ai/energy.md)
powerbi/         model notes + README
devops/          CI/CD notes + README   (only if chosen)
```

Adjust module folders to the product (see reference-design.md for non-data products).

- Every module folder has its own README.md with setup steps, including `pipelines/`.
- `Use_Case_Explanation.md` sits at the top level, separate from the main README, with a short
  section per industry: the problem, the data, the measure, what the demo shows.
- The `ai/` folder has one guide per industry: build a semantic model, a data agent and an
  ontology, plus demo prompts. Buildable in ~15 minutes, with the exact tables, steps and prompts.

## File names and zip

- Short names, no spaces. Zip paths under 100 characters, target under 60, so Windows can unzip.
- Files go at the ROOT of the zip, not under a top folder with the zip's name. Otherwise
  Windows "Extract All" creates a folder inside a folder.
- Zip name: `<Customer>-<Product>-Demo-Kit.zip` (e.g. `Contoso-Fabric-Demo-Kit.zip`).

## README content

- Main README: what it is, prerequisites, setup in order, the demo script (what to click, what to
  say), troubleshooting table, reset steps, a short neutral "Before you present" note.
- No contact/intro line under the H1 of any README or AI guide, and no help offer or personal
  sign-off at the end. Each trainer builds the kit for themselves.
- Voice, header, tables and closing note: see readme-style.md.

## Customer-shared kits

- Include only the customer's own industry pack and its use case.
- Publish with the "General" sensitivity label.
- No internal-only notes, roadmaps or other customers' names.

## Validation before delivery

- Config files load (json.load).
- Generated SQL runs in SQLite where the dialect allows (create tables, insert seed rows, run the
  Gold query). Note which SQL is Fabric/T-SQL-only and was not run.
- Notebook and script code compiles (`compile()` / `py_compile`).
- All JSON is valid; pipeline JSON parses.
- Path lengths within limits; no spaces.
- Zip test-unzips to a temp folder and the file count matches.
- Every README and AI guide starts with an H1 and has no contact line, help offer or sign-off.
- `scripts/check_kit.py` covers most of this in one run.
