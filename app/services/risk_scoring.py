from typing import Tuple, List
from ..models import RiskInput


def calculate_risk(patient_data: RiskInput) -> Tuple[int, str, List[str]]:
    """
    Calculate diabetes risk score based on patient questionnaire data.
    
    Args:
        patient_data: RiskInput object containing patient information
        
    Returns:
        Tuple of (risk_score, risk_level, flags)
    """
    score = 0
    flags = []
    
    # Age scoring
    if patient_data.age >= 45:
        score += 10
        flags.append("age_high")
    
    # BMI scoring
    if patient_data.bmi is not None and patient_data.bmi >= 30:
        score += 15
        flags.append("bmi_high")
    
    # History of high glucose
    if patient_data.history_high_glucose:
        score += 20
        flags.append("high_glucose_history")
    
    # Blood pressure scoring (≥ 140/90)
    if patient_data.bp_sys >= 140 or patient_data.bp_dia >= 90:
        score += 25
        flags.append("bp_high")
    
    # Physical activity scoring (< 4 hours per week)
    if patient_data.physical_activity_hours_per_week < 4:
        score += 10
        flags.append("low_physical_activity")
    
    # Family history scoring
    if patient_data.family_history_diabetes == "second_degree":
        score += 10
        flags.append("family_history_second_degree")
    elif patient_data.family_history_diabetes == "first_degree":
        score += 20
        flags.append("family_history_first_degree")
    
    # Smoking status scoring
    if patient_data.smoking_status in ["former", "moderate"]:
        score += 5
        flags.append("smoking_risk")
    elif patient_data.smoking_status in ["current", "heavy"]:
        score += 15
        flags.append("smoking_high_risk")
    
    # Alcohol status scoring
    if patient_data.alcohol_status == "moderate":
        score += 5
        flags.append("alcohol_risk")
    elif patient_data.alcohol_status in ["current", "heavy"]:
        score += 15
        flags.append("alcohol_high_risk")
    
    # Cap score at 100
    score = min(score, 100)
    
    # Determine risk level
    if score <= 30:
        risk_level = "Low"
    elif score <= 60:
        risk_level = "Medium"
    else:
        risk_level = "High"
    
    return score, risk_level, flags
