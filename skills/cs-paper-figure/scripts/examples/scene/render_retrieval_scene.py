#!/usr/bin/env python3
"""A motivating example drawn as a scene, not a table (140 mm): which passage does each retriever rank first?

Illustrative schematic, written for this skill: a keyword retriever ranks first the passage that repeats
the question's words; the retriever that reads meaning ranks first the passage that answers it. No scores
are shown, only which passage each system ranks first, so nothing here can be read as a measurement.

Register: example-led text, the "motivating example" family (references/registers.md §3).
  * Message: shared words win the keyword retriever; the answer wins ours.
  * Picture: the user asks the question in a bubble; three passage cards lie side by side on one tray; a
    grey thread drops from the shared words to the card the keyword retriever ranks first (cross); a blue
    thread drops from what is asked to the card ours ranks first (tick). The threads landing on different
    cards is the figure. As a table this would be three rows and two rank columns, and the reason for
    each rank, which is the claim, would be gone.
  * Hero: the answering passage, the only blue object (ring, name tab, thread, span).
  * One hue (blue = ours and the relation it follows); the baseline and the words it matches are grey; the
    cross is the only red. Cards are drawn once, ordered so the threads do not cross.
  * Two text sizes (8.0 pt example text, 6.8 pt tabs, tags and thread labels); two strokes (0.55 pt
    outlines, 1.0 pt threads and rings). No arrows: a thread is a relation, with a dot at each end.
"""
import argparse
import os
import sys

from matplotlib.patches import Circle, FancyBboxPatch

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
from paperkit import PT_PER_MM, ROLE, Canvas  # noqa: E402

STEM = "retrieval_scene"
W, M = 140.0, 1.0
TEXT, FINE = 8.0, 6.8
THIN, BOLD = 0.55, 1.0
GREY = dict(soft="#DCE0E6", mark="#6B7480", ink="#3A4250")
OURS = ROLE["blue"]
BAD, TRAY, INK = ROLE["coral"]["mark"], "#E6E8EC", "#000000"
LH = 1.2 * TEXT / PT_PER_MM

# tag "K" = words the question and a passage share; tag "A" = what is asked and what answers it
QUESTION = [("Blade Runner", "K"), (" is based on a novel. ", None), ("Who wrote it?", "A")]
PASSAGES = [  # left to right in the order of the question's spans, so that the two threads do not cross
    dict(text=[("Blade Runner", "K"), (" is a 1982 science-fiction film directed by Ridley Scott.", None)],
         pick="K", tag="no answer"),
    dict(text=[("Ridley Scott also directed Alien, released in 1979.", None)], pick=None, tag="no answer"),
    dict(text=[("Philip K. Dick wrote", "A"), (" Do Androids Dream of Electric Sheep? in 1968; it was filmed"
               " in 1982.", None)], pick="A", tag="answers the question"),
]
SYSTEMS = {"K": ("Keyword: rank 1", GREY, "shares words", False),
           "A": ("Ours: rank 1", OURS, "answers it", True)}


def segs(parts, on):
    return [(t, INK, "normal", SYSTEMS[k][1]["soft"] if k and k in on else None) for t, k in parts]


def name_tab(cv, xr, y, key):
    """The system's name on the card it ranks first: a solid pill on the top border, its verdict inside."""
    name, hue, _, ok = SYSTEMS[key]
    h, w = 3.7, cv.text_width(name, FINE, "bold") + 5.9
    cv.ax.add_patch(FancyBboxPatch((xr - w, y - h / 2), w, h, boxstyle=f"round,pad=0,rounding_size={h / 2}",
                                   fc=hue["mark"], ec="none", zorder=10))
    cv.ax.add_patch(Circle((xr - w + 1.85, y), 1.35, fc="white", ec="none", zorder=11))
    (cv.icon_check if ok else cv.icon_cross)(xr - w + 1.85, y, 1.6, color=hue["mark"] if ok else BAD, lw=BOLD)
    cv.text(xr - w + 4.2, y - 0.05, name, size=FINE, ha="left", color="white", weight="bold")


def build():
    card_w, gap, pad, lines = (W - 2 * M - 2 * 2.2 - 2 * 2.8) / 3, 2.8, 1.9, 3
    card_h = 3.1 + lines * LH + 3.4
    bub_h, zone, tray_pt, tray_pb = LH + 3.5, 9.0, 3.7, 3.0
    H = M + bub_h + zone + tray_pt + card_h + tray_pb + M
    cv = Canvas(W, H, family="serif", size=TEXT)

    # the question, said once by the user
    q = segs(QUESTION, on=("K", "A"))
    qw = sum(cv.text_width(t, TEXT) for t, *_ in q)
    bx, cy = (W - qw) / 2, H - M - bub_h / 2
    cv.icon_user(bx - 8.5, cy + 0.2, 4.6, color="#4A4F57", lw=THIN)
    cv.bubble(bx + qw / 2, cy, "", tail=(bx - 5.6, cy), w=qw + 5.4, h=bub_h, size=TEXT)
    cv.rich(bx, cy, q, size=TEXT)
    asked = {SPAN: s for s, SPAN in zip(list(cv.spans), ("K", "A"))}

    # the store: one tray, three cards, drawn once
    ty = M
    cv.box(M, ty, W - 2 * M, tray_pt + card_h + tray_pb, fill=TRAY, stroke="none", lw=0, radius=2.6, z=1,
           container=True)
    top = ty + tray_pb + card_h
    for i, p in enumerate(PASSAGES):
        x = M + 2.2 + i * (card_w + gap)
        hue = SYSTEMS[p["pick"]][1] if p["pick"] else None
        cv.box(x, top - card_h, card_w, card_h, fill="white", stroke=hue["mark"] if hue else "none",
               lw=BOLD if hue else 0, radius=1.6, z=3)
        k = len(cv.spans)
        cv.para(x + pad, top - 3.1, card_w - 2 * pad, segs(p["text"], on=(p["pick"],)), size=TEXT)
        cv.chip(x + card_w - 2.6, top - card_h, p["tag"], dict(fill="white", soft="white", stroke="#8C95A1",
                ink="#3A4250", mark="#262B33"), size=FINE, h=3.3, solid=p["pick"] == "A", ha="right", lw=THIN)
        if not p["pick"]:
            continue
        name_tab(cv, x + card_w - 2.6, top, p["pick"])
        # the relation the claim is about: from the span in the question to the span on the card it explains
        _, a0, a1, ay = asked[p["pick"]]
        _, b0, b1, by = cv.spans[k]
        p0, p1 = ((a0 + a1) / 2, ay - LH / 2), ((b0 + b1) / 2, by + LH / 2)
        cv.thread(p0, p1, color=hue["mark"], lw=BOLD, z=16)      # above the bubble, so it starts on the span
        # the label sits on the side the curve does not sweep through
        cv.text((p0[0] if p1[0] < p0[0] else (p0[0] + p1[0]) / 2) + 2.2, top + tray_pt + zone / 2,
                SYSTEMS[p["pick"]][2], size=FINE,
                style="italic", color=hue["ink"], ha="left", weight="bold" if p["pick"] == "A" else "normal")
    cv.text(M + 2.2 + 1.5 * card_w + gap, top + 1.9, "indexed passages", size=FINE, color="#6B7480",
            style="italic")

    assert [p["pick"] for p in PASSAGES].count("A") == 1 and [p["pick"] for p in PASSAGES].count("K") == 1
    assert not cv.overlaps(), cv.overlaps()
    assert not cv.text_overlaps(), cv.text_overlaps()
    return cv


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--out", default="figures/scene")
    print(build().save(os.path.join(ap.parse_args().out, STEM)))
