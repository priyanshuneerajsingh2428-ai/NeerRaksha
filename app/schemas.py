from datetime import date
from typing import List, Optional
from pydantic import BaseModel, Field, field_validator

ALLOWED_SYMPTOMS = {
    "diarrhea", "vomiting", "fever", "abdominal_pain",
    "dehydration", "jaundice", "nausea"
}

class SymptomReport(BaseModel):
    village: str = Field(min_length=2, max_length=100)
    report_date: date
    symptoms: List[str] = Field(min_length=1)
    case_count: int = Field(ge=1, le=10000)
    reporter_role: str = Field(default="volunteer")
    age_band: Optional[str] = None

    @field_validator("symptoms")
    @classmethod
    def validate_symptoms(cls, values):
        cleaned = [v.strip().lower() for v in values]
        invalid = set(cleaned) - ALLOWED_SYMPTOMS
        if invalid:
            raise ValueError(f"Unsupported symptom tags: {sorted(invalid)}")
        return cleaned

class WaterObservation(BaseModel):
    village: str = Field(min_length=2, max_length=100)
    observation_date: date
    ph: Optional[float] = Field(default=None, ge=0, le=14)
    turbidity_ntu: Optional[float] = Field(default=None, ge=0, le=10000)
    tds_mg_l: Optional[float] = Field(default=None, ge=0, le=100000)
    coliform_detected: Optional[bool] = None
    source_type: str = "unknown"

class RiskResult(BaseModel):
    village: str
    score: int
    level: str
    factors: List[str]
    report_count_7d: int
    reported_cases_7d: int
    disclaimer: str
