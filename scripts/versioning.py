import copy
from datetime import datetime


def apply_patch(existing_data, updates):
    """
    Applies updates to existing account memo
    Returns updated_data and changelog
    """

    updated_data = copy.deepcopy(existing_data)
    changelog = {
        "from_version": existing_data["meta"]["version"],
        "to_version": "v2",
        "updated_at": datetime.utcnow().isoformat(),
        "changes": []
    }

    for key_path, new_value in updates.items():
        keys = key_path.split(".")
        current = updated_data

        # Traverse nested keys
        for k in keys[:-1]:
            current = current[k]

        last_key = keys[-1]
        old_value = current.get(last_key)

        if old_value != new_value:
            current[last_key] = new_value
            changelog["changes"].append({
                "field": key_path,
                "previous": old_value,
                "updated": new_value
            })

    updated_data["meta"]["version"] = "v2"
    updated_data["meta"]["updated_at"] = datetime.utcnow().isoformat()

    return updated_data, changelog