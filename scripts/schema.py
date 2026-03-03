from datetime import datetime
import uuid


def create_base_account(source="demo_call"):
    return {
        "meta": {
            "account_id": str(uuid.uuid4()),
            "version": "v1",
            "created_at": datetime.utcnow().isoformat(),
            "source": source
        },
        "company_profile": {
            "company_name": "",
            "office_address": "",
            "timezone": ""
        },
        "business_hours": {
            "days": [],
            "start_time": "",
            "end_time": ""
        },
        "services": {
            "supported": [],
            "emergency_triggers": []
        },
        "routing": {
            "emergency": {
                "transfer_targets": [],
                "fallback_action": ""
            },
            "non_emergency": {
                "routing_logic": ""
            }
        },
        "call_transfer_rules": {
            "timeout_seconds": "",
            "retry_count": "",
            "failure_message": ""
        },
        "integration_constraints": [],
        "flow_summaries": {
            "office_hours": "",
            "after_hours": ""
        },
        "questions_or_unknowns": [],
        "notes": ""
    }