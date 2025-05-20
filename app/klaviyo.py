import os
import requests

def fetch_klaviyo_data():
    api_key = os.getenv("KLAVIYO_API_KEY")
    headers = {
        "Authorization": f"Klaviyo-API-Key {api_key}",
        "revision": "2023-02-22"
    }

    response = requests.get("https://a.klaviyo.com/api/metrics/", headers=headers)
    if response.status_code == 200:
        return response.json()
    return {"error": "Could not fetch Klaviyo data"}
# Klaviyo integration module
