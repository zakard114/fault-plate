import json
import sys

REQUIRED = [
    "name",
    "user_facing_message",
    "http_status",
    "log_fields",
    "retry_allowed",
]

def main() -> int:
    plate = json.load(sys.stdin)
    missing = [key for key in REQUIRED if key not in plate]
    if missing:
        print("missing: " + ", ".join(missing))
        return 1
    print("ok")
    return 0

if __name__ == "__main__":
    sys.exit(main())
