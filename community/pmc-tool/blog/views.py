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
import sqlite3


# Set up authentication with access token
with open('token.txt', 'r') as file:
    access_token = file.read().strip()

headers = {'Authorization': f'token {access_token}'}

# Set up API endpoint
OWNER = 'apache'
REPO = 'airflow'
API_ENDPOINT = f'https://api.github.com/repos/{owner}/{repo}/pulls'

# Connect to the SQLite database
conn = sqlite3.connect('pull_requests.db')
c = conn.cursor()

# Create a table to store pull requests if it doesn't exist
c.execute('''
    CREATE TABLE IF NOT EXISTS pull_requests (
        author TEXT,
        count INTEGER
    )
''')

# Retrieve list of pull requests
authors_count = dict()

for page_number in range(1, 8):
    response = requests.get(api_endpoint + f"?page={page_number}", headers=headers, params={'state': 'open'})
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
for author, count in authors_count.items():
    c.execute('INSERT INTO pull_requests VALUES (?, ?)', (author, count))

c.execute('SELECT author, count FROM pull_requests')
results = c.fetchall()

for row in results:
    author, count = row
    print(f'Author: {author}, PRs: {count}')
# Commit the changes and close the database connection
conn.commit()
conn.close()

print(f'Pull request data saved to the database.')
