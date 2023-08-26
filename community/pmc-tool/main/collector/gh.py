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

import os
from datetime import datetime
import requests


def _load_token(file_path):
    file_path = os.path.join(os.path.dirname(__file__), file_path)
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"Token file not found: {file_path}")

    with open(file_path, "r") as file:
        access_token = file.read().strip()

    headers = {"Authorization": f"token {access_token}"}
    return headers


def _get_api_endpoint(endpoint):
    OWNER = "apache"
    REPO = "airflow"
    if endpoint == "pulls":
        return f"https://api.github.com/repos/{OWNER}/{REPO}/pulls"
    elif endpoint == "issues":
        return f"https://api.github.com/repos/{OWNER}/{REPO}/issues"
    else:
        raise ValueError(f"Invalid endpoint: {endpoint}")


def query_prs(last_timestamp):
    api_endpoint = _get_api_endpoint("pulls")
    headers = _load_token("token.txt")
    prs = []
    page_number = 1

    while True:
        response = requests.get(api_endpoint, headers=headers, params={"state": "open", "page": page_number})
        pull_requests = response.json()

        if not pull_requests:
            break

        for pr in pull_requests:
            pr_timestamp = datetime.strptime(pr["created_at"], "%Y-%m-%dT%H:%M:%SZ")
            if pr_timestamp > last_timestamp:
                prs.append(pr)

        page_number += 1

    return prs


def query_issues(last_timestamp):
    api_endpoint = _get_api_endpoint("issues")
    headers = _load_token("token.txt")
    issues = []
    page_number = 1

    while True:
        response = requests.get(api_endpoint, headers=headers, params={"state": "open", "page": page_number})
        issue_data = response.json()

        if not issue_data:
            break

        for issue in issue_data:
            issue_timestamp = datetime.strptime(issue["created_at"], "%Y-%m-%dT%H:%M:%SZ")
            if issue_timestamp > last_timestamp:
                issues.append(issue)

        page_number += 1

    return issues
