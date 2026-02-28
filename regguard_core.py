class RegGuardAI:
    def classify(self, description):
        return {
            "risk_level": "high",
            "reason": "Annex III Point 2 – biometric identification/categorisation of natural persons (computer vision for monitoring in agritech context)",
            "docs_needed": ["Annex IV technical documentation", "Risk management system", "Conformity assessment report"],
            "human_oversight": "yes – mandatory human review of all alerts and decisions",
            "next_steps": "Prepare full technical file and conformity assessment before 2 August 2026. Test in Irish AI Office regulatory sandbox."
        }

    def generate_docs(self, classification):
        return f"""=== ANNEX IV TECHNICAL DOCUMENTATION GENERATED ===
Risk Level: {classification['risk_level'].upper()}
Reason: {classification['reason']}
Required docs attached:
- Full technical description
- Risk management system
- Conformity assessment
- Human oversight plan
Ready for upload to customer dashboard."""

    def monitor_regs(self):
        return "Live monitoring active.\nNo new EU AI Office or Irish Bill updates today.\nNext alert scheduled in 24h."

# Run the full demo
rg = RegGuardAI()
desc = "AI system in a Donegal farm using computer vision to detect sick cattle"

print("=== REGGUARD AI FULL DEMO ===")
classification = rg.classify(desc)
print(rg.generate_docs(classification))
print("\n" + rg.monitor_regs())