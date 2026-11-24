# Deck spec format (input to scripts/build_deck.py)

One JSON object. Counts in brackets are enforced; text limits are checked by the generator.

```
{
  "title":    "<Customer>: a custom <Product> demo",      cover, <= 60 chars
  "subtitle": "<short promise>",                          <= 38 chars
  "story": {
    "title":   "<the business question>",                 <= 48 chars
    "org":     "<fictional organisation>",                one line
    "problem": "<2 sentences>",
    "pains":   ["...", "...", "..."],                     [2-4] one line each
    "measure": {"value": "$2.4M", "label": "<measure> (illustrative)"},
    "proves":  ["...", "...", "..."],                     [2-4]
    "footnote": "All names and figures are fictional."    optional
  },
  "architecture": {
    "title": "...",
    "stages_label": "MEDALLION IN ONE LAKEHOUSE",         optional caps label
    "sources":   [{"name": "...", "desc": "..."}],        [2-4]
    "stages":    [{"name": "...", "desc": "..."}],        [3-5] desc <= ~55 chars
    "consumers": [{"name": "...", "desc": "..."}],        [2-4]
    "spine": {"name": "...", "desc": "..."}               optional
  },
  "moments": {
    "title": "...",
    "items": [{"tag": "Day 1", "title": "...", "desc": "...", "proves": "..."}],  [3-5]
    "takeaway": "<one line band>"                          optional
  },
  "takeaway": {
    "title": "...",
    "assets": [{"name": "15 notebooks", "desc": "..."}],  [3-6] names <= 14 chars
    "steps_label": "RUN IT",                               optional
    "steps": ["...", "...", "..."],                        [2-4]
    "outcome": "<one line, e.g. setup time>"               optional
  },
  "notes": {"cover": "", "story": "", "architecture": "", "moments": "", "takeaway": ""}
}
```

Run: `python scripts/build_deck.py <spec> --out working/<kit>/deck` (add `--check` to validate
only). Output: `deck-1-structure.json` (4 patches) and `deck-2-content.json` (about 80-100
patches), applied in that order to the seeded template copy on `live`.
