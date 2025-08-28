# Contributing to Diabetes Risk Assessment API

Thank you for contributing to our Diabetes Risk Assessment API! This document provides guidelines for collaboration and development.

## 🏗️ Project Architecture

This project follows a **microservices architecture** where different components handle specific responsibilities:

- **Risk Assessment Service** (This repository): Calculates diabetes risk scores and provides structured risk data
- **Health Recommendations Service**: Generates personalized health tips and recommendations
- **Frontend Application**: User interface for data input and result display

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
├── requirements.txt
├── README.md
├── CONTRIBUTING.md
└── .gitignore
```

## 🚀 Development Setup

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd backend
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the development server:**
   ```bash
   python -m uvicorn app.main:app --reload
   ```

4. **Access the API:**
   - Health check: http://localhost:8000/
   - API docs: http://localhost:8000/docs

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

### Pull Request Process
1. Create a feature branch from `main`
2. Make your changes with clear commit messages
3. Test your changes thoroughly
4. Update documentation if needed
5. Create a pull request with detailed description
6. Request review from team members

## 🧪 Testing

### Running Tests
```bash
# Run all tests
python -m pytest

# Run specific test file
python -m pytest tests/test_risk_scoring.py

# Run with coverage
python -m pytest --cov=app
```

### Test Structure
```
tests/
├── __init__.py
├── test_models.py
├── test_risk_scoring.py
└── test_api.py
```

## 📋 Code Standards

### Python Style Guide
- Follow PEP 8 style guidelines
- Use type hints for all function parameters and return values
- Keep functions small and focused
- Add docstrings for all public functions

### FastAPI Best Practices
- Use Pydantic models for request/response validation
- Implement proper error handling
- Add comprehensive API documentation
- Use async/await for I/O operations

### Example Code Structure
```python
from typing import Tuple, List
from pydantic import BaseModel, Field

class RiskInput(BaseModel):
    """Patient data model for risk assessment."""
    name: str = Field(..., description="Patient name")
    age: int = Field(..., ge=10, le=120, description="Patient age")

def calculate_risk(patient_data: RiskInput) -> Tuple[int, str, List[str]]:
    """
    Calculate diabetes risk score based on patient data.
    
    Args:
        patient_data: Patient information for risk assessment
        
    Returns:
        Tuple of (risk_score, risk_level, flags)
    """
    # Implementation here
    pass
```

## 🔗 API Integration

### Service Communication
This service is designed to work with other services:

1. **Input**: Patient questionnaire data
2. **Process**: Risk calculation and scoring
3. **Output**: Structured risk assessment data
4. **Integration**: Other services consume the risk data for recommendations

### API Response Format
```json
{
  "risk_score": 75,
  "risk_level": "High",
  "flags": ["age_high", "bmi_high", "high_glucose_history"],
  "guideline": "Risk assessment completed. Score: 75, Level: High",
  "tips": {
    "risk_factors": ["age_high", "bmi_high", "high_glucose_history"],
    "score_breakdown": "Total risk score: 75/100",
    "next_step": "Forward to health recommendations service"
  }
}
```

## 🚨 Important Notes

### Risk Scoring Logic
- Risk scoring is based on medical guidelines
- Changes to scoring logic require medical review
- All scoring changes must be documented and tested

### Data Privacy
- No patient data is stored permanently
- All data is processed in memory only
- Implement proper data handling for production

### Environment Variables
- Use environment variables for configuration
- Never commit sensitive data to version control
- Create `.env.example` for required environment variables

## 🤝 Collaboration Guidelines

### Communication
- Use GitHub Issues for bug reports and feature requests
- Use GitHub Discussions for general questions
- Tag team members for reviews and discussions

### Code Review
- All code changes require at least one review
- Address all review comments before merging
- Test changes thoroughly before requesting review

### Documentation
- Update README.md for significant changes
- Add inline comments for complex logic
- Document API changes in commit messages

## 🆘 Getting Help

- Create an issue for bugs or feature requests
- Use GitHub Discussions for questions
- Check existing documentation and examples
- Review similar issues and pull requests

## 📝 License

This project is part of a hackathon submission. Please respect the project's license and contribution guidelines.

---

Thank you for contributing to making healthcare technology better! 🏥💻
