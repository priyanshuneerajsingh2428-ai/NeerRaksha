from datetime import date
from app.risk import village_risk

def test_no_data_is_low_and_warns_about_missing_data():
    result = village_risk("Nowhere", [], [], today=date(2026, 10, 30))
    assert result["score"] == 0
    assert result["level"] == "LOW"
    assert any("absence of reports" in f for f in result["factors"])

def test_recent_reports_and_water_flag_raise_demo_score():
    reports = [{
        "village": "A", "report_date": "2026-10-30",
        "symptoms": ["diarrhea"], "case_count": 10
    }]
    water = [{
        "village": "A", "observation_date": "2026-10-30",
        "coliform_detected": True, "turbidity_ntu": 9
    }]
    result = village_risk("A", reports, water, today=date(2026, 10, 30))
    assert result["score"] >= 60
    assert result["level"] == "HIGH"
