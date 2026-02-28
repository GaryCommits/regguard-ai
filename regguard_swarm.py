import requests
import json
import re
from dotenv import load_dotenv
import os
from pinecone_rag import query_reg   # ← this pulls real EU AI Act text

load_dotenv()

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

class RegGuardSwarm:
    def run_full_swarm(self, description_or_image):
        print(f"🚀 Real Claude Haiku 4.5 + RAG Swarm analysing...")

        # Get real regulatory context from Pinecone
        reg_context = query_reg(description_or_image, top_k=4)

        # If it's an image (base64), use vision model
        if "base64" in str(description_or_image):
            model = "claude-3-5-sonnet-20240620"
            content = [
                {"type": "text", "text": f"""You are RegGuard AI — Ireland's official EU AI Act compliance expert.

Use this official EU AI Act text to be 100% accurate:
{reg_context}

Classify this AI system shown in the uploaded image and generate full compliance output.

Return ONLY valid JSON with this exact structure (no markdown, no extra text):
{{
  "risk_level": "prohibited/high/limited/minimal",
  "reason": "exact Annex reference + explanation",
  "docs_needed": ["list of docs"],
  "human_oversight": "yes/no + details",
  "next_steps": "clear actions",
  "technical_documentation": "full Annex IV style summary"
}}"""},
                {"type": "image", "source": {"type": "base64", "media_type": "image/png", "data": description_or_image.split("base64:")[-1]}}
            ]
        else:
            model = "claude-haiku-4-5-20251001"
            content = [{"type": "text", "text": f"""You are RegGuard AI — Ireland's official EU AI Act compliance expert.

Use this official EU AI Act text to be 100% accurate:
{reg_context}

Classify this AI system and generate full compliance output.

System: {description_or_image}

Return ONLY valid JSON with this exact structure (no markdown, no extra text):
{{
  "risk_level": "prohibited/high/limited/minimal",
  "reason": "exact Annex reference + explanation",
  "docs_needed": ["list of docs"],
  "human_oversight": "yes/no + details",
  "next_steps": "clear actions",
  "technical_documentation": "full Annex IV style summary"
}}"""}]

        url = "https://api.anthropic.com/v1/messages"
        payload = {
            "model": model,
            "max_tokens": 1024,
            "temperature": 0,
            "messages": [{"role": "user", "content": content}]
        }
        headers = {
            "x-api-key": ANTHROPIC_API_KEY,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json"
        }

        response = requests.post(url, json=payload, headers=headers)

        if response.status_code == 200:
            raw = response.json()["content"][0]["text"]
            cleaned = re.sub(r'^```json\s*|\s*```$', '', raw.strip()).strip()
            try:
                result = json.loads(cleaned)
            except:
                result = None
        else:
            print(f"Claude error {response.status_code}")
            result = None

        if result is None:
            result = {"risk_level": "high", "reason": "Fallback - RAG active", "docs_needed": ["Annex IV"], "human_oversight": "yes", "next_steps": "Test again", "technical_documentation": "RAG fallback"}

        return result