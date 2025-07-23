from promptme_simulator import load_all_challenge_prompts
from llm_guard_init import prompt_scanner, output_scanner
import openai

def evaluate_challenges():
    prompts = load_all_challenge_prompts()
    results = []

    for item in prompts:
        challenge = item["challenge"]
        prompt = item["prompt"]

        cleaned, prompt_issues = prompt_scanner(prompt)

        if prompt_issues:
            status = "Blocked (input)"
        else:
            try:
                completion = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": cleaned}]
                )
                raw_response = completion.choices[0].message["content"]
                _, output_issues = output_scanner(raw_response)
                if output_issues:
                    status = "Blocked (output)"
                else:
                    status = "Passed"
            except Exception:
                status = "API Error"

        results.append({
            "challenge": challenge,
            "prompt": prompt,
            "status": status
        })

    return results

