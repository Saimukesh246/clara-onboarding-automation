import os
import json
import re
import sys
from scripts.agent_generator import generate_agent_spec
from scripts.versioning import apply_patch


# -----------------------------------
# Extract Updates From Onboarding
# -----------------------------------
def extract_onboarding_updates(transcript_text):
    updates = {}
    text = transcript_text.lower()

    # -----------------------------
    # 24/7 Business Hours Detection
    # -----------------------------
    if "24/7" in text or "24 hours" in text:
        updates["business_hours.start_time"] = "00:00"
        updates["business_hours.end_time"] = "23:59"

    # -----------------------------
    # Timeout Detection (e.g., 60 seconds)
    # -----------------------------
    timeout_match = re.search(r"(\d+)\s*seconds", text)
    if timeout_match:
        updates["call_transfer_rules.timeout_seconds"] = timeout_match.group(1)

    # -----------------------------
    # Retry Detection
    # -----------------------------
    retry_match = re.search(r"retry (once|twice|\d+)", text)
    if retry_match:
        value = retry_match.group(1)

        if value == "once":
            updates["call_transfer_rules.retry_count"] = "1"
        elif value == "twice":
            updates["call_transfer_rules.retry_count"] = "2"
        else:
            updates["call_transfer_rules.retry_count"] = value

    # -----------------------------
    # Timezone Update Detection
    # -----------------------------
    tz_match = re.search(r"(est|pst|cst|mst)", text)
    if tz_match:
        updates["company_profile.timezone"] = tz_match.group(1).upper()

    return updates


# -----------------------------------
# Run Onboarding Update For One Account
# -----------------------------------
def run_onboarding_pipeline(account_id, transcript_path):
    v1_path = os.path.join("outputs", "accounts", account_id, "v1")

    if not os.path.exists(v1_path):
        print(f"❌ v1 not found for account_id: {account_id}")
        return "missing_v1"

    # Load existing v1 account memo
    with open(os.path.join(v1_path, "account_memo.json"), "r") as f:
        existing_data = json.load(f)

    # Read onboarding transcript
    with open(transcript_path, "r", encoding="utf-8") as f:
        transcript = f.read()

    updates = extract_onboarding_updates(transcript)

    if not updates:
        print(f"⚠ No updates detected for account: {account_id}")
        return "no_updates"

    # Apply patch
    updated_data, changelog = apply_patch(existing_data, updates)

    # Prepare v2 path
    v2_path = os.path.join("outputs", "accounts", account_id, "v2")

    # Idempotency check
    if os.path.exists(v2_path):
        print(f"⚠ v2 already exists for account: {account_id}")
        return "already_exists"

    os.makedirs(v2_path, exist_ok=True)

    # Save updated account memo
    with open(os.path.join(v2_path, "account_memo.json"), "w") as f:
        json.dump(updated_data, f, indent=4)

    # Generate updated agent spec
    agent_spec = generate_agent_spec(updated_data)
    with open(os.path.join(v2_path, "agent_spec.json"), "w") as f:
        json.dump(agent_spec, f, indent=4)

    # Save changelog
    with open(os.path.join(v2_path, "changelog.json"), "w") as f:
        json.dump(changelog, f, indent=4)

    print(f"✅ v2 generated successfully for account: {account_id}")
    return "success"


# -----------------------------------
# Batch Processing Mode
# -----------------------------------
def run_batch_onboarding(folder="dataset/onboarding"):
    summary = {
        "processed": 0,
        "success": 0,
        "already_exists": 0,
        "no_updates": 0,
        "missing_v1": 0
    }

    for file in os.listdir(folder):
        if file.startswith("account_") and file.endswith(".txt"):
            account_id = file.replace("account_", "").replace(".txt", "")
            transcript_path = os.path.join(folder, file)

            result = run_onboarding_pipeline(account_id, transcript_path)

            summary["processed"] += 1
            if result in summary:
                summary[result] += 1

    print("\n📊 Onboarding Batch Summary")
    for key, value in summary.items():
        print(f"{key}: {value}")


# -----------------------------------
# CLI Mode
# -----------------------------------
if __name__ == "__main__":
    # If arguments passed → single account mode
    if len(sys.argv) == 3:
        account_id = sys.argv[1]
        transcript_path = sys.argv[2]
        run_onboarding_pipeline(account_id, transcript_path)

    # If no arguments → batch mode
    else:
        run_batch_onboarding()