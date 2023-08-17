import datetime
from main.collector.db import fetch_first_pr_date


def get_new_authors(conn, pr_authors_count):
    current_date = datetime.date.today()
    one_week_ago = current_date - datetime.timedelta(days=7)
    new_authors = []

    for author, count in pr_authors_count.items():
        first_pr_date = fetch_first_pr_date(conn, author)
        if first_pr_date and first_pr_date.date() >= one_week_ago and count == 1:
            new_authors.append(author)

    return new_authors
