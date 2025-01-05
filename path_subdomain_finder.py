import requests
from urllib.parse import urlparse

def path_subdomain_finder(url, wordlist):
    parsed_url = urlparse(url)
    base_domain = parsed_url.netloc
    scheme = parsed_url.scheme
    valid_urls = []

    # Check subdomains
    for word in wordlist:
        subdomain = f"{word}.{base_domain}"
        subdomain_url = f"{scheme}://{subdomain}"
        try:
            response = requests.get(subdomain_url, timeout=3)
            if response.status_code == 200:
                valid_urls.append(subdomain_url)
        except requests.ConnectionError:
            pass

    # Check directories
    for word in wordlist:
        directory_url = f"{url}/{word}"
        try:
            response = requests.get(directory_url, timeout=3)
            if response.status_code == 200:
                valid_urls.append(directory_url)
        except requests.ConnectionError:
            pass

    return valid_urls
