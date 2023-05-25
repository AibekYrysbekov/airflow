import sqlite3


def create_db_connection(db_file):
    conn = sqlite3.connect(db_file)
    return conn


def create_pull_requests_table(conn):
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS pull_requests (
            author TEXT,
            count INTEGER
        )
    ''')
    conn.commit()


def insert_prs_to_db(conn, prs):
    c = conn.cursor()
    for pr in prs:
        author = pr['author']
        count = pr['count']
        c.execute('INSERT INTO pull_requests VALUES (?, ?)', (author, count))
    conn.commit()


def fetch_pull_requests(conn):
    c = conn.cursor()
    c.execute('SELECT author, count FROM pull_requests')
    results = c.fetchall()
    return results
