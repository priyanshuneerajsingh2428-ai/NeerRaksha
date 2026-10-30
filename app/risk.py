from datetime import date, timedelta

DISCLAIMER = (
    "Demonstration-only community signal, not a diagnosis or validated outbreak prediction. "
    "A qualified public-health authority must review and interpret all signals."
)

def village_risk(village, reports, water, today=None):
    today = today or date.today()
    start = today - timedelta(days=6)
    recent = [
        r for r in reports
        if r.get("village", "").lower() == village.lower()
        and start <= date.fromisoformat(str(r["report_date"])[:10]) <= today
    ]
    recent_water = [
        w for w in water
        if w.get("village", "").lower() == village.lower()
        and start <= date.fromisoformat(str(w["observation_date"])[:10]) <= today
    ]

    case_total = sum(int(r.get("case_count", 0)) for r in recent)
    report_count = len(recent)
    score = 0
    factors = []

    # Transparent heuristic for a prototype only; thresholds are not clinical standards.
    if case_total >= 10:
        score += 40
        factors.append("Elevated reported symptom-case volume in the last 7 days")
    elif case_total >= 5:
        score += 25
        factors.append("Increasing reported symptom-case volume in the last 7 days")
    elif case_total > 0:
        score += 10
        factors.append("Recent symptom reports recorded")

    water_flags = 0
    for w in recent_water:
        if w.get("coliform_detected") is True:
            water_flags += 1
        turbidity = w.get("turbidity_ntu")
        if turbidity is not None and float(turbidity) > 5:
            water_flags += 1
    if water_flags:
        score += min(35, 20 + 5 * (water_flags - 1))
        factors.append("Water observation contains one or more review flags (e.g., coliform indication or elevated turbidity)")
    if not recent_water:
        factors.append("No recent water-quality observation: data gap")
    if not recent:
        factors.append("No recent symptom report: absence of reports does not prove absence of illness")

    score = min(score, 100)
    level = "HIGH" if score >= 60 else "MODERATE" if score >= 30 else "LOW"
    return {
        "village": village,
        "score": score,
        "level": level,
        "factors": factors,
        "report_count_7d": report_count,
        "reported_cases_7d": case_total,
        "disclaimer": DISCLAIMER,
    }
