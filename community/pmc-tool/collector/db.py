import sqlite3


def create_db_connection(db_file):
    conn = sqlite3.connect(db_file)
    return conn


def create_pull_requests_table(conn):
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS pullRequests (
            id INTEGER PRIMARY KEY,
            author_username TEXT,
            count INTEGER,
            creation_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()


def create_issues_table(conn):
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS issues (
            id INTEGER PRIMARY KEY,
            creator_username TEXT,
            count INTEGER,
            creation_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()


def insert_pull_requests_to_db(conn, prs):
    c = conn.cursor()
    for author, count in prs:
        c.execute('INSERT INTO pullRequests (author_username, count) VALUES (?, ?)', (author, count))
    conn.commit()


def insert_issues_to_db(conn, issues):
    c = conn.cursor()
    for author, count in issues:
        c.execute('INSERT INTO issues (creator_username, count) VALUES (?, ?)', (author, count))
    conn.commit()


def fetch_pull_requests(conn):
    c = conn.cursor()
    c.execute('SELECT author_username, count FROM pullRequests')
    results = c.fetchall()
    return results


def fetch_issues(conn):
    c = conn.cursor()
    c.execute('SELECT creator_username, count FROM issues')
    results = c.fetchall()
    return results
