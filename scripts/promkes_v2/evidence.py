from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from .common import parse_datetime, sha256_bytes


@dataclass(frozen=True)
class ProvenanceResult:
    status: str
    observed_hash: str | None
    reasons: tuple[str, ...] = ()


def verify_source_snapshot(path: Path, expected_hash: str, *, source_uri: str,
                           support_location: str, accessed_at: str) -> ProvenanceResult:
    reasons = []
    if not source_uri or not support_location or not parse_datetime(accessed_at):
        reasons.append("source URI, support location and timezone-aware access time are required")
    try:
        actual = sha256_bytes(Path(path).read_bytes())
    except OSError as exc:
        return ProvenanceResult("FAIL", None, (f"snapshot unreadable: {exc}",))
    if actual.lower() != str(expected_hash).lower():
        reasons.append("snapshot bytes do not match the recorded SHA-256")
    return ProvenanceResult("PASS" if not reasons else "FAIL", actual, tuple(reasons))


_NEGATIONS = ("tidak", "bukan", "tanpa", "belum", "jangan", "tak", "not", "no", "never", "without")
_STOP = set("yang dan di ke dari untuk pada dengan adalah itu ini atau agar supaya dapat bisa akan telah sudah oleh sebagai dalam secara lebih sangat juga hanya saja karena sehingga the a an of to in for and or is are was were be been with on at by as that this it".split())


def _tokens(text: str) -> set[str]:
    text = unicodedata.normalize("NFKC", text).casefold()
    return {t for t in re.findall(r"[a-z0-9]+", text) if len(t) > 2 and t not in _STOP}


def _has_negation(text: str) -> bool:
    text = unicodedata.normalize("NFKC", text).casefold()
    return any(re.search(rf"\b{re.escape(n)}\b", text) for n in _NEGATIONS)


@dataclass(frozen=True)
class ClaimSupportResult:
    status: str  # SUPPORTED_LEXICALLY | CONTRADICTED | INSUFFICIENT
    quote_found: bool
    overlap: float
    number_mismatches: tuple[str, ...] = ()
    reasons: tuple[str, ...] = ()
    clinical_approval: bool = False


def verify_claim_support(claim_text: str, source_snapshot_text: str, *,
                         verbatim_quote: str | None, min_overlap: float = 0.45) -> ClaimSupportResult:
    if not claim_text.strip() or not source_snapshot_text.strip():
        return ClaimSupportResult("INSUFFICIENT", False, 0.0, reasons=("claim/source text missing",))
    source_norm = re.sub(r"\s+", " ", unicodedata.normalize("NFKC", source_snapshot_text)).casefold()
    quote_norm = re.sub(r"\s+", " ", unicodedata.normalize("NFKC", verbatim_quote or "")).casefold().strip()
    quote_found = bool(quote_norm) and quote_norm in source_norm
    claim_tokens = _tokens(claim_text)
    source_sentences = [x.strip() for x in re.split(r"(?<=[.!?])\s+|\n+", source_snapshot_text) if x.strip()]
    best_sentence, overlap = "", 0.0
    for sentence in source_sentences:
        sentence_tokens = _tokens(sentence)
        score = len(claim_tokens & sentence_tokens) / max(1, len(claim_tokens))
        if score > overlap:
            overlap, best_sentence = score, sentence
    claim_nums = set(re.findall(r"\d+(?:[.,]\d+)?%?", claim_text))
    support_context = best_sentence
    if quote_found:
        support_context += " " + (verbatim_quote or "")
    source_nums = set(re.findall(r"\d+(?:[.,]\d+)?%?", support_context))
    missing_nums = tuple(sorted(claim_nums - source_nums))
    reasons = []
    if not quote_found:
        reasons.append("verbatim source quote absent or not found")
    if missing_nums:
        reasons.append("unsupported numeric values: " + ", ".join(missing_nums))
    if overlap < min_overlap:
        reasons.append("lexical overlap below threshold; human review required")
    # Conservative polarity check uses the best-matching sentence, not the entire
    # document, so an unrelated negated sentence cannot taint another proposition.
    if overlap >= min_overlap and _has_negation(best_sentence) != _has_negation(claim_text):
        return ClaimSupportResult("CONTRADICTED", quote_found, overlap, missing_nums,
                                  tuple(reasons + ["best-matching source proposition has opposite polarity"]), False)
    if reasons:
        return ClaimSupportResult("INSUFFICIENT", quote_found, overlap, missing_nums, tuple(reasons), False)
    return ClaimSupportResult("SUPPORTED_LEXICALLY", True, overlap, (),
                              ("lexical and quote checks pass; this is not clinical truth or approval",), False)


def verify_claim_context(claim_context: dict[str, Any], source_context: dict[str, Any]) -> dict:
    dimensions = ("date", "jurisdiction", "population")
    mismatches = [key for key in dimensions
                  if claim_context.get(key) in (None, "") or source_context.get(key) in (None, "")
                  or str(claim_context.get(key)).casefold() != str(source_context.get(key)).casefold()]
    return {"status": "HUMAN_REVIEW" if mismatches else "CONTEXT_MATCH",
            "mismatches": mismatches,
            "promote_to_verified": False if mismatches else None,
            "note": "Context match alone never constitutes clinical approval"}


def source_gate(source_records: list[dict], snapshot_root: Path) -> tuple[bool, list[str]]:
    reasons = []
    for src in source_records:
        if src.get("verification_status") != "VERIFIED":
            continue
        result = verify_source_snapshot(snapshot_root / src.get("snapshot_path", ""),
                                        src.get("content_hash", ""), source_uri=src.get("source_uri", ""),
                                        support_location=src.get("support_location", ""),
                                        accessed_at=src.get("accessed_at", ""))
        if result.status != "PASS":
            reasons.append(f"{src.get('source_id')}: {'; '.join(result.reasons)}")
    return not reasons, reasons
