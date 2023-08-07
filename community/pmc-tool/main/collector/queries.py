import datetime
from main.collector.db import (
    fetch_first_pr_authors_last_week,
    fetch_first_pr_date,
    fetch_pull_requests,
    fetch_issues,
)
from main.collector.validations import assert_equal


def verify_pull_requests(conn, pr_authors_count):
    pr_results = fetch_pull_requests(conn)
    assert_equal(pr_results, pr_authors_count)
    return pr_results


def verify_issues(conn, issue_authors_count):
    issue_results = fetch_issues(conn)
    assert_equal(issue_results, issue_authors_count)
    return issue_results


def get_first_pr_authors_last_week(conn):
    return fetch_first_pr_authors_last_week(conn)


def get_new_authors(conn, pr_authors_count):
    current_date = datetime.date.today()
    one_week_ago = current_date - datetime.timedelta(days=7)
    new_authors = []

    for author, count in pr_authors_count.items():
        first_pr_date = fetch_first_pr_date(conn, author)
        if first_pr_date and first_pr_date.date() >= one_week_ago and count == 1:
            new_authors.append(author)

    return new_authors
