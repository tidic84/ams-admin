import psutil
import json
sonde = {
    "cpu": psutil.cpu_percent(interval=1.5)
}

res = json.dumps(sonde)

print(res)