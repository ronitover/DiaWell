"""
Health recommendations service for the Diabetes Risk Assessment API.

This service generates personalized health recommendations based on risk assessment data.
"""

import json
import os
from typing import List, Dict, Optional
from pathlib import Path

# Load tips data once at module level
def _load_tips_data() -> Dict:
    """Load the guideline snippets data from JSON file."""
    try:
        # Get the directory where this file is located
        current_dir = Path(__file__).parent
        data_file = current_dir.parent / "data" / "guideline_snippets.json"
        
        with open(data_file, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        # Fallback for development/testing
        return {
            "base_tips": {
                "Low": ["Maintain a healthy lifestyle."],
                "Medium": ["Monitor your health regularly."],
                "High": ["Consult a healthcare professional."]
            },
            "factor_tips": {},
            "disclaimer": "Educational only, not medical advice.",
            "red_flags": "If chest pain, severe breathlessness, confusion, or weakness → seek urgent care."
        }

TIPS_DATA = _load_tips_data()


def generate_health_recommendations(
    risk_level: str, 
    flags: List[str], 
    risk_score: int
) -> Dict[str, any]:
    """
    Generate personalized health recommendations based on risk assessment.
    
    Args:
        risk_level: The risk level (Low, Medium, High)
        flags: List of risk factor flags
        risk_score: Numerical risk score (0-100)
        
    Returns:
        Dictionary containing personalized recommendations
    """
    # Take first 2-3 base tips for the risk level (deterministic)
    base_tips = TIPS_DATA["base_tips"].get(risk_level, [])
    selected_base = base_tips[:3] if len(base_tips) >= 3 else base_tips

    # Add up to 2 factor-specific tips based on risk flags (deterministic, no duplicates)
    factor_tips = []
    seen_tips = set()
    
    for flag in flags:
        if len(factor_tips) >= 2:  # Limit to 2 factor tips
            break
        tip = TIPS_DATA["factor_tips"].get(flag)
        if tip and tip not in seen_tips:
            factor_tips.append(tip)
            seen_tips.add(tip)

    # Build comprehensive recommendations
    recommendations = {
        "headline": f"Personalized recommendations for {risk_level} risk level",
        "risk_summary": {
            "level": risk_level,
            "score": risk_score,
            "risk_factors": flags
        },
        "recommendations": {
            "lifestyle": selected_base,
            "specific_actions": factor_tips
        },
        "priority_actions": _get_priority_actions(risk_level, flags),
        "disclaimer": TIPS_DATA["disclaimer"],
        "credits": TIPS_DATA.get("credits", [])
    }
    
    # Add red flags for high-risk patients
    if risk_level == "High":
        recommendations["red_flags"] = TIPS_DATA["red_flags"]
        recommendations["urgent_actions"] = [
            "Schedule an appointment with your healthcare provider",
            "Begin monitoring blood glucose levels",
            "Start lifestyle modifications immediately"
        ]
    
    return recommendations


def _get_priority_actions(risk_level: str, flags: List[str]) -> List[str]:
    """Get priority actions based on risk level and flags."""
    priority_actions = []
    
    if risk_level == "High":
        priority_actions.extend([
            "Schedule medical consultation within 1 week",
            "Start blood glucose monitoring",
            "Begin lifestyle modifications immediately"
        ])
    elif risk_level == "Medium":
        priority_actions.extend([
            "Schedule check-up within 1 month",
            "Start diet and exercise plan",
            "Monitor blood pressure regularly"
        ])
    else:  # Low risk
        priority_actions.extend([
            "Continue healthy lifestyle habits",
            "Annual health check-up",
            "Stay informed about diabetes prevention"
        ])
    
    # Add specific actions based on flags
    if "bmi_high" in flags:
        priority_actions.append("Focus on weight management")
    if "bp_high" in flags:
        priority_actions.append("Monitor blood pressure closely")
    if "low_physical_activity" in flags:
        priority_actions.append("Increase physical activity to 150+ minutes/week")
    if any("smoking" in flag for flag in flags):
        priority_actions.append("Consider smoking cessation programs")
    if any("alcohol" in flag for flag in flags):
        priority_actions.append("Reduce alcohol consumption")
    
    return priority_actions


def get_recommendation_summary(risk_level: str, risk_score: int) -> str:
    """Generate a brief summary of recommendations."""
    if risk_level == "High":
        return f"High risk (Score: {risk_score}/100) - Immediate medical consultation recommended"
    elif risk_level == "Medium":
        return f"Medium risk (Score: {risk_score}/100) - Lifestyle modifications and monitoring advised"
    else:
        return f"Low risk (Score: {risk_score}/100) - Continue healthy lifestyle habits"
