from db import create_db_connection, create_pull_requests_table, insert_pull_requests_to_db, \
    fetch_pull_requests, create_issues_table, fetch_issues, insert_issues_to_db
from gh import query_prs, query_issues

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

issue_data_to_insert = [{'author': author, 'count': count} for author, count in issue_authors_count.items()]
insert_issues_to_db(conn, issues=issue_data_to_insert)

# Fetch and print pull request data from the database
pr_results = fetch_pull_requests(conn)
print("Pull Requests:")
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
