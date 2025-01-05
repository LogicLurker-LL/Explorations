import fuzzer, path_subdomain_finder, scraper

def main(target):
    valid_urls = path_subdomain_finder(target)
    requests = []
    for url in valid_urls:
        requests.append(scraper(url))
    responses = []
    for request in requests:
        responses.append(fuzzer(request))
    return responses