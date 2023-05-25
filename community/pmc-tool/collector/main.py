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

"""This file contains logic for interfacing with GitHub and fetching PR and issue data."""

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

"""This file contains logic for interfacing with github and fetching PR and issue data."""

import requests
from db import create_db_connection, create_pull_requests_table, insert_prs_to_db, fetch_pull_requests

# Set up authentication with access token
with open('token.txt', 'r') as file:
    access_token = file.read().strip()

headers = {'Authorization': f'token {access_token}'}

# Set up API endpoint
OWNER = 'apache'
REPO = 'airflow'
API_ENDPOINT = f'https://api.github.com/repos/{OWNER}/{REPO}/pulls'

# Connect to the SQLite database
conn = create_db_connection('pull_requests.db')

# Create a table to store pull requests if it doesn't exist
create_pull_requests_table(conn)

# Retrieve list of pull requests
authors_count = {}


for page_number in range(1, 8):
    response = requests.get(API_ENDPOINT + f"?page={page_number}", headers=headers, params={'state': 'open'})
    pull_requests = response.json()

    if not pull_requests:
        break

    # Extract list of pull request authors
    authors = [pr['user']['login'] for pr in pull_requests]

    for author in authors:
        if author not in authors_count:
            authors_count[author] = 0
        authors_count[author] += 1
# Insert pull request data into the database
# insert_prs_to_db(conn, prs=authors_count)
insert_prs_to_db(conn, prs=[{'author': author, 'count': count} for author, count in authors_count.items()])

# Fetch and print pull request data from the database
results = fetch_pull_requests(conn)
for row in results:
    author, count = row
    print(f'Author: {author}, PRs: {count}')

# Close the database connection
conn.close()

print(f'Pull request data saved to the database.')
