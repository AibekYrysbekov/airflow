from datetime import datetime, timedelta
import sqlite3


def create_db_connection(db_file):
    conn = sqlite3.connect(db_file)
    return conn


def create_pull_requests_table(conn):
    c = conn.cursor()
    c.execute(
        """
        CREATE TABLE IF NOT EXISTS pullRequests (
            id INTEGER PRIMARY KEY,
            author_username TEXT,
            count INTEGER,
            creation_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """
    )
    conn.commit()


def create_issues_table(conn):
    c = conn.cursor()
    c.execute(
        """
        CREATE TABLE IF NOT EXISTS issues (
            id INTEGER PRIMARY KEY,
            creator_username TEXT,
            count INTEGER,
            creation_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """
    )
    conn.commit()


def insert_pull_requests_to_db(conn, prs):
    c = conn.cursor()
    for author, count in prs:
        c.execute("INSERT INTO pullRequests (author_username, count) VALUES (?, ?)", (author, count))
    conn.commit()


def insert_issues_to_db(conn, issues):
    c = conn.cursor()
    for author, count in issues:
        c.execute("INSERT INTO issues (creator_username, count) VALUES (?, ?)", (author, count))
    conn.commit()


def fetch_pull_requests(conn, start_date, end_date):
    c = conn.cursor()
    c.execute("SELECT author_username, count FROM pullRequests WHERE creation_timestamp BETWEEN ? AND ?", (start_date, end_date))
    results = c.fetchall()
    return results


def fetch_issues(conn, start_date, end_date):
    c = conn.cursor()
    c.execute("SELECT creator_username, count FROM issues WHERE creation_timestamp BETWEEN ? AND ?", (start_date, end_date))
    results = c.fetchall()
    return results


def fetch_new_authors_pr(conn, start_date, end_date):
    c = conn.cursor()

    c.execute(
        """
        SELECT DISTINCT author_username
        FROM pullRequests
        WHERE DATE(creation_timestamp) >= ? AND DATE(creation_timestamp) <= ?
        AND author_username NOT IN (
            SELECT DISTINCT author_username
            FROM pullRequests
            WHERE DATE(creation_timestamp) < ?
        )
        """
        , (start_date, end_date, start_date)
    )

    results = c.fetchall()
    new_authors_pr = [result[0] for result in results]
    return new_authors_pr


def fetch_new_authors_is(conn, start_date, end_date):
    c = conn.cursor()

    c.execute(
        """
        SELECT DISTINCT creator_username
        FROM issues
        WHERE DATE(creation_timestamp) >= ? AND DATE(creation_timestamp) <= ?
        AND creator_username NOT IN (
            SELECT DISTINCT creator_username
            FROM issues
            WHERE DATE(creation_timestamp) < ?
        )
        """
        , (start_date, end_date, start_date)
    )

    results = c.fetchall()
    new_authors_is = [result[0] for result in results]
    return new_authors_is


def get_last_timestamp_from_db(conn):
    c = conn.cursor()
    c.execute("SELECT MAX(creation_timestamp) FROM pullRequests")
    result = c.fetchone()
    if result and result[0]:
        return datetime.strptime(result[0], "%Y-%m-%d %H:%M:%S")
    else:
        return datetime.min
