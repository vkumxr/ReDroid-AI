import json
from phase2.engine.analyze import analyze

def run(phase1_json_path: str) -> dict:
    with open(phase1_json_path, "r") as f:
        phase1_report = json.load(f)

    return analyze(phase1_report)


if __name__ == "__main__":
    import sys
    result = run(sys.argv[1])
    print(json.dumps(result, indent=2))