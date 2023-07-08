from django.shortcuts import render
from main.collector.db import create_db_connection, create_pull_requests_table, insert_pull_requests_to_db, \
    fetch_pull_requests, create_issues_table, fetch_issues, insert_issues_to_db, \
    fetch_first_pr_authors_last_week
from main.collector.gh import query_prs, query_issues
import logging
import datetime


def assert_equal(db_data, api_data):
    db_set = set(db_data)
    api_set = set(api_data.items())
    if db_set != api_set:
        raise ValueError('The data from the database does not match the data from the API. '
                         + 'Database has %s extra. ' % (db_set - api_set)
                         + 'API has %s extra.' % (api_set - db_set))


def save_data_to_database(request):
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
    assert_equal(pr_results, pr_authors_count)

    # Fetch and print issue data from the database
    issue_results = fetch_issues(conn)
    logging.info("Verifying issues:")
    assert_equal(issue_results, issue_authors_count)

    # Find authors with the first pull request in the last week
    first_pr_authors = fetch_first_pr_authors_last_week(conn)

    # Close the database connection
    conn.close()

    return render(request, 'results.html', {'pr_results': pr_results, 'issue_results': issue_results,
                                            'first_pr_authors': first_pr_authors})

