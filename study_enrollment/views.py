from django.contrib.auth.models import User, check_password
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views.generic.base import View, TemplateView

from study_enrollment.models import ActiveEnrollmentSet, Requirement, UserEnrollment
from study_enrollment.settings import IS_ELIGIBLE_FLAG
from study_enrollment.utils import requirements_needed, transfer_eligibility_info
from study_enrollment.mixins import ReqsMetMixin, LoginRequiredMixin

class BaseEnrollmentView(View):
    def _admin_pwd_changed(self, default_account):
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
            return HttpResponse("Problem with database! One and only one ActiveEnrollmentSet should exist.")
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


class EnrollmentTemplateView(BaseEnrollmentView, TemplateView):
    def dispatch(self, request, *args, **kwargs):
        return super(BaseEnrollmentView, self).dispatch(request, *args, **kwargs)


class IndexView(BaseEnrollmentView):
    def get(self, request, *args, **kwargs):
        context = {'reqs_needed': requirements_needed(request),
                   'not_logged_in': not request.user.is_authenticated(),
                   }
        return render(request, 'study_enrollment/index.html', context)


class RequirementsView(BaseEnrollmentView):
    def get(self, request, *args, **kwargs):
        if not self.enrollment_set.use_req_list:
            return HttpResponseRedirect('/start')
        requirement_choices = [req.requirementchoice_set.all() for req in self.requirements]
        req_items = [ {'requirement': self.requirements[x],
                       'req_choices': requirement_choices[x]}
                      for x in range(len(self.requirements)) ]
        return render(request, 'study_enrollment/requirements.html',
                      { 'req_items': req_items } )

    def post(self, request, *args, **kwargs):
        if not self.enrollment_set.use_req_list:
            return HttpResponseRedirect('/start')
        failed_questions = []
        for req in self.requirements:
            req_choices = req.requirementchoice_set.all()
            choice = req.requirementchoice_set.get(answer=request.POST[req.question])
            if not choice.is_eligible:
                failed_questions.append({'requirement': req, 'choice': choice})
        if failed_questions:
            return render(request, 'study_enrollment/not_eligible.html', { 'reqs_failed': failed_questions })
        else:
            if request.user.is_authenticated():
                user_enrollment, _ = UserEnrollment.objects.get_or_create(user=request.user)
                user_enrollment.is_eligible = True
                user_enrollment.save()
            else:
                request.session[IS_ELIGIBLE_FLAG] = True
            return HttpResponseRedirect(reverse('requirements_passed'))


class StartView(ReqsMetMixin, LoginRequiredMixin, BaseEnrollmentView):

    def get(self, request, *args, **kwargs):
        return HttpResponse("Page for starting enrollment exam.")
