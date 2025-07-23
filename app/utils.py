import openai
from app.llm_guard_init import prompt_scanner, output_scanner
from app.promptme_simulator import load_all_challenge_prompts
import os

def evaluate_challenges():
    results = []
    prompts = load_all_challenge_prompts()

    for item in prompts:
        prompt = item["prompt"]
        challenge = item["challenge"]

        cleaned, issues = prompt_scanner.scan(prompt)
        if issues:
            results.append((challenge, prompt, "❌ Blocked by Input Scanner"))
            continue

        try:
            completion = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": cleaned}]
            )
            raw = completion.choices[0].message["content"]
            safe, out_issues = output_scanner.scan(raw)

            verdict = "✅ Passed" if not out_issues else "⚠️ Blocked by Output Scanner"
            results.append((challenge, prompt, verdict))

        except Exception as e:
            results.append((challenge, prompt, f"⚠️ Error: {e}"))

    return results
