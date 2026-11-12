import json
from pathlib import Path
from scripts.v4_gate_engine import detect_prompt_injection


def test_red_team_corpus_detects_obfuscated_attacks_and_keeps_benign_controls():
    fixture=json.loads((Path(__file__).resolve().parent/"fixtures/v4/prompt-redteam-cases.json").read_text(encoding="utf-8"))
    for attack in fixture["malicious"]:
        assert detect_prompt_injection(attack), f"Expected heuristic match: {attack!r}"
    for benign in fixture["benign"]:
        assert not detect_prompt_injection(benign), f"Unexpected heuristic false positive: {benign!r}"
    for ambiguous in fixture["ambiguous"]:
        # Quoted attack strings may trigger the heuristic; route to human review.
        assert detect_prompt_injection(ambiguous)
