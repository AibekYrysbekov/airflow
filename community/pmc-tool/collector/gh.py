import requests


def query_prs(api_endpoint, headers):
    prs = []
    page_number = 1

    while True:
        response = requests.get(api_endpoint, headers=headers, params={'state': 'open', 'page': page_number})
        pull_requests = response.json()

        if not pull_requests:
            break

        prs.extend(pull_requests)
        page_number += 1

    return prs
