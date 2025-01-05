# given api endpoint and parameters fuzz the endpoint with the given parameters with fuzzing wordlist and return the responses 

import requests
def fuzzer(url, params, wordlist):
    valid_urls = []
    for word in wordlist:
        try:
            response = requests.get(url, params={params: word}, timeout=3)
            if response.status_code == 200:
                valid_urls.append(response.url)
        except requests.ConnectionError:
            pass
    return valid_urls