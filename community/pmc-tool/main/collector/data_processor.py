from main.collector.db import create_db_connection, create_pull_requests_table, insert_pull_requests_to_db, \
    create_issues_table, insert_issues_to_db
from main.collector.gh import query_prs, query_issues
from main.collector.queries import fetch_pull_requests, fetch_issues, fetch_first_pr_authors_last_week, get_new_authors


def save_data_to_db():
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

    # Fetch pull request data from the database
    pr_results = fetch_pull_requests(conn)

    # Fetch issue data from the database
    issue_results = fetch_issues(conn)

    # Find authors with the first pull request in the last week
    first_pr_authors = fetch_first_pr_authors_last_week(conn)

    # Find new authors
    new_authors = get_new_authors(conn, pr_authors_count)

    # Close the database connection
    conn.close()

    return pr_results, issue_results, first_pr_authors, new_authors
