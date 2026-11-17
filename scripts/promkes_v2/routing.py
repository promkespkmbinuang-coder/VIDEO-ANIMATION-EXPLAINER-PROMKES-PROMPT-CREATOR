from __future__ import annotations


def route_input_mode(mode: str, inputs: dict) -> dict:
    mode = (mode or "").upper()
    routes = {
        "POSTER_FIRST": ["S01", "S02", "S03", "S04", "S05", "S13", "S06", "S07", "S08", "S09", "S10", "S12", "M00"],
        "AUDIO_FIRST": ["S09", "S02", "S03", "S04", "S05", "S13", "S06", "S07", "S08", "S10", "S12", "M00"],
        "HYBRID": ["S01+S09_INDEPENDENT_INTAKE", "M00_RECONCILE", "S02", "S03", "S04", "S05", "S13", "S06", "S07", "S08", "S10", "S12", "M00"],
        "SCRIPT_FIRST": ["S01", "S02", "S03", "S04", "S05", "S13", "S06", "S07", "S08", "S10", "S12", "M00"],
    }
    if mode not in routes:
        return {"status": "BLOCKED", "reason": f"unknown input mode: {mode}"}
    required = {"POSTER_FIRST": ("poster",), "AUDIO_FIRST": ("audio", "transcript"),
                "HYBRID": ("poster", "audio", "caption", "transcript"), "SCRIPT_FIRST": ("script",)}[mode]
    present = [x for x in required if inputs.get(x)]
    if mode == "AUDIO_FIRST" and not present:
        return {"status": "BLOCKED", "reason": "audio-first requires audio or transcript input"}
    if mode == "HYBRID" and not (inputs.get("poster") or inputs.get("caption")):
        return {"status": "BLOCKED", "reason": "hybrid requires poster/caption plus audio/transcript"}
    if mode == "SCRIPT_FIRST" and not inputs.get("script"):
        return {"status": "BLOCKED", "reason": "script-first requires script text"}
    timing = "MEASURED" if inputs.get("audio_timing_evidence") else ("ESTIMATED" if inputs.get("timing_estimate_approved") else "NONE")
    if mode == "SCRIPT_FIRST":
        timing = "NONE"  # no source audio, no acoustic metadata or exact sync
    return {"status": "ROUTED", "mode": mode, "route": routes[mode],
            "timing_precision": timing,
            "limitations": ["no exact audio timing claimed"] if timing != "MEASURED" else []}
