import json
from typing import Union, override

import requests

from libofall.main import Requester

MAX_TOPIC_SIZE = 49
MAX_MESSAGE_SIZE = 149

class Level9Requester(Requester):

    @override
    def build_request(self, payload: str) -> dict:
        return {
            "method": "POST",
            "url": f"{self.host}/pm.php",
            "data": {
                "receiver": "m-crap@crappysoft.com",
                "topic": "x",
                "message": payload
            }
        }

    @override
    def evaluate_response_value(self, response: requests.Response) -> bool:
        return response.ok and "your message was sent to" in response.content.decode(errors="ignore")

def eval_weight_for_character(character: str, requester: Requester) -> Union[int, None]:
    max_size = MAX_MESSAGE_SIZE
    if character == "<":
        return None

    if requester.request_and_evaluate(character * max_size):
        return 1

    low = 0
    high = max_size
    while low < high:
        current_size = (low + high + 1) // 2

        if requester.request_and_evaluate(character * current_size):
            low = current_size
        else:
            high = current_size - 1
    weight = max_size // low if low > 0 else None
    print(character, "=", weight)
    return weight

def eval_weight_map(requester: Requester) -> dict[str, Union[int, None]]:
    weight_map: dict[str, Union[int, None]] = {}
    for i in range(1, 255):
        character = chr(i)
        weight_map[character] = eval_weight_for_character(character, requester)

    return weight_map

def main() -> None:
    requester = Level9Requester(host="https://www.hackthissite.org/missions/realistic/9", headers={
        "Referer": "https://www.hackthissite.org/missions/realistic/9/pm.php",
    })
    eval_weight_for_character("&", requester)
    weight_map = eval_weight_map(requester)
    print(weight_map)
    with open("weight_map_message.json", "w", encoding="utf-8") as file:
        json.dump(weight_map, file, indent=4)


if __name__ == "__main__":
    main()