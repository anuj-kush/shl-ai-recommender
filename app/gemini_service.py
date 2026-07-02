import json

import google.generativeai as genai
from app.config import GEMINI_API_KEY
from app.prompts import EXTRACT_REQUIREMENTS_PROMPT

from app.prompts import RANK_PROMPT

genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-2.5-flash")

def extract_requirements(messages):

    conversation = ""

    for m in messages:
        conversation += f"{m['role']}: {m['content']}\n"

    prompt = (
        EXTRACT_REQUIREMENTS_PROMPT
        + "\n\nConversation:\n"
        + conversation
    )

    response = model.generate_content(prompt)

    return json.loads(response.text)

def build_search_query(requirements):

    parts = []

    if requirements.get("role"):
        parts.append(requirements["role"])

    if requirements.get("experience"):
        parts.append(requirements["experience"])

    if requirements.get("job_level"):
        parts.append(requirements["job_level"])

    parts.extend(requirements.get("skills", []))

    if requirements.get("industry"):
        parts.append(requirements["industry"])

    return " ".join(parts)


def rank_assessments(requirements, assessments):

    prompt = f"""
{RANK_PROMPT}

Requirements:

{requirements}

Assessments:

{assessments}
"""

    response = model.generate_content(prompt)

    return json.loads(response.text)

def is_comparison_request(messages):
    last = messages[-1]["content"].lower()

    keywords = [
        "compare",
        "difference",
        "vs",
        "versus"
    ]

    return any(word in last for word in keywords)

