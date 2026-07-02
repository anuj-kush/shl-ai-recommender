from dataclasses import dataclass
from typing import List


@dataclass
class ConversationState:
    intent: str
    role: str
    experience: str
    clarification_needed: bool
    clarification_question: str
    end_of_conversation: bool

def detect_intent(message: str) -> str:

    text = message.lower()

    if any(word in text for word in [
        "compare",
        "difference",
        "vs",
        "versus"
    ]):
        return "comparison"

    if any(word in text for word in [
        "change",
        "replace",
        "remove",
        "add"
    ]):
        return "refinement"

    if any(word in text for word in [
        "thanks",
        "looks good",
        "perfect",
        "final",
        "done"
    ]):
        return "confirmation"

    return "recommendation"

def extract_role(messages):

    text = " ".join(
        m["content"]
        for m in messages
        if m["role"] == "user"
    ).lower()

    if "java" in text:
        return "Java Developer"

    if "python" in text:
        return "Python Developer"

    if "react" in text:
        return "React Developer"

    if "aws" in text:
        return "Cloud Engineer"

    return ""

def extract_experience(messages):

    text = " ".join(
        m["content"]
        for m in messages
        if m["role"] == "user"
    ).lower()

    if "entry" in text:
        return "Entry"

    if "graduate" in text:
        return "Graduate"

    if "mid" in text:
        return "Mid"

    if "senior" in text:
        return "Senior"

    return ""

def clarification_question(role, experience):

    if role == "":
        return True, "What role are you hiring for?"

    if experience == "":
        return True, "What experience level are you looking for?"

    return False, ""

def analyze_conversation(messages):

    last_user = ""

    for msg in reversed(messages):
        if msg["role"] == "user":
            last_user = msg["content"]
            break

    intent = detect_intent(last_user)

    role = extract_role(messages)

    experience = extract_experience(messages)

    need, question = clarification_question(
        role,
        experience
    )

    return ConversationState(
        intent=intent,
        role=role,
        experience=experience,
        clarification_needed=need,
        clarification_question=question,
        end_of_conversation=(intent == "confirmation")
    )

if __name__ == "__main__":

    messages = [
        {
            "role": "user",
            "content": "Hiring a Java Developer"
        },
        {
            "role": "assistant",
            "content": "What experience level?"
        },
        {
            "role": "user",
            "content": "Mid level"
        }
    ]

    state = analyze_conversation(messages)

    print(state)