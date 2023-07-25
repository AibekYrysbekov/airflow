from django.shortcuts import render
from main.collector.data_processor import read_reports


def render_results(request):
    pr_results, issue_results, first_pr_authors, new_authors = read_reports()

    return render(request, 'results.html', {'pr_results': pr_results,
                                            'issue_results': issue_results,
                                            'first_pr_authors': first_pr_authors,
                                            'new_authors': new_authors})
