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
    name: str = Field(..., description="Patient name", example="John Doe")
    age: int = Field(..., ge=10, le=120, description="Patient age (10-120)", example=45)
    gender: str = Field(..., description="Patient gender", example="male")
    height: float = Field(..., ge=50, le=250, description="Height in cm (50-250)", example=175.0)
    weight: float = Field(..., ge=10, le=300, description="Weight in kg (10-300)", example=80.0)
    bmi: Optional[float] = Field(None, ge=10, le=100, description="BMI (auto-calculated if not provided)", example=26.1)
    bp_sys: int = Field(..., ge=60, le=250, description="Systolic blood pressure (60-250)", example=140)
    bp_dia: int = Field(..., ge=40, le=150, description="Diastolic blood pressure (40-150)", example=90)
    history_high_glucose: bool = Field(..., description="History of high glucose levels", example=False)
    physical_activity_hours_per_week: float = Field(..., ge=0, le=168, description="Physical activity hours per week (0-168)", example=3.0)
    family_history_diabetes: FamilyHistoryDiabetes = Field(..., description="Family history of diabetes", example="none")
    smoking_status: SmokingStatus = Field(..., description="Smoking status", example="never")
    alcohol_status: AlcoholStatus = Field(..., description="Alcohol consumption status", example="moderate")
    lang: str = Field(default="en", description="Language preference", example="en")

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
    risk_score: int = Field(..., ge=0, le=100, description="Risk score (0-100)", example=75)
    risk_level: str = Field(..., description="Risk level (Low/Medium/High)", example="High")
    flags: List[str] = Field(..., description="List of risk flags", example=["age_high", "bp_high"])
    guideline: str = Field(..., description="Guideline information", example="Personalized recommendations for High risk level")
    tips: Dict = Field(..., description="Comprehensive health recommendations and tips")
