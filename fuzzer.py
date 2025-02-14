# given api endpoint and parameters fuzz the endpoint with the given parameters with fuzzing wordlist and return the responses 

import requests

class Fuzzer:
    def __init__(self, fuzzing_wordlist):
        self.fuzzing_wordlist = fuzzing_wordlist
        self.requests_responses = []

    def fuzz(self, injection_points):
        for point in injection_points:
            url = point['url']
            parameter = point['parameter']
            for word in self.fuzzing_wordlist:
                payload = {parameter: word}
                try:
                    response = requests.post(url, data=payload)
                    self.requests_responses.append({
                        'url': url,
                        'parameter': parameter,
                        'payload': payload,
                        'response_status': response.status_code,
                        'response_text': response.text
                    })
                    print(f"Fuzzed {url} with {payload} - Status Code: {response.status_code}")
                except requests.RequestException as e:
                    print(f"Failed to fuzz {url} with {payload}: {e}")

    def get_requests_responses(self):
        return self.requests_responses
