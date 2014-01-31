from django.contrib.auth.models import User, check_password
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views.generic.base import View, ContextMixin, TemplateResponseMixin

from study_enrollment.models import ActiveEnrollmentSet, Requirement, UserEnrollment
from study_enrollment.settings import IS_ELIGIBLE_FLAG
from study_enrollment.utils import need_to_check_eligibility, transfer_eligibility_info
from study_enrollment.mixins import ReqsMetMixin, LoginRequiredMixin

class BaseEnrollmentView(View):
    """
    All study_enrollment views should inherit from this view
    in a manner that uses this view's dispatch method.

    """
    def _admin_pwd_changed(self, default_account):
        """Checks that study_admin's password has been changed."""
        # If the password matches "study_admin", it hasn't been changed.
        if check_password('study_admin', default_account.password):
            return False
        else:
            return True

    def dispatch(self, request, *args, **kwargs):
        """
        Wrapper that checks system set up and loads:
          -  self.enrollment_set (always)
          -  self.requirements (if self.enrollment_set.use_req_list is True)
          -  self.user_enrollment (if user.is_authenticated() is True)

        This should check for all potential misconfigurations, including:
          - study_admin password not yet changed
          - missing ActiveEnrollmentSet
          - more than one ActiveEnrollmentSet
          - use_req_list is True, but requirements not specified
        """
        # Check that initial fixture is loaded.
        try:
            default_account = User.objects.get(username='study_admin')
        except User.DoesNotExist:
            return HttpResponse("If you're seeing this message, it's because " +
                                "the study_admin account doesn't exist -- " +
                                "probably because the initialize_data.yaml " +
                                "fixture hasn't been loaded.")
        # Check that study_admin password is changed.
        if not self._admin_pwd_changed(default_account):
            return render(request, 'study_enrollment/system_needs_set_up.html')
        # Check that one and only one ActiveEnrollmentSet exists. Store it.
        active_enrollment_set = ActiveEnrollmentSet.objects.all()
        if len(active_enrollment_set) != 1:
            return HttpResponse("Problem with database! One and only one" +
                                "ActiveEnrollmentSet should exist.")
        self.enrollment_set = active_enrollment_set[0]
        # Check that requirements are set up correctly. Store it if needed.
        if self.enrollment_set.use_req_list:
            self.requirements = Requirement.objects.filter(req_list=self.enrollment_set.req_list)
            if not self.requirements:
                return render(request, 'study_enrollment/requirements_need_set_up.html')
        # Store user_enrollment if user is logged in.
        if request.user.is_authenticated():
            self.user_enrollment, _ = UserEnrollment.objects.get_or_create(user=request.user)
            transfer_eligibility_info(request)

        # Remainder as in django.views.generic.base
        return super(BaseEnrollmentView, self).dispatch(request, *args, **kwargs)

# We're not actually using this... maybe should remove.
class EnrollmentTemplateView(TemplateResponseMixin, ContextMixin, BaseEnrollmentView):
    """Renders template, analogous to django.views.generic.base.TemplateView"""
    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)


class IndexView(BaseEnrollmentView):
    """
    Renders index.html, with context regarding whether requirements have already
    been passed, and if the user is currently logged in.

    """
    def get(self, request, *args, **kwargs):
        context = {'need_to_check_eligibility': need_to_check_eligibility(request),
                   'not_logged_in': not request.user.is_authenticated(),
                   }
        return render(request, 'study_enrollment/index.html', context)


class RequirementsView(BaseEnrollmentView):
    """Display current active list of eligibility Requirements and handle answers."""
    def get(self, request, *args, **kwargs):
        """Display eligibility requirements"""
        # Redirect to StartView if use_req_list is False.
        if not self.enrollment_set.use_req_list:
            return HttpResponseRedirect('/start')
        requirement_choices = [req.requirementchoice_set.all() for req in self.requirements]
        req_items = [ {'requirement': self.requirements[x],
                       'req_choices': requirement_choices[x]}
                      for x in range(len(self.requirements)) ]
        return render(request, 'study_enrollment/requirements.html',
                      { 'req_items': req_items } )

    def post(self, request, *args, **kwargs):
        """Check answers and send to next step or explain why ineligible"""
        if not self.enrollment_set.use_req_list:
            return HttpResponseRedirect('/start')
        failed_questions = []
        for req in self.requirements:
            req_choices = req.requirementchoice_set.all()
            choice = req.requirementchoice_set.get(answer=request.POST[req.question])
            if not choice.is_eligible:
                failed_questions.append({'requirement': req, 'choice': choice})
        if failed_questions:
            # If requirements aren't met, tell user they're not eligible and
            # display explanations for the failed requirements.
            return render(request, 'study_enrollment/not_eligible.html',
                          { 'reqs_failed': failed_questions })
        else:
            # Store that requirements are met -- if user is logged in, in
            # user_enrollment, otherwise in session.
            if request.user.is_authenticated():
                user_enrollment, _ = UserEnrollment.objects.get_or_create(user=request.user)
                user_enrollment.is_eligible = True
                user_enrollment.save()
            else:
                request.session[IS_ELIGIBLE_FLAG] = True
            return HttpResponseRedirect(reverse('requirements_passed'))


class ReqsMetEnrollmentTemplateView(ReqsMetMixin, BaseEnrollmentView):
    """Display requirements_passed.html (check first that requirements met)."""
    def get(self, request, *args, **kwargs):
        return render(request, 'study_enrollment/requirements_passed.html')


class StartView(ReqsMetMixin, LoginRequiredMixin, BaseEnrollmentView):
    """Start enrollment modules."""
    def get(self, request, *args, **kwargs):
        return HttpResponse("Page for starting enrollment exam.")
