import psutil
import json
sonde = {
    "disk": psutil.disk_usage('/').percent
}

res = json.dumps(sonde)

print(res)