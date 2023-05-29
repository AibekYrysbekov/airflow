#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

"""This file contains functionality to query data from GitHub"""


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
    """
    Queries the GitHub API for open pull requests.

    Args:
        api_endpoint (str): The API endpoint to query.
        headers (dict): Headers containing the authentication token.

    Returns:
        list: A list of pull requests.

    """
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
