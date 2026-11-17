from __future__ import annotations

import hashlib
import json
import unicodedata
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def normalize(value: Any) -> Any:
    if isinstance(value, str):
        return unicodedata.normalize("NFC", value.replace("\r\n", "\n").replace("\r", "\n"))
    if isinstance(value, list):
        return [normalize(x) for x in value]
    if isinstance(value, dict):
        return {unicodedata.normalize("NFC", str(k)): normalize(v) for k, v in value.items()}
    return value


def canonical_json_bytes(value: Any) -> bytes:
    return json.dumps(normalize(value), ensure_ascii=False, sort_keys=True,
                      separators=(",", ":"), allow_nan=False).encode("utf-8")


def sha256_bytes(raw: bytes) -> str:
    return "sha256:" + hashlib.sha256(raw).hexdigest()


def sha256_json(value: Any, *, omit: tuple[str, ...] = ()) -> str:
    payload = dict(value) if isinstance(value, dict) else value
    if isinstance(payload, dict):
        for key in omit:
            payload.pop(key, None)
    return sha256_bytes(canonical_json_bytes(payload))


def parse_datetime(value: str | None) -> datetime | None:
    if not value or not isinstance(value, str):
        return None
    try:
        dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
        if dt.tzinfo is None:
            return None
        return dt.astimezone(timezone.utc)
    except ValueError:
        return None


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def resolved_inside(path: Path, root: Path) -> bool:
    try:
        path.resolve().relative_to(root.resolve())
        return True
    except (ValueError, OSError):
        return False
