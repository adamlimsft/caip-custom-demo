# caip-custom-demo

A Cowork skill for Microsoft trainers teaching Cloud & AI Platforms (CAIP) courses such as
Microsoft Fabric, Azure AI Foundry, Azure Machine Learning, Databricks and Power BI.

In one run it builds:

- a customer-specific demo kit (zip): fictional messy data, config-driven modules, a README per
  module, a use-case explanation and an AI guide
- a 5-slide trainer deck that walks through the demo
- a customer-facing solution deck (architecture, design decisions, governance, CI/CD, roadmap,
  value)

Both decks use the Microsoft Learn template.

## Install

1. Download this folder (or the release zip).
2. In Cowork, add it to your skills (OneDrive `Documents/Cowork/skills/caip-custom-demo`).
3. Ask: "Create a custom Fabric demo and deck for Contoso Energy".

## What's inside

| Path                                | What it is                                   |
| ----------------------------------- | -------------------------------------------- |
| SKILL.md                            | The workflow the assistant follows           |
| references/                         | Intake, build rules, designs, deck spec      |
| scripts/check_kit.py                | Local checks for the kit and zip             |
| scripts/build_deck.py               | Trainer deck: spec to slide patches          |
| scripts/build_customer_deck.py      | Customer deck: spec to slide patches         |
| assets/ms-learn-template.pptx       | Microsoft Learn template (cover, content)    |

The template is Microsoft internal courseware branding. Share this skill inside Microsoft only.
