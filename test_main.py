from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_assess_junior_candidate():
    response = client.post(
        "/assess",
        json={
            "name": "John Smith",
            "years_of_experience": 2.0,
            "skills": ["Python", "SQL"],
            "leadership_experience": False
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["candidate_name"] == "John Smith"
    assert data["recommended_level"] == "Junior"
    assert len(data["dimensions"]) == 3

def test_assess_senior_candidate():
    response = client.post(
        "/assess",
        json={
            "name": "Jane Doe",
            "years_of_experience": 8.0,
            "skills": ["Python", "FastAPI", "React", "Docker", "AWS", "SQL", "Redis"],
            "certifications": ["AWS Certified Solutions Architect"],
            "leadership_experience": True
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["candidate_name"] == "Jane Doe"
    assert data["recommended_level"] == "Senior / Lead"
