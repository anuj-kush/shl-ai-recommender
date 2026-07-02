import json
from pathlib import Path

import requests

API_URL = "http://127.0.0.1:8000/chat"

TRACE_DIR = Path("data/traces")


def build_messages(trace_text):
    """
    Convert markdown conversation into API messages.
    """
    messages = []

    lines = trace_text.splitlines()

    current_role = None
    current_content = []

    for line in lines:

        line = line.strip()

        if line == "**User**":

            if current_role:
                messages.append({
                    "role": current_role,
                    "content": "\n".join(current_content).strip()
                })

            current_role = "user"
            current_content = []

        elif line == "**Agent**":

            if current_role:
                messages.append({
                    "role": current_role,
                    "content": "\n".join(current_content).strip()
                })

            current_role = "assistant"
            current_content = []

        elif line.startswith(">"):

            current_content.append(line.replace(">", "").strip())

    if current_role:
        messages.append({
            "role": current_role,
            "content": "\n".join(current_content).strip()
        })

    return messages


def evaluate_trace(file_path):

    print("=" * 80)
    print(file_path.name)

    text = file_path.read_text(encoding="utf-8")

    messages = build_messages(text)

    payload = {
        "messages": messages
    }

    response = requests.post(API_URL, json=payload)

    print("Status:", response.status_code)

    if response.status_code != 200:
        print(response.text)
        return

    result = response.json()

    print(json.dumps(result, indent=2))


if __name__ == "__main__":

    for trace in sorted(TRACE_DIR.glob("*")):
        evaluate_trace(trace)