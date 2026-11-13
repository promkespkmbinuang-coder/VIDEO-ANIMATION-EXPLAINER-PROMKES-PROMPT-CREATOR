import importlib.util, json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def load(name,path):
    spec=importlib.util.spec_from_file_location(name,ROOT/path); mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod); return mod
beat=load("beat","scripts/validate_beat_sheet.py")
risk=load("risk","scripts/validate_risk_assessment.py")
def test_example_beat_sheet_valid():
    data=json.loads((ROOT/"examples/v4/beat-sheet-example.json").read_text())
    assert beat.validate(data)==[]
def test_beat_exact_timing_requires_source():
    data=json.loads((ROOT/"examples/v4/beat-sheet-example.json").read_text()); b=data["beats"][0]
    b["timing_precision"]="EXACT_AUDIO"
    assert any("timing_source_ref" in e for e in beat.validate(data))
def test_beat_rejects_duplicate_ids():
    data=json.loads((ROOT/"examples/v4/beat-sheet-example.json").read_text()); data["beats"].append(dict(data["beats"][0],sequence=2))
    assert any("duplicate beat_id" in e for e in beat.validate(data))
def test_beat_rejects_invalid_frame_interval():
    data=json.loads((ROOT/"examples/v4/beat-sheet-example.json").read_text()); b=data["beats"][0]
    b["start_frame"]=20; b["end_frame_exclusive"]=20
    assert any("half-open" in e for e in beat.validate(data))
def test_unknown_risk_is_elevated_not_low():
    lane,errors=risk.resolve({"dimensions":{"health_claim":"UNKNOWN"}})
    assert lane=="R2" and not errors
def test_critical_trigger_overrides_low_dimensions():
    lane,errors=risk.resolve({"dimensions":{"health_claim":"LOW"},"serious_harm_trigger":True})
    assert lane=="R3" and not errors
def test_declared_lane_cannot_understate_minimum():
    lane,errors=risk.resolve({"dimensions":{"rights":"ELEVATED"},"declared_lane":"R1"})
    assert lane=="R2" and not errors
def test_invalid_risk_value_rejected():
    lane,errors=risk.resolve({"dimensions":{"health_claim":"MAYBE"}})
    assert lane is None and errors

def test_r0_requires_s02_no_claim_evidence(tmp_path, monkeypatch, capsys):
    assessment={"dimensions":{"health_claim":"LOW"},"declared_lane":"R0"}
    p=tmp_path/"risk.json"; p.write_text(json.dumps(assessment))
    monkeypatch.setattr("sys.argv",["validate_risk_assessment.py",str(p)])
    assert risk.main()==1
    assert "S02 NO_MATERIAL_HEALTH_CLAIM" in capsys.readouterr().out
def test_r0_passes_only_with_s02_disposition_ref(tmp_path, monkeypatch, capsys):
    assessment={"dimensions":{"health_claim":"LOW"},"declared_lane":"R0","s02_disposition":"NO_MATERIAL_HEALTH_CLAIM","s02_disposition_ref":"S02-DISP-001"}
    p=tmp_path/"risk.json"; p.write_text(json.dumps(assessment))
    monkeypatch.setattr("sys.argv",["validate_risk_assessment.py",str(p)])
    assert risk.main()==0
    assert "PASS" in capsys.readouterr().out
