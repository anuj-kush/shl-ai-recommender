TEST_TYPE_MAP = {
    "Knowledge & Skills": "K",
    "Personality & Behavior": "P",
    "Ability & Aptitude": "A",
    "Biodata & Situational Judgment": "B",
    "Assessment Exercises": "E",
    "Competencies": "C",
    "Development & 360": "D",
}
def get_test_type(keys):
    for key in keys:
        if key in TEST_TYPE_MAP:
            return TEST_TYPE_MAP[key]
    return "Other"