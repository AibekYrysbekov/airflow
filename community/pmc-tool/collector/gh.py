import requests

# Set up authentication with access token


def load_token(file_path):
    with open(file_path, 'r') as file:
        access_token = file.read().strip()

    headers = {'Authorization': f'token {access_token}'}
    return headers


def get_api_endpoint():
    OWNER = 'apache'
    REPO = 'airflow'
    return f'https://api.github.com/repos/{OWNER}/{REPO}/pulls'


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
