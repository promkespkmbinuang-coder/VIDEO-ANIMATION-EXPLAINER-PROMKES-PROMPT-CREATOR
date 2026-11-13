#!/usr/bin/env python3
"""Fail-closed semantic checks for the canonical MCG manifest."""
import argparse, json
from collections import defaultdict, deque
from pathlib import Path
from jsonschema import Draft202012Validator, FormatChecker

OWNERS = {
 "GUIDE-01":"S05:visual-identity-art-direction",
 "GUIDE-02":"S04:story-screenplay-architect",
 "GUIDE-03":"S05:visual-identity-art-direction",
 "GUIDE-04":"S04:story-screenplay-architect",
 "GUIDE-05":"S09:voice-sound-design",
 "GUIDE-06":"S05:visual-identity-art-direction",
 "GUIDE-07":"S13:continuity-guardian",
}
PROTOCOLS = {"GCL-01", "CCM-01", "CQA-01"}

def read_json(path):
    def pairs(items):
        result = {}
        for key, value in items:
            if key in result:
                raise ValueError("duplicate JSON key: " + key)
            result[key] = value
        return result
    return json.loads(Path(path).read_text(encoding="utf-8"), object_pairs_hook=pairs)

def semantic_errors(m, root):
    errors = []
    guides = m.get("guide_registry", [])
    ids = [g.get("guide_id") for g in guides]
    if len(guides) != 7 or len(set(ids)) != 7 or set(ids) != set(OWNERS):
        errors.append("exactly seven unique GUIDE-01..GUIDE-07 records required")
    for g in guides:
        gid = g.get("guide_id")
        if gid in OWNERS and g.get("primary_owner") != OWNERS[gid]:
            errors.append("single canonical owner mismatch: " + str(gid))
        if g.get("status") == "LOCKED":
            approvals = {a.get("approval_id"): a for a in m.get("approval_records", [])}
            matched = [approvals.get(aid) for aid in g.get("approval_record_ids", [])]
            valid = any(a and a.get("decision") == "APPROVED"
                and g.get("content_hash") in a.get("artifact_hashes", [])
                and gid in a.get("scope", [])
                and g.get("version") in a.get("scope", []) for a in matched)
            if not valid:
                errors.append("LOCKED Guide lacks exact human approval binding: " + str(gid))
    protocols = [p.get("protocol_id") for p in m.get("protocol_refs", [])]
    if len(protocols) != 3 or len(set(protocols)) != 3 or set(protocols) != PROTOCOLS:
        errors.append("exactly three unique continuity protocols required")
    for p in m.get("protocol_refs", []):
        target = (root / p.get("ref", "")).resolve()
        try:
            target.relative_to(root.resolve())
            if not target.is_file():
                errors.append("broken protocol ref: " + str(p.get("protocol_id")))
        except ValueError:
            errors.append("protocol ref escapes package root: " + str(p.get("protocol_id")))
    owners = {x.get("guide_id"): x.get("primary_owner") for x in m.get("domain_ownership", [])}
    if owners != OWNERS:
        errors.append("domain ownership map differs from canonical owner map")
    nodes = set(ids)
    graph, indegree, seen = defaultdict(list), {n: 0 for n in nodes}, set()
    for edge in m.get("dependency_edges", []):
        a, b = edge.get("from_id"), edge.get("to_id")
        if a not in nodes or b not in nodes:
            errors.append("broken dependency reference: %s -> %s" % (a, b))
        elif a == b or (a, b) in seen:
            errors.append("dependency self-cycle or duplicate edge: %s -> %s" % (a, b))
        else:
            seen.add((a, b)); graph[a].append(b); indegree[b] += 1
    queue = deque(n for n, degree in indegree.items() if degree == 0)
    visited = 0
    while queue:
        node = queue.popleft(); visited += 1
        for target in graph[node]:
            indegree[target] -= 1
            if indegree[target] == 0:
                queue.append(target)
    if visited != len(nodes):
        errors.append("dependency cycle/deadlock detected")
    health = m.get("health_truth_registry_ref", {})
    if health.get("owner") != "S02:health-evidence-safety-auditor":
        errors.append("Health Truth Registry must be owned by S02")
    for claim in health.get("claim_refs", []):
        if claim.get("status") == "VERIFIED" and not claim.get("evidence_refs"):
            errors.append("VERIFIED claim lacks evidence refs: " + str(claim.get("claim_id")))
    kinds = set()
    for source in m.get("source_catalog", []):
        kind, owner = source.get("source_kind"), source.get("owner")
        kinds.add(kind)
        if kind in {"AUDIO", "TRANSCRIPT"} and owner != "S09:voice-sound-design":
            errors.append("audio/transcript source must be owned by S09")
        if kind == "SCRIPT" and owner != "S04:story-screenplay-architect":
            errors.append("script source must be owned by S04")
        if source.get("privacy_classification") in {"PERSONAL_DATA", "SENSITIVE_PERSONAL_DATA"} and not source.get("consent_ref"):
            errors.append("personal source lacks consent ref")
    mode = m.get("input_mode")
    expected = {"POSTER_FIRST":"POSTER_IMAGE", "AUDIO_FIRST":"AUDIO",
                "SCRIPT_FIRST":"SCRIPT", "TRANSCRIPT_FIRST":"TRANSCRIPT"}
    if mode in expected and expected[mode] not in kinds:
        errors.append("input mode lacks required source type: " + mode)
    if mode == "HYBRID" and len(kinds) < 2:
        errors.append("HYBRID requires at least two distinct source types")
    scene = m.get("scene_continuity", {})
    if m.get("status") == "READY_FOR_SCENE_PROMPTS":
        if not (scene.get("refresh_after_storyboard") is True
                and scene.get("refresh_gate_status") == "PASS"
                and scene.get("refresh_evidence_ref")):
            errors.append("S13 post-storyboard refresh is not evidenced")
    approvals = {a.get("approval_id"): a for a in m.get("approval_records", [])}
    for lock in m.get("lock_registry", []):
        if lock.get("status") == "LOCKED":
            a = approvals.get(lock.get("approval_record_id"))
            valid = a and a.get("decision") == "APPROVED"
            valid = valid and lock.get("content_hash") in a.get("artifact_hashes", [])
            valid = valid and lock.get("lock_id") in a.get("scope", [])
            valid = valid and lock.get("version") in a.get("scope", [])
            if not valid:
                errors.append("LOCKED lock lacks exact human approval binding")
    for cap in m.get("model_capabilities", []):
        if cap.get("status") == "VERIFIED" and not cap.get("evidence_ref"):
            errors.append("VERIFIED capability lacks evidence ref")
    for asset in m.get("asset_registry", []):
        if asset.get("lifecycle_status") == "APPROVED" and asset.get("rights_status") not in {"VERIFIED", "NOT_APPLICABLE"}:
            errors.append("APPROVED asset has unresolved rights")
        if asset.get("privacy_classification") in {"PERSONAL_DATA", "SENSITIVE_PERSONAL_DATA"} and not asset.get("consent_ref"):
            errors.append("personal asset lacks consent ref")
    return errors

def validate(path):
    path = Path(path)
    root = Path(__file__).resolve().parents[1]
    m = read_json(path)
    schema = read_json(root / "schemas/v4/mcg-manifest.schema.json")
    structural = list(Draft202012Validator(schema, format_checker=FormatChecker()).iter_errors(m))
    errors = ["schema %s: %s" % ("/".join(map(str, e.path)), e.message) for e in structural]
    if not errors:
        errors.extend(semantic_errors(m, root))
    return errors

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("manifest", type=Path)
    args = parser.parse_args()
    errors = validate(args.manifest)
    if errors:
        print("FAIL: MCG validation")
        for error in errors:
            print("- " + error)
        raise SystemExit(1)
    print("PASS: structural and semantic MCG checks only; no clinical truth, runtime, rights authority or human approval is inferred.")

if __name__ == "__main__":
    main()
