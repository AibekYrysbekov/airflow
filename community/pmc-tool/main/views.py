from django.shortcuts import render
from main.collector.data_processor import save_data_to_db


def render_results(request):
    pr_results, issue_results, first_pr_authors, new_authors = save_data_to_db()

    return render(request, 'results.html', {'pr_results': pr_results,
                                            'issue_results': issue_results,
                                            'first_pr_authors': first_pr_authors,
                                            'new_authors': new_authors})
