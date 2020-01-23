from Hotel import settings
import requests, json
from extral_apps import MD5

import base64, os

headers = {"content-type": "application/json"}
data = {"id": 0, "status": 0, "type": "sms", "subtype": "generate", "data": {"phone": "19857160634"}}
response = requests.post(url="http://127.0.0.1:8848/api/test/", data=json.dumps(data), headers=headers)
print(response.text)
