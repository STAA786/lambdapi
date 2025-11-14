import json
import requests

def lambda_handler(event, context):
    city = event.get("city", "New York")
    url = f"https://wttr.in/{city}?format=j1"

    try:
        r = requests.get(url, timeout=5)
        data = r.json()
        temp_c = data["current_condition"][0]["temp_C"]
        
        return {
            "statusCode": 200,
            "body": json.dumps({
                "city": city,
                "temperature_c": temp_c
            })
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
