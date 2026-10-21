#!/usr/bin/env python3
"""Find inspected figure references without loading every atlas into context.

Examples:
  python reference_catalog.py stats
  python reference_catalog.py search --query "feedback loop" --since 2025
  python reference_catalog.py search --company NVIDIA --limit 5
  python reference_catalog.py show qwen38-next --figure "Figure 1"

The search is a transparent lexical lookup, not a scientific quality ranking.
Sources keep their original evidence categories. No observations are inferred.
"""
from __future__ import annotations

import argparse
from collections import Counter
import json
from pathlib import Path
import re
import sys
from urllib.parse import urlsplit, urlunsplit


INDEX_NAMES = (
    "source-index.json", "modern-source-index.json", "recent-expansion-index.json",
    "dense-expansion-index.json",
)
COMPANIES = (
    ("OpenAI", ("openai",)),
    ("Anthropic", ("anthropic",)),
    ("Google / DeepMind", ("google", "deepmind", "gemini team")),
    ("Meta / FAIR", ("meta", "facebook", "fair at")),
    ("NVIDIA", ("nvidia",)),
    ("DeepSeek", ("deepseek",)),
    ("Tencent", ("tencent", "hunyuan")),
    ("Alibaba / Qwen", ("alibaba", "qwen")),
    ("Microsoft Research", ("microsoft",)),
)


def words(value):
    return re.findall(r"[\w]+", str(value).casefold())


def canonical_source(paper):
    """Identify an underlying paper across arXiv versions or official URLs."""
    for key in ("arxiv_id", "arxiv_version", "primary_pdf_url", "pdf_url", "abs_url", "landing_url"):
        found = re.search(r"(?<!\d)(\d{4}\.\d{4,5})(?:v\d+)?", str(paper.get(key, "")))
        if found:
            return "arxiv:" + found.group(1)
    url = next((paper[k] for k in ("canonical_url", "landing_url", "abs_url", "source_url", "pdf_url", "primary_pdf_url") if paper.get(k)), None)
    if not url:
        raise ValueError(f"Source URL missing for {paper.get('id', paper.get('paper_id'))}")
    parts = urlsplit(url)
    return urlunsplit((parts.scheme.lower(), parts.netloc.lower(), parts.path.rstrip("/"), "", ""))


def primary_company(paper):
    raw = paper.get("primary_company") or paper.get("organizations") or paper.get("organization", "")
    text = " ".join(raw) if isinstance(raw, list) else str(raw)
    for name, needles in COMPANIES:
        if any(needle in text.casefold() for needle in needles):
            return name
    return text or "Unspecified"


def figure_anchor(figure):
    anchor = figure.get("anchor") or figure.get("figure_id") or figure.get("descriptive_anchor")
    if anchor is None:
        raise ValueError("A figure is missing its source anchor")
    return str(anchor)


def figure_identity(figure):
    anchor = figure_anchor(figure).strip()
    # "1" and "Figure 1" are the same anchor; separate panels are not extra figures.
    numbered = re.fullmatch(r"(?:fig(?:ure)?\.?\s*)?([A-Z]?\d+)", anchor, re.I)
    return ("figure:" + numbered.group(1).casefold()) if numbered else anchor.casefold()


def matches_figure(figure, requested):
    """Accept a full anchor, a figure number, or the exact native asset stem."""
    if figure_identity(figure) == figure_identity({"anchor": requested}):
        return True
    asset_url = figure.get("asset_url")
    return bool(asset_url and Path(urlsplit(asset_url).path).stem.casefold() == requested.casefold())


def load_corpus(root):
    records, identities, identifiers = [], {}, set()
    for filename in INDEX_NAMES:
        path = root / filename
        if not path.exists():
            if filename == "recent-expansion-index.json":
                continue
            raise ValueError(f"Required reference index not found: {path}")
        data = json.loads(path.read_text(encoding="utf-8"))
        for original in data["papers"]:
            identifier = original.get("id", original.get("paper_id"))
            if not identifier or identifier in identifiers:
                raise ValueError(f"Missing or duplicate paper ID: {identifier}")
            identity = canonical_source(original)
            if identity in identities:
                raise ValueError(f"Duplicate paper across indexes: {identifier} and {identities[identity]} ({identity})")
            figures = original.get("figures", [])
            anchors = [figure_identity(f) for f in figures]
            if len(set(anchors)) != len(anchors):
                raise ValueError(f"Repeated figure anchor in {identifier}")
            record = {
                "id": identifier,
                "title": original["title"],
                "year": int(original.get("year", original.get("original_year"))),
                "company": primary_company(original),
                "canonical_source": identity,
                "source_index": filename,
                "landing_url": original.get("landing_url") or original.get("abs_url") or original.get("source_url") or original.get("pdf_url") or original.get("primary_pdf_url"),
                "figures": figures,
                "record": original,
            }
            records.append(record)
            identifiers.add(identifier)
            identities[identity] = identifier
    return records


def stats(records):
    years = Counter(p["year"] for p in records)
    companies = sorted(set(p["company"] for p in records))
    return {
        "papers": len(records),
        "figure_anchors": sum(len(p["figures"]) for p in records),
        "papers_by_year": dict(sorted(years.items())),
        "company_counts": [{
            "company": c,
            "papers": sum(p["company"] == c for p in records),
            "papers_since_2025": sum(p["company"] == c and p["year"] >= 2025 for p in records),
            "figure_anchors": sum(len(p["figures"]) for p in records if p["company"] == c),
        } for c in companies],
        "counting_policy": "Each canonical paper and each numbered/descriptive figure anchor is counted once. Panels are not counted separately. Company counts use the primary corporate family; collaborations are not double-counted.",
        "qualification": "Counts describe the curated source records. They do not establish venue acceptance or independently verify a record's inspection claim.",
    }


def search(records, *, query="", company=None, since=None, family=None, limit=8):
    tokens = words(query)
    hits = []
    for paper in records:
        if since is not None and paper["year"] < since:
            continue
        if company and company.casefold() not in paper["company"].casefold():
            continue
        for figure in paper["figures"]:
            families = figure.get("family", figure.get("figure_family", paper["record"].get("figure_families", [])))
            if family and family.casefold() not in str(families).casefold():
                continue
            haystack = json.dumps({"title": paper["title"], "figure": figure, "families": families}, ensure_ascii=False).casefold()
            counts = Counter(words(haystack))
            score = sum(min(counts[t], 5) for t in tokens)
            if tokens and score == 0:
                continue
            if query and query.casefold() in haystack:
                score += 5
            hits.append({
                "paper_id": paper["id"], "title": paper["title"],
                "company": paper["company"], "year": paper["year"],
                "figure": figure_anchor(figure),
                "figure_title": figure.get("title", figure.get("descriptive_anchor")),
                "pdf_page": figure.get("pdf_page", figure.get("pdf_page_1based")),
                "family": families or None,
                "source_index": paper["source_index"], "source_url": paper["landing_url"],
                "lexical_score": score,
            })
    hits.sort(key=lambda h: (-h["lexical_score"], -h["year"], h["paper_id"], h["figure"]))
    return hits[:limit]


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--references", type=Path, default=Path(__file__).resolve().parents[1] / "references")
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("stats", help="Audit distinct source and figure counts")
    finder = commands.add_parser("search", help="Find figure-level source anchors")
    finder.add_argument("--query", default="")
    finder.add_argument("--company")
    finder.add_argument("--since", type=int)
    finder.add_argument("--family")
    finder.add_argument("--limit", type=int, default=8)
    show = commands.add_parser("show", help="Return one complete source record or figure")
    show.add_argument("paper_id")
    show.add_argument("--figure")
    args = parser.parse_args()
    try:
        corpus = load_corpus(args.references)
        if args.command == "stats":
            result = stats(corpus)
        elif args.command == "search":
            if not 1 <= args.limit <= 100:
                raise ValueError("--limit must be from 1 to 100")
            result = search(corpus, query=args.query, company=args.company, since=args.since, family=args.family, limit=args.limit)
        else:
            paper = next((p for p in corpus if p["id"] == args.paper_id), None)
            if paper is None:
                raise ValueError(f"Unknown paper ID: {args.paper_id}")
            result = paper["record"]
            if args.figure:
                matches = [f for f in paper["figures"] if matches_figure(f, args.figure)]
                if not matches:
                    raise ValueError(f"Figure {args.figure!r} not found in {args.paper_id}")
                result = {"paper_id": paper["id"], "title": paper["title"], "source_index": paper["source_index"], "source_url": paper["landing_url"], "figure": matches[0]}
        print(json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False))
    except (ValueError, KeyError, OSError) as exc:
        print(f"reference_catalog: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
