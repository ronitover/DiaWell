#!/bin/bash

# DiaWell API Testing with curl
# No Flutter required!

echo "🚀 DiaWell API Testing with curl"
echo "=================================="

BASE_URL="http://localhost:8000"

# Test 1: Health Check
echo ""
echo "🔍 Testing Health Check..."
curl -s "$BASE_URL/" | jq '.'

# Test 2: Risk Assessment
echo ""
echo "🧪 Testing Risk Assessment..."
curl -s -X POST "$BASE_URL/risk/submit" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Sarah Johnson",
    "age": 52,
    "gender": "female",
    "height": 165.0,
    "weight": 78.0,
    "bp_sys": 148,
    "bp_dia": 92,
    "history_high_glucose": true,
    "physical_activity_hours_per_week": 2.0,
    "family_history_diabetes": "first_degree",
    "smoking_status": "former",
    "alcohol_status": "moderate",
    "lang": "en"
  }' | jq '.'

# Test 3: Recommendations
echo ""
echo "💡 Testing Recommendations..."
curl -s -X POST "$BASE_URL/recommendations/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "risk_level": "High",
    "risk_score": 75,
    "flags": ["age_high", "bp_high", "high_glucose_history"]
  }' | jq '.'

echo ""
echo "✅ Testing complete!"
