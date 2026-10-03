import requests

class Requester:
    def __init__(self, host: str, headers: dict[str, str]) -> None:
        self.host = host
        self.headers = headers
        self.proxies = {
            "https": "http://127.0.0.1:8080"
        }

    def build_request(self, payload: str) -> dict:
        raise NotImplementedError()

    def evaluate_response_value(self, response: requests.Response):
        raise NotImplementedError()

    def make_request(self, payload: str) -> requests.Response:
        request = self.build_request(payload)
        response = requests.request(**request, headers=self.headers, proxies=self.proxies, verify=False)
        return response

    def request_and_evaluate(self, payload: str):
        response = self.make_request(payload)
        return self.evaluate_response_value(response)