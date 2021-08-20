import requests
from urllib3.exceptions import InsecureRequestWarning
from flask import jsonify
import json

# Suppress only the single warning from urllib3 needed.
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

data = {"user_id":"2", "date":"2021-08-19 00:00:00"}

r = requests.post('https://0.0.0.0/api/daily-record',json=json.dumps(data), verify=False)
if not r:
    print("Error.")
print (r.json())