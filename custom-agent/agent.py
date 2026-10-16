import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.oncall import repair_url

if __name__ == "__main__":
    url = os.environ.get("PLATE_URL", "https://fault-plate.onrender.com")
    print(repair_url(url))
