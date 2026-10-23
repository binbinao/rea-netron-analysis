#!/usr/bin/env python3
"""Summarize a REA JavaScript/Electron analysis JSON.

The full evidence file is ~60MB. This prints the parts worth reading by hand.

Usage:
    python3 scripts/summarize.py [evidence-file]
"""
import collections
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEFAULT = sorted((ROOT / "evidence").glob("netron-*-analyze-javascript-application.json"))


def load(path: Path) -> dict:
    with path.open() as fh:
        return json.load(fh)


def report(doc: dict) -> None:
    subject = doc["subject"]
    print("== subject")
    print(f"   name       {subject.get('name')}")
    print(f"   path       {subject.get('local_path')}")
    for algo, value in subject.get("digest", {}).items():
        print(f"   {algo:<10} {value}")

    provider = doc["provider"]
    print("\n== provider")
    print(f"   {provider['name']} v{provider['version']} (id={provider['id']})")
    print(f"   confidence {doc.get('confidence')}   authority {doc.get('authority')}")
    print(f"   evidence_id {doc.get('evidence_id')}")

    result = doc["normalized_result"]
    print("\n== electron summary")
    print(json.dumps(result["summary"], indent=2, ensure_ascii=False))

    print("\n== statistics")
    print(json.dumps(result["statistics"], indent=2, ensure_ascii=False))

    graph = result["graph"]
    kinds = collections.Counter(n["kind"] for n in graph["nodes"])
    edges = collections.Counter(e["relation"] for e in graph["edges"])
    print(f"\n== graph  {len(graph['nodes'])} nodes / {len(graph['edges'])} edges")
    for kind, count in kinds.most_common():
        print(f"   node  {kind:<20} {count}")
    for kind, count in edges.most_common():
        print(f"   edge  {kind:<20} {count}")

    print("\n== electron entrypoints")
    for node in graph["nodes"]:
        if node["kind"] not in ("electron-main", "electron-renderer"):
            continue
        for obs in node.get("observations") or []:
            props = obs.get("properties", {})
            print(
                f"   {node['kind']:<17} {props.get('resolved_path')}"
                f"   [{props.get('mechanism')}, {props.get('resolution_status')}]"
            )

    print("\n== packages")
    for node in graph["nodes"]:
        if node["kind"] != "package":
            continue
        for obs in node.get("observations") or []:
            props = obs.get("properties", {})
            name, version = props.get("name"), props.get("version")
            if name and name != subject.get("name"):
                print(f"   {name:<24} {version}")

    semantic = result["semantic_graph"]
    skinds = collections.Counter(n["kind"] for n in semantic["nodes"])
    print(
        f"\n== semantic graph  {len(semantic['nodes'])} nodes / "
        f"{len(semantic['relations'])} relations / {len(semantic['unknowns'])} unknowns"
    )
    for kind, count in skinds.most_common():
        print(f"   {kind:<20} {count}")

    reasons = collections.Counter(u.get("reason") for u in semantic["unknowns"])
    print("\n== unknown reasons")
    for reason, count in reasons.most_common(10):
        print(f"   {reason:<20} {count}")

    print(f"\n== limitations: {len(result['limitations'])} recorded")


def main() -> None:
    if len(sys.argv) > 1:
        path = Path(sys.argv[1])
    elif DEFAULT:
        path = DEFAULT[-1]
    else:
        sys.exit("no evidence file found under evidence/")
    if not path.is_file():
        sys.exit(f"evidence file not found: {path}")
    report(load(path))


if __name__ == "__main__":
    main()
