from __future__ import annotations

import base64
import binascii
import hashlib
import json
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey
from jsonschema import Draft202012Validator, FormatChecker

from .common import canonical_json_bytes, parse_datetime, resolved_inside


class TrustError(ValueError):
    """Trust registry or approval verification failed closed."""


@dataclass(frozen=True)
class Authority:
    approver_id: str
    role: str
    key_id: str
    public_key_b64: str
    active: bool
    valid_from: str
    valid_to: str
    credential_ref: str
    credential_status: str
    credential_verified_at: str
    issuer_ref: str


class TrustRegistry:
    """Externally pinned, root-signed authority registry.

    The registry file must not reside inside the project being audited. The
    pinned root public key is supplied by deployment configuration, never by
    the project payload. The registry signature is checked over canonical JSON
    excluding only `root_signature`.
    """

    def __init__(self, authorities: list[Authority], revoked_key_ids: set[str],
                 registry_id: str, root_fingerprint: str, valid_to: str,
                 resource_profiles: dict[str, dict[str, str]] | None = None):
        self.registry_id = registry_id
        self.root_fingerprint = root_fingerprint
        self.valid_to = valid_to
        self.resource_profiles = dict(resource_profiles or {})
        self._revoked = set(revoked_key_ids)
        self._by_role_key: dict[tuple[str, str], Authority] = {}
        # One human may legitimately hold more than one authorized role/key.
        # Quorum logic deduplicates approver_id across accepted approvals, so
        # multiple role records cannot inflate the distinct-human count.
        for item in authorities:
            key = (item.role, item.key_id)
            if key in self._by_role_key:
                raise TrustError(f"duplicate role/key entry: {key}")
            self._by_role_key[key] = item

    @classmethod
    def load(cls, path: Path, *, pinned_root_public_key_b64: str,
             project_root: Path | None = None, now: datetime | None = None) -> "TrustRegistry":
        path = Path(path)
        if project_root is not None and resolved_inside(path, Path(project_root)):
            raise TrustError("trust registry must be outside the project root")
        try:
            raw = path.read_bytes()
            doc = json.loads(raw)
        except (OSError, json.JSONDecodeError) as exc:
            raise TrustError(f"cannot read external trust registry: {exc}") from exc
        if not isinstance(doc, dict):
            raise TrustError("trust registry root must be an object")
        schema_path = Path(__file__).resolve().parents[2] / "schemas/v4/trust-registry.schema.json"
        try:
            schema = json.loads(schema_path.read_text(encoding="utf-8"))
            Draft202012Validator.check_schema(schema)
            schema_errors = list(Draft202012Validator(schema, format_checker=FormatChecker()).iter_errors(doc))
        except Exception as exc:
            raise TrustError(f"cannot load external trust registry schema: {type(exc).__name__}") from exc
        if schema_errors:
            raise TrustError("external trust registry schema invalid: " + "; ".join(e.message for e in schema_errors[:5]))
        signature_b64 = doc.get("root_signature")
        body = {k: v for k, v in doc.items() if k != "root_signature"}
        try:
            root_key_bytes = base64.b64decode(pinned_root_public_key_b64, validate=True)
            signature = base64.b64decode(signature_b64 or "", validate=True)
            root_key = Ed25519PublicKey.from_public_bytes(root_key_bytes)
        except (ValueError, binascii.Error, TypeError) as exc:
            raise TrustError("invalid externally pinned root key or registry signature encoding") from exc
        fingerprint = "sha256:" + hashlib.sha256(root_key_bytes).hexdigest()
        declared_pin = doc.get("root_fingerprint")
        if declared_pin != fingerprint:
            raise TrustError("registry root fingerprint does not match external pin")
        try:
            root_key.verify(signature, canonical_json_bytes(body))
        except InvalidSignature as exc:
            raise TrustError("external trust registry root signature is invalid") from exc
        except Exception as exc:
            raise TrustError(f"trust registry signature verification failed: {type(exc).__name__}") from exc

        now = (now or datetime.now(timezone.utc)).astimezone(timezone.utc)
        not_before = parse_datetime(doc.get("valid_from"))
        not_after = parse_datetime(doc.get("valid_to"))
        if not not_before or not not_after:
            raise TrustError("registry validity interval is missing or invalid")
        if now < not_before or now >= not_after:
            raise TrustError("external trust registry is not currently valid")

        required_top = {"registry_id", "registry_version", "valid_from", "valid_to",
                        "root_fingerprint", "authorities", "revoked_key_ids", "root_signature"}
        missing = required_top - set(doc)
        if missing:
            raise TrustError(f"trust registry missing fields: {sorted(missing)}")
        authorities = []
        for row in doc.get("authorities", []):
            try:
                authority = Authority(**row)
            except (TypeError, KeyError) as exc:
                raise TrustError(f"invalid authority record: {exc}") from exc
            credential_verified_at = parse_datetime(authority.credential_verified_at)
            if (authority.credential_status != "VERIFIED" or not authority.credential_ref
                    or not authority.issuer_ref or not credential_verified_at):
                raise TrustError(f"authority {authority.approver_id} lacks valid externally verified credential metadata")
            if credential_verified_at > now:
                raise TrustError(f"authority {authority.approver_id} credential verification is future-dated")
            authorities.append(authority)
        resource_rows = doc.get("resource_profiles", [])
        if not isinstance(resource_rows, list):
            raise TrustError("resource_profiles must be a list")
        resource_profiles: dict[str, dict[str, str]] = {}
        for row in resource_rows:
            if not isinstance(row, dict):
                raise TrustError("resource profile trust record must be an object")
            profile_id, route, content_hash = row.get("profile_id"), row.get("route"), row.get("content_hash")
            required_categories = row.get("required_categories")
            allowed_categories = {"provider_cost", "render_seconds", "memory_mb", "asset_bytes", "retry_count", "cpu_seconds"}
            if (not isinstance(profile_id, str) or not profile_id.strip()
                    or not isinstance(route, str) or not route.strip()
                    or not isinstance(content_hash, str)
                    or not re.fullmatch(r"sha256:[a-fA-F0-9]{64}", content_hash)
                    or not isinstance(required_categories, list)
                    or len(required_categories) != len(set(required_categories))
                    or not set(required_categories).issubset(allowed_categories)):
                raise TrustError("resource profile trust record needs profile_id, route, SHA-256 content_hash and valid required_categories")
            if profile_id in resource_profiles:
                raise TrustError(f"duplicate trusted resource profile: {profile_id}")
            resource_profiles[profile_id] = {"route": route, "content_hash": content_hash.lower(),
                                             "required_categories": sorted(required_categories)}
        return cls(authorities, set(doc.get("revoked_key_ids", [])),
                   doc["registry_id"], fingerprint, doc["valid_to"], resource_profiles)

    def authority(self, role: str, key_id: str, *, now: datetime | None = None) -> Authority:
        now = (now or datetime.now(timezone.utc)).astimezone(timezone.utc)
        if key_id in self._revoked:
            raise TrustError(f"key revoked: {key_id}")
        auth = self._by_role_key.get((role, key_id))
        if auth is None:
            raise TrustError(f"key is not registered for role {role}: {key_id}")
        if not auth.active:
            raise TrustError(f"authority inactive: {auth.approver_id}")
        valid_from, valid_to = parse_datetime(auth.valid_from), parse_datetime(auth.valid_to)
        if not valid_from or not valid_to or now < valid_from or now >= valid_to:
            raise TrustError(f"authority expired or outside validity: {auth.approver_id}")
        if auth.credential_status != "VERIFIED" or not auth.credential_ref:
            raise TrustError(f"authority credential not verified: {auth.approver_id}")
        return auth


def approval_payload(approval: dict[str, Any]) -> bytes:
    keys = ("approval_id", "approver_id", "role", "decision", "artifact_hashes",
            "signing_key_id", "created_at", "expires_at", "scope")
    return canonical_json_bytes({k: approval.get(k) for k in keys})


def verify_approval(approval: dict[str, Any], registry: TrustRegistry, *,
                    required_hashes: set[str] | None = None,
                    known_hashes: set[str] | None = None,
                    required_scope: str | None = None,
                    now: datetime | None = None) -> tuple[bool, str]:
    now = (now or datetime.now(timezone.utc)).astimezone(timezone.utc)
    if not isinstance(approval, dict) or approval.get("decision") != "APPROVED":
        return False, "approval is not APPROVED"
    created = parse_datetime(approval.get("created_at"))
    expires = parse_datetime(approval.get("expires_at"))
    if not created or not expires or created > now or expires <= now:
        return False, "approval timestamp missing, invalid, future-dated or expired"
    role, key_id = approval.get("role"), approval.get("signing_key_id")
    try:
        authority = registry.authority(role, key_id, now=now)
    except TrustError as exc:
        return False, str(exc)
    if approval.get("approver_id") != authority.approver_id:
        return False, "approver identity does not match externally registered key owner"
    if required_scope is not None and approval.get("scope") != required_scope:
        return False, f"approval scope must be {required_scope}"
    hashes = set(approval.get("artifact_hashes") or [])
    if not hashes:
        return False, "approval is not bound to any artifact hash"
    if required_hashes and not required_hashes.issubset(hashes):
        return False, "approval does not bind all required artifact hashes"
    if known_hashes is not None and not hashes.issubset(known_hashes):
        return False, "approval binds unknown artifact hashes"
    try:
        pub = Ed25519PublicKey.from_public_bytes(base64.b64decode(authority.public_key_b64, validate=True))
        sig = base64.b64decode(approval.get("signature", ""), validate=True)
        pub.verify(sig, approval_payload(approval))
    except InvalidSignature:
        return False, "approval signature is invalid"
    except (ValueError, TypeError, binascii.Error):
        return False, "approval key/signature encoding is invalid"
    return True, f"verified against externally pinned registry {registry.registry_id}"


def release_quorum(approvals: list[dict[str, Any]], registry: TrustRegistry, *,
                   required_hashes: set[str], required_roles: tuple[str, ...],
                   known_hashes: set[str] | None = None,
                   min_distinct_humans: int = 2,
                   now: datetime | None = None) -> tuple[bool, list[str]]:
    reasons: list[str] = []
    approved_by_role: dict[str, set[str]] = {r: set() for r in required_roles}
    # Never derive the allow-list from the approvals being validated. If the
    # caller has no external artifact inventory, only the explicitly required
    # immutable hashes are recognized.
    known = set(known_hashes) if known_hashes is not None else set(required_hashes)
    if not required_hashes or not required_hashes.issubset(known):
        return False, ["externally known artifact hash set is missing required release hashes"]
    for approval in approvals:
        ok, detail = verify_approval(approval, registry, required_hashes=required_hashes,
                                     known_hashes=known, required_scope="RELEASE", now=now)
        if not ok:
            reasons.append(f"{approval.get('approval_id', '<unknown>')}: {detail}")
            continue
        role = approval.get("role")
        if role in approved_by_role:
            approved_by_role[role].add(approval["approver_id"])
    for role in required_roles:
        if not approved_by_role[role]:
            reasons.append(f"missing valid approval for role {role}")
    all_humans = set().union(*approved_by_role.values()) if approved_by_role else set()
    if len(all_humans) < min_distinct_humans:
        reasons.append(f"distinct human quorum not met: {len(all_humans)}/{min_distinct_humans}")
    return not reasons, reasons
