import os
import json
from scripts.extractor import extract_demo
from scripts.agent_generator import generate_agent_spec

def run_demo_pipeline(transcript_path):
    with open(transcript_path, "r", encoding="utf-8") as f:
        transcript = f.read()

    account_data = extract_demo(transcript)
    account_id = account_data["meta"]["account_id"]

    output_dir = os.path.join("outputs", "accounts", account_id, "v1")

    if os.path.exists(output_dir):
        print(f"⚠ Skipping {transcript_path} (already processed)")
        return

    os.makedirs(output_dir, exist_ok=True)

    with open(os.path.join(output_dir, "account_memo.json"), "w") as f:
        json.dump(account_data, f, indent=4)

    agent_spec = generate_agent_spec(account_data)

    with open(os.path.join(output_dir, "agent_spec.json"), "w") as f:
        json.dump(agent_spec, f, indent=4)

    print(f"✅ v1 generated for {transcript_path}")


def run_batch_demo(folder="dataset/demo"):
    for file in os.listdir(folder):
        if file.endswith(".txt"):
            run_demo_pipeline(os.path.join(folder, file))


if __name__ == "__main__":
    run_batch_demo()