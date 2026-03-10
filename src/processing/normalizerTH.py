def normalize_theharvester(data):
    normalized = {
        "emails": [],
        "hosts": [],
        "ips": []
    }

    if not data:
        return normalized

    normalized["emails"] = data.get("emails", [])
    normalized["hosts"] = data.get("hosts", [])
    normalized["ips"] = data.get("ips", [])

    return normalized