from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "skills/animation-motion-design/references/remotion-pattern-adoption-v4.1.11.md"


def test_catalogue_lists_reusable_motion_families_and_guardrails():
    text = CATALOG.read_text(encoding="utf-8")
    for token in ["RMP-01", "RMP-17", "Ken Burns", "Parallax depth", "Audio-linked motion/SFX", "Word/phrase-synchronized captions"]:
        assert token in text
    for token in ["reduced-motion", "fail closed", "end_frame_exclusive", "NOT_RUN", "NOT_VERIFIED"]:
        assert token in text


def test_motion_catalogue_is_optional_and_not_a_universal_style_rule():
    text = CATALOG.read_text(encoding="utf-8").lower()
    assert "not a mandatory style" in text
    assert "static holds" in text
    assert "not universal" in text


def test_adapter_profile_and_encoded_media_qa_are_explicit():
    text = CATALOG.read_text(encoding="utf-8")
    assert "cut-only transitions" in text
    assert "arbitrary motion paths" in text
    assert "Encoded-media QA" in text
    assert "mapping-loss" in text


def test_s07_and_s10_route_to_the_adoption_reference():
    s07 = (ROOT / "skills/animation-motion-design/SKILL.md").read_text(encoding="utf-8")
    s10 = (ROOT / "skills/editing-postproduction/SKILL.md").read_text(encoding="utf-8")
    assert "remotion-pattern-adoption-v4.1.11.md" in s07
    assert "remotion-pattern-adoption-v4.1.11.md" in s10
