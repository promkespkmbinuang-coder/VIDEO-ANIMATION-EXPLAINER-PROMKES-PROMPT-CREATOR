from __future__ import annotations

from typing import Any
import math

from .common import sha256_json

VALID_CATEGORIES = {"provider_cost", "render_seconds", "memory_mb", "asset_bytes", "retry_count", "cpu_seconds"}


def evaluate_resource_budget(route: str, profile: dict | None, usage: dict | None,
                             required_categories: set[str], *,
                             trusted_profile_records: dict[str, dict[str, Any]] | None = None) -> dict:
    if not required_categories.issubset(VALID_CATEGORIES):
        return {"status": "BLOCKED", "reason": "unknown resource category in policy"}
    if profile is None:
        return {"status": "BLOCKED", "reason": f"no approved resource profile for route {route}"}
    if profile.get("status") not in {"APPROVED", "NOT_APPLICABLE"}:
        return {"status": "BLOCKED", "reason": "resource profile must be APPROVED or externally authorized NOT_APPLICABLE"}
    profile_id = profile.get("profile_id")
    trusted_record = (trusted_profile_records or {}).get(profile_id) if isinstance(profile_id, str) else None
    if trusted_record is None:
        return {"status": "BLOCKED", "reason": "resource profile/exception is not present in externally trusted profile registry"}
    if profile.get("route") != route or trusted_record.get("route") != route:
        return {"status": "BLOCKED", "reason": "approved resource profile route mismatch"}
    try:
        actual_profile_hash = sha256_json(profile)
    except (TypeError, ValueError):
        return {"status": "BLOCKED", "reason": "resource profile is not finite canonical JSON"}
    if actual_profile_hash.lower() != str(trusted_record.get("content_hash", "")).lower():
        return {"status": "BLOCKED", "reason": "resource profile bytes/fields differ from externally root-signed profile hash"}
    trusted_categories = set(trusted_record.get("required_categories", []))
    if required_categories != trusted_categories:
        return {"status": "BLOCKED", "reason": "required resource categories differ from externally signed route policy"}
    if profile.get("status") == "NOT_APPLICABLE":
        reason = profile.get("reason")
        if not isinstance(reason, str) or not reason.strip():
            return {"status": "BLOCKED", "reason": "NOT_APPLICABLE requires a non-empty rationale"}
        if required_categories or profile.get("ceilings") not in ({}, None):
            return {"status": "BLOCKED", "reason": "externally signed NOT_APPLICABLE exception cannot carry resource ceilings or required categories"}
        return {"status": "NOT_APPLICABLE", "reason": reason, "profile_id": profile_id}
    if not profile.get("approved_by") or not profile.get("approval_ref"):
        return {"status": "BLOCKED", "reason": "resource profile is not explicitly approved and traceable"}
    limits = profile.get("ceilings", {})
    usage = usage or {}
    missing = sorted(c for c in trusted_categories if c not in limits or c not in usage)
    if missing:
        return {"status": "BLOCKED", "reason": "missing required resource declarations: " + ", ".join(missing)}
    violations = []
    for category in trusted_categories:
        try:
            raw_usage, raw_limit = usage[category], limits[category]
            if isinstance(raw_usage, bool) or isinstance(raw_limit, bool):
                raise ValueError("boolean is not a numeric resource measurement")
            used, ceiling = float(raw_usage), float(raw_limit)
            if not math.isfinite(used) or not math.isfinite(ceiling):
                raise ValueError("resource values must be finite numbers")
            if used < 0 or ceiling < 0:
                violations.append(f"{category} must be non-negative")
            elif used > ceiling:
                violations.append(f"{category}={raw_usage} exceeds {raw_limit}")
        except (TypeError, ValueError, OverflowError):
            violations.append(f"{category} has non-numeric, non-finite or invalid usage/ceiling")
    return {"status": "FAIL" if violations else "PASS",
            "violations": violations, "profile_id": profile_id}
