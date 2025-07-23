# app/llm_guard_init.py

from llm_guard.input_scanners.prompt_injection import PromptInjection

def prompt_scanner(prompt):
    scanner = PromptInjection()
    cleaned_prompt, is_injection, score = scanner.scan(prompt)

    threshold = 0.75  # you can tune this
    if is_injection and score >= threshold:
        return None, [f"Prompt blocked (score {score:.2f})"]
    
    return cleaned_prompt, []

# 🔧 Output scanner is a no-op for now
def output_scanner(output):
    return output, []

