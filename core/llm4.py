import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("MISTRAL_KEY")


def ask_mistral(prompt):

    print("🤖 Calling Mistral...")

    url = "https://api.mistral.ai/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "mistral-small",
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    try:
        res = requests.post(url, json=data, headers=headers, timeout=20)

        # -----------------------
        # ERROR CHECK
        # -----------------------
        if res.status_code != 200:
            print("❌ LLM ERROR:", res.status_code, res.text)
            return "Sorry, LLM failed."

        result = res.json()

        # -----------------------
        # SAFE EXTRACTION
        # -----------------------
        if "choices" not in result:
            return "Invalid LLM response structure."

        return result["choices"][0]["message"]["content"]

    except requests.exceptions.Timeout:
        return "LLM timeout error."

    except Exception as e:
        return f"Unexpected error: {str(e)}"