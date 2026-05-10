# Candidate Capability Assessment Service

A simple Python backend service built with FastAPI that accepts a candidate profile and returns a structured capability assessment based on defined criteria.

## Evaluation Dimensions
The system evaluates candidates across three primary dimensions:
1. **Technical Competence**: Assessed based on the breadth of skills and number of certifications.
2. **Professional Experience**: Assessed based on the total years of professional experience.
3. **Leadership Potential**: Evaluated by combining explicit leadership experience flags with overall tenure.

## Approach & Architecture
- **Framework**: FastAPI for its high performance, automatic OpenAPI documentation, and robust request/response validation.
- **Validation**: Pydantic models are used to enforce strict schema definitions for both inputs (`CandidateProfile`) and outputs (`CapabilityAssessment`).
- **Scoring Logic**: Simple heuristic-based scoring algorithms convert qualitative and quantitative profile attributes into a normalized 0-10 score per dimension. An overall score and recommended seniority level are synthesized from these dimensions.

## Requirements
- Python 3.8+

## Installation & Running

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
uvicorn main:app --reload
```

3. Test the API:
The interactive API documentation (Swagger UI) is available at:
`http://127.0.0.1:8000/docs`

### Example Request
```json
POST /assess
{
  "name": "Jane Doe",
  "years_of_experience": 6.5,
  "skills": ["Python", "FastAPI", "PostgreSQL", "Docker", "AWS"],
  "certifications": ["AWS Certified Solutions Architect"],
  "leadership_experience": true
}
```

### Example Response
```json
{
  "candidate_name": "Jane Doe",
  "overall_score": 8.0,
  "dimensions": [
    {
      "dimension_name": "Technical Competence",
      "score": 7,
      "feedback": "Demonstrates knowledge in 5 skill(s) and holds 1 certification(s). Solid technical background."
    },
    {
      "dimension_name": "Professional Experience",
      "score": 8,
      "feedback": "Has 6.5 years of professional experience."
    },
    {
      "dimension_name": "Leadership Potential",
      "score": 9,
      "feedback": "Strong indicators of leadership capabilities coupled with tenure."
    }
  ],
  "recommended_level": "Senior / Lead"
}
```
