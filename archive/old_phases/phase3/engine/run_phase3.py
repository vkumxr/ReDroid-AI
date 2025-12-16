import json
import sys
from phase3.ai.reasoner import reason

def run(phase2_json_path: str) -> dict:
    with open(phase2_json_path, "r") as f:
        phase2_report = json.load(f)

    return reason(phase2_report)

if __name__ == "__main__":
    result = run(sys.argv[1])
    print(json.dumps(result, indent=2))