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


from db import create_db_connection, create_pull_requests_table, insert_pull_requests_to_db, \
    fetch_pull_requests, create_issues_table, fetch_issues, insert_issues_to_db
from gh import query_prs, query_issues
import logging


def assert_equal(db_data, api_data):
    db_set = set(db_data)
    api_set = set(api_data.items())
    if db_set != api_set:
        raise ValueError('The data from the database does not match the data from the API. '
                         + 'Database has %s extra. ' % (db_set - api_set)
                         + 'API has %s extra.' % (api_set - db_set))


# Connect to the SQLite database
conn = create_db_connection('pull_requests.db')

# Create a table to store pull requests if it doesn't exist
create_pull_requests_table(conn)
create_issues_table(conn)

# Retrieve list of pull requests
pull_requests = query_prs()
issues = query_issues()

# Extract list of pull request authors
pr_authors_count = {}

for pr in pull_requests:
    author = pr['user']['login']
    if author not in pr_authors_count:
        pr_authors_count[author] = 0
    pr_authors_count[author] += 1

# Extract list of issue authors
issue_authors_count = {}

for issue in issues:
    author = issue['user']['login']
    if author not in issue_authors_count:
        issue_authors_count[author] = 0
    issue_authors_count[author] += 1

# Insert pull request and issue data into the database
insert_pull_requests_to_db(conn, prs=list(pr_authors_count.items()))
insert_issues_to_db(conn, issues=list(issue_authors_count.items()))

# Fetch and print pull request data from the database
pr_results = fetch_pull_requests(conn)
logging.info("Verifying pull requests:")
for row in pr_results:
    author, count = row
    print(f'Author: {author}, PRs: {count}')

# Fetch and print issue data from the database
issue_results = fetch_issues(conn)
print("Issues:")
for row in issue_results:
    author, count = row
    print(f'Author: {author}, Issues: {count}')

# Close the database connection
conn.close()

print(f'Pull request and issue data saved to the database.')
