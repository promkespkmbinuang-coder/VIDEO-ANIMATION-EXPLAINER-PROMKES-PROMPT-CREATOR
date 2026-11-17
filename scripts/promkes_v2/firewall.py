from __future__ import annotations

import base64
import binascii
import html
import re
import unicodedata
from dataclasses import dataclass, field
from urllib.parse import unquote
from typing import Callable

_CONFUSABLE = str.maketrans({
    "а": "a", "е": "e", "о": "o", "р": "p", "с": "c", "у": "y", "і": "i",
    "ј": "j", "ѕ": "s", "ԁ": "d", "ɡ": "g", "һ": "h", "ⅼ": "l", "ո": "n",
    "ս": "u", "０": "0", "１": "1", "Ａ": "A", "ａ": "a", "Ｉ": "I", "ｉ": "i",
})
_INVISIBLE = re.compile(r"[\u200b-\u200f\u202a-\u202e\u2060-\u2064\ufeff\u00ad]")
_PATTERNS: tuple[tuple[str, str], ...] = (
    ("ID-OVERRIDE", r"\b(abaikan|lupakan|tinggalkan|kesampingkan|batalkan|timpa|ganti)\s+(semua|seluruh|segenap|apa pun|apa-pun)?\s*(instruksi|arahan|perintah|aturan|pedoman|ketentuan|petunjuk)\s*(sebelumnya|di atas|diatas|terdahulu|sebelum ini|tadi|awal)\b"),
    ("ID-LEAK", r"\b(tampilkan|perlihatkan|bocorkan|cetak|sebutkan|ungkap|buka)\s+(prompt|instruksi|arahan|perintah|aturan)\s*(sistem|system|tersembunyi|internal|rahasia|developer)\b"),
    ("ID-JAILBREAK", r"\b(mulai sekarang|sekarang kamu|kamu sekarang|berperanlah sebagai|bertindaklah sebagai)[^.]{0,100}(tanpa (aturan|batasan|batas)|tidak terikat|bebas aturan|tanpa filter|mode pengembang)\b"),
    ("ID-EXFIL", r"\b(kirim|unggah|transfer|teruskan|bocorkan|salin)\s+(semua|seluruh)?\s*(kredensial|kata sandi|password|kunci api|api key|token|rahasia|data pasien)\b"),
    ("ID-POLICY", r"\b(nonaktifkan|matikan|lewati|abaikan|cabut|hapus)\s+(kebijakan|aturan|filter|pemeriksaan|verifikasi)\s*(keamanan|keselamatan|konten|klinis|kesehatan)?\b"),
    ("ID-APPROVE", r"\b(setujui|loloskan|sahkan|tandai (lulus|pass)|nyatakan (verified|terverifikasi))\s+(semua|seluruh|tanpa)\s*(klaim|klaim kesehatan|verifikasi|pemeriksaan|review)?\b"),
    ("EN-OVERRIDE", r"\b(ignore|disregard|forget|bypass|override|discard)\s+(all\s+|any\s+)?(the\s+)?(previous|prior|above|earlier|preceding)\s+(system\s+|developer\s+)?instructions?\b"),
    ("EN-LEAK", r"\b(reveal|show|print|expose|dump|leak)\s+(the\s+)?(hidden\s+)?(system|developer|internal)\s+prompt\b"),
    ("EN-EXFIL", r"\b(exfiltrate|send|forward|upload|post)\s+(all\s+)?(the\s+)?(secrets|credentials|api keys|tokens|passwords)\b"),
    ("STR-DELIM", r"(```|<\s*/?\s*(system|assistant|tool_call|instruction)\s*>|\[\s*(system|inst)\s*\]|###\s*(system|instruction))"),
    ("ROLE-DIRECTIVE", r"\b(catatan|pesan|instruksi)\s+(untuk|kepada)\s+(asisten|ai|model|sistem|chatbot)\b"),
)


@dataclass(frozen=True)
class FirewallVerdict:
    status: str
    allowed: bool
    quarantine: bool
    hits: tuple[dict, ...] = ()
    variants_checked: int = 0
    note: str = ""


def normalized_variants(text: str, max_chars: int = 200_000) -> tuple[str, ...]:
    if not isinstance(text, str) or not text.strip():
        return ()
    if len(text) > max_chars:
        raise ValueError(f"untrusted text exceeds scanner size limit ({max_chars})")
    base = unicodedata.normalize("NFKC", html.unescape(text))
    base = _INVISIBLE.sub("", base)
    decoded = unquote(base)
    variants = {base, decoded, base.translate(_CONFUSABLE), decoded.translate(_CONFUSABLE)}
    variants |= {x.translate(str.maketrans({"0":"o", "1":"i", "3":"e", "4":"a", "5":"s", "7":"t", "@":"a", "$":"s"})) for x in tuple(variants)}
    for candidate in tuple(variants):
        for token in re.findall(r"[A-Za-z0-9+/]{16,}={0,2}", candidate):
            try:
                raw = base64.b64decode(token, validate=True)
                decoded_text = raw.decode("utf-8")
                if decoded_text and all(ch.isprintable() or ch.isspace() for ch in decoded_text):
                    variants.add(decoded_text)
            except (binascii.Error, UnicodeDecodeError, ValueError):
                pass
        for token in re.findall(r"(?<![0-9a-f])[0-9a-fA-F]{24,}(?![0-9a-f])", candidate):
            try:
                decoded_text = bytes.fromhex(token).decode("utf-8")
                if decoded_text and all(ch.isprintable() or ch.isspace() for ch in decoded_text):
                    variants.add(decoded_text)
            except (ValueError, UnicodeDecodeError):
                pass
    return tuple(sorted({re.sub(r"\s+", " ", x).strip().casefold() for x in variants if x.strip()}))


def inspect_untrusted_text(text: str) -> FirewallVerdict:
    variants = normalized_variants(text)
    if not variants:
        return FirewallVerdict("BLOCKED", False, True, note="actual source text missing; fail-closed")
    hits: dict[tuple[str, str], dict] = {}
    for vi, variant in enumerate(variants):
        for label, pattern in _PATTERNS:
            match = re.search(pattern, variant, re.IGNORECASE)
            if match:
                hits[(label, match.group(0))] = {
                    "label": label, "match": match.group(0)[:120], "variant_index": vi,
                    "severity": "CRITICAL" if label not in {"ROLE-DIRECTIVE", "STR-DELIM"} else "HIGH",
                }
    found = tuple(sorted(hits.values(), key=lambda x: (x["label"], x["match"])))
    if found:
        return FirewallVerdict("QUARANTINE", False, True, found, len(variants),
                               "Treat as untrusted data; no tool execution or instruction authority")
    return FirewallVerdict("NO_PATTERN_MATCH", False, False, (), len(variants),
                           "No heuristic hit is not proof of safety; structural isolation remains mandatory")


def intake_preflight(sources: list[dict], *, text_reader: Callable[[dict], str] | None = None) -> dict:
    """Scan concrete intake text. Empty/malformed source lists are BLOCKED."""
    if not isinstance(sources, list) or not sources:
        return {"status": "BLOCKED", "scanned": 0, "quarantined": [],
                "reason": "no actual untrusted source text supplied"}
    reader = text_reader or (lambda x: x.get("text", ""))
    results, quarantined = [], []
    try:
        for source in sources:
            sid = source.get("source_id", "<unknown>")
            text = reader(source)
            if not isinstance(text, str) or not text.strip():
                return {"status": "BLOCKED", "scanned": len(results), "quarantined": quarantined,
                        "reason": f"source {sid} has no readable text"}
            verdict = inspect_untrusted_text(text)
            results.append({"source_id": sid, "status": verdict.status,
                            "hits": list(verdict.hits), "variants_checked": verdict.variants_checked})
            if verdict.quarantine:
                quarantined.append(sid)
    except Exception as exc:
        return {"status": "BLOCKED", "scanned": len(results), "quarantined": quarantined,
                "reason": f"scanner execution error: {type(exc).__name__}"}
    return {"status": "QUARANTINE" if quarantined else "PASS_WITH_ISOLATION",
            "scanned": len(results), "quarantined": quarantined, "results": results,
            "source_instructions_executed": False,
            "note": "PASS_WITH_ISOLATION is only an execution-state result, not a safety proof"}


def rescan_at_boundary(text: str) -> dict:
    """Rescan transformed text immediately before a tool/execution boundary."""
    verdict = inspect_untrusted_text(text)
    blocked = verdict.quarantine or verdict.status == "BLOCKED"
    return {"status": "BLOCKED" if blocked else "PASS_WITH_ISOLATION",
            # A scan can quarantine hostile content; it can never grant tool
            # authority to the scanned source. Tool execution needs a separate
            # trusted workflow decision, not a text-scanner allow bit.
            "allow_tool_execution": False,
            "source_instruction_execution_allowed": False,
            "tool_authorization": "NOT_GRANTED_BY_SOURCE_SCAN",
            "heuristic_hits": list(verdict.hits), "note": verdict.note}
