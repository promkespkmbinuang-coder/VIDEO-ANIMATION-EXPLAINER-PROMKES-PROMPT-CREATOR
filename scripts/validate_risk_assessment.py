#!/usr/bin/env python3
"""Conservative R0-R3 risk-lane resolver. It never authorizes publication."""
import json, sys
from pathlib import Path
LEVELS={"LOW":0,"STANDARD":1,"ELEVATED":2,"CRITICAL":3,"UNKNOWN":2}
LANES=["R0","R1","R2","R3"]
def resolve(data):
    dims=data.get("dimensions",{})
    if not isinstance(dims,dict) or not dims: return None,["dimensions must be a non-empty object"]
    errors=[]
    for key,value in dims.items():
        if value not in LEVELS: errors.append(f"invalid dimension {key}: {value}")
    if errors: return None,errors
    lane=LANES[max(LEVELS[v] for v in dims.values())]
    if data.get("serious_harm_trigger") is True or data.get("unauthorized_sensitive_data") is True:
        lane="R3"
    return lane,[]
def main():
    if len(sys.argv)!=2: print("usage: python scripts/validate_risk_assessment.py FILE"); return 2
    try: data=json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    except Exception as exc: print(f"INVALID JSON: {exc}"); return 2
    lane,errors=resolve(data)
    if errors: print("\n".join(errors)); return 1
    declared=data.get("declared_lane")
    if declared not in LANES or LANES.index(declared)<LANES.index(lane):
        print(f"FAIL: declared lane {declared!r} is lower than minimum {lane}"); return 1
    print(f"PASS: minimum lane {lane}; this is triage only, not approval")
    return 0
if __name__=="__main__": raise SystemExit(main())
