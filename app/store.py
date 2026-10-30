from pathlib import Path
import pandas as pd
from datetime import date

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"

def load_demo():
    reports = pd.read_csv(DATA / "demo_symptom_reports.csv")
    water = pd.read_csv(DATA / "demo_water_observations.csv")
    return reports.to_dict("records"), water.to_dict("records")

reports, water_observations = load_demo()

def add_report(item):
    reports.append(item.model_dump(mode="json"))
    return reports[-1]

def add_water(item):
    water_observations.append(item.model_dump(mode="json"))
    return water_observations[-1]
