import os
import json

def load_all_challenge_prompts(challenges_dir="promptme/challenges"):
    prompts = []
    for root, _, files in os.walk(challenges_dir):
        for file in files:
            if file.endswith(".json"):
                with open(os.path.join(root, file)) as f:
                    data = json.load(f)
                    for item in data:
                        if "prompt" in item:
                            prompts.append({"challenge": os.path.basename(root), "prompt": item["prompt"]})
    return prompts
