#!/usr/bin/env python3
"""Enumerate 10x10x10 candidate control IDs; does not execute controls."""
import argparse, itertools, json
from pathlib import Path

DOMAINS = [
 "EVIDENCE","SOURCE_INTEGRITY","NARRATIVE","VISUAL","MOTION",
 "PROMPT","AUDIO","RENDERER_CODE","SECURITY_PRIVACY_RIGHTS","QA_RELEASE"
]
GATES = [
 "INTAKE","FACT_LOCK","NARRATIVE_LOCK","VISUAL_LOCK","PROMPT_PREFLIGHT",
 "MOTION_LOCK","MANIFEST_LOCK","CODE_LOCK","RENDER_GATE","RELEASE_GATE"
]
FAMILIES = [
 "SCHEMA","PROVENANCE","RED_TEAM_INJECTION","CONSISTENCY_REGRESSION",
 "TIMING_ARITHMETIC","CAPABILITY_COMPATIBILITY","ACCESSIBILITY",
 "RIGHTS_PRIVACY","ARTIFACT_INSPECTION","HUMAN_SIGNOFF"
]

def generate():
    rows=[]
    for domain, gate, family in itertools.product(DOMAINS, GATES, FAMILIES):
        cid=f"CTL-{domain}-{gate}-{family}"
        rows.append({
            "control_id":cid,"domain":domain,"gate":gate,"test_family":family,
            "definition_status":"CANDIDATE_UNREVIEWED",
            "applicability":"UNASSESSED","execution_status":"NOT_RUN",
            "verdict":"NOT_VERIFIED","owner":"UNASSIGNED",
            "oracle":None,"threshold":None,"evidence_refs":[],
            "remediation":None,"retest_rule":None
        })
    return rows

if __name__ == "__main__":
    ap=argparse.ArgumentParser()
    ap.add_argument("--output",default="control-candidates.v4.json")
    args=ap.parse_args()
    rows=generate()
    Path(args.output).write_text(json.dumps({
      "registry_version":"0.1.0","model":"10x10x10 candidate enumeration",
      "execution_claim":False,"candidate_count":len(rows),"controls":rows
    },indent=2)+"\n",encoding="utf-8")
    print(f"Wrote {len(rows)} candidate definitions; none were executed.")
