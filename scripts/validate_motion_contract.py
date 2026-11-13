#!/usr/bin/env python3
"""Validate Promkes V4 renderer-neutral motion and AI-video adapter records."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
MOTION_SCHEMA = ROOT / "schemas/v4/motion-record.schema.json"
ADAPTER_SCHEMA = ROOT / "schemas/v4/video-platform-adapter.schema.json"


def schema_errors(instance: dict[str, Any], schema_path: Path) -> list[str]:
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    return [f"{error.json_path}: {error.message}" for error in validator.iter_errors(instance)]


def validate_motion_record(record: dict[str, Any]) -> list[str]:
    errors = schema_errors(record, MOTION_SCHEMA)
    timing = record.get("timing", {})
    start = timing.get("start_frame")
    end = timing.get("end_frame_exclusive")
    duration = timing.get("duration_frames")

    if all(isinstance(value, int) and not isinstance(value, bool) for value in (start, end, duration)):
        if end <= start:
            errors.append("timing.end_frame_exclusive must be greater than timing.start_frame")
        elif duration != end - start:
            errors.append("timing.duration_frames must equal end_frame_exclusive - start_frame (half-open range)")

        for index, keyframe in enumerate(record.get("keyframes", [])):
            frame = keyframe.get("frame")
            if isinstance(frame, int) and not isinstance(frame, bool) and not (start <= frame < end):
                errors.append(f"keyframes[{index}].frame must be inside the half-open motion interval")

        for index, phase in enumerate(record.get("motion_phases", [])):
            phase_start = phase.get("start_frame")
            phase_end = phase.get("end_frame_exclusive")
            if isinstance(phase_start, int) and isinstance(phase_end, int):
                if phase_start < start or phase_end > end or phase_end <= phase_start:
                    errors.append(f"motion_phases[{index}] must be a non-empty interval inside the motion interval")

    frames = [item.get("frame") for item in record.get("keyframes", []) if isinstance(item, dict)]
    if len(frames) != len(set(frames)):
        errors.append("keyframe frame values must be unique")
    if frames != sorted(frames):
        errors.append("keyframes must be ordered by ascending frame")

    easing = record.get("easing", {})
    if easing.get("type") == "CUBIC_BEZIER" and "cubic_bezier" not in easing:
        errors.append("CUBIC_BEZIER easing requires cubic_bezier values")
    if easing.get("type") == "SPRING" and "spring" not in easing:
        errors.append("SPRING easing requires spring parameters")
    if easing.get("type") == "MODEL_LANGUAGE_ONLY" and not easing.get("model_language"):
        errors.append("MODEL_LANGUAGE_ONLY easing requires an explicit model_language description")

    if record.get("target_kind") == "CAMERA_REFERENCE" and not record.get("camera_plan_ref"):
        errors.append("camera motion must reference an S06-owned camera plan; S07 does not author camera design")

    if timing.get("timing_source") == "S09_AUDIO":
        if timing.get("source_precision") in (None, "UNKNOWN", "ESTIMATED"):
            errors.append("S09_AUDIO timing must preserve actual source precision; estimated timing is not exact")
        if not timing.get("source_time_ref"):
            errors.append("S09_AUDIO timing requires source_time_ref")

    return errors


def validate_platform_adapter(record: dict[str, Any]) -> list[str]:
    errors = schema_errors(record, ADAPTER_SCHEMA)
    status = record.get("status")
    if status in {"DOCS_VERIFIED", "RUNTIME_TESTED"}:
        if not record.get("checked_at"):
            errors.append(f"{status} adapter requires checked_at")
        if not record.get("official_docs_refs"):
            errors.append(f"{status} adapter requires official_docs_refs")
    if status == "RUNTIME_TESTED" and not record.get("runtime_test_refs"):
        errors.append("RUNTIME_TESTED adapter requires runtime_test_refs")
    for index, feature in enumerate(record.get("feature_matrix", [])):
        if feature.get("support") in {"SUPPORTED", "UNSUPPORTED", "CONDITIONAL"} and not feature.get("evidence_refs"):
            errors.append(f"feature_matrix[{index}] requires evidence_refs for a non-UNKNOWN support claim")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--example-motion", type=Path, default=ROOT / "tests/fixtures/v4/motion-valid.json")
    parser.add_argument("--example-adapter", type=Path, default=ROOT / "tests/fixtures/v4/platform-adapter-not-checked.json")
    args = parser.parse_args()

    checks = [
        ("motion", args.example_motion, validate_motion_record),
        ("platform-adapter", args.example_adapter, validate_platform_adapter),
    ]
    failed = False
    for label, path, validator in checks:
        try:
            record = json.loads(path.read_text(encoding="utf-8"))
            errors = validator(record)
        except Exception as exc:
            errors = [f"validator exception: {type(exc).__name__}: {exc}"]
        if errors:
            failed = True
            print(f"FAIL {label}: {path}")
            for error in errors:
                print(f"  - {error}")
        else:
            print(f"PASS {label}: {path}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
