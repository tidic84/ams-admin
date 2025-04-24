import psutil
import json
sonde = {
    "ram": psutil.virtual_memory().percent
}

res = json.dumps(sonde)

print(res)