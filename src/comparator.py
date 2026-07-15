import json
def load_hr_requirements(file_path: str):
    with open(file_path, "r") as file:
        return json.load(file)

def compare_resume(resume, hr):
    matched_skills = []
    missing_skills = []

    resume_skills = {skill.lower() for skill in resume.skills}
    for skill in hr["skills"]:
        if skill.lower() in resume_skills:
            matched_skills.append(skill)
        else:
            missing_skills.append(skill)

    experience_match = resume.experience >= hr["experience"]
    project_match = len(resume.projects) >= hr["projects"]

    return{
        "matched_skills" : matched_skills,
        "missing_skills" : missing_skills,
        "experience_match" : experience_match,
        "projects_match" : project_match
    }


    