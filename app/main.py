from fastapi import FastAPI, HTTPException
from app.schemas import SymptomReport, WaterObservation
from app.store import reports, water_observations, add_report, add_water
from app.risk import village_risk

app = FastAPI(
    title="NeerRaksha — SIH25001",
    description="Research prototype for community symptom and water observation surveillance.",
    version="1.0.0"
)

@app.get("/api/health")
def health():
    return {"status": "ok", "service": "NeerRaksha API"}

@app.post("/api/reports", status_code=201)
def create_report(report: SymptomReport):
    return {"message": "Report recorded", "report": add_report(report)}

@app.get("/api/reports")
def list_reports():
    return {"reports": reports}

@app.post("/api/water-observations", status_code=201)
def create_water_observation(observation: WaterObservation):
    return {"message": "Water observation recorded", "observation": add_water(observation)}

@app.get("/api/water-observations")
def list_water_observations():
    return {"water_observations": water_observations}

@app.get("/api/villages")
def villages():
    names = sorted({r["village"] for r in reports} | {w["village"] for w in water_observations})
    return {"villages": names}

@app.get("/api/risk/{village}")
def risk(village: str):
    known = {r["village"].lower() for r in reports} | {w["village"].lower() for w in water_observations}
    if village.lower() not in known:
        raise HTTPException(status_code=404, detail="Village not found. Add a report or water observation first.")
    return village_risk(village, reports, water_observations)

@app.get("/api/summary")
def summary():
    names = sorted({r["village"] for r in reports} | {w["village"] for w in water_observations})
    results = [village_risk(n, reports, water_observations) for n in names]
    return {
        "village_count": len(names),
        "symptom_report_count": len(reports),
        "water_observation_count": len(water_observations),
        "risk_by_village": results,
        "notice": "Prototype indicators only; not validated public-health alerts."
    }
