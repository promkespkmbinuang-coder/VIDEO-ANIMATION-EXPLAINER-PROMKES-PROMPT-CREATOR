#!/usr/bin/env python3
"""Dependency-light semantic validator for V4.1.8 beat-sheet JSON."""
import json, sys
from pathlib import Path

def validate(data):
    errors=[]
    if not isinstance(data,dict): return ["root must be an object"]
    if data.get("version")!="4.1.8": errors.append("version must be 4.1.8")
    beats=data.get("beats")
    if not isinstance(beats,list) or not beats: return errors+["beats must be a non-empty array"]
    ids=set(); previous_sequence=0
    for i,b in enumerate(beats):
        p=f"beats[{i}]"
        if not isinstance(b,dict): errors.append(f"{p} must be an object"); continue
        bid=b.get("beat_id")
        if not isinstance(bid,str) or not bid: errors.append(f"{p}.beat_id required")
        elif bid in ids: errors.append(f"duplicate beat_id: {bid}")
        else: ids.add(bid)
        seq=b.get("sequence")
        if not isinstance(seq,int) or seq<=previous_sequence: errors.append(f"{p}.sequence must be strictly increasing")
        else: previous_sequence=seq
        tin,tout=b.get("time_in"),b.get("time_out")
        if not isinstance(tin,(int,float)) or not isinstance(tout,(int,float)) or tout<=tin:
            errors.append(f"{p} requires time_out > time_in")
        precision=b.get("timing_precision")
        if precision not in {"EXACT_AUDIO","SOURCE_TIMECODE","ESTIMATED","UNSPECIFIED"}: errors.append(f"{p}.timing_precision invalid")
        if precision in {"EXACT_AUDIO","SOURCE_TIMECODE"} and not b.get("timing_source_ref"):
            errors.append(f"{p} exact/source timing requires timing_source_ref")
        sf,ef=b.get("start_frame"),b.get("end_frame_exclusive")
        if (sf is None) != (ef is None): errors.append(f"{p} frame interval must provide both endpoints")
        if sf is not None and (not isinstance(sf,int) or not isinstance(ef,int) or sf<0 or ef<=sf):
            errors.append(f"{p} frame interval must be half-open with end > start")
        for key in ("scene_id","shot_id","narrative_function","accessibility_fallback","qa_oracle"):
            if not isinstance(b.get(key),str) or not b[key].strip(): errors.append(f"{p}.{key} required")
        for key in ("motion_refs","element_refs","audio_refs","overlay_refs","transition_refs","claim_refs","message_refs"):
            if key in b and not isinstance(b[key],list): errors.append(f"{p}.{key} must be an array")
    return errors

def main():
    if len(sys.argv)!=2: print("usage: python scripts/validate_beat_sheet.py FILE"); return 2
    path=Path(sys.argv[1])
    try: data=json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc: print(f"INVALID JSON: {exc}"); return 2
    errors=validate(data)
    if errors:
        print("\n".join(f"FAIL: {e}" for e in errors)); return 1
    print("PASS: beat-sheet structure and semantic checks")
    return 0
if __name__=="__main__": raise SystemExit(main())
