from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .models import RiskInput, RiskResponse, RecoInput
from .services.risk_scoring import calculate_risk
from .services.recommendations import generate_health_recommendations
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Diabetes Risk Assessment API",
    description="API for assessing diabetes risk based on patient questionnaire data",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def ping():
    """Health check endpoint"""
    return {"message": "Diabetes Risk Assessment API is running!", "status": "healthy"}


@app.post("/risk/submit", response_model=RiskResponse)
async def submit_risk_assessment(patient_data: RiskInput):
    """
    Submit patient questionnaire data for comprehensive diabetes risk assessment and health recommendations.
    
    This endpoint calculates a risk score based on various health factors including:
    - Age, height, weight (BMI auto-calculated)
    - Blood pressure
    - Medical history (high glucose)
    - Lifestyle factors (physical activity, smoking, alcohol)
    - Family history of diabetes
    
    Returns comprehensive assessment including:
    - Risk score and level classification
    - Identified risk factors
    - Personalized health recommendations
    - Priority actions and lifestyle tips
    - Medical guidance based on WHO, CDC, and ICMR guidelines
    """
    try:
        logger.info(f"Processing risk assessment for patient: {patient_data.name}")
        
        # Calculate risk score, level, and flags
        risk_score, risk_level, flags = calculate_risk(patient_data)
        
        # Generate personalized health recommendations
        health_recommendations = generate_health_recommendations(
            risk_level=risk_level,
            flags=flags,
            risk_score=risk_score
        )
        
        # Build tips_block with flat structure
        tips_block = {
            "headline": health_recommendations["headline"],
            "actions": health_recommendations["recommendations"]["lifestyle"] + health_recommendations["recommendations"]["specific_actions"],
            "disclaimer": health_recommendations["disclaimer"]
        }
        
        # Add red_flags only for High risk
        if risk_level == "High":
            tips_block["red_flags"] = health_recommendations["red_flags"]
        
        # Create comprehensive response with risk assessment and recommendations
        response = RiskResponse(
            risk_score=risk_score,
            risk_level=risk_level,
            flags=flags,
            guideline=health_recommendations["headline"],
            tips=tips_block
        )
        
        logger.info(f"Risk assessment completed for {patient_data.name}: Score={risk_score}, Level={risk_level}")
        return response
        
    except Exception as e:
        logger.error(f"Error processing risk assessment: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error during risk assessment")


@app.post("/recommendations/generate")
async def generate_recommendations(reco_input: RecoInput):
    """
    Generate health recommendations based on risk assessment data.
    
    This endpoint provides personalized health recommendations based on:
    - Risk level (Low, Medium, High)
    - Risk score (0-100)
    - Risk factor flags
    
    Returns comprehensive health recommendations including lifestyle tips,
    priority actions, and medical guidance based on WHO, CDC, and ICMR guidelines.
    """
    try:
        logger.info(f"Generating recommendations for risk level: {reco_input.risk_level}, score: {reco_input.risk_score}")
        
        recommendations = generate_health_recommendations(
            risk_level=reco_input.risk_level,
            flags=reco_input.flags,
            risk_score=reco_input.risk_score
        )
        
        logger.info(f"Recommendations generated successfully for {reco_input.risk_level} risk level")
        return recommendations
        
    except Exception as e:
        logger.error(f"Error generating recommendations: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error during recommendation generation")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
