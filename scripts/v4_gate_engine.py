#!/usr/bin/env python3
"""Evidence-contract-gated validator and production gate engine for Promkes V4.

The engine is deterministic and fail-closed. It validates supplied records and
provenance; it cannot prove that an external human, AI model, ASR service, or
renderer actually performed an operation unless corresponding inspectable
artifact evidence is supplied and independently verified.
"""
from __future__ import annotations

import argparse
import hashlib
import html
import json
import re
import sys
import unicodedata
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath
from urllib.parse import unquote
from typing import Any, Callable

ENGINE_ID = "promkes-v4-gate-engine"
ENGINE_VERSION = "4.0.0"
ROOT = Path(__file__).resolve().parents[1]
SCHEMA_DIR = ROOT / "schemas" / "v4"

GATE_ORDER = [
    "G0_INTAKE_OK",
    "G1_FACT_LOCK",
    "G2_NARRATIVE_LOCK",
    "G3_VISUAL_LOCK",
    "G4_PROMPT_PREFLIGHT",
    "G5_MANIFEST_VALID",
    "G6_CODE_VALID",
    "G7_RELEASE_APPROVED",
]

CONTROL_IDS = {
    "G0_INTAKE_OK": ["CTRL-INTAKE-INVENTORY", "CTRL-PRIVACY-CLASSIFICATION", "CTRL-RIGHTS-BASIS", "CTRL-UNTRUSTED-INPUTS"],
    "G1_FACT_LOCK": ["CTRL-CLAIM-SCHEMA", "CTRL-SOURCE-PROVENANCE", "CTRL-MATERIAL-CLAIMS", "CTRL-CLINICAL-APPROVAL"],
    "G2_NARRATIVE_LOCK": ["CTRL-NARRATIVE-TRACEABILITY", "CTRL-SAFE-WORDING"],
    "G3_VISUAL_LOCK": ["CTRL-CONTINUITY-LOCKS", "CTRL-VISUAL-REFERENCES"],
    "G4_PROMPT_PREFLIGHT": ["CTRL-PROMPT-INJECTION", "CTRL-PROMPT-BOUNDARY"],
    "G5_MANIFEST_VALID": ["CTRL-SCENE-TIMING", "CTRL-MANIFEST-INTEGRITY"],
    "G6_CODE_VALID": ["CTRL-CAPABILITY-VERIFICATION", "CTRL-CODE-STATIC"],
    "G7_RELEASE_APPROVED": ["CTRL-ARTIFACT-QA", "CTRL-ACCESSIBILITY-QA", "CTRL-RELEASE-APPROVAL"],
}

PASSABLE = {"PASS", "NOT_APPLICABLE"}
FAIL_CLOSED = {"NOT_RUN", "NOT_VERIFIED", "BLOCKED", "STALE", "INVALIDATED", "PARTIAL", "IN_PROGRESS", "NOT_STARTED"}
CLAIM_BLOCKING = {"UNVERIFIED", "CONTRADICTED", "UNKNOWN", "STALE"}
MATERIAL_CLAIM_TYPES = {"PREVENTION", "TREATMENT", "RISK", "STATISTIC", "CAUSAL"}
PRIVACY_CLASSES = {"PUBLIC", "INTERNAL", "CONFIDENTIAL", "SENSITIVE"}
RIGHTS_STATES = {"CLEARED", "RESTRICTED", "PENDING", "UNKNOWN", "NOT_APPLICABLE"}

INJECTION_PATTERNS = [
    re.compile(r"(ignore|disregard|forget|bypass|override)\s+(all\s+)?(the\s+)?(previous|prior|above|earlier)\s+(system\s+|developer\s+)?instructions?", re.I),
    re.compile(r"(reveal|show|print|expose|dump)\s+(the\s+)?(hidden\s+)?(system|developer|internal)\s+prompt", re.I),
    re.compile(r"(show|reveal|print|expose)\s+(me\s+)?hidden\s+instructions", re.I),
    re.compile(r"(exfiltrat(e|ion)|send|forward|upload|post)\s+(all\s+)?(the\s+)?(secrets|credentials|api\s+keys|tokens|passwords)", re.I),
    re.compile(r"(disable|override|bypass|suspend)\s+(the\s+)?(safety|security|content)\s+(policy|rules?|guardrails?)", re.I),
    re.compile(r"(act\s+as|become|switch\s+to)\s+(an?\s+)?(dan|jailbreak|unrestricted|unfiltered)\b", re.I),
    re.compile(r"you\s+are\s+now\s+.*(not\s+bound|no\s+restrictions|ignore\s+policy)", re.I),
    re.compile(r"(call|invoke|use)\s+(the\s+)?(browser|tool|function)(\s+tool)?\s+and\s+(send|upload|exfiltrate)", re.I),
]


def normalize_prompt_text(value: str) -> str:
    """Normalize common obfuscation before applying heuristic injection patterns."""
    text = unicodedata.normalize("NFKC", html.unescape(value))
    text = unquote(text)
    text = re.sub(r"[\u200b-\u200f\u2060\ufeff]", "", text)
    return re.sub(r"\s+", " ", text).strip()


def detect_prompt_injection(value: str) -> list[str]:
    """Return matched heuristic pattern labels; absence of a match is not proof of safety."""
    normalized = normalize_prompt_text(value)
    return [pattern.pattern for pattern in INJECTION_PATTERNS if pattern.search(normalized)]



def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def _normalize(value: Any) -> Any:
    if isinstance(value, str):
        return unicodedata.normalize("NFC", value.replace("\r\n", "\n").replace("\r", "\n"))
    if isinstance(value, list):
        return [_normalize(item) for item in value]
    if isinstance(value, dict):
        return {unicodedata.normalize("NFC", str(k)): _normalize(v) for k, v in value.items()}
    return value


def canonical_json_bytes(value: Any) -> bytes:
    """Canonical UTF-8 JSON: NFC strings, LF newlines, sorted keys, no whitespace."""
    normalized = _normalize(value)
    return json.dumps(normalized, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False).encode("utf-8")


def content_hash(value: Any, *, exclude: tuple[str, ...] = ("content_hash",)) -> str:
    payload = dict(value) if isinstance(value, dict) else value
    if isinstance(payload, dict):
        for key in exclude:
            payload.pop(key, None)
    return "sha256:" + hashlib.sha256(canonical_json_bytes(payload)).hexdigest()


def sha256_bytes(raw: bytes) -> str:
    return "sha256:" + hashlib.sha256(raw).hexdigest()


def is_sha256(value: Any) -> bool:
    return isinstance(value, str) and re.fullmatch(r"sha256:[0-9a-fA-F]{64}", value) is not None


def safe_relative_path(value: Any) -> bool:
    if not isinstance(value, str) or not value.strip() or "\\" in value or "\x00" in value:
        return False
    if re.match(r"^[A-Za-z]:", value) or value.startswith(("/", "~")):
        return False
    parts = PurePosixPath(value).parts
    return bool(parts) and all(p not in {"", ".", ".."} for p in parts)


def _schema_validator(kind: str):
    try:
        from jsonschema import Draft202012Validator, FormatChecker
    except ImportError as exc:
        raise RuntimeError("jsonschema is required; install requirements-dev.txt") from exc
    schema_path = SCHEMA_DIR / f"{kind}.schema.json"
    if not schema_path.is_file():
        raise FileNotFoundError(f"Schema not found: {schema_path}")
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    return Draft202012Validator(schema, format_checker=FormatChecker())


def validate_record(record: dict[str, Any], kind: str) -> list[str]:
    if not isinstance(record, dict):
        return ["record must be a JSON object"]
    if kind not in {"claim-record", "artifact-envelope"}:
        raise ValueError(f"Unsupported schema kind: {kind}")
    errors = [f"{e.json_path}: {e.message}" for e in _schema_validator(kind).iter_errors(record)]
    if kind == "claim-record":
        errors.extend(validate_claim_semantics(record))
    elif kind == "artifact-envelope":
        expected = content_hash(record)
        if record.get("content_hash") != expected:
            errors.append(f"content_hash mismatch: expected {expected}")
        if record.get("status") == "PASS" and record.get("validation_result") != "PASS":
            errors.append("status PASS requires validation_result PASS")
        if record.get("validation_result") == "PASS" and record.get("status") in FAIL_CLOSED:
            errors.append("validation_result PASS conflicts with a fail-closed artifact status")
    return errors


def validate_claim_semantics(claim: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    status = claim.get("status")
    if status in CLAIM_BLOCKING and claim.get("allowed_wording"):
        errors.append(f"{status} claim must not expose allowed_wording")
    if status == "VERIFIED" and claim.get("evidence_level") == "UNVERIFIED":
        errors.append("VERIFIED claim cannot have evidence_level UNVERIFIED")
    if status == "VERIFIED" and not claim.get("source_ids"):
        errors.append("VERIFIED claim requires at least one source_id")
    if claim.get("reviewed_by_human") is True:
        if not claim.get("reviewer_id") or not claim.get("reviewed_at"):
            errors.append("human-reviewed claim requires reviewer_id and reviewed_at")
        if claim.get("reviewer_role") != "CLINICIAN" and claim.get("claim_type") in MATERIAL_CLAIM_TYPES:
            errors.append("material health claim review requires reviewer_role CLINICIAN")
    if claim.get("valid_from") and claim.get("valid_to") and claim["valid_from"] > claim["valid_to"]:
        errors.append("valid_from must not be later than valid_to")
    return errors


def _out(control_id: str, status: str, reason: str, observed: Any = None, evidence: list[str] | None = None) -> dict[str, Any]:
    return {
        "control_id": control_id,
        "status": status,
        "reason": reason,
        "observed": observed,
        "oracle": "deterministic-v4-gate-engine",
        "executed_at": utc_now(),
        "environment": {"python": sys.version.split()[0], "engine": ENGINE_VERSION},
        "evidence_refs": evidence or [],
    }


def _missing(control_id: str, field: str) -> dict[str, Any]:
    return _out(control_id, "NOT_RUN", f"Required input '{field}' is absent or incomplete")


def _evidence_refs(value: Any) -> list[str]:
    return [x for x in value if isinstance(x, str) and x.strip()] if isinstance(value, list) else []


def _valid_approval(project: dict[str, Any], domain: str, role: str, hashes: set[str] | None = None, approver_ids: set[str] | None = None) -> tuple[bool, str, list[str]]:
    registry = {x.get("approver_id"): x for x in project.get("approver_registry", []) if isinstance(x, dict)}
    for approval in project.get("approvals", []):
        if not isinstance(approval, dict) or approval.get("domain") != domain or approval.get("decision") != "APPROVED":
            continue
        approver_id = approval.get("approver_id")
        if approver_ids and approver_id not in approver_ids:
            continue
        identity = registry.get(approver_id)
        if not identity or identity.get("active") is not True or role not in identity.get("roles", []):
            continue
        if not identity.get("authority_evidence_ref") or not approval.get("approved_at"):
            continue
        if not approval.get("signature_evidence_ref"):
            continue
        bound = set(approval.get("artifact_hashes", []))
        if hashes and not hashes.issubset(bound):
            continue
        refs = [identity["authority_evidence_ref"], approval["signature_evidence_ref"]]
        refs.extend(_evidence_refs(approval.get("evidence_refs")))
        return True, f"{domain} approval structurally matches active approver registry", refs
    return False, f"No hash-bound {domain} approval from an active approver with required role {role}", []


def _source_map(project: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {x.get("source_id"): x for x in project.get("sources", []) if isinstance(x, dict) and x.get("source_id")}


def _claim_map(project: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {x.get("claim_id"): x for x in project.get("claims", []) if isinstance(x, dict) and x.get("claim_id")}


def _control(project: dict[str, Any], control_id: str) -> dict[str, Any]:
    """Run one named deterministic control and return an auditable observation."""
    if control_id == "CTRL-INTAKE-INVENTORY":
        intake = project.get("intake")
        inputs = intake.get("inputs") if isinstance(intake, dict) else None
        if not isinstance(inputs, list) or not inputs:
            return _missing(control_id, "intake.inputs")
        bad = [i for i, x in enumerate(inputs) if not isinstance(x, dict) or not all(x.get(k) for k in ("input_id", "input_type", "origin"))]
        if bad:
            return _out(control_id, "FAIL", "Each intake input needs input_id, input_type and origin", {"invalid_indexes": bad})
        return _out(control_id, "PASS", "All intake inputs are inventoried", {"count": len(inputs)}, [f"engine://{control_id}/inventory"])

    if control_id == "CTRL-PRIVACY-CLASSIFICATION":
        value = project.get("privacy_classification")
        if value not in PRIVACY_CLASSES:
            return _out(control_id, "BLOCKED", "Project privacy classification is missing or UNKNOWN", {"privacy_classification": value})
        return _out(control_id, "PASS", "Privacy classification uses a controlled value", {"privacy_classification": value}, [f"engine://{control_id}/classification"])

    if control_id == "CTRL-RIGHTS-BASIS":
        rights = project.get("rights", {})
        state = rights.get("status") if isinstance(rights, dict) else None
        refs = _evidence_refs(rights.get("evidence_refs")) if isinstance(rights, dict) else []
        rationale = rights.get("not_applicable_rationale") if isinstance(rights, dict) else None
        if state == "NOT_APPLICABLE":
            if rationale:
                return _out(control_id, "NOT_APPLICABLE", rationale, {"status": state})
            return _out(control_id, "FAIL", "NOT_APPLICABLE rights status requires a rationale", {"status": state})
        if state != "CLEARED" or not refs:
            return _out(control_id, "BLOCKED", "Rights must be CLEARED with evidence refs before production", {"status": state, "evidence_refs": refs})
        return _out(control_id, "PASS", "Rights status is CLEARED with recorded evidence references", {"status": state}, refs)

    if control_id == "CTRL-UNTRUSTED-INPUTS":
        items = project.get("untrusted_inputs")
        if not isinstance(items, list):
            return _missing(control_id, "untrusted_inputs")
        if not items:
            rationale = project.get("no_untrusted_inputs_rationale")
            if rationale:
                return _out(control_id, "NOT_APPLICABLE", rationale)
            return _out(control_id, "BLOCKED", "Empty untrusted_inputs requires explicit rationale")
        invalid = []
        base = Path(project.get("project_root", ROOT)).resolve()
        for i, item in enumerate(items):
            if not isinstance(item, dict) or not item.get("origin") or not is_sha256(item.get("content_hash")) or item.get("delimited") is not True or item.get("treat_as_data") is not True:
                invalid.append(i)
                continue
            observed_hash = None
            if isinstance(item.get("content"), str):
                observed_hash = sha256_bytes(item["content"].encode("utf-8"))
            elif safe_relative_path(item.get("snapshot_path")):
                snapshot = (base / item["snapshot_path"]).resolve()
                try:
                    snapshot.relative_to(base)
                except ValueError:
                    invalid.append(i)
                    continue
                if snapshot.is_file():
                    observed_hash = sha256_bytes(snapshot.read_bytes())
            if observed_hash != item["content_hash"]:
                invalid.append(i)
        if invalid:
            return _out(control_id, "FAIL", "Untrusted inputs must carry origin, byte-verifiable SHA-256, explicit delimiting and data-only treatment", {"invalid_indexes": invalid})
        return _out(control_id, "PASS", "All untrusted inputs are provenance-tagged and isolated as data", {"count": len(items)}, [f"engine://{control_id}/inventory"])

    if control_id == "CTRL-CLAIM-SCHEMA":
        claims = project.get("claims")
        if not isinstance(claims, list) or not claims:
            return _missing(control_id, "claims")
        all_errors = []
        for claim in claims:
            if not isinstance(claim, dict):
                all_errors.append("claim entry is not an object")
                continue
            all_errors.extend(f"{claim.get('claim_id', '<missing>')}: {e}" for e in validate_record(claim, "claim-record"))
        if all_errors:
            return _out(control_id, "FAIL", "One or more claim records violate the schema or semantic contract", {"errors": all_errors})
        return _out(control_id, "PASS", "All claim records satisfy schema and semantic constraints", {"count": len(claims)}, [f"engine://{control_id}/schema-validation"])

    if control_id == "CTRL-SOURCE-PROVENANCE":
        claims = project.get("claims")
        sources = _source_map(project)
        if not isinstance(claims, list) or not claims:
            return _missing(control_id, "claims")
        missing = []
        malformed = []
        for claim in claims:
            if not isinstance(claim, dict):
                continue
            for sid in claim.get("source_ids", []):
                source = sources.get(sid)
                if not source:
                    missing.append(sid)
                elif not source.get("source_uri") or not source.get("retrieved_at") or not is_sha256(source.get("source_hash")):
                    malformed.append(sid)
                elif source.get("source_hash") not in claim.get("source_hashes", []):
                    malformed.append(sid)
                elif isinstance(source.get("snapshot_text"), str):
                    if sha256_bytes(source["snapshot_text"].encode("utf-8")) != source["source_hash"]:
                        malformed.append(sid)
                elif source.get("snapshot_path"):
                    base = Path(project.get("project_root", ROOT)).resolve()
                    p = (base / source["snapshot_path"]).resolve()
                    try:
                        p.relative_to(base)
                    except ValueError:
                        malformed.append(sid)
                        continue
                    if not p.is_file() or sha256_bytes(p.read_bytes()) != source["source_hash"]:
                        malformed.append(sid)
                else:
                    malformed.append(sid)
        if missing or malformed:
            return _out(control_id, "FAIL", "Source references are missing or provenance metadata/hash is invalid", {"missing_source_ids": sorted(set(missing)), "invalid_source_ids": sorted(set(malformed))})
        return _out(control_id, "PASS", "All claim source references resolve to provenance records", {"source_count": len(sources)}, [f"engine://{control_id}/provenance-check"])

    if control_id == "CTRL-MATERIAL-CLAIMS":
        claims = project.get("claims")
        if not isinstance(claims, list) or not claims:
            return _missing(control_id, "claims")
        blocked = [x.get("claim_id") for x in claims if isinstance(x, dict) and (x.get("status") in CLAIM_BLOCKING or x.get("evidence_level") == "UNVERIFIED")]
        partial = [x.get("claim_id") for x in claims if isinstance(x, dict) and x.get("status") in {"PARTIALLY_SUPPORTED", "MIXED"}]
        if blocked:
            return _out(control_id, "BLOCKED", "Material unverified, contradicted, unknown or stale claims prevent Fact Lock", {"blocked_claim_ids": blocked})
        if partial:
            held = [x.get("claim_id") for x in claims if isinstance(x, dict) and x.get("status") in {"PARTIALLY_SUPPORTED", "MIXED"} and not x.get("allowed_wording")]
            if held:
                return _out(control_id, "BLOCKED", "Partially supported or mixed claims require constrained allowed_wording", {"claim_ids": held})
        return _out(control_id, "PASS", "No claim is in a fail-closed evidence state", {"claim_count": len(claims)}, [f"engine://{control_id}/claim-ledger"])

    if control_id == "CTRL-CLINICAL-APPROVAL":
        claims = project.get("claims", [])
        material = [c for c in claims if isinstance(c, dict) and c.get("claim_type") in MATERIAL_CLAIM_TYPES]
        if not material:
            rationale = project.get("no_material_health_claims_rationale")
            return _out(control_id, "NOT_APPLICABLE", rationale, {"material_claims": 0}) if rationale else _out(control_id, "BLOCKED", "No material health claims found; explicit N/A rationale is required")
        unreviewed = [c.get("claim_id") for c in material if c.get("reviewed_by_human") is not True or c.get("reviewer_role") != "CLINICIAN" or not c.get("reviewer_id") or not c.get("reviewed_at")]
        if unreviewed:
            return _out(control_id, "BLOCKED", "Every material health claim requires a named clinical review record", {"claim_ids": unreviewed})
        approval_refs = []
        missing_claims = []
        for claim in material:
            claim_hashes = {h for h in claim.get("source_hashes", []) if is_sha256(h)}
            reviewer_ids = {claim.get("reviewer_id")} if claim.get("reviewer_id") else set()
            ok, reason, refs = _valid_approval(project, "CLINICAL", "CLINICIAN", claim_hashes, reviewer_ids)
            if not ok:
                missing_claims.append(claim.get("claim_id"))
            else:
                approval_refs.extend(refs)
        if missing_claims:
            return _out(control_id, "BLOCKED", "Every material claim must have its own reviewer-matched, source-hash-bound clinical approval", {"claim_ids": missing_claims})
        return _out(control_id, "PASS", "Every material claim has a reviewer-matched, source-hash-bound clinical approval", {"reviewed_claims": len(material)}, sorted(set(approval_refs)))

    if control_id == "CTRL-NARRATIVE-TRACEABILITY":
        lines = project.get("narrative_lines")
        claims = _claim_map(project)
        if not isinstance(lines, list) or not lines:
            return _missing(control_id, "narrative_lines")
        problems = []
        for i, line in enumerate(lines):
            if not isinstance(line, dict) or not isinstance(line.get("claim_refs"), list) or not line.get("claim_refs"):
                problems.append(f"line[{i}] has no claim_refs")
            elif any(cid not in claims for cid in line["claim_refs"]):
                problems.append(f"line[{i}] references unknown claims")
        if problems:
            return _out(control_id, "FAIL", "Narrative lines must trace to known claim IDs", {"problems": problems})
        return _out(control_id, "PASS", "Every narrative line is traceable to the claim ledger", {"line_count": len(lines)}, [f"engine://{control_id}/traceability"])

    if control_id == "CTRL-SAFE-WORDING":
        lines = project.get("narrative_lines")
        claims = _claim_map(project)
        if not isinstance(lines, list) or not lines:
            return _missing(control_id, "narrative_lines")
        problems = []
        for i, line in enumerate(lines):
            if not isinstance(line, dict):
                problems.append(f"line[{i}] is not an object")
                continue
            text = re.sub(r"\s+", " ", str(line.get("text", "")).strip()).casefold()
            for cid in line.get("claim_refs", []):
                claim = claims.get(cid, {})
                allowed = [re.sub(r"\s+", " ", str(x).strip()).casefold() for x in claim.get("allowed_wording", [])]
                forbidden = [re.sub(r"\s+", " ", str(x).strip()).casefold() for x in claim.get("forbidden_wording", [])]
                if any(term and term in text for term in forbidden):
                    problems.append(f"line[{i}] contains forbidden wording for {cid}")
                if not allowed or not any(text == phrase for phrase in allowed):
                    problems.append(f"line[{i}] does not exactly match an allowed phrase for {cid}")
        if problems:
            return _out(control_id, "BLOCKED", "Narrative wording exceeds or deviates from claim-approved wording", {"problems": problems})
        return _out(control_id, "PASS", "All narrative claim wording matches an approved phrase exactly", {"line_count": len(lines)}, [f"engine://{control_id}/wording-check"])

    if control_id == "CTRL-CONTINUITY-LOCKS":
        lock = project.get("continuity_lock")
        if not isinstance(lock, dict):
            return _missing(control_id, "continuity_lock")
        if lock.get("status") != "LOCKED" or not lock.get("canon_version") or not is_sha256(lock.get("content_hash")) or not _evidence_refs(lock.get("evidence_refs")):
            return _out(control_id, "BLOCKED", "Continuity lock requires LOCKED status, version, SHA-256 and evidence", {"status": lock.get("status")})
        return _out(control_id, "PASS", "Continuity canon is hash-locked", {"canon_version": lock["canon_version"]}, _evidence_refs(lock.get("evidence_refs")))

    if control_id == "CTRL-VISUAL-REFERENCES":
        scenes = project.get("scenes")
        refs = {r.get("reference_id") for r in project.get("reference_assets", []) if isinstance(r, dict) and r.get("reference_id")}
        if not isinstance(scenes, list) or not scenes:
            return _missing(control_id, "scenes")
        missing = []
        for scene in scenes:
            ids = scene.get("reference_ids", []) if isinstance(scene, dict) else []
            if not ids or any(x not in refs for x in ids):
                missing.append(scene.get("scene_id", "<unknown>") if isinstance(scene, dict) else "<invalid>")
        if missing:
            return _out(control_id, "BLOCKED", "Every scene requires resolvable visual reference IDs", {"scene_ids": missing})
        return _out(control_id, "PASS", "All scene reference IDs resolve", {"scene_count": len(scenes)}, [f"engine://{control_id}/reference-index"])

    if control_id == "CTRL-PROMPT-INJECTION":
        prompts = project.get("prompts")
        if not isinstance(prompts, list) or not prompts:
            return _missing(control_id, "prompts")
        hits = []
        for i, item in enumerate(prompts):
            if not isinstance(item, dict):
                hits.append(f"prompt[{i}] is not an object")
                continue
            body = str(item.get("trusted_instructions", ""))
            for pattern_label in detect_prompt_injection(body):
                hits.append(f"prompt[{i}] matched heuristic {pattern_label}")
        if hits:
            return _out(control_id, "BLOCKED", "Potential instruction-smuggling text detected in trusted instruction area; heuristic requires human inspection", {"hits": hits})
        return _out(control_id, "PASS", "No configured injection heuristic matched trusted instruction fields (not a proof of safety)", {"prompt_count": len(prompts)}, [f"engine://{control_id}/heuristic-scan"])

    if control_id == "CTRL-PROMPT-BOUNDARY":
        prompts = project.get("prompts")
        if not isinstance(prompts, list) or not prompts:
            return _missing(control_id, "prompts")
        bad = []
        for i, item in enumerate(prompts):
            if not isinstance(item, dict):
                bad.append(i)
            elif item.get("untrusted_payloads") and (item.get("boundary_markers") != ["<UNTRUSTED_SOURCE>", "</UNTRUSTED_SOURCE>"] or item.get("treat_payload_as_data") is not True):
                bad.append(i)
        if bad:
            return _out(control_id, "FAIL", "Untrusted prompt payloads need canonical delimiters and data-only instruction", {"prompt_indexes": bad})
        return _out(control_id, "PASS", "Prompt records preserve trusted/untrusted instruction boundaries", {"prompt_count": len(prompts)}, [f"engine://{control_id}/boundary-check"])

    if control_id == "CTRL-SCENE-TIMING":
        scenes = project.get("scenes")
        if not isinstance(scenes, list) or not scenes:
            return _missing(control_id, "scenes")
        errors = [f"scene[{i}] is not an object" for i, scene in enumerate(scenes) if not isinstance(scene, dict)]
        rows = sorted((x for x in scenes if isinstance(x, dict)), key=lambda x: (x.get("order", -1), x.get("start_frame", -1)))
        fps_values = set()
        for i, scene in enumerate(rows):
            start, end, fps = scene.get("start_frame"), scene.get("end_frame"), scene.get("fps")
            if isinstance(start, bool) or isinstance(end, bool) or isinstance(fps, bool) or not isinstance(start, int) or not isinstance(end, int) or not isinstance(fps, (int, float)) or start < 0 or end <= start or fps <= 0:
                errors.append(f"scene {scene.get('scene_id', i)} has invalid frame/fps values")
            if isinstance(fps, (int, float)):
                fps_values.add(fps)
            if i == 0 and start != 0:
                errors.append("first scene must start at frame 0")
            if i > 0:
                previous = rows[i - 1]
                if isinstance(previous, dict) and isinstance(start, int) and isinstance(previous.get("end_frame"), int):
                    if start != previous["end_frame"]:
                        errors.append(f"gap or overlap between {previous.get('scene_id')} and {scene.get('scene_id')}")
        if len(fps_values) > 1:
            errors.append("all scenes must use one project fps/timebase")
        if errors:
            return _out(control_id, "FAIL", "Scene timing arithmetic is invalid", {"errors": errors})
        return _out(control_id, "PASS", "Scene frame ranges are contiguous, positive and use one fps", {"scene_count": len(rows), "fps": next(iter(fps_values))}, [f"engine://{control_id}/timing-validation"])

    if control_id == "CTRL-MANIFEST-INTEGRITY":
        manifest = project.get("manifest")
        if not isinstance(manifest, dict):
            return _missing(control_id, "manifest")
        errors = validate_record(manifest, "artifact-envelope")
        paths = manifest.get("asset_paths", [])
        unsafe = [p for p in paths if not safe_relative_path(p)]
        if unsafe:
            errors.append(f"unsafe asset paths: {unsafe}")
        if errors:
            return _out(control_id, "FAIL", "Manifest schema/hash/path validation failed", {"errors": errors})
        return _out(control_id, "PASS", "Manifest contract, canonical hash and asset paths validate", {"asset_count": len(paths)}, [f"engine://{control_id}/manifest-validation"])

    if control_id == "CTRL-CAPABILITY-VERIFICATION":
        renderer = project.get("renderer")
        if not isinstance(renderer, dict) or renderer.get("requested") is not True:
            rationale = renderer.get("not_requested_rationale") if isinstance(renderer, dict) else None
            return _out(control_id, "NOT_APPLICABLE", rationale, {"renderer_requested": False}) if rationale else _out(control_id, "BLOCKED", "Renderer not requested requires explicit N/A rationale")
        capability = next((x for x in project.get("capabilities", []) if isinstance(x, dict) and x.get("operation") == "render" and x.get("provider") == renderer.get("provider") and x.get("target") == renderer.get("target") and x.get("version") == renderer.get("version")), None)
        if not capability or capability.get("status") != "VERIFIED" or not capability.get("checked_at") or not _evidence_refs(capability.get("evidence_refs")):
            return _out(control_id, "BLOCKED", "Exact renderer/provider/version capability lacks VERIFIED status and evidence", {"renderer": renderer, "capability": capability})
        return _out(control_id, "PASS", "Exact renderer operation and version have recorded capability evidence", {"provider": renderer["provider"], "target": renderer["target"], "version": renderer["version"]}, _evidence_refs(capability.get("evidence_refs")))

    if control_id == "CTRL-CODE-STATIC":
        checks = project.get("code_checks")
        if not isinstance(checks, list) or not checks:
            return _missing(control_id, "code_checks")
        bad = [i for i, c in enumerate(checks) if not isinstance(c, dict) or c.get("status") != "PASS" or not c.get("test_id") or not c.get("command") or not c.get("executed_at") or not c.get("environment") or not _evidence_refs(c.get("evidence_refs"))]
        if bad:
            return _out(control_id, "BLOCKED", "Every static code check needs PASS, test_id and evidence refs", {"invalid_indexes": bad})
        return _out(control_id, "PASS", "All declared static code checks have evidence", {"check_count": len(checks)}, [f"engine://{control_id}/code-check-ledger"])

    if control_id == "CTRL-ARTIFACT-QA":
        artifacts = project.get("rendered_artifacts")
        if not isinstance(artifacts, list) or not artifacts:
            return _missing(control_id, "rendered_artifacts")
        bad = []
        for i, art in enumerate(artifacts):
            if not isinstance(art, dict) or not safe_relative_path(art.get("path")) or not is_sha256(art.get("sha256")) or art.get("inspected") is not True or art.get("qa_status") != "PASS" or not _evidence_refs(art.get("qa_evidence_refs")):
                bad.append(i)
                continue
            base = Path(project.get("project_root", ROOT)).resolve()
            p = (base / art["path"]).resolve()
            try:
                p.relative_to(base)
            except ValueError:
                bad.append(i)
                continue
            if not p.is_file() or sha256_bytes(p.read_bytes()) != art["sha256"]:
                bad.append(i)
        if bad:
            return _out(control_id, "BLOCKED", "Every rendered artifact needs a real in-root file, matching hash and inspectable QA evidence", {"invalid_indexes": bad})
        return _out(control_id, "PASS", "Rendered artifact hashes and QA records match local files", {"artifact_count": len(artifacts)}, [f"engine://{control_id}/artifact-qa"])

    if control_id == "CTRL-ACCESSIBILITY-QA":
        qa = project.get("accessibility_qa")
        if not isinstance(qa, dict) or not qa.get("standard"):
            return _missing(control_id, "accessibility_qa.standard")
        if qa.get("status") != "PASS" or not qa.get("scope") or not _evidence_refs(qa.get("evidence_refs")):
            return _out(control_id, "BLOCKED", "Accessibility QA needs named standard, scope, PASS and evidence refs", {"status": qa.get("status")})
        ok, reason, approval_refs = _valid_approval(project, "ACCESSIBILITY", "ACCESSIBILITY_REVIEWER")
        if not ok:
            return _out(control_id, "BLOCKED", reason, {"standard": qa["standard"], "scope": qa["scope"]})
        return _out(control_id, "PASS", "Accessibility QA and authorized reviewer record are evidence-linked", {"standard": qa["standard"], "scope": qa["scope"]}, _evidence_refs(qa.get("evidence_refs")) + approval_refs)

    if control_id == "CTRL-RELEASE-APPROVAL":
        hashes = {a.get("sha256") for a in project.get("rendered_artifacts", []) if isinstance(a, dict) and is_sha256(a.get("sha256"))}
        ok, reason, refs = _valid_approval(project, "RELEASE", "PRODUCER", hashes if hashes else None)
        if not ok:
            return _out(control_id, "BLOCKED", reason)
        return _out(control_id, "PASS", reason, {"hashes_bound": sorted(hashes)}, refs)

    return _out(control_id, "NOT_VERIFIED", "No evaluator is registered for this control ID")


def evaluate_project(project: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(project, dict):
        raise ValueError("Project input must be a JSON object")
    gate_results: list[dict[str, Any]] = []
    prior_status = "PASS"
    for gate_id in GATE_ORDER:
        control_results = []
        if prior_status != "PASS":
            gate_results.append({"gate_id": gate_id, "status": "BLOCKED", "reason": f"Predecessor gate did not PASS (status={prior_status})", "controls": []})
            prior_status = "BLOCKED"
            continue
        for control_id in CONTROL_IDS[gate_id]:
            control_results.append(_control(project, control_id))
        failing = [x for x in control_results if x["status"] == "FAIL"]
        blocked = [x for x in control_results if x["status"] == "BLOCKED"]
        unrun = [x for x in control_results if x["status"] in FAIL_CLOSED]
        invalid_na = [x for x in control_results if x["status"] == "NOT_APPLICABLE" and not x.get("reason")]
        if failing:
            status, reason = "FAIL", "One or more required controls failed"
        elif blocked:
            status, reason = "BLOCKED", "One or more required controls are blocked"
        elif unrun:
            status, reason = "NOT_RUN", "One or more required controls have not been executed or verified"
        elif invalid_na:
            status, reason = "FAIL", "NOT_APPLICABLE control has no rationale"
        elif all(x["status"] in PASSABLE for x in control_results):
            status, reason = "PASS", "All required controls passed or were explicitly not applicable with rationale"
        else:
            status, reason = "NOT_VERIFIED", "Gate status could not be established"
        gate_results.append({"gate_id": gate_id, "status": status, "reason": reason, "controls": control_results})
        prior_status = status
    all_pass = all(x["status"] == "PASS" for x in gate_results)
    return {
        "engine_id": ENGINE_ID,
        "engine_version": ENGINE_VERSION,
        "project_id": project.get("project_id"),
        "evaluated_at": utc_now(),
        "policy": "FAIL_CLOSED",
        "release_eligible": all_pass,
        "overall_status": "PASS" if all_pass else next((x["status"] for x in gate_results if x["status"] != "PASS"), "NOT_VERIFIED"),
        "gates": gate_results,
        "summary": {
            "gate_count": len(gate_results),
            "passed": sum(x["status"] == "PASS" for x in gate_results),
            "failed": sum(x["status"] == "FAIL" for x in gate_results),
            "blocked": sum(x["status"] == "BLOCKED" for x in gate_results),
            "not_run_or_unverified": sum(x["status"] in {"NOT_RUN", "NOT_VERIFIED", "IN_PROGRESS", "NOT_STARTED", "PARTIAL"} for x in gate_results),
        },
        "limitations": [
            "Structural approval records do not independently authenticate a person's identity or credentials.",
            "Prompt-injection scanning is heuristic and cannot prove prompt safety or model behavior.",
            "A PASS only covers controls evaluated by this engine against supplied data and evidence references.",
            "Live ChatGPT invocation, external AI/ASR/diarization, renderer runtime and media QA require separate real execution evidence.",
        ],
    }


def validate_dependency_graph(records: list[dict[str, Any]]) -> list[str]:
    errors = []
    ids = [x.get("artifact_id") for x in records if isinstance(x, dict)]
    if len(ids) != len(set(ids)):
        errors.append("duplicate artifact_id in dependency graph")
    known = set(ids)
    graph: dict[str, list[str]] = {}
    for item in records:
        if not isinstance(item, dict) or not item.get("artifact_id"):
            errors.append("dependency record missing artifact_id")
            continue
        deps = item.get("depends_on", [])
        if not isinstance(deps, list):
            errors.append(f"depends_on must be a list for {item['artifact_id']}")
            continue
        missing = [x for x in deps if x not in known]
        if missing:
            errors.append(f"unknown dependencies for {item['artifact_id']}: {missing}")
        graph[item["artifact_id"]] = deps
    visiting: set[str] = set()
    visited: set[str] = set()
    def visit(node: str) -> bool:
        if node in visiting:
            return True
        if node in visited:
            return False
        visiting.add(node)
        for dep in graph.get(node, []):
            if dep in graph and visit(dep):
                return True
        visiting.remove(node)
        visited.add(node)
        return False
    for node in graph:
        if visit(node):
            errors.append("dependency graph contains a cycle")
            break
    return errors


def invalidation_plan(records: list[dict[str, Any]], changed_ids: list[str]) -> list[str]:
    errors = validate_dependency_graph(records)
    if errors:
        raise ValueError("; ".join(errors))
    known = {x["artifact_id"] for x in records}
    unknown = sorted(set(changed_ids) - known)
    if unknown:
        raise ValueError(f"Unknown changed artifact IDs: {unknown}")
    dependents: dict[str, set[str]] = {x: set() for x in known}
    for item in records:
        for dep in item.get("depends_on", []):
            dependents[dep].add(item["artifact_id"])
    invalidated = set()
    frontier = list(changed_ids)
    while frontier:
        node = frontier.pop()
        for child in dependents[node]:
            if child not in invalidated and child not in changed_ids:
                invalidated.add(child)
                frontier.append(child)
    return sorted(invalidated)


def _load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    for command, kind in (("validate-claim", "claim-record"), ("validate-artifact", "artifact-envelope")):
        p = sub.add_parser(command)
        p.add_argument("--input", required=True, type=Path)
    p = sub.add_parser("evaluate")
    p.add_argument("--project", required=True, type=Path)
    p.add_argument("--output", type=Path)
    p.add_argument("--require-release", action="store_true", help="Exit non-zero unless all eight gates PASS")
    p = sub.add_parser("invalidation-plan")
    p.add_argument("--project", required=True, type=Path)
    p.add_argument("--changed", required=True, nargs="+")
    p.add_argument("--output", type=Path)
    p = sub.add_parser("hash")
    p.add_argument("--input", required=True, type=Path)
    args = parser.parse_args(argv)
    try:
        if args.command in {"validate-claim", "validate-artifact"}:
            kind = "claim-record" if args.command == "validate-claim" else "artifact-envelope"
            record = _load_json(args.input)
            errors = validate_record(record, kind)
            if errors:
                print(json.dumps({"status": "FAIL", "errors": errors}, indent=2))
                return 1
            print(json.dumps({"status": "PASS", "kind": kind, "engine_version": ENGINE_VERSION}, indent=2))
            return 0
        if args.command == "evaluate":
            report = evaluate_project(_load_json(args.project))
            if args.output:
                _write_json(args.output, report)
            print(json.dumps(report, ensure_ascii=False, indent=2))
            return 1 if args.require_release and not report["release_eligible"] else 0
        if args.command == "invalidation-plan":
            project = _load_json(args.project)
            items = project.get("dependency_graph", [])
            plan = {"changed": args.changed, "invalidated_dependents": invalidation_plan(items, args.changed), "status": "PLAN_ONLY_NO_MUTATION"}
            if args.output:
                _write_json(args.output, plan)
            print(json.dumps(plan, indent=2))
            return 0
        if args.command == "hash":
            print(content_hash(_load_json(args.input)))
            return 0
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
