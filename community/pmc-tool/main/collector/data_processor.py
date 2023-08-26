from main.collector.db import (
    create_db_connection,
    create_pull_requests_table,
    insert_pull_requests_to_db,
    create_issues_table,
    insert_issues_to_db,
    get_last_timestamp_from_db, fetch_issues, fetch_first_pr_authors_last_week,
)
from main.collector.gh import query_prs, query_issues


def fetch_and_store_data_from_github():
    conn = create_db_connection("pull_requests.db")

    create_pull_requests_table(conn)
    create_issues_table(conn)

    last_timestamp = get_last_timestamp_from_db(conn)

    pull_requests = query_prs(last_timestamp)
    issues = query_issues(last_timestamp)

    pr_authors_count = {}
    for pr in pull_requests:
        author = pr["user"]["login"]
        pr_authors_count[author] = pr_authors_count.get(author, 0) + 1

    issue_authors_count = {}
    for issue in issues:
        author = issue["user"]["login"]
        issue_authors_count[author] = issue_authors_count.get(author, 0) + 1

    insert_pull_requests_to_db(conn, prs=list(pr_authors_count.items()))
    insert_issues_to_db(conn, issues=list(issue_authors_count.items()))

    conn.close()

    return pr_authors_count


# def read_reports():
#     conn = create_db_connection("pull_requests.db")
#
#     pr_results = fetch_and_store_data_from_github(conn)
#     issue_results = fetch_issues(conn)
#     first_pr_authors = fetch_first_pr_authors_last_week(conn)
#     new_authors = get_new_authors(conn, pr_results)
#
#     conn.close()
#
#     return pr_results, issue_results, first_pr_authors, new_authors

# fetch_and_store_data_from_github()

