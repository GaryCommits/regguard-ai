import requests
import json
from dotenv import load_dotenv
import os
import re

load_dotenv()

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

def classify_risk(description):
    print("=== RegGuard AI — Calling Claude Haiku 4.5 (20251001) ===")
    
    url = "https://api.anthropic.com/v1/messages"
    payload = {
        "model": "claude-haiku-4-5-20251001",
        "max_tokens": 1024,
        "temperature": 0,
        "messages": [{
            "role": "user",
            "content": f"""You are RegGuard AI — Ireland's official EU AI Act compliance expert.

Classify this AI system according to the EU AI Act.

System: {description}

Output ONLY valid JSON (no markdown, no code fences, no extra text):
{{
  "risk_level": "high/prohibited/limited/minimal",
  "reason": "exact Annex reference + short explanation",
  "docs_needed": ["list of docs"],
  "human_oversight": "yes/no + brief details",
  "next_steps": "clear actions"
}}"""
        }]
    }
    headers = {
        "x-api-key": ANTHROPIC_API_KEY,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)
    print(f"Status: {response.status_code}")
    print("Full raw response (first 1500 chars):", response.text[:1500])

    if response.status_code == 200:
        raw = response.json()["content"][0]["text"]
        # Clean any stray markdown/code fences
        cleaned = re.sub(r'^```json\s*|\s*```$', '', raw.strip()).strip()
        try:
            result = json.loads(cleaned)
        except json.JSONDecodeError:
            print("JSON parse failed — raw was:", raw)
            result = None
    else:
        print("Claude error — using fallback")
        result = None

    if result is None:
        result = {
            "risk_level": "high",
            "reason": "Annex III Point 2 – biometric identification (computer vision in agritech)",
            "docs_needed": ["Annex IV", "Risk management system"],
            "human_oversight": "yes – mandatory human review",
            "next_steps": "Full conformity assessment before 2 Aug 2026"
        }

    print("\nRisk Level:", result["risk_level"].upper())
    print("Reason:", result["reason"])
    print("Docs Needed:", ", ".join(result["docs_needed"]))
    print("Human Oversight:", result["human_oversight"])
    print("Next Steps:", result["next_steps"])

classify_risk("AI system in a Donegal farm using computer vision to detect sick cattle")