import argparse

from src.extract_text import extract_text
from src.llm_extractor import extract_data
from src.comparator import load_hr_requirements, compare_resume
from src.scorer import calculate_score
from src.report import generate_report, save_report

def main():

    parser = argparse.ArgumentParser(
        description="AI Resume Matcher"
    )

    parser.add_argument(
        "resume",
        help="Path to resume PDF or DOCX"
    )

    args = parser.parse_args()

    resume_text = extract_text(args.resume)

    resume = extract_data(resume_text)

    hr = load_hr_requirements("data/hr_requirements.json")

    comparison = compare_resume(resume, hr)

    score = calculate_score(comparison, hr)

    generate_report(
        resume,
        comparison,
        score
    )
    save_report(
    resume,
    comparison,
    score
)

if __name__ == "__main__":
    main()