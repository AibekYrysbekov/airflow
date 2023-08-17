from main.collector.db import fetch_pull_requests, fetch_issues


def assert_equal(db_data, api_data):
    db_set = set(db_data)
    api_set = set(api_data.items())
    if db_set != api_set:
        raise ValueError(
            "The data from the database does not match the data from the API. "
            + "Database has %s extra. " % (db_set - api_set)
            + "API has %s extra." % (api_set - db_set)
        )


def verify_pull_requests(conn, pr_authors_count):
    pr_results = fetch_pull_requests(conn)
    assert_equal(pr_results, pr_authors_count)
    return pr_results


def verify_issues(conn, issue_authors_count):
    issue_results = fetch_issues(conn)
    assert_equal(issue_results, issue_authors_count)
    return issue_results
