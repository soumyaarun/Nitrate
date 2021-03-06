# -*- coding: utf-8 -*-

import logging

from operator import attrgetter

from django import forms
from django.contrib.auth.decorators import permission_required
from django.core.validators import ValidationError
from django.http import JsonResponse
from django.shortcuts import Http404
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_GET

from tcms.integration.issuetracker.models import Issue
from tcms.integration.issuetracker.services import find_service
from tcms.testcases.forms import CaseRunIssueForm
from tcms.testruns.models import TestCaseRun
from tcms.testruns.models import TestRun
from tcms.utils import HTTP_BAD_REQUEST
from tcms.utils import HTTP_FORBIDDEN
from tcms.utils import HTTP_NOT_FOUND
from tcms.utils import form_errors_to_list

logger = logging.getLogger(__name__)


# TODO: Split this actions class into individual view.

@require_GET
@permission_required('testruns.change_testrun')
def manage_case_run_issues(request, run_id):
    """Process the issues for case runs."""

    class CaseRunIssueActions(object):
        __all__ = ['add', 'remove']

        def __init__(self, request, run):
            self.request = request
            self.run = run

        def add(self):
            # TODO: make a migration for the permission
            if not self.request.user.has_perm('issuetracker.add_issue'):
                return JsonResponse({'messages': ['Permission denied.']},
                                    status=HTTP_FORBIDDEN)

            form = CaseRunIssueForm(request.GET)

            if not form.is_valid():
                msgs = form_errors_to_list(form)
                return JsonResponse({'messages': msgs}, status=HTTP_BAD_REQUEST)

            service = find_service(form.cleaned_data['tracker'])
            issue_key = form.cleaned_data['issue_key']
            link_et = form.cleaned_data['link_external_tracker']
            case_runs = form.cleaned_data['case_run']

            # FIXME: maybe, make sense to validate in the form.
            if not all(case_run.run_id == self.run.pk for case_run in case_runs):
                return JsonResponse(
                    {'messages': [
                        'Not all case runs belong to run {}.'.format(self.run.pk)
                    ]},
                    status=HTTP_BAD_REQUEST)

            try:
                for case_run in case_runs:
                    service.add_issue(issue_key,
                                      case_run.case,
                                      case_run=case_run,
                                      add_case_to_issue=link_et)
            except ValidationError as e:
                logger.exception(
                    'Failed to add issue to case run %s. Error reported: %s',
                    form.case_run.pk, str(e))
                return JsonResponse({'messages': [str(e)]}, status=HTTP_BAD_REQUEST)

            return self.run_issues_info(case_runs)

        def remove(self):
            if not self.request.user.has_perm('issuetracker.delete_issue'):
                return JsonResponse({'messages': ['Permission denied.']},
                                    status=HTTP_FORBIDDEN)

            class RemoveIssueForm(forms.Form):
                issue_key = forms.CharField()
                case_run = forms.ModelMultipleChoiceField(
                    queryset=TestCaseRun.objects.all().only('pk'),
                    error_messages={
                        'required': 'Case run id is missed.',
                        'invalid_pk_value': 'Case run %(pk)s does not exist.',
                    },
                )

            form = RemoveIssueForm(request.GET)
            if not form.is_valid():
                return JsonResponse({'messages': form_errors_to_list(form)},
                                    status=HTTP_BAD_REQUEST)

            issue_key = form.cleaned_data['issue_key']
            case_runs = form.cleaned_data['case_run']
            for case_run in case_runs:
                try:
                    case_run.remove_issue(issue_key)
                except Exception:
                    msg = 'Failed to remove issue {} from case run {}'.format(
                        issue_key, case_run.pk)
                    logger.exception(msg)
                    return JsonResponse(
                        {'messages': [msg]}, status=HTTP_BAD_REQUEST)

            return self.run_issues_info(case_runs)

        def run_issues_info(self, case_runs):
            """Return a JSON response including run's issues info"""
            return JsonResponse({
                # The total number of issues this run has
                'run_issues_count': self.run.get_issues_count(),

                # The number of issues each of case run has
                'caserun_issues_count': Issue.count_by_case_run(
                    list(map(attrgetter('pk'), case_runs)))
            })

    try:
        run = get_object_or_404(TestRun, pk=run_id)
    except Http404:
        return JsonResponse(
            {'messages': ['Test run {} does not exist.'.format(run_id)]},
            status=HTTP_NOT_FOUND)

    crba = CaseRunIssueActions(request=request, run=run)

    if not request.GET.get('a') in crba.__all__:
        return JsonResponse({'messages': ['Unrecognizable actions']},
                            status=HTTP_BAD_REQUEST)

    func = getattr(crba, request.GET['a'])
    return func()
