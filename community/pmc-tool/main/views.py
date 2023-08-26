from django.shortcuts import render
from datetime import datetime
from .collector.data_processor import fetch_and_store_data_from_github
from .collector.db import (
    create_db_connection,
    fetch_pull_requests,
    fetch_issues,
    fetch_first_pr_authors_last_week, fetch_new_authors
)


def render_results(request):
    if request.method == 'POST':
        data_type = request.POST.get('data_type')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')

        if not start_date or not end_date:
            return render(
                request,
                "results.html",
                {
                    "data": None,
                    "data_type": data_type,
                    "message": "Please complete both fields with dates.",
                },
            )

        try:
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
        except ValueError:
            return render(
                request,
                "results.html",
                {
                    "data": None,
                    "data_type": data_type,
                    "message": "Incorrect date format.",
                },
            )

        conn = create_db_connection("pull_requests.db")


        if data_type == "pull_requests":
            pr_results = fetch_pull_requests(conn, start_date, end_date)
            data = pr_results
        elif data_type == "issues":
            issue_results = fetch_issues(conn, start_date, end_date)
            data = issue_results
        elif data_type == "pr_authors_last_week":
            first_pr_authors = fetch_first_pr_authors_last_week(conn)
            data = first_pr_authors
        elif data_type == "new_authors":
            new_authors = fetch_new_authors(conn, start_date, end_date)
            data = new_authors

        conn.close()

        return render(
            request,
            "results.html",
            {
                "data": data,
                "data_type": data_type,
            },
        )

    return render(
        request,
        "results.html",
    )


def update_data(request):
    fetch_and_store_data_from_github()
    update_message = 'Data updated successfully.'
    return render(
        request,
        "results.html",
        {"update_message": update_message},
    )

