from src.extract_text import extract_text
from src.llm_extractor import extract_data
from src.comparator import (
    load_hr_requirements,
    compare_resume,
)

text = extract_text("data/resumes/resume.pdf")

resume = extract_data(text)

hr = load_hr_requirements("data/hr_requirements.json")

result = compare_resume(resume, hr)

print(result)