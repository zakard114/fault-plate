import json
import os
import urllib.request

from mcp.server.fastmcp import FastMCP

PLATE_URL = os.environ.get("PLATE_URL", "https://fault-plate.onrender.com/plates")
mcp = FastMCP("fault-plate")

def fetch_plate() -> str:
    with urllib.request.urlopen(PLATE_URL) as response:
        return response.read().decode()

@mcp.tool()
def get_plate() -> str:
    return fetch_plate()

if __name__ == "__main__":
    mcp.run()
