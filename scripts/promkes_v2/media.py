from __future__ import annotations

import shutil
from pathlib import Path
from typing import Any


REQUIRED_COMPOSITION_FIELDS = {
    "composition_id", "editorial_decision_list_ref", "scene_order", "shot_map", "layers",
    "overlay_map", "subtitle_map", "audio_map", "safe_areas", "fps", "resolution", "export_profile",
}


def validate_media_production_handoff(handoff: dict) -> tuple[bool, list[str]]:
    errors = sorted(REQUIRED_COMPOSITION_FIELDS - set(handoff))
    if "scene_order" in handoff and not handoff["scene_order"]: errors.append("scene_order must not be empty")
    if "layers" in handoff and not handoff["layers"]: errors.append("layers must not be empty")
    if "fps" in handoff and (not isinstance(handoff["fps"], (int, float)) or handoff["fps"] <= 0): errors.append("fps must be positive")
    if "resolution" in handoff and not all(isinstance(handoff["resolution"].get(k), int) and handoff["resolution"][k] > 0 for k in ("width", "height")):
        errors.append("resolution requires positive integer width and height")
    if "layers" in handoff:
        layer_ids = [x.get("layer_id") for x in handoff["layers"]]
        if None in layer_ids or len(layer_ids) != len(set(layer_ids)): errors.append("layers need unique stable layer_id values")
        for i, layer in enumerate(handoff["layers"]):
            if not layer.get("source_ref") or not isinstance(layer.get("z_index"), int):
                errors.append(f"layers[{i}] requires source_ref and integer z_index")
    return not errors, errors


def renderer_preflight(capability: dict | None, *, provider: str, version: str) -> dict:
    if not capability:
        return {"status": "HANDOFF", "availability": "UNAVAILABLE", "render_claim_allowed": False,
                "reason": "renderer capability record absent"}
    checks = {
        "provider": capability.get("provider") == provider,
        "operation": capability.get("operation") == "render",
        "exact_version": capability.get("exact_version") == version,
        "permission": capability.get("permission_granted") is True,
        "evidence": bool(capability.get("evidence_ref")),
        "status": capability.get("status") == "VERIFIED",
    }
    failed = [k for k, ok in checks.items() if not ok]
    if failed:
        return {"status": "HANDOFF", "availability": "UNAVAILABLE", "render_claim_allowed": False,
                "reason": "renderer capability unsupported/unverified: " + ", ".join(failed)}
    return {"status": "READY", "availability": "VERIFIED", "render_claim_allowed": True,
            "capability_ref": capability.get("capability_id")}


def has_mp4_signature(path: Path) -> bool:
    try:
        with Path(path).open("rb") as f:
            header = f.read(16)
    except OSError:
        return False
    return len(header) >= 8 and header[4:8] == b"ftyp"


def actual_media_inspection(path: Path, *, inspector_available: bool,
                            inspection_record: dict | None = None) -> dict:
    path = Path(path)
    if not path.is_file():
        return {"status": "NOT_RUN", "reason": "render output file absent"}
    if not inspector_available:
        return {"status": "NOT_VERIFIED", "reason": "media inspector/playback capability unavailable"}
    if not has_mp4_signature(path):
        return {"status": "FAIL", "reason": "file does not have an MP4 ftyp signature"}
    if not inspection_record:
        return {"status": "NOT_RUN", "reason": "file exists but no actual inspection record supplied"}
    required = {"inspector_id", "inspected_at", "file_hash", "playability", "video_stream", "audio_stream", "duration_seconds", "dimensions", "fps", "frame_review"}
    missing = sorted(required - set(inspection_record))
    if missing:
        return {"status": "NOT_VERIFIED", "reason": "inspection record incomplete: " + ", ".join(missing)}
    if inspection_record.get("playability") != "PASS" or inspection_record.get("frame_review") != "PASS":
        return {"status": "FAIL", "reason": "actual media inspection contains failed checks"}
    return {"status": "PASS", "reason": "actual media inspection record complete; independent QA still required"}


def delivery_claim(*, build_status: str, output_path: Path | None,
                   media_inspection: dict | None, s12_media_qa: dict | None) -> dict:
    if build_status != "PASS":
        return {"status": "RENDER_BLOCKED", "rendered_verified": False, "release_ready": False}
    if output_path is None or not Path(output_path).is_file():
        return {"status": "RENDER_READY", "rendered_verified": False, "release_ready": False,
                "reason": "build passed but actual output artifact is absent"}
    inspection_status = (media_inspection or {}).get("status", "NOT_RUN")
    qa = s12_media_qa or {}
    if inspection_status != "PASS" or qa.get("status") != "PASS" or qa.get("inspected_by") != "S12" or qa.get("artifact_hash_verified") is not True:
        return {"status": "RENDERED_PARTIALLY_VERIFIED", "rendered_verified": False, "release_ready": False,
                "reason": "actual media inspection and independent S12 QA evidence are both required"}
    return {"status": "RENDERED_VERIFIED", "rendered_verified": True, "release_ready": False,
            "reason": "technical QA complete; human clinical/legal/institutional approvals remain separate"}
