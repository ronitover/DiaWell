from pydantic import BaseModel, Field, model_validator
from typing import List, Dict, Optional, Any
from enum import Enum


class FamilyHistoryDiabetes(str, Enum):
    none = "none"
    second_degree = "second_degree"
    first_degree = "first_degree"


class SmokingStatus(str, Enum):
    never = "never"
    former = "former"
    moderate = "moderate"
    current = "current"
    heavy = "heavy"


class AlcoholStatus(str, Enum):
    never = "never"
    former = "former"
    moderate = "moderate"
    current = "current"
    heavy = "heavy"


class RiskInput(BaseModel):
    name: str = Field(..., description="Patient name")
    age: int = Field(..., ge=10, le=120, description="Patient age (10-120)")
    gender: str = Field(..., description="Patient gender")
    height: float = Field(..., ge=50, le=250, description="Height in cm (50-250)")
    weight: float = Field(..., ge=10, le=300, description="Weight in kg (10-300)")
    bmi: Optional[float] = Field(None, ge=10, le=100, description="BMI (optional, auto-calculated from height/weight if not provided)")
    bp_sys: int = Field(..., ge=60, le=250, description="Systolic blood pressure (60-250)")
    bp_dia: int = Field(..., ge=40, le=150, description="Diastolic blood pressure (40-150)")
    history_high_glucose: bool = Field(..., description="History of high glucose levels")
    physical_activity_hours_per_week: float = Field(..., ge=0, le=168, description="Physical activity hours per week (0-168)")
    family_history_diabetes: FamilyHistoryDiabetes = Field(..., description="Family history of diabetes")
    smoking_status: SmokingStatus = Field(..., description="Smoking status")
    alcohol_status: AlcoholStatus = Field(..., description="Alcohol consumption status")
    lang: str = Field(default="en", description="Language preference")

    @model_validator(mode='after')
    def calculate_bmi_if_not_provided(self) -> 'RiskInput':
        if self.bmi is None:
            height_m = self.height / 100  # Convert cm to meters
            self.bmi = round(self.weight / (height_m ** 2), 1)
        return self


class RecoInput(BaseModel):
    risk_level: str = Field(..., description="Risk level (Low, Medium, High)")
    risk_score: int = Field(..., ge=0, le=100, description="Risk score (0-100)")
    flags: List[str] = Field(..., description="List of risk factor flags")


class RiskResponse(BaseModel):
    risk_score: int = Field(..., ge=0, le=100, description="Risk score (0-100)")
    risk_level: str = Field(..., description="Risk level (Low/Medium/High)")
    flags: List[str] = Field(..., description="List of risk flags")
    guideline: str = Field(..., description="Guideline information")
    tips: Dict = Field(..., description="Comprehensive health recommendations and tips")
