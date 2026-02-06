import os
import requests
import re
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL = "llama3-70b-8192"


def clean_keywords(text: str) -> str:
    """
    Normalize LLM output into space-separated keywords
    """
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def ask_llm(prompt: str) -> str:
    """
    Extract keywords from user query using Groq.
    Falls back safely if API fails.
    """

    # 🔒 Hard fallback (never break app)
    if not GROQ_API_KEY:
        return clean_keywords(prompt)

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": MODEL,
        "messages": [
            {
                "role": "system",
                "content": (
                    "You extract important visual keywords from photo search queries. "
                    "Return ONLY keywords, no sentences."
                ),
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
        "temperature": 0,
    }

    try:
        res = requests.post(GROQ_URL, json=payload, headers=headers, timeout=10)
        res.raise_for_status()

        raw = res.json()["choices"][0]["message"]["content"]
        return clean_keywords(raw)

    except Exception as e:
        print("LLM FALLBACK:", e)
        return clean_keywords(prompt)
