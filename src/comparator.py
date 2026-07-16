import json
import os

from dotenv import load_dotenv
from groq import Groq

from src.model import JobD, Resume, MatchResult

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("GROQ_API_KEY not found in .env")

client = Groq(api_key=api_key)

MODEL = "llama-3.1-8b-instant"

def normalize_skill(skill: str) -> str:
    """
    Normalize a skill for comparison.
    """
    return skill.strip().lower()

SKILL_ALIASES = {
    "cloud platforms": {
        "aws",
        "azure",
        "gcp",
        "google cloud"
    },
    "database systems": {
        "sql",
        "mysql",
        "postgresql",
        "mongodb",
        "redis",
        "sqlite"
    },
    "version control systems": {
        "git",
        "github",
        "gitlab",
        "bitbucket"
    },
    "nosql": {
        "mongodb",
        "redis",
        "cassandra"
    },
    "ci/cd": {
        "github actions",
        "jenkins",
        "gitlab ci",
        "azure devops"
    },
    "containerization": {
        "docker",
        "kubernetes"
    }
}

def skill_matches(job_skill: str, resume_skills: set[str]) -> bool:
    normalized = normalize_skill(job_skill)

    if normalized in resume_skills:
        return True

    aliases = SKILL_ALIASES.get(normalized)

    if aliases:
        return any(alias in resume_skills for alias in aliases)

    return False

def load_job_description(file_path: str):
    with open(file_path, "r", encoding="utf-8") as file:
        if file_path.endswith(".json"):
            return JobD.model_validate(json.load(file))
        return file.read()

def compare_resume(job: JobD, resume: Resume) -> MatchResult:
    schema = MatchResult.model_json_schema()

    prompt = f"""
You are an expert technical recruiter.

Compare the following candidate with the job description.

Return ONLY valid JSON following this exact structure:
{{
  "score": 0.0,
  "matched_skills": ["string"],
  "missing_skills": ["string"],
  "strengths": ["string"],
  "weaknesses": ["string"],
  "recommendation": "string"
}}

Schema:
{schema}

Job Description:
{job.model_dump_json(indent=2)}

Candidate Resume:
{resume.model_dump_json(indent=2)}

Scoring Guidelines:
- Skills Match (40%)
- Experience Match (30%)
- Projects (20%)
- Education (10%)

Return:
- score (0-100)
- details
"""

    response = client.chat.completions.create(
        model=MODEL,
        response_format={"type": "json_object"},
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
    )

    data = json.loads(response.choices[0].message.content)

    match_result = MatchResult.model_validate(data)

    # Deterministic skill comparison
    resume_skills = {
        normalize_skill(skill)
        for skill in resume.skills
    }

    matched_skills = []
    missing_skills = []

    for skill in job.required_skills:
        if skill_matches(skill, resume_skills):
            matched_skills.append(skill)
        else:
            missing_skills.append(skill)

    for skill in job.preferred_skills:
        if skill_matches(skill, resume_skills):
            matched_skills.append(skill)
        else:
            missing_skills.append(skill)

    match_result.matched_skills = matched_skills
    match_result.missing_skills = missing_skills

    return match_result
