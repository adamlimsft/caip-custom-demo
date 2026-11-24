# Reference design (Fabric example, built and refined)

Use this as the template for data products (Fabric, Databricks, Azure SQL, Power BI). For other
products keep the principles and swap the modules (last section).

## Per-industry pack shape

Each industry pack has the same five feeds, so every module works for every pack:

| Feed        | Source                 | Load pattern             | Notes                      |
| ----------- | ---------------------- | ------------------------ | -------------------------- |
| Entity      | On-prem DB             | SCD2                     | assets, accounts, stores   |
| Events      | On-prem DB / API       | SCD1 (upsert)            | work orders, tickets       |
| Readings    | File drop, 15-min      | Insert-only              | meters, telemetry, sales   |
| CRM party   | JSON                   | PII treatment + soft del | customers, patients        |
| Extra feed  | Any                    | Onboarded live           | metadata rows only, no code|

- The extra feed is the "wow" moment: add rows to the control tables and rerun; no code change.

## Layers

landing → bronze → silver → gold, plus quarantine.

- Landing: raw files as delivered.
- Bronze: raw + load metadata (run_id, source_file, load_ts).
- Silver: typed, deduped, SCD applied, PII treated, DQ applied.
- Gold: business scorecard per industry.
- Quarantine: rows that failed a quarantine-level rule, with the rule id and reason.

## Control tables (`meta.*`)

| Table              | Purpose                                               |
| ------------------ | ----------------------------------------------------- |
| ingestion_object   | one row per feed: source, path, load type, keys       |
| column_map         | source → target column, type, PII treatment           |
| dq_rule            | rule id, object, expression, type, severity           |
| run_log            | one row per object per run: status, rows, timings     |
| dq_result          | rule outcomes per run: pass/fail counts               |
| watermark          | last loaded value per object for incremental loads    |

## DQ rules

- Technical rules: nulls in keys, types, ranges, duplicates, schema drift.
- Business rules: domain logic (reading above asset capacity, claim after policy end).
- Severity:
  - `warn`: load the row, log the result.
  - `quarantine`: divert the row to quarantine, continue the load.
  - `fail`: stop the object's load and mark the run failed.
- Rerun-failed-only: the orchestrator reads `run_log` and reruns only objects that failed.

## Gold scorecard

One table per pack: entity key, a few KPIs, a 0-100 risk score, a risk band and an illustrative
dollar column. Gold SQL lives in config so a new industry is a new config, not new code.

## The 9 industry example use cases

| Industry         | Use case                                  | Dollar measure (illustr.) |
| ---------------- | ----------------------------------------- | ------------------------- |
| Energy           | Asset health and maintenance              | Outage cost at risk       |
| Telco            | Network service assurance                 | Revenue at risk           |
| FSI              | Fraud, credit risk and collections        | Expected loss             |
| Manufacturing    | Predictive maintenance                    | Downtime cost             |
| Healthcare       | Patient flow and ward pressure            | Access-block cost         |
| IT & ITeS        | Client SLAs and contract health           | Contract revenue at risk  |
| Government       | Infrastructure and citizen services       | Cost at risk              |
| Retail           | Stock availability                        | Lost sales at risk        |
| Digital natives  | Platform reliability and customer health  | ARR at risk               |

- Government measures performance against published service standards.
- All dollar figures are illustrative and labelled so.

## AI module (per industry, ~15 minutes)

- Semantic model over the Gold scorecard + 1-2 silver dimension tables (name the exact tables).
- Data agent grounded on that model, with instructions and 5-8 demo prompts.
- Ontology: the main entities and relationships for that industry.
- Demo prompts start simple ("top 10 assets by risk") and end with a business question
  ("where should we send crews this week to cut outage cost at risk?").

## Other CAIP products

The skill is CAIP-focused but not limited to CAIP. For any other Microsoft product (M365
Copilot, Copilot Studio, Dynamics 365, Power Platform, security), apply the same principles and
pick modules that fit the product.

Same principles (fictional messy data, per-industry config, one README per module, small zip),
product-specific modules:

| Product                 | Typical modules                                                 |
| ----------------------- | --------------------------------------------------------------- |
| Azure AI Foundry        | agents, prompt flows, AI Search index, eval datasets, safety    |
| Azure OpenAI + RAG      | sample docs, chunking + embeddings, grounded chat, evaluation   |
| Azure Machine Learning  | datasets, training jobs, MLflow registry, endpoint, monitoring  |
| Azure Databricks        | Auto Loader, DLT / Lakeflow, Unity Catalog, Genie, MLflow       |
| Power BI                | semantic model, DAX measures, report, Copilot prompts           |
| Azure SQL / Cosmos DB   | schema + seed data, mirroring to Fabric, vector search          |
| AKS / App Service       | sample app, manifests or Bicep, CI/CD, monitoring runbook       |

Foundry example (same industry stories): the "messy data" is a folder of fictional documents
(policies, work orders, manuals) with planted problems (outdated versions, conflicting answers,
PII); the "wow" moment is adding a new document source or a new evaluation rule by config, and
re-running the evaluation to show groundedness and safety scores change.
