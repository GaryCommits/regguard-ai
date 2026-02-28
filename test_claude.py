import re
import json
import anthropic
from dotenv import load_dotenv
import os

load_dotenv()

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

def classify_risk(description):
    print("=== RegGuard AI — Calling Claude ===")

    message = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=1024,
        messages=[{
            "role": "user",
            "content": f"""You are RegGuard AI — Ireland's official EU AI Act compliance expert.

Classify this AI system according to the EU AI Act.

System: {description}

Output ONLY valid JSON with no markdown, no code fences, no explanation:
{{
  "risk_level": "high/prohibited/limited/minimal",
  "reason": "exact Annex reference + short explanation",
  "docs_needed": ["list of docs"],
  "human_oversight": "yes/no + brief details",
  "next_steps": "clear actions"
}}"""
        }]
    )

    raw = message.content[0].text
    print("Raw response:", raw[:500])

    cleaned = re.sub(r"```(?:json)?\s*|\s*```", "", raw).strip()
    result = json.loads(cleaned)

    print(f"\nRisk Level: {result['risk_level'].upper()}")
    print(f"Reason: {result['reason']}")
    print(f"Docs Needed: {', '.join(result['docs_needed'])}")
    print(f"Human Oversight: {result['human_oversight']}")
    print(f"Next Steps: {result['next_steps']}")

# This line actually calls the function — without it nothing runs!
classify_risk("AI system in a Donegal farm using computer vision to detect sick cattle")