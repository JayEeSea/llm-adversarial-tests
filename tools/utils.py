import csv
import os
import requests
from datetime import datetime
from config import ADVERSARIALTRACKER_API_URL, TEST_TYPE_MAP, REVERSE_TEST_TYPE_MAP
from apisecrets import OPENAI_API_KEY
from openai import OpenAI

# Client instantiation
openai_client = OpenAI(api_key=OPENAI_API_KEY)

def LogToCSV(timestamp, model_name, test_type_id, prompt, result, file_path="attempt_log.csv"):
    file_exists = os.path.isfile(file_path)
    is_empty = not file_exists or os.stat(file_path).st_size == 0

    # Convert ID to name
    test_type_name = REVERSE_TEST_TYPE_MAP.get(test_type_id, f"Unknown({test_type_id})")

    with open(file_path, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f, quoting=csv.QUOTE_ALL)

        # Write header if file is new or empty
        if is_empty:
            writer.writerow(["Timestamp", "Model", "TestType", "Prompt", "Result"])

        writer.writerow([timestamp, model_name, test_type_name, prompt, result])
        
def TestPromptAgainstModel(prompt_text, test_type_id, model_entry):
    name = model_entry["name"]
    provider = model_entry["provider"]
    model_id = model_entry["model_used_id"]
    model_key = model_entry["model"]

    print(f"\nTesting {provider.upper()} model: {name}")

    try:
        if provider == "openai":
            # Use temperature=1.0 for o4-mini, else 0.7
            temperature = 1.0 if model_key == "o4-mini" else 0.7

            response = openai_client.chat.completions.create(
                model=model_key,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt_text}
                ],
                temperature=temperature
            )
            result_text = response.choices[0].message.content.strip()

        else:
            print(f"Unknown provider: {provider}")
            return

        print("Model response:")
        print(result_text[:250] + "..." if len(result_text) > 250 else result_text)

    except Exception as e:
        print(f"{provider.upper()} request failed: {e}")
        return

    # Post to Tracker
    payload = {
        "PromptText": prompt_text,
        "TestType": test_type_id,
        "ModelUsedId": model_id,
        "Result": result_text,
        "Success": False
    }

    try:
        r = requests.post(
            ADVERSARIALTRACKER_API_URL,
            headers={"Content-Type": "application/json"},
            json=payload,
            verify=False
        )

        if r.status_code == 201:
            print(f"Logged to Adversarial Tracker for {name}")
            LogToCSV(datetime.now(), name, test_type_id, prompt_text, result_text)
        else:
            print(f"API error for {name}: {r.status_code} - {r.text}")

    except Exception as e:
        print(f"Failed to post to Tracker for {name}: {e}")