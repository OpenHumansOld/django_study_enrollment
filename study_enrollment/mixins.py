from django.contrib import messages
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from study_enrollment.utils import need_to_check_eligibility

class ReqsMetMixin(object):
    """If requirements need to be passed, redirect to requirements url"""
    def dispatch(self, request, *args, **kwargs):
        if not need_to_check_eligibility(request):
            return super(ReqsMetMixin, self).dispatch(request, *args, **kwargs)
        messages.add_message(
            request, messages.ERROR, 
            'Please first complete our study requirements ' +
            'questionnaire to see if you qualify.')
        return HttpResponseRedirect(reverse('requirements'))


class LoginRequiredMixin(object):
    """If not logged in, redirect to login url"""
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return super(LoginRequiredMixin, self).dispatch(request, *args, **kwargs)
        messages.add_message(
            request, messages.ERROR, 
            'Please create an account or log in to continue')
        return HttpResponseRedirect(reverse('registration_register'))
