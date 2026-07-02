from fastapi import FastAPI
from google.api_core.exceptions import ResourceExhausted

from app.retriever import search, compare_assessments
from app.logger import logger
from app.schemas import ChatRequest, ChatResponse, Recommendation
from app.gemini_service import (
    extract_requirements,
    build_search_query,
    is_comparison_request,
)

app = FastAPI()


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):

    messages = [m.model_dump() for m in request.messages]

    # -----------------------------
    # Handle assessment comparison
    # -----------------------------
    if is_comparison_request(messages):

        text = messages[-1]["content"]

        if " vs " in text.lower():

            parts = text.split(" vs ")

            if len(parts) == 2:

                result = compare_assessments(
                    parts[0].replace("Compare", "").strip(),
                    parts[1].strip(),
                )

                if result:

                    a = result["assessment_1"]
                    b = result["assessment_2"]

                    comparison = f"""
Assessment Comparison

{a['name']}

• Duration: {a['duration']}
• Job Levels: {a['job_levels']}
• Remote Testing: {a['remote']}
• Adaptive: {a['adaptive']}

VS

{b['name']}

• Duration: {b['duration']}
• Job Levels: {b['job_levels']}
• Remote Testing: {b['remote']}
• Adaptive: {b['adaptive']}
"""

                    return ChatResponse(
                        reply=comparison,
                        recommendations=[],
                        end_of_conversation=True,
                    )

    try:
        # Extract hiring requirements using Gemini
        requirements = extract_requirements(messages)

        # Ask clarification if needed
        if requirements.get("clarification_needed", False):
            return ChatResponse(
                reply=requirements["clarification_question"],
                recommendations=[],
                end_of_conversation=False,
            )

        # Build semantic search query
        query = build_search_query(requirements)

        logger.info(f"Search Query: {query}")

        # Retrieve top assessments
        retrieved = search(query, top_k=5)

        logger.info(f"Retrieved {len(retrieved)} assessments")

        recommendations = []

        for assessment in retrieved:
            recommendations.append(
                Recommendation(
                    name=assessment["name"],
                    url=assessment["url"],
                    test_type=assessment["test_type"],
                )
            )

        return ChatResponse(
            reply="Based on your requirements, here are the most relevant SHL assessments.",
            recommendations=recommendations,
            end_of_conversation=True,
        )

    except ResourceExhausted:
        logger.error("Gemini API quota exceeded.")

        return ChatResponse(
            reply="The AI service is temporarily unavailable because the Gemini API quota has been exceeded. Please try again later.",
            recommendations=[],
            end_of_conversation=False,
        )

    except Exception as e:
        logger.exception(e)

        return ChatResponse(
            reply="An unexpected error occurred while processing your request.",
            recommendations=[],
            end_of_conversation=False,
        )