import os
import urllib.request

PLATE_URL = os.environ.get("PLATE_URL", "https://fault-plate.onrender.com/plates")

with urllib.request.urlopen(PLATE_URL) as response:
    print(response.read().decode())
