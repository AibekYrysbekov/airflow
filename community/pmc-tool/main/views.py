# views.py
from django.shortcuts import render
from main.collector.db import create_db_connection, fetch_pull_requests, fetch_issues, fetch_first_pr_authors_last_week
from main.collector.queries import get_new_authors

def render_results(request):
    if request.method == 'POST':
        data_type = request.POST.get('data_type')

        conn = create_db_connection("pull_requests.db")

        if data_type == "pull_requests":
            pr_results = fetch_pull_requests(conn)
            data = pr_results
        elif data_type == "issues":
            issue_results = fetch_issues(conn)
            data = issue_results
        elif data_type == "pr_authors_last_week":
            first_pr_authors = fetch_first_pr_authors_last_week(conn)
            data = first_pr_authors
        elif data_type == "new_authors":
            pr_authors_count = dict(fetch_pull_requests(conn))
            new_authors = get_new_authors(conn, pr_authors_count)
            data = new_authors
        else:
            data = None
            data_type = None

        conn.close()

    else:
        data = None
        data_type = None

    return render(
        request,
        "results.html",
        {
            "data": data,
            "data_type": data_type,
        },
    )
