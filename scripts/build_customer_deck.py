#!/usr/bin/env python3
"""Build the CUSTOMER-FACING solution deck as live PowerPoint patches (stdlib only).

This is the second deck of a caip-custom-demo run. The trainer deck (build_deck.py) explains the
demo kit; this one shows the customer the target design the demo proves: architecture, design
decisions, data flow, governance, CI/CD, roadmap and value, in the Microsoft Learn template style.

Built on a copy of assets/ms-learn-template.pptx (slide 0 cover, 1 content, 2 closing).
Never writes a .pptx. Writes two patch files for host-EditArtifact on surface="live":

  <out>-1-structure.json  duplicate the content slide so there are N content slides + closing
  <out>-2-content.json    cover, every content slide (drawn from shapes), notes

Usage:
  python build_customer_deck.py <customer_deck_spec.json> --out working/<kit>/cust [--check]

Spec format and slide types: references/customer-deck.md.
Example: references/customer-deck-example.json.
"""
import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_deck as bd  # shared palette, helpers, fit checks and the architecture slide

from build_deck import (PUR, T1, T2, ORG, ORGT, INK, GREY, NEU, WHITE, LINE,
                        X0, XW, Y0, YB, box, txt, arrow, title, notes, need)

MAX_CONTENT = 7


def band(s, text, y=None, h=0.6):
    y = YB - h if y is None else y
    box(s, X0, y, XW, h, [text], fill=NEU, bold=True, size=14, label="band")


def bullets(items):
    return [{"text": "• " + i} for i in items]


# ---------- slide types ----------
def s_architecture(s, d):
    bd.architecture(s, d)


def s_table(s, d):
    """Decision / comparison grid: header row in purple, first column bold on a tint."""
    title(s, need(d, "title", where="table"))
    rows = need(d, "rows", list, 2, 8, "table")
    ncol = len(rows[0])
    if not 2 <= ncol <= 5:
        raise SystemExit("spec error: table needs 2-5 columns")
    widths = d.get("widths") or [XW / ncol] * ncol
    if abs(sum(widths) - XW) > 0.05:
        widths = [w * XW / sum(widths) for w in widths]
    foot = d.get("band")
    avail = YB - Y0 - (0.75 if foot else 0)
    hh = 0.5
    rh = min(0.85, (avail - hh) / (len(rows) - 1))
    y = Y0
    for r, row in enumerate(rows):
        if len(row) != ncol:
            raise SystemExit(f"spec error: table row {r} has {len(row)} cells, expected {ncol}")
        h = hh if r == 0 else rh
        x = X0
        for c, cell in enumerate(row):
            w = widths[c]
            if r == 0:
                box(s, x, y, w - 0.04, h - 0.04, [cell], fill=PUR, color=WHITE, bold=True,
                    size=14, label="table header")
            else:
                fill = T2 if c == 0 else (T1 if r % 2 else WHITE)
                box(s, x, y, w - 0.04, h - 0.04, [cell], fill=fill,
                    line=(LINE if fill == WHITE else None), bold=(c == 0), size=14 if c == 0
                    else 12, label="table cell")
            x += w
        y += h
    if foot:
        band(s, foot)


def s_process(s, d):
    """3-6 steps left to right (chevrons) with a card under each; optional band."""
    title(s, need(d, "title", where="process"))
    steps = need(d, "steps", list, 3, 6, "process")
    n = len(steps)
    gap = 0.18
    w = (XW - gap * (n - 1)) / n
    foot = d.get("band")
    bottom = min(YB - (0.8 if foot else 0), Y0 + 0.72 + 2.0)
    x = X0
    for st in steps:
        box(s, x, Y0, w, 0.62, [st["name"]], fill=PUR, color=WHITE, bold=True, size=14,
            preset="homePlate", label="step tag")
        body = [{"text": l} for l in st.get("lines", [])]
        if st.get("desc"):
            body = [{"text": st["desc"]}] + body
        box(s, x, Y0 + 0.72, w, bottom - Y0 - 0.72, body or [" "], fill=T1, size=12,
            label="step body")
        x += w + gap
    if foot:
        band(s, foot, y=bottom + 0.25, h=0.65)


def s_lanes(s, d):
    """2-4 columns (environments, workspaces, zones) with arrows between headers; optional band.

    Each lane: {"name", "sub", "items": [..]}. Good for Dev -> Test -> Prod CI/CD."""
    title(s, need(d, "title", where="lanes"))
    lanes = need(d, "lanes", list, 2, 4, "lanes")
    n = len(lanes)
    gap = 0.5 if d.get("arrows", True) else 0.25
    w = (XW - gap * (n - 1)) / n
    foot = d.get("band")
    bottom = min(YB - (1.0 if foot else 0), Y0 + 1.05 + 2.3)
    x = X0
    for i, ln in enumerate(lanes):
        head = [{"text": ln["name"], "bold": True, "sizePt": 16}]
        if ln.get("sub"):
            head.append({"text": ln["sub"], "sizePt": 12, "bold": False})
        box(s, x, Y0, w, 0.95, head, fill=PUR, color=WHITE, size=16, label="lane header")
        box(s, x, Y0 + 1.05, w, bottom - Y0 - 1.15, bullets(ln.get("items", [])), fill=T1,
            size=14, label="lane body")
        if d.get("arrows", True) and i < n - 1:
            arrow(s, x + w + 0.07, Y0 + 0.3, gap - 0.14, 0.36)
        x += w + gap
    if foot:
        box(s, X0, bottom + 0.25, XW, 0.85,
            [{"text": foot.get("name", ""), "bold": True, "sizePt": 14, "color": PUR},
             {"text": foot.get("desc", ""), "sizePt": 12, "color": INK}],
            fill=WHITE, line=PUR, size=14, label="lane band")


def s_cards(s, d):
    """3-4 cards, each a heading and 2-4 bullets. One card may be lifted ("lift": true)."""
    title(s, need(d, "title", where="cards"))
    cards = need(d, "cards", list, 2, 4, "cards")
    n = len(cards)
    gap = 0.25
    w = (XW - gap * (n - 1)) / n
    foot = d.get("band")
    bottom = min(YB - (0.8 if foot else 0), Y0 + 3.2)
    x = X0
    for c in cards:
        lift = c.get("lift")
        box(s, x, Y0, w, bottom - Y0, fill=T1, line=(ORG if lift else None))
        txt(s, x + 0.15, Y0 + 0.15, w - 0.3, 0.55, [c["name"]], size=16, bold=True, color=PUR,
            label="card title")
        if c.get("sub"):
            txt(s, x + 0.15, Y0 + 0.7, w - 0.3, 0.5, [c["sub"]], size=12, color=GREY,
                label="card sub")
        top = Y0 + (1.25 if c.get("sub") else 0.8)
        txt(s, x + 0.15, top, w - 0.3, bottom - top - 0.15, bullets(c.get("items", [])),
            size=14, label="card body")
        x += w + gap
    if foot:
        band(s, foot, y=bottom + 0.25, h=0.65)


def s_timeline(s, d):
    """3-5 phases on a rail: label above the dot, title + lines below. Good for migration."""
    title(s, need(d, "title", where="timeline"))
    ph = need(d, "phases", list, 3, 5, "timeline")
    n = len(ph)
    w = XW / n
    rail_y = Y0 + 0.95
    P = bd.P
    P.append({"op": "add_shape", "slide": s, "preset": "rect", "x": bd.E(X0 + w / 2),
              "y": bd.E(rail_y - 0.02), "cx": bd.E(XW - w), "cy": bd.E(0.04), "fill": PUR,
              "line": PUR})
    foot = d.get("band")
    bottom = min(YB - (0.8 if foot else 0), rail_y + 0.4 + 2.0)
    for i, p in enumerate(ph):
        cx = X0 + w * i + w / 2
        txt(s, X0 + w * i + 0.1, Y0, w - 0.2, 0.55, [p.get("when", "")], size=12, bold=True,
            color=ORGT, align="center", label="phase when")
        box(s, cx - 0.17, rail_y - 0.17, 0.34, 0.34, fill=(ORG if p.get("now") else PUR),
            preset="ellipse")
        box(s, X0 + w * i + 0.1, rail_y + 0.4, w - 0.2, bottom - rail_y - 0.4,
            [{"text": p["name"], "bold": True, "sizePt": 16, "color": PUR}]
            + [{"text": l, "sizePt": 12} for l in p.get("lines", [])],
            fill=T1, size=14, label="phase card")
    if foot:
        band(s, foot, y=bottom + 0.25, h=0.65)


def s_value(s, d):
    """Value and next steps: big measure tile, 3-4 outcomes, next-step band."""
    title(s, need(d, "title", where="value"))
    m = need(d, "measure", where="value")
    outs = need(d, "outcomes", list, 2, 4, "value")
    lw = 4.3
    box(s, X0, Y0, lw, 2.2, [{"text": m["value"], "sizePt": 40, "bold": True},
                             {"text": m["label"], "sizePt": 14}],
        fill=PUR, color=WHITE, label="value tile")
    txt(s, X0, Y0 + 2.35, lw, 1.3, [d.get("footnote", "Illustrative estimate from the "
                                          "demo's fictional data, not a forecast.")],
        size=12, color=GREY, label="value footnote")
    rx, rw = X0 + lw + 0.35, XW - lw - 0.35
    nxt = d.get("next")
    bottom = YB - (0.95 if nxt else 0)
    oh = (bottom - Y0) / len(outs)
    y = Y0
    for o in outs:
        box(s, rx, y, rw, oh - 0.15,
            [{"text": o["name"], "bold": True, "sizePt": 16, "color": PUR},
             {"text": o.get("desc", ""), "sizePt": 14}], fill=T1, size=14, label="outcome")
        y += oh
    if nxt:
        box(s, X0, YB - 0.8, XW, 0.8, [nxt], fill=WHITE, line=ORG, bold=True, size=14,
            label="next step")


TYPES = {"architecture": s_architecture, "table": s_table, "process": s_process,
         "lanes": s_lanes, "cards": s_cards, "timeline": s_timeline, "value": s_value}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("spec")
    ap.add_argument("--out", default="working/cust")
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args()
    spec = json.load(open(a.spec, encoding="utf-8"))
    need(spec, "title")
    need(spec, "subtitle")
    slides = need(spec, "slides", list, 3, MAX_CONTENT)
    bd.cover(spec)
    for i, sl in enumerate(slides, start=1):
        t = sl.get("type")
        if t not in TYPES:
            raise SystemExit(f"spec error: slide {i} type '{t}' not one of {sorted(TYPES)}")
        TYPES[t](i, sl)
        notes(i, sl.get("notes", ""))
    closing = len(slides) + 1
    notes(closing, spec.get("closing_notes", "Questions, then agree the next step."))
    fails = [w for w in bd.WARN if w.startswith("FAIL")]
    for w in bd.WARN:
        print(w)
    if a.check:
        print("OK" if not fails else f"{len(fails)} problem(s)")
        sys.exit(1 if fails else 0)
    if fails:
        print("Fix the spec (shorter text) before building.")
        sys.exit(1)
    structure = [{"op": "duplicate_slide", "slide": 1, "position": 2}
                 for _ in range(len(slides) - 1)]
    json.dump(structure, open(a.out + "-1-structure.json", "w"), indent=0)
    json.dump(bd.P, open(a.out + "-2-content.json", "w"), indent=0)
    print(f"wrote {a.out}-1-structure.json ({len(structure)} patches) and "
          f"{a.out}-2-content.json ({len(bd.P)} patches); deck = cover + {len(slides)} + closing")
    if len(bd.P) > 200:
        print("FAIL: content batch over 200 patches; split it at a slide boundary or trim the spec")
        sys.exit(1)


if __name__ == "__main__":
    main()
