import time
import csv
from utils import TestPromptAgainstModel
from config import TEST_TYPE_MAP, models_to_test

# ─────────────────────────────────────────────────────
# CONFIGURATION
# ─────────────────────────────────────────────────────

def load_prompts_from_csv(path):
    prompts = []
    with open(path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            prompts.append({
                "PromptText": row["Prompt"].strip(),
                "TestType": row["TestType"].strip()
            })
    return prompts

prompt_entries = load_prompts_from_csv("prompts.csv")

# ─────────────────────────────────────────────────────
# SEND THE PROMPT AND RECORD THE RESPONSE
# ─────────────────────────────────────────────────────

if __name__ == "__main__":
    for prompt in prompt_entries:
        prompt_text = prompt.get("PromptText", "").strip()
        test_type_str = prompt.get("TestType", "").strip()
        test_type_id = TEST_TYPE_MAP.get(test_type_str)

        if test_type_id is None:
            raise ValueError(f"Invalid TestType in CSV: {test_type_str}")

        for model in models_to_test:
            TestPromptAgainstModel(prompt_text, test_type_id, model)
            time.sleep(1)