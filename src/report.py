import json
import os 

def generate_report(resume, comparison, score):

    print("\n" + "=" * 50)
    print("        RESUME MATCH REPORT")
    print("=" * 50)

    print(f"\nCandidate : {resume.name}")
    print(f"Match Score : {score}%")

    print("\nMatched Skills")
    print("-" * 20)

    for skill in comparison["matched_skills"]:
        print(f"✓ {skill}")

    print("\nMissing Skills")
    print("-" * 20)

    for skill in comparison["missing_skills"]:
        print(f"✗ {skill}")

    print("\nExperience Match :", comparison["experience_match"])
    print("Project Match    :", comparison["projects_match"])


    print("\nRecommendation")

    if score >= 80:
        print("Strong Match")

    elif score >= 60:
        print("Good Match")

    elif score >= 40:
        print("Average Match")

    else:
        print("Poor Match")

def save_report(resume, comparison, score):

    report = {
        "candidate": resume.name,
        "match_score": score,
        "matched_skills": comparison["matched_skills"],
        "missing_skills": comparison["missing_skills"],
        "experience_match": comparison["experience_match"],
        "project_match": comparison["projects_match"]
    }

    if score >= 80:
        report["recommendation"] = "Strong Match"
    elif score >= 60:
        report["recommendation"] = "Good Match"
    elif score >= 40:
        report["recommendation"] = "Average Match"
    else:
        report["recommendation"] = "Poor Match"

    os.makedirs("output", exist_ok=True)

    with open("output/report.json", "w", encoding="utf-8") as file:
        json.dump(report, file, indent=4)