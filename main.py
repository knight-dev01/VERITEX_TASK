from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI(
    title="Candidate Capability Assessment API",
    description="A simple backend service to assess candidate profiles.",
    version="1.0.0"
)

# Input Models
class CandidateProfile(BaseModel):
    name: str
    years_of_experience: float
    skills: List[str]
    certifications: Optional[List[str]] = []
    leadership_experience: bool = False

# Output Models
class AssessmentDimension(BaseModel):
    dimension_name: str
    score: int  # 0 to 10 scale
    feedback: str

class CapabilityAssessment(BaseModel):
    candidate_name: str
    overall_score: float
    dimensions: List[AssessmentDimension]
    recommended_level: str

def assess_technical_competence(skills: List[str], certs: List[str]) -> AssessmentDimension:
    """Evaluates technical competence based on breadth of skills and certifications."""
    score = min(len(skills) + (len(certs) * 2), 10)
    feedback = f"Demonstrates knowledge in {len(skills)} skill(s) and holds {len(certs)} certification(s)."
    
    if score >= 8:
        feedback += " Excellent technical foundation."
    elif score >= 5:
        feedback += " Solid technical background."
    else:
        feedback += " May require additional technical training."
        
    return AssessmentDimension(
        dimension_name="Technical Competence",
        score=score,
        feedback=feedback
    )

def assess_experience(years: float) -> AssessmentDimension:
    """Evaluates professional tenure."""
    if years >= 8:
        score = 10
    elif years >= 5:
        score = 8
    elif years >= 3:
        score = 6
    elif years >= 1:
        score = 4
    else:
        score = 2
    
    feedback = f"Has {years} years of professional experience."
    return AssessmentDimension(
        dimension_name="Professional Experience",
        score=score,
        feedback=feedback
    )

def assess_leadership(leadership: bool, years: float) -> AssessmentDimension:
    """Evaluates leadership potential using explicit indicators and tenure."""
    if leadership and years >= 5:
        score = 9
        feedback = "Strong indicators of leadership capabilities coupled with tenure."
    elif leadership:
        score = 7
        feedback = "Shows leadership potential."
    elif years >= 5:
        score = 5
        feedback = "Has tenure, but lacks explicit leadership experience."
    else:
        score = 3
        feedback = "Early in career, leadership potential yet to be developed."
        
    return AssessmentDimension(
        dimension_name="Leadership Potential",
        score=score,
        feedback=feedback
    )

@app.post("/assess", response_model=CapabilityAssessment)
async def assess_candidate(profile: CandidateProfile):
    """
    Endpoint to assess a candidate profile and return a structured capability evaluation.
    """
    try:
        # Evaluate dimensions
        dim_tech = assess_technical_competence(profile.skills, profile.certifications or [])
        dim_exp = assess_experience(profile.years_of_experience)
        dim_lead = assess_leadership(profile.leadership_experience, profile.years_of_experience)
        
        dimensions = [dim_tech, dim_exp, dim_lead]
        overall = sum([d.score for d in dimensions]) / len(dimensions)
        
        # Determine recommended level
        level = "Junior"
        if overall >= 7.5:
            level = "Senior / Lead"
        elif overall >= 4.5:
            level = "Mid-Level"
            
        return CapabilityAssessment(
            candidate_name=profile.name,
            overall_score=round(overall, 1),
            dimensions=dimensions,
            recommended_level=level
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred during assessment: {str(e)}")
