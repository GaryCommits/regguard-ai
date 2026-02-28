import requests

# ←←← PASTE YOUR FULL KEY HERE (replace everything between the quotes)
GROK_API_KEY = "xai-oldV9XoRkB6B3rp8oemrb5JCEUIR5grpfHOZ48WzkCcsZWp9rHRARwzlw7aphe2V715DbfbAx0y0576"

def classify_risk(description):
    url = "https://api.x.ai/v1/chat/completions"
    payload = {
        "model": "grok-4",
        "messages": [
            {"role": "system", "content": "You are RegGuard AI — Ireland's official EU AI Act compliance expert. Classify exactly per the EU AI Act. Output ONLY valid JSON."},
            {"role": "user", "content": f"""System: {description}
Output ONLY this JSON (nothing else):
{{
  "risk_level": "prohibited/high/limited/minimal",
  "reason": "exact Annex reference + explanation",
  "docs_needed": ["Annex IV", "risk management system"],
  "human_oversight": "yes/no + details",
  "next_steps": "clear actions"
}}"""}
        ],
        "temperature": 0
    }
    headers = {
        "Authorization": f"Bearer {GROK_API_KEY}",
        "Content-Type": "application/json"
    }
    response = requests.post(url, json=payload, headers=headers)
    content = response.json()["choices"][0]["message"]["content"]
    print("\n=== RegGuard AI Classification ===\n")
    print(content)

# TEST IT
classify_risk("AI system in a Donegal farm using computer vision to detect sick cattle")