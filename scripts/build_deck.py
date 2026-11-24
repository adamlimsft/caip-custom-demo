#!/usr/bin/env python3
"""Build the 5-slide "explain the custom demo" deck as live PowerPoint patches (stdlib only).

The deck is built on a copy of assets/ms-learn-template.pptx (Microsoft Learn template:
slide 0 cover, slide 1 content "Blank_with Head", slide 2 closing). This script never writes a
.pptx. It writes two patch files for host-EditArtifact on surface="live":

  <out>-1-structure.json  duplicate the content slide 3x, drop the closing slide (5 slides)
  <out>-2-content.json    cover text + 4 content slides drawn from shapes, plus speaker notes

Usage:
  python build_deck.py <deck_spec.json> --out working/deck   [--check]

--check only validates the spec and reports text-fit problems (exit 1 on any FAIL).
Spec format: references/deck-spec.md.  Example: references/deck-spec-example.json.
"""
import argparse
import json
import sys

E = lambda v: int(round(v * 914400))  # inches -> EMU

# Microsoft Learn template palette (purple family) and Segoe UI, as used in the template.
PUR, T1, T2 = "702573", "F5EDF5", "E8D3E9"
ORG, ORGT = "FE5B38", "B3360F"
INK, GREY, NEU, WHITE, LINE = "1F1F1F", "595959", "F2F0ED", "FFFFFF", "D9D9D9"
STAGE_FILLS = ["EEEAE5", "EAD7EB", "C995CB", PUR, "5A1D5C"]
FONT = "Segoe UI"
CW = 0.60  # average character width factor for Segoe UI (renders wider in LibreOffice)

P, WARN = [], []


# ---------- low-level helpers ----------
def _paras(paras, size, bold, color):
    out = []
    for p in paras:
        if isinstance(p, str):
            p = {"text": p}
        out.append({"text": p["text"], "sizePt": p.get("sizePt", size),
                    "bold": p.get("bold", bold), "color": p.get("color", color)})
    return out


def _fit(slide, w, h, paras, label):
    """Estimate wrapped height; warn when text would overflow its box or a word is too long."""
    avail = (w - 0.2) * 72
    tot = 0.12
    for p in paras:
        sz = p["sizePt"]
        if sz < 12:
            WARN.append(f"FAIL slide {slide}: {sz}pt is under the 12pt floor ({label})")
        cw = sz * CW * (1.07 if p["bold"] else 1)
        lines, cur = 1, 0
        for wd in p["text"].split(" "):
            L = len(wd) * cw
            if L > avail:
                WARN.append(f"FAIL slide {slide}: word too long '{wd}' ({label})")
            if cur == 0:
                cur = L
            elif cur + cw + L <= avail:
                cur += cw + L
            else:
                lines += 1
                cur = L
        tot += lines * sz * 1.2 / 72
    if tot > h + 0.01:
        WARN.append(f"FAIL slide {slide}: text overflows ({label}): needs {tot:.2f}in, "
                    f"box is {h:.2f}in :: '{paras[0]['text'][:40]}'")


def box(s, x, y, w, h, paras=None, fill=None, line=None, size=14, bold=False, color=INK,
        align="left", preset="rect", label="box"):
    op = {"op": "add_shape", "slide": s, "preset": preset, "x": E(x), "y": E(y),
          "cx": E(w), "cy": E(h)}
    if fill:
        op["fill"] = fill
    if line:
        op["line"] = line
        op["lineWidth"] = 12700
    elif fill:
        op["line"] = fill
    if paras:
        pp = _paras(paras, size, bold, color)
        op.update({"paragraphs": pp, "fontFamily": FONT, "align": align, "color": color,
                   "sizePt": size})
        _fit(s, w, h, pp, label)
    P.append(op)


def txt(s, x, y, w, h, paras, size=14, bold=False, color=INK, align="left", label="text"):
    pp = _paras(paras, size, bold, color)
    _fit(s, w, h, pp, label)
    P.append({"op": "add_text_box", "slide": s, "x": E(x), "y": E(y), "cx": E(w), "cy": E(h),
              "paragraphs": pp, "fontFamily": FONT, "align": align, "color": color,
              "sizePt": size})


def arrow(s, x, y, w, h, d="right", color=GREY):
    pre = {"right": "rightArrow", "down": "downArrow"}[d]
    P.append({"op": "add_shape", "slide": s, "preset": pre, "x": E(x), "y": E(y),
              "cx": E(w), "cy": E(h), "fill": color, "line": color})


def title(s, t):
    if len(t) > 48:
        WARN.append(f"FAIL slide {s}: title over 48 characters, it will wrap: '{t}'")
    P.append({"op": "set_text", "slide": s, "shape": 0, "paragraph": 0, "run": 0, "text": t,
              "keepFormat": True})


def notes(s, t):
    if t:
        P.append({"op": "set_notes", "slide": s, "text": t})


def need(d, key, kind=None, lo=None, hi=None, where="spec"):
    if key not in d:
        raise SystemExit(f"spec error: '{key}' missing in {where}")
    v = d[key]
    if kind is list and lo is not None and not (lo <= len(v) <= hi):
        raise SystemExit(f"spec error: '{key}' in {where} needs {lo}-{hi} items, has {len(v)}")
    return v


# ---------- slides ----------
X0, XW = 0.62, 12.08          # content left edge and width (inches); slide is 13.333 x 7.5
Y0, YB = 1.45, 6.50           # content top and bottom (title sits above, footer below)


def cover(spec):
    P.append({"op": "set_text", "slide": 0, "shape": 0, "paragraph": 0, "run": 0,
              "text": spec["title"], "keepFormat": True})
    P.append({"op": "set_text", "slide": 0, "shape": 1, "paragraph": 0, "run": 0,
              "text": spec["subtitle"], "keepFormat": True})
    if len(spec["title"]) > 60:
        WARN.append("FAIL slide 0: cover title over 60 characters")
    if len(spec["subtitle"]) > 38:
        WARN.append("FAIL slide 0: cover subtitle over 38 characters, it will wrap")
    notes(0, spec.get("notes", {}).get("cover", ""))


def story(s, st):
    """Slide 1: the challenge (left) and what the demo proves (right)."""
    title(s, need(st, "title", where="story"))
    pains = need(st, "pains", list, 2, 4, "story")
    proves = need(st, "proves", list, 2, 4, "story")
    m = need(st, "measure", where="story")
    # left card
    lw = 5.75
    box(s, X0, Y0, lw, 0.5, ["THE CHALLENGE"], fill=PUR, color=WHITE, bold=True, size=14,
        label="challenge header")
    box(s, X0, Y0 + 0.5, lw, YB - Y0 - 0.5, fill=T1)
    txt(s, X0 + 0.15, Y0 + 0.65, lw - 0.3, 0.45, [need(st, "org", where="story")], size=16,
        bold=True, color=PUR, label="org")
    txt(s, X0 + 0.15, Y0 + 1.15, lw - 0.3, 1.25, [need(st, "problem", where="story")], size=14,
        label="problem")
    py, ph = Y0 + 2.5, (YB - Y0 - 2.6) / len(pains)
    for p in pains:
        box(s, X0 + 0.2, py + ph / 2 - 0.07, 0.14, 0.14, fill=ORG)
        txt(s, X0 + 0.45, py, lw - 0.6, ph, [p], size=14, label="pain")
        py += ph
    # right column
    rx, rw = X0 + lw + 0.35, XW - lw - 0.35
    box(s, rx, Y0, rw, 1.55, [{"text": m["value"], "sizePt": 36, "bold": True},
                              {"text": m["label"], "sizePt": 14}],
        fill=PUR, color=WHITE, label="measure tile")
    txt(s, rx, Y0 + 1.7, rw, 0.4, ["WHAT THE DEMO PROVES"], size=12, bold=True, color=PUR,
        label="proves header")
    gy, gh = Y0 + 2.15, (YB - (Y0 + 2.15) - 0.45) / len(proves)
    for i, p in enumerate(proves):
        box(s, rx, gy, 0.55, gh - 0.1, [str(i + 1)], fill=PUR, color=WHITE, bold=True,
            size=16, align="center", label="proof number")
        box(s, rx + 0.6, gy, rw - 0.6, gh - 0.1, [p], fill=WHITE, line=LINE, size=14,
            label="proof")
        gy += gh
    txt(s, rx, YB - 0.4, rw, 0.4, [st.get("footnote", "All names and figures are fictional.")],
        size=12, color=GREY, label="footnote")


def architecture(s, a):
    """Slide 2: sources -> product stages -> consumers, with the control/metadata spine."""
    title(s, need(a, "title", where="architecture"))
    src = need(a, "sources", list, 2, 4, "architecture")
    stg = need(a, "stages", list, 3, 5, "architecture")
    con = need(a, "consumers", list, 2, 4, "architecture")
    cw, aw = 2.0, 0.38
    sx, cx = X0, X0 + XW - cw
    mx0, mx1 = sx + cw + aw + 0.12, cx - aw - 0.12
    head_h = 0.4
    txt(s, sx, Y0, cw, head_h, ["SOURCES"], size=12, bold=True, color=GREY, label="src hdr")
    txt(s, mx0, Y0, mx1 - mx0, head_h, [a.get("stages_label", "THE DEMO BUILD")], size=12,
        bold=True, color=GREY, label="stage hdr")
    txt(s, cx, Y0, cw, head_h, ["WHO USES IT"], size=12, bold=True, color=GREY, label="con hdr")
    top = Y0 + head_h + 0.1
    spine = a.get("spine")
    bottom = YB - (1.05 if spine else 0)

    def column(items, x):
        h = (bottom - top) / len(items)
        y = top
        for it in items:
            box(s, x, y, cw, h - 0.12, [{"text": it["name"], "bold": True, "sizePt": 14},
                                        {"text": it.get("desc", ""), "sizePt": 12}],
                fill=NEU, size=14, label="column card")
            y += h
    column(src, sx)
    column(con, cx)
    mid = (top + bottom) / 2
    arrow(s, sx + cw + 0.06, mid - 0.22, aw, 0.44)
    arrow(s, cx - aw - 0.06, mid - 0.22, aw, 0.44)
    n = len(stg)
    gap = 0.3
    w = (mx1 - mx0 - gap * (n - 1)) / n
    x = mx0
    for i, it in enumerate(stg):
        f = STAGE_FILLS[min(i + (5 - n), 4)] if n < 5 else STAGE_FILLS[i]
        dark = f in (PUR, "5A1D5C")
        box(s, x, top, w, 0.6, [it["name"]], fill=f, color=(WHITE if dark else INK),
            bold=True, size=14, label="stage header")
        box(s, x, top + 0.65, w, bottom - top - 0.75, [it.get("desc", "")], fill=T1, size=12,
            label="stage body")
        if i < n - 1:
            arrow(s, x + w + 0.03, top + 0.16, gap - 0.06, 0.28)
        x += w + gap
    if spine:
        box(s, mx0, YB - 0.9, mx1 - mx0, 0.9,
            [{"text": spine["name"], "bold": True, "sizePt": 14, "color": PUR},
             {"text": spine.get("desc", ""), "sizePt": 12, "color": INK}],
            fill=WHITE, line=PUR, size=14, label="spine")


def moments(s, mo):
    """Slide 3: the demo moments, left to right, each with what it proves."""
    title(s, need(mo, "title", where="moments"))
    items = need(mo, "items", list, 3, 5, "moments")
    n = len(items)
    gap = 0.22
    w = (XW - gap * (n - 1)) / n
    band = mo.get("takeaway")
    bottom = YB - (0.85 if band else 0)
    x = X0
    for it in items:
        box(s, x, Y0, w, 0.62, [it["tag"]], fill=PUR, color=WHITE, bold=True, size=14,
            preset="homePlate", label="moment tag")
        box(s, x, Y0 + 0.72, w, bottom - Y0 - 0.72, fill=T1)
        txt(s, x + 0.1, Y0 + 0.82, w - 0.2, 0.85, [it["title"]], size=16, bold=True,
            color=PUR, label="moment title")
        txt(s, x + 0.1, Y0 + 1.72, w - 0.2, bottom - Y0 - 2.75, [it["desc"]], size=14,
            label="moment desc")
        txt(s, x + 0.1, bottom - 0.98, w - 0.2, 0.88,
            [{"text": "PROVES", "sizePt": 12, "bold": True, "color": ORGT},
             {"text": it["proves"], "sizePt": 12}], size=12, label="moment proves")
        x += w + gap
    if band:
        box(s, X0, YB - 0.7, XW, 0.7, [band], fill=WHITE, line=ORG, bold=True, size=14,
            label="takeaway band")


def takeaway(s, t):
    """Slide 4: what is in the kit (left), how to run it (right), outcome band (bottom)."""
    title(s, need(t, "title", where="takeaway"))
    assets = need(t, "assets", list, 3, 6, "takeaway")
    steps = need(t, "steps", list, 2, 4, "takeaway")
    out = t.get("outcome")
    bottom = YB - (0.85 if out else 0)
    lw = 7.1
    txt(s, X0, Y0, lw, 0.4, ["IN THE KIT"], size=12, bold=True, color=GREY, label="kit hdr")
    cols = 2 if len(assets) <= 4 else 3
    rows = (len(assets) + cols - 1) // cols
    gw = 0.18
    tw = (lw - gw * (cols - 1)) / cols
    th = min(1.25, (bottom - (Y0 + 0.5) - gw * (rows - 1)) / rows)
    for i, a in enumerate(assets):
        r, c = divmod(i, cols)
        box(s, X0 + c * (tw + gw), Y0 + 0.5 + r * (th + gw), tw, th,
            [{"text": a["name"], "bold": True, "sizePt": 14, "color": PUR},
             {"text": a.get("desc", ""), "sizePt": 12, "color": INK}],
            fill=T1, size=14, label="kit tile")
    rx, rw = X0 + lw + 0.4, XW - lw - 0.4
    txt(s, rx, Y0, rw, 0.4, [t.get("steps_label", "RUN IT")], size=12, bold=True,
        color=GREY, label="steps hdr")
    sh = min(1.0, (bottom - (Y0 + 0.5)) / len(steps))
    y = Y0 + 0.5
    for i, st in enumerate(steps):
        box(s, rx, y + 0.08, 0.56, 0.56, [str(i + 1)], fill=PUR, color=WHITE, bold=True,
            size=14, align="center", preset="ellipse", label="step number")
        txt(s, rx + 0.7, y, rw - 0.7, sh - 0.1, [st], size=14, label="step")
        y += sh
    if out:
        box(s, X0, YB - 0.7, XW, 0.7, [out], fill=PUR, color=WHITE, bold=True, size=14,
            label="outcome")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("spec")
    ap.add_argument("--out", default="working/deck")
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args()
    spec = json.load(open(a.spec, encoding="utf-8"))
    for k in ("title", "subtitle", "story", "architecture", "moments", "takeaway"):
        need(spec, k)
    cover(spec)
    story(1, spec["story"])
    architecture(2, spec["architecture"])
    moments(3, spec["moments"])
    takeaway(4, spec["takeaway"])
    nt = spec.get("notes", {})
    for i, k in enumerate(("story", "architecture", "moments", "takeaway"), start=1):
        notes(i, nt.get(k, ""))
    fails = [w for w in WARN if w.startswith("FAIL")]
    for w in WARN:
        print(w)
    if a.check:
        print("OK" if not fails else f"{len(fails)} problem(s)")
        sys.exit(1 if fails else 0)
    if fails:
        print("Fix the spec (shorter text) before building.")
        sys.exit(1)
    structure = [{"op": "duplicate_slide", "slide": 1, "position": 2} for _ in range(3)]
    structure.append({"op": "delete_slide", "slide": 2})  # pre-batch index 2 = closing slide
    json.dump(structure, open(a.out + "-1-structure.json", "w"), indent=0)
    json.dump(P, open(a.out + "-2-content.json", "w"), indent=0)
    print(f"wrote {a.out}-1-structure.json ({len(structure)} patches) and "
          f"{a.out}-2-content.json ({len(P)} patches)")
    if len(P) > 200:
        print("FAIL: content batch over 200 patches; cut items from the spec")
        sys.exit(1)


if __name__ == "__main__":
    main()
