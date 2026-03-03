import re
from scripts.schema import create_base_account


def extract_demo(transcript_text):
    data = create_base_account(source="demo_call")
    text = transcript_text.lower()

    # -----------------------------
    # Company Name Detection
    # -----------------------------
    company_match = re.search(r"this is (.+?)(\.|\n)", text)
    if company_match:
        data["company_profile"]["company_name"] = company_match.group(1).title()
    else:
        data["questions_or_unknowns"].append("Company name not clearly specified")

    # -----------------------------
    # Business Hours Detection
    # -----------------------------
    hours_match = re.search(r"(\d+ ?(am|pm)) to (\d+ ?(am|pm))", text)
    if hours_match:
        data["business_hours"]["start_time"] = hours_match.group(1)
        data["business_hours"]["end_time"] = hours_match.group(3)
    else:
        data["questions_or_unknowns"].append("Business hours not clearly specified")

    # -----------------------------
    # Business Days Detection
    # -----------------------------
    if "monday" in text and "friday" in text:
        data["business_hours"]["days"] = ["Mon", "Tue", "Wed", "Thu", "Fri"]

    # -----------------------------
    # Timezone Detection
    # -----------------------------
    tz_match = re.search(r"(est|pst|cst|mst)", text)
    if tz_match:
        data["company_profile"]["timezone"] = tz_match.group(1).upper()
    else:
        data["questions_or_unknowns"].append("Timezone not specified")

    # -----------------------------
    # Emergency Triggers Detection
    # -----------------------------
    emergency_keywords = [
        "sprinkler",
        "fire alarm",
        "gas leak",
        "system failure"
    ]

    for keyword in emergency_keywords:
        if keyword in text:
            data["services"]["emergency_triggers"].append(keyword.title())

    if not data["services"]["emergency_triggers"]:
        data["questions_or_unknowns"].append("Emergency triggers not specified")

    return data