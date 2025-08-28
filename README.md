# Diabetes Risk Assessment API

A FastAPI backend for assessing diabetes risk based on patient questionnaire data. This service is designed as part of a microservices architecture to provide structured risk assessment data to other services.

## 🏗️ Architecture

This project follows a **microservices architecture** where different components handle specific responsibilities:

- **Risk Assessment Service** (This repository): Calculates diabetes risk scores and provides structured risk data
- **Health Recommendations Service**: Generates personalized health tips and recommendations
- **Frontend Application**: User interface for data input and result display

## ✨ Features

- **Risk Scoring**: Calculates diabetes risk score (0-100) based on multiple health factors
- **Comprehensive Assessment**: Considers age, BMI, blood pressure, medical history, lifestyle factors, and family history
- **Personalized Recommendations**: Generates health recommendations based on WHO, CDC, and ICMR guidelines
- **AI Enhancement**: Optional Granite AI integration for empathetic, age-appropriate health tips
- **Flutter Ready**: Optimized for Flutter mobile app integration with complete client examples
- **RESTful API**: Clean REST endpoints with automatic documentation
- **Input Validation**: Robust Pydantic models with field validation and examples
- **CORS Enabled**: Ready for cross-platform frontend integration
- **Medical Guidelines**: Evidence-based recommendations from leading health organizations
- **Comprehensive Testing**: Full test suite with coverage reporting
- **CI/CD Ready**: GitHub Actions workflow for automated testing
- **Cross-Platform**: Works on Windows, macOS, and Linux

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- pip

### Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd backend
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables (Optional - for Granite AI enhancement):**
   ```bash
   # Copy the example environment file
   cp env.example .env
   
   # Edit .env file with your IBM WatsonX credentials
   # Get your credentials from: https://cloud.ibm.com/apis/watsonx
   ```
   
   **Note**: The API works without Granite AI configuration. If not configured, it will use the original health tips.

4. **Run the application (Multiple Options):**

   **Option 1: Using the start script (Recommended)**
   ```bash
   python start_server.py
   ```

   **Option 2: Using uvicorn directly**
   ```bash
   python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

   **Option 3: Using the run script**
   ```bash
   python run.py
   ```

5. **Access the API:**
   - Health check: http://localhost:8000/
   - API docs: http://localhost:8000/docs
   - Alternative docs: http://localhost:8000/redoc

## 🔧 Troubleshooting

### Common Issues:

**1. Import Error: No module named 'app'**
- **Solution**: Make sure you're in the Backend directory when running the server
- **Alternative**: Use `python start_server.py` which handles path issues automatically

**2. Port already in use**
- **Solution**: Change the port in the start script or use a different port
- **Command**: `python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8001`

**3. Missing dependencies**
- **Solution**: Install all requirements: `pip install -r requirements.txt`

**4. Permission denied (Linux/macOS)**
- **Solution**: Make scripts executable: `chmod +x start_server.py run.py`

## 📋 API Endpoints

- `GET /` - Health check endpoint with API information
- `POST /risk/submit` - Submit patient data for comprehensive risk assessment and recommendations
- `POST /recommendations/generate` - Generate health recommendations based on risk data
- `GET /docs` - Interactive API documentation (Swagger UI)
- `GET /redoc` - Alternative API documentation

## 📱 Flutter Integration

Ready-to-use Flutter integration files:
- `flutter_api_client.dart` - Complete API client for Flutter
- `FLUTTER_INTEGRATION.md` - Comprehensive integration guide with full widget example

## 📝 Sample Request

```json
{
  "name": "John Doe",
  "age": 55,
  "gender": "male",
  "height": 175.0,
  "weight": 85.0,
  "bp_sys": 145,
  "bp_dia": 95,
  "history_high_glucose": true,
  "physical_activity_hours_per_week": 2.5,
  "family_history_diabetes": "first_degree",
  "smoking_status": "former",
  "alcohol_status": "moderate",
  "lang": "en"
}
```

## 📊 Sample Response

```json
{
  "risk_score": 75,
  "risk_level": "High",
  "flags": [
    "age_high",
    "bmi_high",
    "high_glucose_history",
    "bp_high",
    "low_physical_activity",
    "family_history_first_degree",
    "smoking_risk",
    "alcohol_risk"
  ],
  "guideline": "Personalized recommendations for High risk level",
  "tips": {
    "headline": "Personalized recommendations for High risk level",
    "risk_summary": {
      "level": "High",
      "score": 75,
      "risk_factors": ["age_high", "bmi_high", "high_glucose_history", "bp_high", "low_physical_activity", "family_history_first_degree", "smoking_risk", "alcohol_risk"]
    },
    "recommendations": {
      "lifestyle": [
        "Consult a healthcare professional for personalized diabetes prevention advice.",
        "Follow a structured plan for diet, exercise, and regular screening."
      ],
      "specific_actions": [
        "Work towards a healthy weight through balanced diet and regular exercise.",
        "Monitor and manage your blood pressure with lifestyle changes and medical advice."
      ]
    },
    "priority_actions": [
      "Schedule medical consultation within 1 week",
      "Start blood glucose monitoring",
      "Begin lifestyle modifications immediately",
      "Focus on weight management",
      "Monitor blood pressure closely"
    ],
    "red_flags": "If you experience symptoms such as extreme thirst, frequent urination, unexplained weight loss, or vision changes, seek medical attention promptly.",
    "urgent_actions": [
      "Schedule an appointment with your healthcare provider",
      "Begin monitoring blood glucose levels",
      "Start lifestyle modifications immediately"
    ],
    "disclaimer": "These tips are based on WHO guidance for diabetes prevention. For personalized advice, consult a healthcare professional.",
    "credits": [
      {
        "organization": "World Health Organization (WHO)",
        "contribution": "Global diabetes prevention and lifestyle guidelines",
        "link": "https://www.who.int/news-room/fact-sheets/detail/diabetes"
      }
    ]
  }
}
```

## 🧪 Testing

### Run Tests
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/test_risk_scoring.py

# Run tests with verbose output
pytest -v
```

### Test Coverage
The project includes comprehensive tests for:
- ✅ Pydantic models validation
- ✅ Risk scoring logic
- ✅ API endpoints
- ✅ Error handling
- ✅ Edge cases

## 🔄 Git Workflow

### Branch Naming Convention
- `feature/risk-assessment-api` - New features
- `fix/import-errors` - Bug fixes
- `docs/update-readme` - Documentation updates
- `refactor/scoring-logic` - Code refactoring

### Commit Message Format
```
type(scope): description

[optional body]

[optional footer]
```

Examples:
- `feat(api): add new risk factor validation`
- `fix(models): resolve BMI calculation edge case`
- `docs(readme): update API endpoint documentation`

## 🏥 Risk Scoring Logic

The risk score is calculated based on the following factors:

- **Age ≥ 45**: +10 points
- **BMI ≥ 30**: +15 points
- **History of high glucose**: +20 points
- **BP ≥ 140/90**: +25 points
- **Physical activity < 4 hr/week**: +10 points
- **Family history**: second_degree +10, first_degree +20
- **Smoking**: former/moderate +5, current/heavy +15
- **Alcohol**: moderate +5, current/heavy +15

**Risk Levels:**
- 0-30: Low
- 31-60: Medium
- 61-100: High

## 📁 Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application
│   ├── models.py            # Pydantic models
│   └── services/
│       ├── __init__.py
│       └── risk_scoring.py  # Risk calculation logic
├── tests/
│   ├── __init__.py
│   ├── test_models.py       # Model validation tests
│   ├── test_risk_scoring.py # Risk scoring tests
│   └── test_api.py          # API endpoint tests
├── .github/
│   └── workflows/
│       └── ci.yml           # CI/CD pipeline
├── requirements.txt         # Python dependencies
├── pytest.ini             # Test configuration
├── start_server.py         # Cross-platform start script
├── run.py                  # Alternative start script
├── .gitignore             # Git ignore rules
├── CONTRIBUTING.md        # Contribution guidelines
└── README.md              # This file
```

## 🤝 Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

### Development Setup
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Run the test suite
6. Submit a pull request

## 📊 Service Integration

This API is designed as a **risk assessment service** that provides structured data to other services:

- **Risk Score**: Numerical score (0-100) indicating diabetes risk
- **Risk Level**: Categorical classification (Low/Medium/High)
- **Risk Flags**: Specific risk factors identified
- **Integration Ready**: Clean data structure for health recommendations services

### Example Integration
See `example_integration.py` for a complete example of how another service would integrate with this API.

## 🚨 Important Notes

### Risk Scoring Logic
- Risk scoring is based on medical guidelines
- Changes to scoring logic require medical review
- All scoring changes must be documented and tested

### Data Privacy
- No patient data is stored permanently
- All data is processed in memory only
- Implement proper data handling for production

## 📝 License

This project is part of a hackathon submission. Please respect the project's license and contribution guidelines.

## 🆘 Support

- Create an issue for bugs or feature requests
- Use GitHub Discussions for questions
- Check existing documentation and examples
- Review similar issues and pull requests

---

**Built with ❤️ for better healthcare technology** 🏥💻
