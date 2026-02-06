import os
import requests

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

def ask_llm(prompt):
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "llama3-70b-8192",
        "messages": [
            {"role": "system", "content": "You are an AI photo assistant."},
            {"role": "user", "content": prompt}
        ]
    }

    res = requests.post(GROQ_URL, json=payload, headers=headers)
    res.raise_for_status()
    return res.json()["choices"][0]["message"]["content"]
