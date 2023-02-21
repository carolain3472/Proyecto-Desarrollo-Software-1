import requests
import json

url = "https://energy-service-ds-v3cot.ondigitalocean.app/consumption"

payload = json.dumps({
  "client_id": "255"
})

headers = {
  'Content-Type': 'application/json'
}


response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)