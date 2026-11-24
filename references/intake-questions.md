# Intake questions

Ask with `core-AskUserQuestion`, batched into one or two calls (up to ~5 questions per call).
Skip any question already answered in the trainer's message or found in M365 (meeting transcript,
emails, Teams chats). Tell the trainer what you pre-filled and where it came from.

## Before asking: search M365

| Source           | Tool                                                  |
| ---------------- | ----------------------------------------------------- |
| Meeting notes    | `graph_deferred-GetMyRecentTranscripts`               |
| Emails           | `ExecuteSql` on `messages WHERE MATCH('<customer>')`  |
| Teams / files    | `m365_search-SearchM365` with the customer name       |

## Call 1: scope

| # | Header    | Question                                         | Type          |
| - | --------- | ------------------------------------------------ | ------------- |
| 1 | Customer  | Customer name, or generic / reusable kit?        | free text     |
| 2 | Industry  | Which industry or industries?                    | multi-select  |
| 3 | Product   | Microsoft product(s) and course, if any?         | free text     |
| 4 | Use cases | Which use cases or business problems?            | single select |
| 5 | Sources   | Customer's real source systems and formats?      | free text     |

Option notes:
- Industry options: Energy & utilities, Telco, FSI, Manufacturing, Healthcare, IT & ITeS,
  Government, Retail, Digital natives. AskUserQuestion takes up to ~5 options per question, so
  split into two multi-select questions if needed. "Other" is typed as free text, not an option.
- CAIP product examples: DP-700 / DP-600 Fabric, AI-102 / AI-3016 Azure AI Foundry, DP-100 Azure
  ML, DP-3011 / DP-203 Databricks, PL-300 Power BI, AZ-204 App Service, AZ-104 / AKS. Other
  Microsoft products (M365 Copilot, Copilot Studio, Dynamics 365, Power Platform, security) are
  fine too if the trainer asks.
- Use case options: "Derive from the meeting transcript", "Suggest common high-value ones",
  "I'll list them".
- Sources: e.g. on-prem SQL Server, Oracle Fusion / BICC CSV, SAP SuccessFactors, Salesforce,
  Excel, SharePoint. Cap at 3 by default to keep the zip small.

## Call 2: shape

| # | Header   | Question                                       | Type          |
| - | -------- | ---------------------------------------------- | ------------- |
| 6 | Modules  | Which demo modules should the kit include?     | multi-select  |
| 7 | Audience | Who is the audience and how much build time?   | single select |
| 8 | Sharing  | Internal trainer kit or shared with customer?  | single select |

Option notes:
- Modules are product-specific. Fabric: notebooks, data pipelines, metadata control tables,
  materialized lake views, warehouse, Real-Time Intelligence, Dataflow Gen2, Power BI, AI
  (Copilot, data agent, ontology), CI/CD. Foundry and other CAIP products: see the end of reference-design.md.
- Audience: architects, engineers, business, mixed class; time: 10-minute quick demo, 1-hour
  demo, half-day / full workshop.
- Sharing: "Internal trainer kit" or "Shared with the customer" (then only that customer's
  industry, and the zip gets the "General" sensitivity label).
- Don't ask for the trainer's name or email: READMEs carry no contact line or sign-off.
- Don't ask whether they want the decks: the kit, the 5-slide trainer deck and the customer-facing
  solution deck are always built together. Only skip one if the trainer says so.
- Ask (or take from the transcript) which topics the customer cares about, to pick the customer
  deck's slides: architecture, design decisions, onboarding, governance, CI/CD, migration, value.

## Defaults when the trainer skips a question

- Customer: generic, fictional organisation per industry
- Sources: 3 (on-prem DB, file drop, CRM JSON)
- Audience: mixed class, 1-hour demo
- Sharing: internal
