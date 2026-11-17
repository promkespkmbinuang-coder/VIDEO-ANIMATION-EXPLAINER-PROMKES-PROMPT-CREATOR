from __future__ import annotations

import re
from collections import Counter
from typing import Any

from .dependency import reference_closure, DependencyError


GUIDE_OWNER = {
    "GUIDE-01": "S05",  # Master Character Guide
    "GUIDE-02": "S04",  # Character/Profile and narrative personality canon
    "GUIDE-03": "S05",  # Master Visual Style Guide
    "GUIDE-04": "S04",  # Master Narrative Style Guide
    "GUIDE-05": "S09",  # Master Voice & Audio Guide
    "GUIDE-06": "S05",  # Master World & Environment Guide
    "GUIDE-07": "S13",  # Scene Continuity Guide registry and integration
}


def extract_atomic_claims(text: str) -> list[dict]:
    """Conservative clause segmentation, not an automatic clinical verifier."""
    if not isinstance(text, str) or not text.strip():
        return []
    clauses = re.split(r"[;\n]+|(?<=[.!?])\s+", text.strip())
    expanded = []
    for clause in clauses:
        # Split coordinated clauses only when the right side restarts a subject.
        parts = re.split(r"\s+(?:dan|serta|tetapi|namun|sedangkan)\s+", clause, flags=re.I)
        if len(parts) > 1 and all(re.search(r"\b(fogging|fogging|nyamuk|virus|masyarakat|petugas|kegiatan|obat|vaksin|program|pemerintah|anak|orang)\b", p, re.I) for p in parts):
            expanded.extend(parts)
        else:
            expanded.append(clause)
    cleaned = [re.sub(r"\s+", " ", x).strip(" .") for x in expanded if x.strip(" .")]
    return [{"claim_id": f"CLM-{i:03d}", "text": value, "status": "UNVERIFIED"}
            for i, value in enumerate(cleaned, 1)]


def validate_health_claim(claim: dict, source: dict | None) -> tuple[str, list[str]]:
    reasons = []
    if source is None or source.get("access") != "ACCESSIBLE":
        return "UNVERIFIED", ["source unavailable or inaccessible"]
    if source.get("status") in {"STALE", "CONTRADICTED", "UNVERIFIED", "UNKNOWN"}:
        return "UNVERIFIED", [f"source status is {source.get('status')}"]
    if source.get("context_match") is not True:
        return "HUMAN_REVIEW", ["date/jurisdiction/population context does not match"]
    if claim.get("support_status") != "SUPPORTED_LEXICALLY":
        return "HUMAN_REVIEW", ["semantic support has not passed conservative pre-review"]
    if claim.get("human_clinical_approval") is not True:
        return "PENDING_HUMAN_APPROVAL", ["clinical truth requires authorized human review"]
    return "APPROVED_BY_HUMAN", []


def safe_simplification(original: str, simplified: str) -> tuple[bool, list[str]]:
    original_l, simple_l = original.casefold(), simplified.casefold()
    reasons = []
    if any(re.search(rf"\b{re.escape(n)}\b", original_l) for n in ("tidak", "bukan", "tanpa", "belum")) and not any(
        re.search(rf"\b{re.escape(n)}\b", simple_l) for n in ("tidak", "bukan", "tanpa", "belum")):
        reasons.append("simplification removed source negation")
    hedges = ("dapat", "bisa", "mungkin", "berpotensi", "cenderung")
    strong = ("pasti", "selalu", "menjamin", "mencegah", "menghentikan", "menyembuhkan", "membasmi")
    source_hedged = any(re.search(rf"\b{w}\b", original_l) for w in hedges)
    simplified_strong = any(re.search(rf"\b{w}\b", simple_l) for w in strong)
    if source_hedged and simplified_strong:
        reasons.append("simplification strengthens certainty or prevention/cure guarantee")
    causal_original = any(x in original_l for x in ("berkaitan dengan", "berhubungan dengan", "diasosiasikan"))
    causal_simple = any(x in simple_l for x in ("menyebabkan", "mengakibatkan", "akibat langsung", "pasti karena"))
    if causal_original and causal_simple:
        reasons.append("simplification strengthens association into causation")
    return not reasons, reasons


def validate_claim_context_fields(claim: dict, source: dict) -> tuple[bool, list[str]]:
    fields = ("date", "jurisdiction", "population")
    mismatch = [f for f in fields if not claim.get(f) or not source.get(f)
                or str(claim[f]).casefold() != str(source[f]).casefold()]
    return not mismatch, mismatch


def validate_campaign(plan: dict) -> tuple[bool, list[str]]:
    objectives = plan.get("objectives", [])
    ctas = plan.get("ctas", [])
    primary_objectives = [x for x in objectives if x.get("priority") == "PRIMARY"]
    primary_ctas = [x for x in ctas if x.get("priority") == "PRIMARY"]
    errors = []
    if len(primary_objectives) != 1:
        errors.append("campaign must have exactly one primary objective")
    if len(primary_ctas) != 1:
        errors.append("campaign must have exactly one primary CTA")
    if primary_objectives and primary_ctas:
        if primary_objectives[0].get("behavior_id") != primary_ctas[0].get("behavior_id"):
            errors.append("primary CTA does not implement the primary behavior objective")
    if len({x.get("objective_id") for x in primary_objectives}) != len(primary_objectives):
        errors.append("duplicate primary objective")
    return not errors, errors


def validate_localization(details: list[dict]) -> tuple[bool, list[str]]:
    errors = []
    for item in details:
        kind = item.get("kind")
        if kind in {"DEMOGRAPHIC", "DIALECT", "LOCAL_BEHAVIOR"} and not item.get("evidence_ref"):
            if item.get("classification") != "ASSUMPTION":
                errors.append(f"{item.get('detail_id')}: unsupported local detail must be ASSUMPTION or removed")
    return not errors, errors


def validate_screenplay(lines: list[dict]) -> tuple[bool, list[str]]:
    errors = []
    for i, line in enumerate(lines):
        if line.get("factual") and not (line.get("claim_refs") or line.get("message_refs")):
            errors.append(f"line[{i}] factual line lacks claim/message trace")
        if line.get("introduces_health_proposition") and not line.get("claim_refs"):
            errors.append(f"line[{i}] introduces a health proposition; route to S02")
    return not errors, errors


def validate_visual_plan(assets: list[dict], character_uses: list[dict]) -> tuple[str, list[str]]:
    errors = []
    for asset in assets:
        if asset.get("kind") in {"LOGO", "TRADEMARK", "OFFICIAL_SEAL"} and asset.get("permission_status") != "APPROVED":
            errors.append(f"{asset.get('asset_id')}: logo/seal permission not approved")
        if asset.get("kind") in {"PERSON_LIKENESS", "IDENTIFIABLE_PERSON"} and asset.get("consent_status") != "APPROVED":
            errors.append(f"{asset.get('asset_id')}: likeness consent not approved")
    for use in character_uses:
        if not use.get("character_id") or not use.get("guide_id") or not use.get("guide_version"):
            errors.append("character use lacks stable identity/Guide version")
        if use.get("guide_version") != use.get("locked_guide_version"):
            errors.append(f"{use.get('character_id')}: stale character lock")
    return ("HOLD" if errors else "DRAFT"), errors


def validate_duration(policy: dict) -> tuple[bool, str]:
    if policy.get("duration_frames") is not None:
        if not isinstance(policy["duration_frames"], int) or policy["duration_frames"] <= 0:
            return False, "duration_frames must be positive integer"
        if policy.get("basis") not in {"MEASURED", "ESTIMATED", "APPROVED_PROFILE"}:
            return False, "numeric duration requires MEASURED, ESTIMATED, or APPROVED_PROFILE basis"
        return True, "duration basis explicit"
    if policy.get("duration_seconds") is not None:
        if not isinstance(policy["duration_seconds"], (int, float)) or policy["duration_seconds"] <= 0:
            return False, "duration_seconds must be positive"
        if policy.get("basis") not in {"MEASURED", "ESTIMATED", "APPROVED_PROFILE"}:
            return False, "duration requires explicit basis"
        return True, "duration basis explicit"
    if policy.get("profile_id") and policy.get("profile_approved") is True:
        return True, "approved profile supplies duration policy"
    return False, "no duration or approved duration profile; no hidden numeric default is allowed"


def validate_scene_timeline(scenes: list[dict], *, fps: int) -> tuple[bool, list[str]]:
    errors = []
    if not isinstance(fps, int) or fps <= 0:
        return False, ["fps must be a positive integer"]
    ordered = sorted(scenes, key=lambda s: s.get("start_frame", -1))
    seen = set()
    for i, scene in enumerate(ordered):
        sid = scene.get("scene_id")
        if not sid or sid in seen: errors.append(f"scene[{i}] missing/duplicate ID")
        seen.add(sid)
        start, end = scene.get("start_frame"), scene.get("end_frame")
        if not isinstance(start, int) or not isinstance(end, int) or start < 0 or end <= start:
            errors.append(f"{sid}: frame interval must be valid half-open [start,end)")
        if scene.get("fps") != fps: errors.append(f"{sid}: fps mismatch")
        if i:
            prev = ordered[i-1]
            overlap = prev.get("end_frame", 0) - start if isinstance(start, int) else 0
            declared = scene.get("transition_overlap_frames", 0)
            if overlap > 0 and overlap != declared:
                errors.append(f"{sid}: actual overlap {overlap} differs from declared transition {declared}")
            if overlap < 0 and not scene.get("gap_approved"):
                errors.append(f"{sid}: undeclared timeline gap {-overlap} frames")
    return not errors, errors


def validate_motion_record(record: dict) -> tuple[bool, list[str]]:
    errors = []
    required = ("element_id", "fps", "timebase", "position_unit", "scale_unit", "keyframes")
    missing = [x for x in required if record.get(x) in (None, "", [])]
    if missing: errors.append("motion record missing: " + ", ".join(missing))
    if not isinstance(record.get("fps"), (int, float)) or record.get("fps", 0) <= 0:
        errors.append("fps must be positive")
    if record.get("timebase") not in {"FRAMES", "SECONDS"}:
        errors.append("timebase must be FRAMES or SECONDS")
    if record.get("position_unit") not in {"px", "%", "normalized"}:
        errors.append("position_unit unsupported/missing")
    if record.get("scale_unit") not in {"ratio", "%"}:
        errors.append("scale_unit unsupported/missing")
    kfs = record.get("keyframes", [])
    times = [k.get("at") for k in kfs]
    if any(not isinstance(t, (int, float)) for t in times) or times != sorted(times) or len(times) != len(set(times)):
        errors.append("keyframes must have strictly increasing numeric times")
    return not errors, errors


def check_scene_state_continuity(previous: dict, following: dict) -> tuple[bool, list[str]]:
    out_state = previous.get("state_out", {})
    in_state = following.get("state_in", {})
    if out_state == in_state:
        return True, []
    return False, [f"state discontinuity {previous.get('scene_id')} -> {following.get('scene_id')}; route to S13"]


def validate_guide_registry(guides: list[dict], scene_locks: list[dict]) -> tuple[bool, list[str]]:
    errors = []
    ids = [g.get("guide_id") for g in guides]
    counts = Counter(ids)
    for gid, count in counts.items():
        if not gid or count > 1: errors.append(f"duplicate or missing Guide ID: {gid}")
    if set(ids) != set(GUIDE_OWNER):
        errors.append(f"Guide inventory mismatch: expected {sorted(GUIDE_OWNER)}, got {sorted(set(ids))}")
    by_id = {g.get("guide_id"): g for g in guides}
    for gid, expected_owner in GUIDE_OWNER.items():
        guide = by_id.get(gid)
        if guide and guide.get("owner_skill_id") != expected_owner:
            errors.append(f"{gid}: expected single owner {expected_owner}, got {guide.get('owner_skill_id')}")
    for lock in scene_locks:
        guide = by_id.get(lock.get("guide_id"))
        if not guide or lock.get("guide_version") != guide.get("version") or guide.get("status") != "LOCKED":
            errors.append(f"{lock.get('scene_id')}: stale or non-locked Guide reference {lock.get('guide_id')}")
    return not errors, errors


def guide_change_invalidation(guides: list[dict], edges: list[tuple[str, str]], changed_guide_id: str) -> tuple[list[str], list[str]]:
    try:
        invalidated = sorted(reference_closure(edges, changed_guide_id))
    except DependencyError as exc:
        return [], [str(exc)]
    known = {a for edge in edges for a in edge}
    if changed_guide_id not in known:
        return [], [f"unknown changed Guide {changed_guide_id}"]
    return invalidated, []
