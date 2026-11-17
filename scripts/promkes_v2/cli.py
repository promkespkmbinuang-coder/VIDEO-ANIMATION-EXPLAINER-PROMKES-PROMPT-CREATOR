from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker

from .firewall import intake_preflight, rescan_at_boundary
from .handoff import validate_handoff
from .registry import validate_registry
from .evidence import verify_source_snapshot
from .resource import evaluate_resource_budget
from .common import sha256_bytes, resolved_inside


def _read(path: Path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Promkes V2 deterministic enforcement CLI")
    sub = ap.add_subparsers(dest="command", required=True)
    p = sub.add_parser("scan-intake"); p.add_argument("input", type=Path); p.add_argument("--output", type=Path)
    p = sub.add_parser("scan-boundary"); p.add_argument("input", type=Path); p.add_argument("--output", type=Path)
    p = sub.add_parser("validate-handoff"); p.add_argument("handoff", type=Path); p.add_argument("--schema", type=Path, default=Path("schemas/v4/handoff-envelope.schema.json")); p.add_argument("--artifact-index", type=Path, required=True); p.add_argument("--artifact-index-sha256", required=True); p.add_argument("--project-root", type=Path, required=True); p.add_argument("--expected-producer", required=True); p.add_argument("--dependency-statuses", type=Path)
    p = sub.add_parser("validate-control-registry"); p.add_argument("--registry", type=Path, default=Path("schemas/v4/control-registry.v2.json"))
    p = sub.add_parser("verify-snapshot"); p.add_argument("snapshot", type=Path); p.add_argument("--expected-hash", required=True); p.add_argument("--source-uri", required=True); p.add_argument("--support-location", required=True); p.add_argument("--accessed-at", required=True)
    p = sub.add_parser("check-budget"); p.add_argument("input", type=Path); p.add_argument("--trust-registry", type=Path, required=True); p.add_argument("--pinned-root-key", required=True); p.add_argument("--project-root", type=Path, required=True)
    p = sub.add_parser("run-acceptance"); p.add_argument("--all-regression", action="store_true")
    args = ap.parse_args(argv)

    if args.command == "scan-intake":
        data = _read(args.input); result = intake_preflight(data.get("sources", []))
    elif args.command == "scan-boundary":
        data = _read(args.input); result = rescan_at_boundary(data.get("text", ""))
    elif args.command == "validate-handoff":
        errors = []
        try:
            if resolved_inside(args.artifact_index, args.project_root):
                raise ValueError("artifact index must be externally managed outside the project root")
            actual_index_hash = sha256_bytes(args.artifact_index.read_bytes())
            if actual_index_hash.lower() != args.artifact_index_sha256.lower():
                raise ValueError("external artifact index hash does not match runtime pin")
            index = _read(args.artifact_index)
            dependencies = _read(args.dependency_statuses) if args.dependency_statuses else {}
            errors = validate_handoff(_read(args.handoff), args.schema,
                                      expected_producer=args.expected_producer,
                                      artifact_index=index, artifact_root=args.project_root,
                                      dependency_statuses=dependencies)
        except (ValueError, TypeError, OSError, json.JSONDecodeError) as exc:
            errors = [f"external handoff validation context invalid: {type(exc).__name__}: {exc}"]
        result = {"status": "FAIL" if errors else "PASS", "errors": errors}
    elif args.command == "validate-control-registry":
        errors = validate_registry(args.registry)
        result = {"status": "FAIL" if errors else "PASS", "errors": errors}
    elif args.command == "verify-snapshot":
        from .evidence import verify_source_snapshot
        check = verify_source_snapshot(args.snapshot, args.expected_hash, source_uri=args.source_uri,
                                       support_location=args.support_location, accessed_at=args.accessed_at)
        result = {"status": check.status, "observed_hash": check.observed_hash, "reasons": list(check.reasons)}
    elif args.command == "check-budget":
        from .trust import TrustRegistry, TrustError
        data = _read(args.input)
        try:
            profile = data.get("profile")
            if profile is not None:
                profile_schema = _read(Path("schemas/v4/resource-profile-v2.schema.json"))
                Draft202012Validator.check_schema(profile_schema)
                profile_errors = list(Draft202012Validator(profile_schema, format_checker=FormatChecker()).iter_errors(profile))
                if profile_errors:
                    raise ValueError("resource profile schema invalid: " + "; ".join(e.message for e in profile_errors[:5]))
            registry = TrustRegistry.load(args.trust_registry,
                                          pinned_root_public_key_b64=args.pinned_root_key,
                                          project_root=args.project_root)
            result = evaluate_resource_budget(data["route"], data.get("profile"), data.get("usage"),
                                              set(data.get("required_categories", [])),
                                              trusted_profile_records=registry.resource_profiles)
        except (TrustError, KeyError, ValueError, TypeError, OSError, json.JSONDecodeError) as exc:
            result = {"status": "BLOCKED", "reason": f"external resource trust registry unavailable or invalid: {type(exc).__name__}"}
    elif args.command == "run-acceptance":
        tests = ["tests/test_v2_acceptance.py"]
        if args.all_regression:
            tests = ["tests"]
        env = dict(os.environ); env["PYTHONPATH"] = "." + (os.pathsep + env["PYTHONPATH"] if env.get("PYTHONPATH") else "")
        return subprocess.run([sys.executable, "-m", "pytest", "-q", *tests], env=env).returncode
    else:
        return 2

    rendered = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    if getattr(args, "output", None):
        args.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
    return 0 if result.get("status") in {"PASS", "PASS_WITH_ISOLATION", "NO_PATTERN_MATCH", "NOT_APPLICABLE"} else 1
