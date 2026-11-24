# README style

## Voice

- Write in the trainer's own first-person voice: plain, practical, short sentences.
- Not AI-sounding. Avoid phrases like "seamlessly", "leverage", "robust", "dive into",
  "comprehensive", "elevate", "unlock", "in today's fast-paced world".
- Never write "I've checked everything I can without a capacity" or claim testing that didn't
  happen. Only describe checks that actually ran (e.g. "the SQL runs in SQLite").

## Header (every README and every AI guide)

Start with the H1 and go straight into the content. Each trainer builds the kit for themselves, so:

- Do NOT add a contact/intro line under the H1, such as "If you'd like a hand setting this up...
  feel free to email/message me (<name> <email>). I'm happy to walk you through it...".
- No trainer name or email anywhere in the READMEs or AI guides.

## Tables

- 5 columns or fewer, short cells, no empty header cells.
- A blank line before every table.
- Pad columns so they line up in plain-text editors too.
- Move long explanations into bullet lists under the table.

Example:

```
| Symptom             | Likely cause          | Fix                        |
| ------------------- | --------------------- | -------------------------- |
| Pipeline fails      | Wrong lakehouse name  | Update config, rerun       |
| No rows in silver   | Watermark too new     | Reset watermark (below)    |
```

## Main README must include

- Troubleshooting table (symptom, likely cause, fix).
- Reset steps (numbered: clear tables, reset watermarks, rerun generator).
- A note that all organisations, people and identifiers are fictional.

## Closing note (main README, last section)

Short, honest and neutral, for example:

```
## Before you present

The product UI and previews change often, so do a dry run in your own tenant before you present,
and expect to fix the odd small thing.
```

- Do NOT end any README with a help offer ("If you hit something, let me know and I'm happy to
  help") or a personal sign-off (name / title, e.g. "<Name>, <Title>, Microsoft").
