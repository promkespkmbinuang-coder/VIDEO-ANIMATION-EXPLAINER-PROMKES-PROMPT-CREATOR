#!/usr/bin/env python3
"""Heuristically triage the 10x10x10 control candidate matrix; never executes controls."""
from __future__ import annotations
import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any

DOMAIN_SEVERITY = {
 "EVIDENCE":5,"SOURCE_INTEGRITY":5,"NARRATIVE":4,"VISUAL":3,"MOTION":3,
 "PROMPT":5,"AUDIO":4,"RENDERER_CODE":4,"SECURITY_PRIVACY_RIGHTS":5,"QA_RELEASE":5
}
GATE_EXPOSURE = {
 "INTAKE":5,"FACT_LOCK":5,"NARRATIVE_LOCK":4,"VISUAL_LOCK":3,"PROMPT_PREFLIGHT":5,
 "MOTION_LOCK":3,"MANIFEST_LOCK":4,"CODE_LOCK":4,"RENDER_GATE":4,"RELEASE_GATE":5
}
FAMILY_LIKELIHOOD = {
 "SCHEMA":4,"PROVENANCE":5,"RED_TEAM_INJECTION":5,"CONSISTENCY_REGRESSION":4,
 "TIMING_ARITHMETIC":3,"CAPABILITY_COMPATIBILITY":4,"ACCESSIBILITY":4,
 "RIGHTS_PRIVACY":5,"ARTIFACT_INSPECTION":4,"HUMAN_SIGNOFF":5
}
FAMILY_ESCAPE_DIFFICULTY = {
 "SCHEMA":2,"PROVENANCE":4,"RED_TEAM_INJECTION":5,"CONSISTENCY_REGRESSION":4,
 "TIMING_ARITHMETIC":2,"CAPABILITY_COMPATIBILITY":3,"ACCESSIBILITY":4,
 "RIGHTS_PRIVACY":5,"ARTIFACT_INSPECTION":3,"HUMAN_SIGNOFF":5
}
DOMAIN_CORE_GATES = {
 "EVIDENCE":{"FACT_LOCK","NARRATIVE_LOCK","RELEASE_GATE"},
 "SOURCE_INTEGRITY":{"INTAKE","FACT_LOCK","MANIFEST_LOCK"},
 "NARRATIVE":{"NARRATIVE_LOCK"},
 "VISUAL":{"VISUAL_LOCK","MOTION_LOCK"},
 "MOTION":{"MOTION_LOCK","MANIFEST_LOCK","RENDER_GATE"},
 "PROMPT":{"INTAKE","PROMPT_PREFLIGHT"},
 "AUDIO":{"MOTION_LOCK","MANIFEST_LOCK","RENDER_GATE"},
 "RENDERER_CODE":{"CODE_LOCK","RENDER_GATE","RELEASE_GATE"},
 "SECURITY_PRIVACY_RIGHTS":{"INTAKE","PROMPT_PREFLIGHT","RELEASE_GATE"},
 "QA_RELEASE":{"MANIFEST_LOCK","RENDER_GATE","RELEASE_GATE"}
}
EXECUTABLE_GATE_MAP = {
 "INTAKE": "G0_INTAKE_OK",
 "FACT_LOCK": "G1_FACT_LOCK",
 "NARRATIVE_LOCK": "G2_NARRATIVE_LOCK",
 "VISUAL_LOCK": "G3_VISUAL_LOCK",
 "PROMPT_PREFLIGHT": "G4_PROMPT_PREFLIGHT",
 "MOTION_LOCK": "G5_MANIFEST_VALID",
 "MANIFEST_LOCK": "G5_MANIFEST_VALID",
 "CODE_LOCK": "G6_CODE_VALID",
 "RENDER_GATE": "G7_RELEASE_APPROVED",
 "RELEASE_GATE": "G7_RELEASE_APPROVED",
}

FAMILY_CORE_GATES = {
 "SCHEMA":set(GATE_EXPOSURE),
 "PROVENANCE":{"INTAKE","FACT_LOCK","MANIFEST_LOCK","RENDER_GATE","RELEASE_GATE"},
 "RED_TEAM_INJECTION":{"INTAKE","PROMPT_PREFLIGHT"},
 "CONSISTENCY_REGRESSION":set(GATE_EXPOSURE),
 "TIMING_ARITHMETIC":{"MOTION_LOCK","MANIFEST_LOCK","RENDER_GATE"},
 "CAPABILITY_COMPATIBILITY":{"CODE_LOCK","RENDER_GATE"},
 "ACCESSIBILITY":{"VISUAL_LOCK","MOTION_LOCK","RENDER_GATE","RELEASE_GATE"},
 "RIGHTS_PRIVACY":{"INTAKE","PROMPT_PREFLIGHT","RELEASE_GATE"},
 "ARTIFACT_INSPECTION":{"RENDER_GATE","RELEASE_GATE"},
 "HUMAN_SIGNOFF":{"FACT_LOCK","RELEASE_GATE"}
}


def classify(row: dict[str,Any]) -> dict[str,Any]:
 domain,gate,family=row["domain"],row["gate"],row["test_family"]
 dcore=gate in DOMAIN_CORE_GATES[domain]
 fcore=gate in FAMILY_CORE_GATES[family]
 if dcore and fcore:
  app,reason="CORE","Domain and test family both map directly to this gate."
 elif dcore or fcore:
  app,reason="CROSS_CUTTING","One dimension maps directly; project scope must confirm the other."
 else:
  app,reason="CONDITIONAL","No direct mapping; retain for project review and do not auto-exclude."
 severity=DOMAIN_SEVERITY[domain]
 likelihood=FAMILY_LIKELIHOOD[family]
 escape=max(1,min(5,round((GATE_EXPOSURE[gate]+FAMILY_ESCAPE_DIFFICULTY[family])/2)))
 score=round(0.40*severity+0.35*likelihood+0.25*escape,2)
 priority="P0" if score>=4.50 else "P1" if score>=4.00 else "P2" if score>=3.25 else "P3"
 result=dict(row)
 result.update({
  "applicability_candidate":app,
  "executable_gate_id":EXECUTABLE_GATE_MAP[gate],
  "applicability_state":"NEEDS_PROJECT_REVIEW",
  "applicability_reason":reason,
  "risk":{"severity_1_to_5":severity,"likelihood_1_to_5":likelihood,
          "escape_difficulty_1_to_5":escape,"score_1_to_5":score,
          "priority":priority,"model":"heuristic-v1"},
  "triage_disposition":"REVIEW_BEFORE_EXECUTION",
  "execution_status":"NOT_RUN",
  "verdict":"NOT_VERIFIED"
 })
 return result


def triage(registry:dict[str,Any])->dict[str,Any]:
 controls=registry.get("controls")
 if not isinstance(controls,list):
  raise ValueError("input registry must contain a controls array")
 ids=[x.get("control_id") for x in controls if isinstance(x,dict)]
 if len(ids)!=len(controls) or len(ids)!=len(set(ids)):
  raise ValueError("controls must be objects with unique control_id values")
 enriched=[classify(row) for row in controls]
 rank={"P0":0,"P1":1,"P2":2,"P3":3}
 enriched.sort(key=lambda x:(rank[x["risk"]["priority"]],-x["risk"]["score_1_to_5"],x["control_id"]))
 priorities=Counter(x["risk"]["priority"] for x in enriched)
 applicability=Counter(x["applicability_candidate"] for x in enriched)
 return {
  "registry_version":"0.2.0","source_registry_version":registry.get("registry_version"),
  "model":"10x10x10 heuristic risk/applicability triage","candidate_count":len(enriched),
  "candidate_to_executable_gate_map":EXECUTABLE_GATE_MAP,
  "execution_claim":False,"project_specific_applicability":"NOT_ASSESSED",
  "summary":{
   "priority_counts":{k:priorities.get(k,0) for k in ("P0","P1","P2","P3")},
   "applicability_candidate_counts":{k:applicability.get(k,0) for k in ("CORE","CROSS_CUTTING","CONDITIONAL")},
   "executed_count":0,
   "not_run_count":sum(x["execution_status"]=="NOT_RUN" for x in enriched),
   "not_verified_count":sum(x["verdict"]=="NOT_VERIFIED" for x in enriched)
  },
  "top_priority_candidates":[x["control_id"] for x in enriched[:25]],
  "risk_model_limits":[
   "Weights are an initial heuristic and require review/calibration by clinical, security, QA and production owners.",
   "Applicability classes are routing hints, not project-specific N/A decisions.",
   "No candidate is executed or verified by this triage step."
  ],
  "controls":enriched
 }


def main()->int:
 parser=argparse.ArgumentParser(description=__doc__)
 parser.add_argument("--input",required=True,type=Path)
 parser.add_argument("--output",required=True,type=Path)
 args=parser.parse_args()
 report=triage(json.loads(args.input.read_text(encoding="utf-8")))
 args.output.parent.mkdir(parents=True,exist_ok=True)
 args.output.write_text(json.dumps(report,ensure_ascii=False,indent=2,sort_keys=True)+"\n",encoding="utf-8")
 print(f"Triage complete: {report['candidate_count']} candidates ranked; none executed; all require project review.")
 print(json.dumps(report["summary"],indent=2))
 return 0

if __name__=="__main__":
 raise SystemExit(main())
